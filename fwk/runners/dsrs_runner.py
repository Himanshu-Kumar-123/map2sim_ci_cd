# Standard imports
import platform
import sys
import subprocess
import os
import threading
from enum import Enum, auto
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json

# Local imports
from analysis_utils.validate_logs_util import LogsSaverMethods
from generic_utils.helper_util import HelperMethods
from generic_utils.reporting_util import ReportingMethods
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger
from fwk.runners.iteration_controller import IterationController
from fwk.shared.constants import (
    DSRS_LAUNCH_LOG_FILE_NAME,
    DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME,
    DSRS_SCENARIO_TYPE,
    KIT_PROCESS_NAME
)

class TestStatus(Enum):
    PENDING = auto()    # Test waiting to be executed
    RUNNING = auto()    # Test currently running
    COMPLETED = auto()  # Test completed successfully 
    FAILED = auto()     # Test failed
    SKIPPED = auto()    # Test was skipped
    RETRY = auto()      # Test needs to be retried

@dataclass
class TestResult:
    status: TestStatus = TestStatus.PENDING
    attempts: int = 0
    error_message: Optional[str] = None
    logs_analysis: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    new_count: int = 0
    commands_executed: List[str] = field(default_factory=list)
    updated_toml_name: Optional[str] = None

# Get logger for DSRSRunner
logger = get_logger(__name__, varc.framework_logs_path)


class DSRSRunner:
    """Runner specifically for DSRS component tests"""
    
    def __init__(self):
        self.iteration_controller = IterationController()
        self.launch_log_file = DSRS_LAUNCH_LOG_FILE_NAME
        self.scenario_log_file = DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME
    
    def run_tests(self, tests_list):
        """Run all DSRS tests using a queue-based approach with dynamic iteration support"""
        
        # Initialize test queue with wrapping test items (simple, no pre-processing)
        test_queue = deque([
            {
                'test_dict': test,
                'result': TestResult()
            } for test in tests_list
        ])
        
        logger.info(f"Processing {len(test_queue)} initial tests")
        
        # Final results collection
        final_results = []
        current_index = 0
        
        # Process all tests in the queue (iterations will be added dynamically)
        while current_index < len(test_queue):
            test_item = test_queue[current_index]
            test_dict = test_item['test_dict']
            result = test_item['result']
            
            # Skip tests that have already been processed
            if result.status in (TestStatus.COMPLETED, TestStatus.SKIPPED, TestStatus.FAILED):
                final_results.append({
                    'name': test_dict.get('updated_name', test_dict.get('name', 'Unknown')),
                    'status': result.status.name,
                    'attempts': result.attempts,
                    'new_count': result.new_count,
                    'error': result.error_message
                })
                current_index += 1
                continue
            
            # Check max retry attempts (safety net for existing retry logic)
            if result.attempts >= 3:  # Max 3 attempts per test (existing retry logic)
                result.status = TestStatus.FAILED
                result.error_message = "Exceeded maximum retry attempts"
                logger.error(f"Test [{test_dict['name']}]: {result.error_message}")
                final_results.append({
                    'name': test_dict.get('updated_name', test_dict.get('name', 'Unknown')),
                    'status': result.status.name,
                    'attempts': result.attempts,
                    'new_count': result.new_count,
                    'error': result.error_message
                })
                current_index += 1
                continue
            
            # Mark as running and increment attempt counter
            result.status = TestStatus.RUNNING
            result.attempts += 1
            
            try:
                # Execute the test, main logic
                self.execute_test(test_dict, result)
                
                # Handle test result
                if result.status == TestStatus.RETRY:
                    # Put back in queue for retry (existing retry logic)
                    logger.info(f"Test [{test_dict['name']}]: Flagged for retry (attempt {result.attempts})")
                    # Don't increment current_index, retry this test
                    continue
                    
                elif result.status in (TestStatus.COMPLETED, TestStatus.FAILED):
                    # Test completed - check for iterations (AFTER test completion like original)
                    original_queue_size = len(test_queue)
                    
                    # Handle iteration logic (like original reference)
                    self.iteration_controller.handle_test_result(test_dict, test_queue, current_index)
                    
                    # Check if iteration was added
                    if len(test_queue) > original_queue_size:
                        logger.info(f"Added iteration test at index {current_index + 1}")
                    
                    # Add to final results
                    final_results.append({
                        'name': test_dict.get('updated_name', test_dict.get('name', 'Unknown')),
                        'status': result.status.name,
                        'attempts': result.attempts,
                        'new_count': result.new_count,
                        'error': result.error_message
                    })
                    
                    # Generate reports for completed tests
                    if result.status == TestStatus.COMPLETED:
                        self._generate_reports(test_dict)
                    
                    # Move to next test
                    current_index += 1
                
                else:
                    # Other statuses, just move to next test
                    final_results.append({
                        'name': test_dict.get('updated_name', test_dict.get('name', 'Unknown')),
                        'status': result.status.name,
                        'attempts': result.attempts,
                        'new_count': result.new_count,
                        'error': result.error_message
                    })
                    current_index += 1
                
            except Exception as e:
                # Handle unexpected errors
                result.status = TestStatus.FAILED
                result.error_message = f"Unexpected error: {str(e)}"
                logger.error(f"Test [{test_dict['name']}]: {result.error_message}")
                
                # Add to final results
                final_results.append({
                    'name': test_dict.get('updated_name', test_dict.get('name', 'Unknown')),
                    'status': result.status.name,
                    'attempts': result.attempts,
                    'new_count': result.new_count,
                    'error': result.error_message
                })
                
                # Move to next test
                current_index += 1
        
        logger.info(f"DSRS test execution completed. Processed {len(final_results)} tests")
        return final_results
        
    def execute_test(self, test_dict, result):
        """Execute a single DSRS test with proper phase management"""
        from generic_utils.command_runner_util import CommandRunnerMethods
        from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods, PosttestAnalysisCallerMethods
        
        try:
            # Initialize test environment variables
            self._initialize_test_variables(test_dict)
            
            # DSRS-specific execution phases
            # (Screen recording is now handled inside the runner after app launch)
            CommandRunnerMethods.dsrs_runner(test_dict, result)
            
            # Copy Kit logs
            logger.info(f"Attempting to copy Kit logs for test {test_dict['name']}")
            LogsSaverMethods.copy_kit_logs(test_dict) 
            
            # *** POST-EXECUTION LOG ANALYSIS ***
            # Perform comprehensive log analysis after execution completes
            logger.info(f"[{test_dict['name']}] Starting post-execution log analysis")
            try:
                # Set test type for DSRS
                test_dict['type'] = DSRS_SCENARIO_TYPE
                
                # Call comprehensive log analysis
                self._perform_logs_analysis(test_dict, result)
                logger.info(f"[{test_dict['name']}] Post-execution log analysis completed")
                
            except Exception as log_analysis_error:
                logger.error(f"[{test_dict['name']}] Log analysis failed: {str(log_analysis_error)}")
                # Store error but don't fail the test due to log analysis issues
                result.logs_analysis['log_analysis_error'] = str(log_analysis_error)
            
            # Store result in test_dict for access during report generation
            test_dict['test_result'] = result
            
            # Transfer result data to test_dict for main framework reports
            self._transfer_result_data_to_test_dict(test_dict, result)
            
            # Set final verdict based on result status FIRST
            if result.status == TestStatus.COMPLETED:
                test_dict['verdicts']['final-verdict'] = "PASS"
            elif result.status in (TestStatus.FAILED, TestStatus.RETRY):
                test_dict['verdicts']['final-verdict'] = "FAIL"
            else:
                test_dict['verdicts']['final-verdict'] = result.status.name
            
            # THEN update reports with complete verdict information
            ReportingMethods.report_updater(test_dict)
            
            # Cleanup
            self._cleanup_environment(test_dict, result)
            
            # Only update status if it's still RUNNING (dsrs_runner didn't set it)
            if result.status == TestStatus.RUNNING:
                result.status = TestStatus.COMPLETED
            
        except Exception as e:
            # Ensure result status reflects failure
            result.status = TestStatus.FAILED
            result.error_message = f"Execution Exception: {e}"
            test_dict['verdicts']['final-verdict'] = "FAIL"
            test_dict['verdicts']['process-specific-errors'] = f"Execution Exception: {e}"
            
            # Update reports even for failed tests
            ReportingMethods.report_updater(test_dict)

            # Still try to copy logs even if test failed mid-way
            try:
                self._copy_kit_logs(test_dict)
            except Exception as log_copy_err:
                logger.error(f"Failed to copy kit logs after execution exception: {log_copy_err}")

        finally:
            # Ensure cleanup happens even if there are issues before the main cleanup call
            try:
                # All cleanup is now handled in _cleanup_environment
                pass
            except Exception as final_cleanup_err:
                logger.error(f"Error during final cleanup: {final_cleanup_err}")

    def _initialize_test_variables(self, test_dict):
        """Initialize variables needed for test execution and handle process management"""
        logger.info(f"Initializing variables for test: {test_dict.get('name', 'unnamed')}")
        
        # Import CLI mode handler and Windows develop mode
        from generic_utils.cli_mode_handler import CLIModeHandler
        from generic_utils.windows_develop_mode import WindowsDevelopMode
        
        # Check CLI mode FIRST - it takes precedence over develop mode
        if CLIModeHandler.is_cli_mode_enabled(test_dict):
            logger.info("CLI Mode enabled - skipping all UI-related setup and process management")
            varc.skip_dsrs_process_launch = True
            varc.cli_mode_enabled = True
            return
        
        # Check if Windows develop mode is enabled (only if CLI mode is not enabled)
        if WindowsDevelopMode.is_develop_mode_enabled(test_dict):
            logger.info("Windows Develop Mode enabled - checking for existing DSRS process with UI automator")
            WindowsDevelopMode.check_kit_process(test_dict, "DSRS")
            logger.info("Windows Develop Mode: Using existing DSRS process, skipping process cleanup")
            varc.skip_dsrs_process_launch = True
            
        else:
            # Normal mode - perform process cleanup
            logger.info("Normal mode - performing process cleanup")
            
            # Pre-test Process Cleanup (Windows Specific)
            try:
                # Kill specific Kit process using reusable method
                if not HelperMethods.kill_kit_process(KIT_PROCESS_NAME):
                    logger.error(f"Failed to kill Kit process: {KIT_PROCESS_NAME}")
                    raise Exception(f"Failed to kill Kit process: {KIT_PROCESS_NAME}")

            except Exception as e:
                logger.error(f"Error during pre-test process cleanup: {e}")

    def _cleanup_environment(self, test_dict, result):
        """Clean up the test environment on windows"""
        try:
            if not varc.skip_dsrs_process_launch:
                logger.info("Cleaning up DSRS Kit process...")
                if not HelperMethods.kill_kit_process(KIT_PROCESS_NAME):
                    logger.warning(f"Failed to kill Kit process: {KIT_PROCESS_NAME}")
                    # Don't raise exception here, just log warning
                logger.info("DSRS Kit process cleanup completed")
            else:
                logger.info("Skipping DSRS process cleanup (develop mode)")
            
        except Exception as e:
            result.error_message = f"Environment cleanup error: {str(e)}"

    def _generate_reports(self, test_dict):
        """
        Generate test reports after DSRS test execution
        
        Args:
            test_dict: Dictionary containing test information
        """
        logger.info(f"Generating reports for test: {test_dict.get('name', 'unnamed')}")
        
        try:
            # Get test name for reporting
            test_name = test_dict.get('name', 'unknown_test')
            
            # Determine test status - use result status from TestResult if available
            test_status = "UNKNOWN"
            error_message = "NA"
            
            # Get the test result object if it exists in the test_dict
            result = test_dict.get('test_result') 
            
            if result and hasattr(result, 'status'):
                status = result.status
                
                if status == TestStatus.COMPLETED:
                    test_status = "PASS"
                elif status in (TestStatus.FAILED, TestStatus.RETRY):
                    test_status = "FAIL"
                else:
                    test_status = status.name
                    
                # Get error message from result object
                if hasattr(result, 'error_message') and result.error_message:
                    error_message = result.error_message
            # Fallback to verdicts if result object is not available or lacks status
            elif 'verdicts' in test_dict and 'final-verdict' in test_dict['verdicts']:
                test_status = test_dict['verdicts']['final-verdict']
            
            # Get execution timing from metrics if available
            metrics = {}
            if result and hasattr(result, 'metrics'):
                metrics = result.metrics
            
            # Add the log folder path
            log_folder_path = test_dict.get('test_logs_path', 'NA')

            # Create report data structure with available information
            report_data = {
                'test_name': test_name,
                'test_type': test_dict.get('type', 'DSRS'), # Ensure this gets the correct type
                'status': test_status,
                'log_folder_path': log_folder_path, # Added log folder path
                'execution_time': {
                    'launch_time': f"{metrics.get('launch_time', 'NA'):.2f}s" if 'launch_time' in metrics and isinstance(metrics.get('launch_time'), (int, float)) else "NA",
                    'total_time': f"{metrics.get('total_execution_time', 'NA'):.2f}s" if 'total_execution_time' in metrics and isinstance(metrics.get('total_execution_time'), (int, float)) else "NA"
                },
                'errors': {
                    'error_message': error_message,
                    'process_errors': test_dict['verdicts'].get('process-specific-errors', 'NA')
                }
            }
            
            # Save report to file
            report_path = os.path.join(test_dict['test_path'], 'test_report.json')
            with open(report_path, 'w', encoding='utf-8') as f: # Added encoding
                json.dump(report_data, f, indent=4)
            
            logger.info(f"Report generated successfully: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating reports: {str(e)}")
            # Continue execution despite reporting error
        
        return True

    def _perform_logs_analysis(self, test_dict, result):
        """
        Perform comprehensive log analysis for DSRS tests if enabled
        
        Args:
            test_dict: Dictionary containing test information
            result: TestResult object to store analysis results
        """
        from generic_utils.command_runner_util import CommandRunnerMethods
        import time
        
        logger.info(f"[{test_dict['name']}] Checking if logs analysis is required")
        
        try:
            # Set test type for DSRS
            test_dict['type'] = 'DSRS'
            
            # Call main logs analysis runner (with flag control)
            analysis_success = CommandRunnerMethods.logs_analysis_runner(test_dict)
            
            # Store analysis results in TestResult object
            result.logs_analysis['analysis_completed'] = analysis_success
            result.logs_analysis['analysis_timestamp'] = time.time()
            result.logs_analysis['component_type'] = 'DSRS'
            
            if analysis_success:
                logger.info(f"[{test_dict['name']}] DSRS logs analysis completed successfully")
            else:
                logger.info(f"[{test_dict['name']}] DSRS logs analysis skipped or failed")

        except Exception as e:
            logger.exception(f"[{test_dict['name']}] Error during DSRS logs analysis: {e}")
            result.logs_analysis['analysis_error'] = str(e)
            result.logs_analysis['analysis_completed'] = False

    def _transfer_result_data_to_test_dict(self, test_dict, result):
        """
        Transfer result data to test_dict for main framework reports
        
        Args:
            test_dict: Dictionary containing test information
            result: TestResult object to transfer data from
        """
        try:
            # Transfer metrics data (execution times, etc.)
            if hasattr(result, 'metrics') and result.metrics:
                test_dict.setdefault('execution_metrics', {}).update(result.metrics)
                
                # Map specific metrics to expected report fields
                if 'launch_time' in result.metrics:
                    test_dict['verdicts']['launch-time'] = f"{result.metrics['launch_time']:.2f}s"
                
                if 'total_execution_time' in result.metrics:
                    test_dict['verdicts']['execution-time'] = f"{result.metrics['total_execution_time']:.2f}s"
            
            # Transfer logs analysis data
            if hasattr(result, 'logs_analysis') and result.logs_analysis:
                test_dict.setdefault('result_logs_analysis', {}).update(result.logs_analysis)
            
            # Transfer execution details
            if hasattr(result, 'commands_executed') and result.commands_executed:
                test_dict['commands_executed'] = result.commands_executed
            
            if hasattr(result, 'new_count'):
                test_dict['new_count'] = result.new_count
                
            if hasattr(result, 'updated_toml_name') and result.updated_toml_name:
                test_dict['updated_toml_name'] = result.updated_toml_name
                
            # Transfer error details if present
            if hasattr(result, 'error_message') and result.error_message:
                # Already handled by setting process-specific-errors in command_runner_util
                # but ensure it's properly set
                if 'process-specific-errors' not in test_dict['verdicts'] or not test_dict['verdicts']['process-specific-errors']:
                    test_dict['verdicts']['process-specific-errors'] = result.error_message
            
            logger.debug(f"Transferred result data to test_dict for {test_dict.get('name', 'unnamed')}")
            
        except Exception as e:
            logger.warning(f"Error transferring result data to test_dict: {e}")
            # Don't fail the test due to data transfer issues