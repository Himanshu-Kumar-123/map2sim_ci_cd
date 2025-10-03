# -*- coding: utf-8 -*-
"""
CLI Mode Handler for DMF Framework
Handles CLI mode detection, execution, and test infrastructure
"""

import os
import sys
import json
import base64
import logging
import subprocess
import time
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime

# Local imports
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger
from generic_utils.helper_util import HelperMethods

logger = get_logger(__name__)

class CLIModeHandler:
    """Handles CLI mode detection, execution, and test infrastructure"""
    
    @staticmethod
    def is_cli_mode_enabled(test_dict: Dict[str, Any]) -> bool:
        """
        Check if CLI mode is enabled via automation flags
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            bool: True if CLI mode should be used, False otherwise
        """
        # Check both test-specific and suite-level flags dictionaries
        flag_dicts_to_check = []
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            flag_dicts_to_check.append(('test-level', test_dict['automation_flags_dict']))
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            flag_dicts_to_check.append(('suite-level', test_dict['automation_suite_flags_dict']))
        
        # Look for --enable_cli_mode flag in dictionaries
        for level_name, flag_dict in flag_dicts_to_check:
            if '--enable_cli_mode' in flag_dict:
                logger.info(f"[{test_dict['name']}] Found --enable_cli_mode flag in {level_name} flags, enabling CLI mode")
                return True
        
        # Default: CLI mode disabled
        logger.debug(f"[{test_dict['name']}] No --enable_cli_mode flag found, CLI mode disabled")
        return False
    
    @staticmethod
    def should_skip_ui_setup(test_dict: Dict[str, Any]) -> bool:
        """
        Determine if UI setup should be skipped based on CLI mode
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            bool: True if UI setup should be skipped
        """
        return CLIModeHandler.is_cli_mode_enabled(test_dict)
    
    @staticmethod
    def generate_cli_pytest_command(test_dict: Dict[str, Any]) -> str:
        """
        Generate pytest command for CLI mode execution
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            str: Pytest command for CLI execution
        """
        from generic_utils.command_generator_util import CommandGeneratorMethods
        
        # Get Python executable
        try:
            python_exe = CommandGeneratorMethods._get_python_executable()
            logger.info(f"Using Python executable for CLI pytest: {python_exe}")
        except RuntimeError as e:
            logger.error(f"Failed to get suitable Python executable: {e}")
            raise
        
        # Get script path and scenario
        script_path = test_dict['script_path']
        scenario_name = test_dict['scenario']
        scenario_full_path = os.path.join(script_path, scenario_name)
        
        logger.info(f"CLI Mode: Using scenario path: {scenario_full_path}")
        
        # Build CLI-specific pytest command
        pytest_command = f"{python_exe} -m pytest -s {scenario_full_path}"
        pytest_command += f" --output_path={test_dict['test_path']}"
        pytest_command += " --cli_mode=true"  # Add CLI mode flag
        
        # Add CLI-specific flags if any
        cli_flags_dict = CLIModeHandler._extract_cli_flags(test_dict)
        # Always include batch_file_path and batch_args if present so tests can consume without hardcoding
        try:
            if test_dict.get('batch_file_path'):
                cli_flags_dict.setdefault('batch_file_path', test_dict['batch_file_path'])
            if test_dict.get('batch_args') is not None:
                cli_flags_dict.setdefault('batch_args', test_dict['batch_args'])
        except Exception:
            pass
        if cli_flags_dict:
            # Serialize CLI flags to JSON and encode as base64
            cli_flags_json = json.dumps(cli_flags_dict)
            encoded_json = base64.b64encode(cli_flags_json.encode('utf-8')).decode('ascii')
            pytest_command += f" --json_data_b64 {encoded_json}"
        
        return pytest_command
    
    @staticmethod
    def _extract_cli_flags(test_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract CLI-specific flags from test configuration
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            Dict: CLI-specific flags
        """
        cli_flags = {}
        
        # Add automation suite flags
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            for key, value in test_dict['automation_suite_flags_dict'].items():
                # Filter for CLI-specific flags
                if key.startswith("--cli") or key == "--ui_debug_mode":
                    cli_flags[key] = value
        
        # Add automation flags
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            for key, value in test_dict['automation_flags_dict'].items():
                # Filter for CLI-specific flags
                if key.startswith("--cli") or key == "--ui_debug_mode":
                    cli_flags[key] = value
        
        return cli_flags
    
    @staticmethod
    def create_cli_test_log(test_dict: Dict[str, Any], log_path: str) -> None:
        """
        Create a CLI mode test log
        
        Args:
            test_dict: Test configuration dictionary
            log_path: Path to log file
        """
        try:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write("=== CLI MODE TEST EXECUTION ===\n")
                f.write(f"Test Name: {test_dict.get('name', 'unnamed')}\n")
                f.write(f"Test Type: {test_dict.get('type', 'unknown')}\n")
                f.write(f"Component: {test_dict.get('component', 'unknown')}\n")
                f.write(f"Script Path: {test_dict.get('script_path', 'unknown')}\n")
                f.write(f"Scenario: {test_dict.get('scenario', 'unknown')}\n")
                f.write(f"CLI Mode: ENABLED\n")
                f.write(f"UI App Launch: SKIPPED\n")
                f.write(f"UI Automator: NOT REQUIRED\n")
                f.write("=" * 50 + "\n")
        except Exception as e:
            logger.warning(f"Failed to create CLI test log: {e}")
    
    @staticmethod
    def validate_cli_test_requirements(test_dict: Dict[str, Any]) -> bool:
        """
        Validate that CLI test has required configuration
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            bool: True if requirements are met
        """
        required_fields = ['script_path', 'scenario', 'test_path']
        
        for field in required_fields:
            if field not in test_dict or not test_dict[field]:
                logger.error(f"CLI Mode: Missing required field '{field}' in test configuration")
                return False
        
        # Check if scenario file exists
        scenario_path = os.path.join(test_dict['script_path'], test_dict['scenario'])
        if not os.path.exists(scenario_path):
            logger.error(f"CLI Mode: Scenario file not found: {scenario_path}")
            return False
        
        return True

    @staticmethod
    def setup_cli_logging(test_dict: Dict[str, Any]) -> Tuple[object, str]:
        """
        Setup CLI-specific logging using DMF framework logger
        
        Args:
            test_dict: Test configuration dictionary
            
        Returns:
            Tuple of (logger, log_file_path)
        """
        test_name = test_dict.get('name', 'unnamed_cli_test')
        test_path = test_dict.get('test_path', './cli_test_logs')
        
        # Create CLI-specific log directory
        cli_log_dir = os.path.join(test_path, 'cli_logs')
        os.makedirs(cli_log_dir, exist_ok=True)
        
        # Use DMF framework logger with CLI-specific naming
        cli_logger = get_logger(f'CLI_MODE_{test_name}', file_path=varc.framework_logs_path)
        
        # Create CLI-specific log file
        log_file = os.path.join(cli_log_dir, f'{test_name}_cli_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        # Add file handler for CLI-specific logs
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - CLI Mode - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            cli_logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Failed to add CLI-specific file handler: {e}")
        
        return cli_logger, log_file

    @staticmethod
    def execute_cli_test_with_reporting(test_dict: Dict[str, Any], pytest_command: str) -> Tuple[Dict, str]:
        """
        Execute CLI test with proper DMF logging and reporting integration
        
        Args:
            test_dict: Test configuration dictionary
            pytest_command: Pytest command to execute
            
        Returns:
            Tuple of (test_result_dict, report_file_path)
        """
        # Use framework TestStatus if available; otherwise, fallback to simple string statuses
        try:
            from fwk.shared.test_status import TestStatus  # type: ignore
        except Exception:
            class TestStatus:  # Fallback for CLI-only contexts
                RUNNING = "RUNNING"
                COMPLETED = "COMPLETED"
                FAILED = "FAILED"
        
        # Setup CLI logging
        cli_logger, log_file = CLIModeHandler.setup_cli_logging(test_dict)
        
        cli_logger.info(f"Starting CLI test execution: {test_dict.get('name')}")
        cli_logger.info(f"Pytest command: {pytest_command}")
        
        # Initialize test result structure compatible with DMF framework
        test_result = {
            'test_name': test_dict.get('name'),
            'execution_mode': 'CLI',
            'start_time': datetime.now().isoformat(),
            'status': TestStatus.RUNNING,
            'return_code': None,
            'output': '',
            'error_output': '',
            'execution_time': 0
        }
        
        start_time = time.time()
        
        # Determine if screen recording is requested via flags
        screen_recording_requested = False
        try:
            screen_recording_requested = (
                ("automation_flags_dict" in test_dict and "--record-screen" in test_dict["automation_flags_dict"]) or
                ("automation_suite_flags_dict" in test_dict and "--record-screen" in test_dict["automation_suite_flags_dict"])
            )
        except Exception:
            screen_recording_requested = False

        ffmpeg_process = None

        try:
            # If requested, start screen recording for CLI as well
            if screen_recording_requested:
                try:
                    from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                    cli_logger.info("CLI Mode: Starting screen recording as --record-screen was requested")
                    ffmpeg_process = PretestAnalysisCallerMethods.windows_ffmpeg_recorder_caller(test_dict)
                    if ffmpeg_process:
                        cli_logger.info(f"CLI Mode: Screen recording started (PID: {ffmpeg_process.pid})")
                    else:
                        # Align with UI behavior: fail the test if recording was requested but failed to start
                        error_msg = "Screen recording FAILED to start when --record-screen flag was specified (CLI mode)"
                        cli_logger.error(error_msg)
                        test_result.update({
                            'status': TestStatus.FAILED,
                            'error_output': error_msg,
                            'verdict': 'FAIL'
                        })
                        raise RuntimeError(error_msg)
                except Exception as rec_err:
                    error_msg = f"Screen recording FAILED with exception when --record-screen flag was specified (CLI mode): {str(rec_err)}"
                    cli_logger.error(error_msg)
                    test_result.update({
                        'status': TestStatus.FAILED,
                        'error_output': error_msg,
                        'verdict': 'FAIL'
                    })
                    raise

            # Execute the CLI test
            cli_logger.info(f"Executing CLI test: {test_dict.get('name')}")
            # Prepare environment so child process (pytest, and any subprocesses it spawns) know per-test paths
            env = os.environ.copy()
            try:
                if test_dict.get('test_path'):
                    env.setdefault('DMF_TEST_OUTPUT_PATH', test_dict['test_path'])
                if test_dict.get('test_logs_path'):
                    env.setdefault('DMF_TEST_LOGS_PATH', test_dict['test_logs_path'])
                if test_dict.get('test_raw_data_path'):
                    env.setdefault('DMF_TEST_RAW_DATA_PATH', test_dict['test_raw_data_path'])
                if test_dict.get('name'):
                    env.setdefault('DMF_TEST_NAME', test_dict['name'])
            except Exception:
                pass
            process = subprocess.Popen(
                pytest_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd(),
                env=env
            )
            
            # Capture output in real-time
            output_lines = []
            error_lines = []
            
            # Read stdout
            for line in iter(process.stdout.readline, ''):
                output_lines.append(line.strip())
                cli_logger.info(f"CLI Output: {line.strip()}")
            
            # Read stderr
            for line in iter(process.stderr.readline, ''):
                error_lines.append(line.strip())
                cli_logger.warning(f"CLI Error: {line.strip()}")
            
            # Wait for completion
            return_code = process.wait()
            
            # Calculate execution time
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Update test result
            test_result.update({
                'status': TestStatus.COMPLETED if return_code == 0 else TestStatus.FAILED,
                'return_code': return_code,
                'output': '\n'.join(output_lines),
                'error_output': '\n'.join(error_lines),
                'execution_time': execution_time,
                'end_time': datetime.now().isoformat()
            })
            
            # Analyze results using DMF patterns
            verdict = CLIModeHandler._analyze_cli_test_output(
                test_result['output'], test_result['error_output'], test_dict.get('name'), test_result.get('return_code')
            )
            test_result['verdict'] = verdict
            
            cli_logger.info(f"CLI test completed with return code: {return_code}")
            cli_logger.info(f"CLI test verdict: {verdict}")
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            error_msg = f"CLI test execution failed: {str(e)}"
            cli_logger.error(error_msg)
            
            test_result.update({
                'status': TestStatus.FAILED,
                'return_code': -1,
                'error_output': error_msg,
                'execution_time': execution_time,
                'end_time': datetime.now().isoformat(),
                'verdict': 'FAIL'
            })
        finally:
            # Stop screen recording if it was started
            if ffmpeg_process:
                try:
                    from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                    cli_logger.info("CLI Mode: Stopping screen recording")
                    PretestAnalysisCallerMethods.windows_stop_ffmpeg_recording(ffmpeg_process)
                    cli_logger.info("CLI Mode: Screen recording stopped successfully")
                except Exception as stop_err:
                    cli_logger.error(f"CLI Mode: Error stopping screen recording: {stop_err}")
        
        # Generate CLI report using DMF reporting system
        report_file = CLIModeHandler._generate_cli_report(test_dict, test_result, log_file)
        
        # Print CLI summary
        CLIModeHandler._print_cli_summary(test_result, report_file)
        
        return test_result, report_file

    @staticmethod
    def _analyze_cli_test_output(output: str, error_output: str, test_name: str, return_code: Optional[int] = None) -> str:
        """
        Analyze CLI test output using DMF-compatible patterns
        
        Args:
            output: Standard output from test
            error_output: Error output from test
            test_name: Name of the test
            
        Returns:
            str: Test verdict (PASS/FAIL/UNKNOWN)
        """
        
        # CLI-specific success patterns
        success_patterns = [
            f"CLI Mode: {test_name} completed successfully",
            "PASSED",
            "test passed",
            "CLI operation completed",
            "CLI Mode: Test execution successful",
            "=== CLI Mode Test Completed Successfully ==="
        ]
        
        # CLI-specific failure patterns
        failure_patterns = [
            f"CLI Mode: {test_name} failed",
            "FAILED",
            "test failed",
            "CLI Mode: Test execution failed",
            "Error in CLI operation",
            "CLI Mode: Exception occurred",
            "AssertionError",
            "Exception:",
            "Traceback (most recent call last):"
        ]
        
        # Combine output and error for analysis
        combined_output = f"{output}\n{error_output}"
        
        # Check for failure patterns first (they take precedence)
        failure_found = any(pattern in combined_output for pattern in failure_patterns)
        success_found = any(pattern in combined_output for pattern in success_patterns)

        # Heuristic: recognize standard pytest summaries like "1 passed" or "passed in 0.01s"
        try:
            import re
            if not success_found:
                if re.search(r"\b\d+\s+passed\b", combined_output, flags=re.IGNORECASE):
                    success_found = True
                elif re.search(r"\bpassed in\b", combined_output, flags=re.IGNORECASE):
                    success_found = True
        except Exception:
            # Do not fail verdicting due to regex errors
            pass
        
        if failure_found:
            return "FAIL"
        elif success_found:
            return "PASS"
        # As a final fallback, treat return code 0 as PASS for CLI mode
        elif return_code == 0:
            return "PASS"
        else:
            return "UNKNOWN"

    @staticmethod
    def _generate_cli_report(test_dict: Dict[str, Any], test_result: Dict[str, Any], log_file: str) -> str:
        """
        Generate CLI-specific test report using DMF reporting system
        
        Args:
            test_dict: Test configuration dictionary
            test_result: Test execution result
            log_file: Path to CLI log file
            
        Returns:
            str: Path to generated report file
        """
        test_name = test_dict.get('name', 'unnamed_cli_test')
        test_path = test_dict.get('test_path', './cli_test_logs')
        
        # Create reports directory
        reports_dir = os.path.join(test_path, 'cli_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate report file
        report_file = os.path.join(reports_dir, f'{test_name}_cli_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        # Create DMF-compatible report structure
        report_data = {
            'test_name': test_name,
            'execution_mode': 'CLI',
            'timestamp': datetime.now().isoformat(),
            'test_result': test_result,
            'log_file': log_file,
            'framework_log_file': varc.framework_logs_path,
            'status': test_result.get('verdict', 'UNKNOWN'),
            'execution_time': test_result.get('execution_time', 0),
            'return_code': test_result.get('return_code', -1)
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"CLI report generated: {report_file}")
            
            # Also update main DMF report if possible
            CLIModeHandler._update_dmf_main_report(test_dict, report_data)
            
        except Exception as e:
            logger.error(f"Failed to generate CLI report: {e}")
        
        return report_file

    @staticmethod
    def _update_dmf_main_report(test_dict: Dict[str, Any], report_data: Dict[str, Any]) -> None:
        """
        Update main DMF report with CLI test results
        
        Args:
            test_dict: Test configuration dictionary
            report_data: CLI test report data
        """
        try:
            from generic_utils.reporting_util import ReportingMethods
            
            # Create test_dict compatible with DMF reporting
            dmf_test_dict = {
                'name': test_dict.get('name'),
                'verdicts': {
                    'final-verdict': report_data['status'],
                    'execution-mode': 'CLI',
                    'execution-time': report_data['execution_time'],
                    'return-code': report_data['return_code']
                },
                'test_result': report_data['test_result']
            }
            
            # Update DMF report
            ReportingMethods.report_updater(dmf_test_dict)
            
        except Exception as e:
            logger.warning(f"Failed to update DMF main report: {e}")

    @staticmethod
    def _print_cli_summary(test_result: Dict[str, Any], report_file: str) -> None:
        """
        Print CLI test execution summary using DMF logging
        
        Args:
            test_result: Test execution result
            report_file: Path to report file
        """
        logger.info("\n" + "="*80)
        logger.info("CLI MODE TEST EXECUTION SUMMARY")
        logger.info("="*80)
        logger.info(f"Test Name: {test_result.get('test_name', 'Unknown')}")
        logger.info(f"Execution Mode: CLI")
        logger.info(f"Status: {test_result.get('status', 'Unknown')}")
        logger.info(f"Verdict: {test_result.get('verdict', 'Unknown')}")
        logger.info(f"Return Code: {test_result.get('return_code', 'Unknown')}")
        logger.info(f"Execution Time: {test_result.get('execution_time', 0):.2f} seconds")
        logger.info(f"Report File: {report_file}")
        logger.info("="*80)
