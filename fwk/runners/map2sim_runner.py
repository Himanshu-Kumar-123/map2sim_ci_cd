# fwk/runners/map2sim_runner.py - MAP2SIM Component Runner

# Standard imports
import platform
import sys
import subprocess
import os
import threading
import time
from enum import Enum, auto
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json
import re
import shutil
from pathlib import Path

# Local imports
from analysis_utils.validate_logs_util import LogsSaverMethods
from generic_utils.helper_util import HelperMethods
from generic_utils.reporting_util import ReportingMethods
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger
from fwk.shared.constants import (
    KIT_PROCESS_NAME,
    MAP2SIM_LAUNCH_LOG_FILE_NAME,
    MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME
)
from generic_utils.windows_develop_mode import WindowsDevelopMode

# Platform detection
IS_WINDOWS = platform.system() == "Windows"

# Get logger for MAP2SIMRunner
logger = get_logger(__name__, varc.framework_logs_path)

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

class MAP2SIMRunner:
    """Runner specifically for MAP2SIM component tests"""
    
    def __init__(self):
        self.launch_log_file = MAP2SIM_LAUNCH_LOG_FILE_NAME
        self.scenario_log_file = MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME

    def run_tests(self, tests_list):
        """Run all tests using a queue-based approach with dynamic iteration support"""
        
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

                    # Handle iteration logic only if controller exists and not in CLI mode
                    try:
                        from generic_utils.cli_mode_handler import CLIModeHandler
                        cli_enabled = CLIModeHandler.is_cli_mode_enabled(test_dict)
                    except Exception:
                        cli_enabled = False

                    if hasattr(self, 'iteration_controller') and self.iteration_controller and not cli_enabled:
                        try:
                            self.iteration_controller.handle_test_result(test_dict, test_queue, current_index)
                        except Exception as iter_err:
                            logger.warning(f"Iteration controller error (ignored): {iter_err}")
                    
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
        
        logger.info(f"Test execution completed. Processed {len(final_results)} tests")
        return final_results
        
    def execute_test(self, test_dict, result):
        """Execute a single MAP2SIM test with proper phase management"""
        test_name = test_dict.get('name', 'unnamed')
        test_type = test_dict.get('type', 'MAP2SIM_UNKNOWN')
        
        logger.info(f"Executing MAP2SIM test: {test_name} (type: {test_type})")
        
        # Flag to prevent double report generation
        report_generated = False
        
        try:
            # Initialize test environment variables
            self._initialize_test_variables(test_dict)
            
            # Call the MAP2SIM runner from command_runner_util
            # (Screen recording is now handled inside the runner after app launch)
            from generic_utils.command_runner_util import CommandRunnerMethods
            CommandRunnerMethods.map2sim_runner(test_dict, result)
            
            # Copy application logs if available
            logger.info(f"Attempting to copy kit logs for test {test_name}")
            LogsSaverMethods.copy_kit_logs(test_dict, component='MAP2SIM')
            
            # Store result in test_dict for access during report generation
            test_dict['test_result'] = result
            
            # Transfer result data to test_dict for main framework reports
            self._transfer_result_data_to_test_dict(test_dict, result)
            
            # Set final verdict based on result status
            if result.status == TestStatus.COMPLETED:
                test_dict['verdicts']['final-verdict'] = "PASS"
            elif result.status in (TestStatus.FAILED, TestStatus.RETRY):
                test_dict['verdicts']['final-verdict'] = "FAIL"
            else:
                test_dict['verdicts']['final-verdict'] = result.status.name
            
            # Update reports with complete verdict information
            try:
                ReportingMethods.report_updater(test_dict)
                report_generated = True
            except Exception as report_err:
                logger.error(f"Error during report generation: {report_err}")
                # Don't re-raise here, let cleanup happen
            
            # Only update status if it's still RUNNING
            if result.status == TestStatus.RUNNING:
                result.status = TestStatus.COMPLETED
            
        except Exception as e:
            # Handle exceptions...
            result.status = TestStatus.FAILED
            result.error_message = f"Execution Exception: {e}"
            test_dict['verdicts']['final-verdict'] = "FAIL"
            test_dict['verdicts']['process-specific-errors'] = f"Execution Exception: {e}"
            
            # Only generate report if not already generated
            if not report_generated:
                try:
                    ReportingMethods.report_updater(test_dict)
                except Exception as report_err:
                    logger.error(f"Error during exception report generation: {report_err}")

            # Still try to copy logs even if test failed mid-way
            try:
                LogsSaverMethods.copy_kit_logs(test_dict, component='MAP2SIM')
            except Exception as log_copy_err:
                logger.error(f"Failed to copy application logs after execution exception: {log_copy_err}")
            
        finally:
            # Cleanup ALWAYS runs regardless of success/failure/exception
            try:
                self._cleanup_environment(test_dict, result)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")

    def _initialize_test_variables(self, test_dict):
        """Initialize variables needed for test execution and handle process management"""
        logger.info(f"Initializing variables for test: {test_dict.get('name', 'unnamed')}")
        
        # Import CLI mode handler
        from generic_utils.cli_mode_handler import CLIModeHandler
        
        # Check CLI mode FIRST - it takes precedence over develop mode
        if CLIModeHandler.is_cli_mode_enabled(test_dict):
            logger.info("CLI Mode enabled - skipping all UI-related setup and process management")
            varc.skip_map2sim_process_launch = True
            varc.cli_mode_enabled = True
            return
            
        # Check if Windows develop mode is enabled (only if CLI mode is not enabled)
        if WindowsDevelopMode.is_develop_mode_enabled(test_dict):
            logger.info("Windows Develop Mode enabled - checking for existing MAP2SIM process with UI automator")
            
            # Check for existing Kit process with UI automator (specify MAP2SIM component)
            WindowsDevelopMode.check_kit_process(test_dict, "MAP2SIM")
            
            # If we reach here, suitable process was found
            logger.info("Windows Develop Mode: Using existing MAP2SIM process, skipping process cleanup")
            varc.skip_map2sim_process_launch = True
            
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
        """Clean up the MAP2SIM test environment on Windows"""
        try:
                             
            if not varc.skip_map2sim_process_launch:
                logger.info("Cleaning up MAP2SIM Kit process...")
                if not HelperMethods.kill_kit_process(KIT_PROCESS_NAME):
                    logger.warning(f"Failed to kill Kit process: {KIT_PROCESS_NAME}")
                    # Don't raise exception here, just log warning
                logger.info("MAP2SIM Kit process cleanup completed")
            else:
                logger.info("Skipping MAP2SIM process cleanup (develop mode)")
            
            logger.debug("MAP2SIM environment cleanup completed")
            
        except Exception as e:
            result.error_message = f"Environment cleanup error: {str(e)}"
            logger.error(f"Error during MAP2SIM environment cleanup: {e}")

    def _generate_reports(self, test_dict):
        """Generate test reports after MAP2SIM test execution"""
        logger.info(f"Generating reports for MAP2SIM test: {test_dict.get('name', 'unnamed')}")
        
        try:
            # Get test name for reporting
            test_name = test_dict.get('name', 'unknown_test')
            
            # Determine test status
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
            elif 'verdicts' in test_dict and 'final-verdict' in test_dict['verdicts']:
                test_status = test_dict['verdicts']['final-verdict']
            
            # Get execution timing from metrics if available
            metrics = {}
            if result and hasattr(result, 'metrics'):
                metrics = result.metrics
            
            # Get log folder path
            log_folder_path = test_dict.get('test_logs_path', 'NA')

            # Create report data structure
            report_data = {
                'test_name': test_name,
                'test_type': test_dict.get('type', 'MAP2SIM'),
                'status': test_status,
                'log_folder_path': log_folder_path,
                'execution_time': {
                    'total_time': f"{metrics.get('execution_time', 'NA'):.2f}s" if 'execution_time' in metrics and isinstance(metrics.get('execution_time'), (int, float)) else "NA"
                },
                'errors': {
                    'error_message': error_message,
                    'process_errors': test_dict['verdicts'].get('process-specific-errors', 'NA')
                }
            }
            
            # Save report to file
            report_path = os.path.join(test_dict['test_path'], 'test_report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4)
            
            logger.info(f"MAP2SIM report generated successfully: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating MAP2SIM reports: {str(e)}")
        
        return True 

    def _perform_logs_analysis(self, test_dict, result):
        """
        Perform comprehensive log analysis for MAP2SIM tests if enabled
        
        Args:
            test_dict: Dictionary containing test information
            result: TestResult object to store analysis results
        """
        from generic_utils.command_runner_util import CommandRunnerMethods
        import time
        
        logger.info(f"[{test_dict['name']}] Checking if logs analysis is required")
        
        try:
            # Set test type for MAP2SIM
            test_dict['type'] = 'MAP2SIM'
            
            # Call main logs analysis runner (with flag control)
            analysis_success = CommandRunnerMethods.logs_analysis_runner(test_dict)
            
            # Store analysis results in TestResult object
            result.logs_analysis['analysis_completed'] = analysis_success
            result.logs_analysis['analysis_timestamp'] = time.time()
            result.logs_analysis['component_type'] = 'MAP2SIM'
            
            if analysis_success:
                logger.info(f"[{test_dict['name']}] MAP2SIM logs analysis completed successfully")
            else:
                logger.info(f"[{test_dict['name']}] MAP2SIM logs analysis skipped or failed")

        except Exception as e:
            logger.exception(f"[{test_dict['name']}] Error during MAP2SIM logs analysis: {e}")
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