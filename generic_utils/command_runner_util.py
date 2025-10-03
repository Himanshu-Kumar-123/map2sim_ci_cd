# Standard library imports
import os
import time
import json
import threading
import subprocess
from enum import Enum
import re

# Local imports
from fwk.shared.variables_util import varc
from generic_utils.helper_util import HelperMethods
from generic_utils.command_generator_util import CommandGeneratorMethods
from generic_utils.analysis_caller_util import PosttestAnalysisCallerMethods
from fwk.runners.dsrs_runner import TestResult, TestStatus
from analysis_utils.validate_logs_util import LoggerMethods, LogsSaverMethods
from fwk.shared.constants import (
    DSRS_LAUNCH_LOG_FILE_NAME,
    MAP2SIM_LAUNCH_LOG_FILE_NAME,
    DSRS_SCENARIO_TYPE,
    MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME,
    MAP2SIM_SCENARIO_TYPE,
    PYTEST_ROOT_DIR,
    DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME, 
    DSRS_SCENARIO_TYPE, 
    MAP2SIM_LAUNCH_TIMEOUT, 
    DSRS_LAUNCH_TIMEOUT, 
    MAP2SIM_SCENARIO_LAUNCH_TIMEOUT, 
    DSRS_SCENARIO_LAUNCH_TIMEOUT
)
from fwk.fwk_logger.fwk_logging import get_logger
from generic_utils.windows_develop_mode import WindowsDevelopMode

logger = get_logger(__name__, varc.framework_logs_path)


class CommandRunnerMethods:
    '''This class consist of methods that are used to run different DSRS and MAP2SIM commands'''
    
    @staticmethod
    def _get_timeout_values(test_dict, component='DSRS'):
        """
        Extract timeout values from automation flags or use defaults
        
        Args:
            test_dict: Test dictionary containing automation flags
            component: Component type ('DSRS' or 'MAP2SIM')
            
        Returns:
            dict: Dictionary with launch_timeout and scenario_timeout values
        """
        # Default timeout values based on component
        if component == 'DSRS':
            default_launch = DSRS_LAUNCH_TIMEOUT
            default_scenario = DSRS_SCENARIO_LAUNCH_TIMEOUT
        else:  # MAP2SIM
            default_launch = MAP2SIM_LAUNCH_TIMEOUT
            default_scenario = MAP2SIM_SCENARIO_LAUNCH_TIMEOUT
        
        # Check for custom timeout in automation flags
        custom_timeout = None
        
        # Check both test-specific and suite-level flags dictionaries
        flag_dicts_to_check = []
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            flag_dicts_to_check.append(('test-level', test_dict['automation_flags_dict']))
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            flag_dicts_to_check.append(('suite-level', test_dict['automation_suite_flags_dict']))
        
        # Look for --timeout flag in dictionaries
        for level_name, flag_dict in flag_dicts_to_check:
            if '--timeout' in flag_dict:
                timeout_value = flag_dict['--timeout']
                if timeout_value is not None:
                    try:
                        custom_timeout = int(timeout_value)
                        logger.info(f"Found custom timeout in {level_name} flags: {custom_timeout}s")
                        break
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid timeout value in {level_name} flags: '{timeout_value}' (expected integer)")
                else:
                    logger.warning(f"Found --timeout flag in {level_name} flags but no value specified")
        
        # Apply custom timeout logic: custom timeout affects both launch and scenario
        if custom_timeout:
            launch_timeout = custom_timeout
            scenario_timeout = custom_timeout
            logger.info(f"Using custom timeouts - Launch: {launch_timeout}s, Scenario: {scenario_timeout}s")
        else:
            # Use default timeouts for both
            launch_timeout = default_launch
            scenario_timeout = default_scenario
            logger.info(f"Using default timeouts - Launch: {launch_timeout}s, Scenario: {scenario_timeout}s")
        
        return {
            'launch_timeout': launch_timeout,
            'scenario_timeout': scenario_timeout
        }
    @staticmethod
    def logs_analysis_runner(test_dict):
        '''This function is used to call analyze logs class for Windows DMF framework
        
        Args:
            test_dict (dict): A dictionary containing test data.
            
        Returns:
            bool: True if analysis completed successfully, False otherwise
        '''
        
        # Check if logs analysis is enabled via automation flags
        if not CommandRunnerMethods._is_logs_analysis_enabled(test_dict):
            logger.info(f"[{test_dict['name']}] Logs analysis disabled - skipping analysis")
            return False
        
        logger.info(f"[{test_dict['name']}] Starting comprehensive logs analysis for Windows DMF framework")
        
        try:
            # 1. Always analyze sim terminal logs (main execution logs)
            logger.debug(f"[{test_dict['name']}] Analyzing sim terminal logs")
            PosttestAnalysisCallerMethods.analyze_sim_terminal_logs_caller(test_dict)
            
            # 2. Always analyze Kit logs (both DSRS and MAP2SIM use Kit)
            logger.debug(f"[{test_dict['name']}] Analyzing Kit logs")
            if hasattr(varc, 'kit_file_name') and varc.kit_file_name is not None:
                PosttestAnalysisCallerMethods.analyze_kit_logs_caller(test_dict)
            else:
                logger.warning(f"[{test_dict['name']}] Kit file name not available for analysis")
            
            # 3. Always analyze pytest logs (both DSRS and MAP2SIM use pytest for UI automation)
            logger.debug(f"[{test_dict['name']}] Analyzing pytest logs")
            PosttestAnalysisCallerMethods.analyze_pytest_logs_caller(test_dict)
            
            logger.info(f"[{test_dict['name']}] Logs analysis completed successfully")
            return True

        except Exception as e:
            error_msg = f"Logs analysis failed: {str(e)}"
            logger.exception(f"[{test_dict['name']}] {error_msg}")
            test_dict['verdicts']['process_specific_errors'] = error_msg
            return False

    @staticmethod
    def _is_logs_analysis_enabled(test_dict):
        '''Check if logs analysis is enabled via automation flags
        
        Args:
            test_dict (dict): A dictionary containing test data.
            
        Returns:
            bool: True if logs analysis should be performed, False otherwise
        '''
        
        # Check both test-specific and suite-level flags dictionaries
        flag_dicts_to_check = []
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            flag_dicts_to_check.append(('test-level', test_dict['automation_flags_dict']))
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            flag_dicts_to_check.append(('suite-level', test_dict['automation_suite_flags_dict']))
        
        # Look for --enable_logs_analysis_runner flag in dictionaries
        for level_name, flag_dict in flag_dicts_to_check:
            if '--enable_logs_analysis_runner' in flag_dict:
                logger.debug(f"[{test_dict['name']}] Found --enable_logs_analysis_runner flag in {level_name} flags, enabling logs analysis")
                return True
        
        # Default: logs analysis disabled
        logger.debug(f"[{test_dict['name']}] No --enable_logs_analysis_runner flag found, logs analysis disabled")
        return False
    
    @staticmethod
    def _is_cli_mode_enabled(test_dict):
        '''Check if CLI mode is enabled via automation flags
        
        Args:
            test_dict (dict): A dictionary containing test data.
            
        Returns:
            bool: True if CLI mode should be used (skip app launch), False otherwise
        '''
        # Use the new CLI mode handler
        from generic_utils.cli_mode_handler import CLIModeHandler
        return CLIModeHandler.is_cli_mode_enabled(test_dict)
    
    @staticmethod
    def dsrs_runner(test_dict, result):
        """
        This function is used to run DSRS commands
        
        Supports multiple execution modes:
        - Normal Mode: Launches DSRS app and runs scenario
        - Develop Mode: Uses existing DSRS process (via skip_dsrs_process_launch)
        - CLI Mode: Skips app launch entirely and runs scenario directly (via --enable_cli_mode flag)
        
        Args:
            test_dict: Dictionary containing test information
            result: TestResult object to store execution results
            
        Returns:
            ui_commands_list: List of DSRS commands executed
        """
        
        # Get timeout values (custom or default)
        timeout_values = CommandRunnerMethods._get_timeout_values(test_dict, 'DSRS')
        launch_timeout = timeout_values['launch_timeout']
        scenario_timeout = timeout_values['scenario_timeout']
        varc.sim_terminal_log_path = f"{test_dict['test_logs_path']}/{DSRS_LAUNCH_LOG_FILE_NAME}"
        
        # Set up environment variables for colored output
        env = os.environ.copy()
        env['FORCE_COLOR'] = '1'
        env['PY_COLORS'] = '1'
        ui_commands_list = None
        
        # Mark as running and store start time
        result.status = TestStatus.RUNNING
        start_time = time.time()
        
        try:
            logger.info(f"[{test_dict['name']}] Starting DSRS runner with timeouts - Launch: {launch_timeout}s, Scenario: {scenario_timeout}s")
            
            ui_automation_start_event = threading.Event()
            ui_automation_end_event = threading.Event()
            ui_automation_timeout_event = threading.Event()
            
            # Generate commands
            ui_commands_list = CommandGeneratorMethods.dsrs_command_generator(test_dict)
            varc.test_command_dict["dsrs_commands_list"] = ui_commands_list
            
            # Store commands in result object
            result.commands_executed.extend([cmd[0] for cmd in ui_commands_list[0]])
            
            logger.info(f"Executing DSRS commands --- {ui_commands_list[0][0]} and {ui_commands_list[0][1]}")
            
            # At the top of the dsrs_runner method:
            output1 = None
            output2 = None
            
            # CHECK FOR CLI MODE OR DEVELOP MODE - SKIP PROCESS LAUNCH
            cli_mode_enabled = CommandRunnerMethods._is_cli_mode_enabled(test_dict)
            develop_mode_enabled = hasattr(varc, 'skip_dsrs_process_launch') and varc.skip_dsrs_process_launch
            
            if cli_mode_enabled or develop_mode_enabled:
                if cli_mode_enabled:
                    logger.info(f"[{test_dict['name']}] CLI Mode: Skipping DSRS app launch, running scenario directly")
                else:
                    logger.info(f"[{test_dict['name']}] Windows Develop Mode: Skipping DSRS process launch, using existing process")
                
                # Set the start event to indicate "launch" is complete
                ui_automation_start_event.set()
                launch_successful = True
                
                # Record minimal launch time since we're skipping
                result.metrics['launch_time'] = 0.0
                
            else:
                # NORMAL MODE - FULL LAUNCH FLOW
                logger.info(f"[{test_dict['name']}] Normal Mode: Launching DSRS process")

            # Then in the build_launch function:
            def build_launch():
                nonlocal output1  # Access the outer variable
                logger.info(f"[{test_dict['name']}] Launching Sim Ready Studio")
                output1 = subprocess.Popen(
                    ui_commands_list[0][0], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    cwd=varc.cwd, 
                    shell=True,
                    bufsize=0,  # Force unbuffered output
                    universal_newlines=True,
                    encoding='utf-8',
                    errors='ignore'  # Text mode improves line handling
                )
                LoggerMethods.dsrs_launch_verification(
                    test_dict, 
                    output1,
                    DSRS_SCENARIO_TYPE, 
                    start_event=ui_automation_start_event,
                    end_event=ui_automation_end_event,
                    timeout_event=ui_automation_timeout_event,
                    timeout=launch_timeout  # Pass custom timeout
                )
            
            # Start the DSRS launch thread
            thread1 = threading.Thread(target=build_launch)
            thread1.daemon = True
            thread1.start()
            
            # Wait for either start event (success) or end event (failure)
            launch_start = time.time()
            last_status_report = time.time()  # For periodic status updates
            logger.info(f"[{test_dict['name']}] Waiting for DSRS launch events...")

            # --- Check Status and Perform Fallback Logic ---
            launch_successful = False
            
            # Continuously check events while thread is running
            while thread1.is_alive():
                current_time = time.time()
                elapsed = current_time - launch_start
                
                # Provide periodic status updates (every 10 seconds)
                if current_time - last_status_report > 10:
                    logger.info(f"[{test_dict['name']}] Still waiting for DSRS launch - elapsed: {elapsed:.1f}s")
                    logger.info(f"[{test_dict['name']}] Event status - start: {ui_automation_start_event.is_set()}, end: {ui_automation_end_event.is_set()}, timeout: {ui_automation_timeout_event.is_set()}")
                    last_status_report = current_time
                
                # Check for success
                if ui_automation_start_event.is_set():
                    launch_successful = True
                    logger.info(f"[{test_dict['name']}] DSRS launch confirmed via stdout.")
                    break
                
                # Check for failure
                if ui_automation_end_event.is_set():
                    logger.error(f"[{test_dict['name']}] DSRS launch failed (end_event set).")
                    result.error_message = "DSRS launch verification failed"
                    result.status = TestStatus.FAILED
                    test_dict['verdicts']['process-specific-errors'] = result.error_message
                    return ui_commands_list
                
                # Check for timeout - if timeout, try fallback
                if ui_automation_timeout_event.is_set():
                    logger.warning(f"[{test_dict['name']}] Timeout event set, trying fallback check in Kit log.")
                    
                    # Check Kit log as fallback
                    if LogsSaverMethods.check_kit_log_for_app_ready(test_dict, DSRS_LAUNCH_LOG_FILE_NAME, 'DSRS'):
                        launch_successful = True
                        logger.info(f"[{test_dict['name']}] Fallback successful: 'app ready' found in Kit log.")
                        break
                    else:
                        logger.error(f"[{test_dict['name']}] Fallback check failed: 'app ready' not found in Kit log.")
                        result.error_message = "DSRS launch failed: 'app ready' not found in stdout or Kit log"
                        result.status = TestStatus.FAILED
                        test_dict['verdicts']['process-specific-errors'] = result.error_message
                        return ui_commands_list
                
                    # Handle main timeout (don't rely on timeout_event) - Use custom timeout
                if elapsed > launch_timeout:
                    logger.warning(f"[{test_dict['name']}] Launch timeout reached ({launch_timeout}s), checking Kit log directly.")
                    
                    # Try fallback check in Kit log
                    if LogsSaverMethods.check_kit_log_for_app_ready(test_dict, DSRS_LAUNCH_LOG_FILE_NAME, 'DSRS'):
                        launch_successful = True
                        logger.info(f"[{test_dict['name']}] Fallback successful: 'app ready' found in Kit log.")
                        break
                    else:
                        logger.error(f"[{test_dict['name']}] Fallback check failed: 'app ready' not found in Kit log.")
                        result.error_message = f"DSRS launch failed: 'app ready' not found within {launch_timeout}s timeout or in Kit log"
                        result.status = TestStatus.FAILED
                        test_dict['verdicts']['process-specific-errors'] = result.error_message
                        return ui_commands_list
                
                # Sleep briefly to avoid CPU spinning
                time.sleep(1)

                # Record launch time for normal mode
            if launch_successful:
                launch_time = time.time() - start_time
                result.metrics['launch_time'] = launch_time
                logger.info(f"[{test_dict['name']}] DSRS launch completed in {launch_time:.2f} seconds")
                
            # --- Proceed if Launch Successful (ALL MODES) ---
            if launch_successful:
                logger.info(f"[{test_dict['name']}] DSRS ready - proceeding with scenario execution")
                
                # Skip UI-related setup in CLI mode
                if not cli_mode_enabled:
                    # Give app a moment to fully render its window before recording
                    logger.info(f"[{test_dict['name']}] Waiting 5 seconds for app window to be fully ready...")
                    time.sleep(5)
                else:
                    logger.info(f"[{test_dict['name']}] CLI Mode: Skipping UI setup, proceeding directly to scenario")
                
                # START SCREEN RECORDING AFTER APP IS READY
                ffmpeg_process = None
                screen_recording_requested = "--record-screen" in test_dict['automation_flags_dict'] or "--record-screen" in test_dict['automation_suite_flags_dict']
                
                if screen_recording_requested:
                    if not cli_mode_enabled:
                        logger.info(f"[{test_dict['name']}] App is ready - starting screen recording")
                        try:
                            from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                            ffmpeg_process = PretestAnalysisCallerMethods.windows_ffmpeg_recorder_caller(test_dict)
                            if ffmpeg_process:
                                logger.info(f"[{test_dict['name']}] Screen recording started successfully with PID: {ffmpeg_process.pid}")
                                # Store in varc so it can be accessed later for cleanup
                                varc.ffmpeg_process = ffmpeg_process
                            else:
                                # FAIL THE TEST if recording was requested but failed to start
                                error_msg = "Screen recording FAILED to start when --record-screen flag was specified"
                                logger.error(f"[{test_dict['name']}] {error_msg}")
                                result.status = TestStatus.FAILED
                                result.error_message = error_msg
                                test_dict['verdicts']['process-specific-errors'] = error_msg
                                ui_automation_end_event.set()  # Signal to end
                                return ui_commands_list
                        except Exception as e:
                            # FAIL THE TEST if recording was requested but encountered an exception
                            error_msg = f"Screen recording FAILED with exception when --record-screen flag was specified: {str(e)}"
                            logger.error(f"[{test_dict['name']}] {error_msg}")
                            result.status = TestStatus.FAILED
                            result.error_message = error_msg
                            test_dict['verdicts']['process-specific-errors'] = error_msg
                            ui_automation_end_event.set()  # Signal to end
                            return ui_commands_list
                
                # Thread function for launching scenario (SAME FOR BOTH MODES)
                def scenario_launch():
                    nonlocal output2  # Access the outer variable
                    logger.info(f"[{test_dict['name']}] Launching Scenario...")
                    
                    logger.debug(f"pytest root path: {PYTEST_ROOT_DIR}")
                                    
                    # Print the scenario command for debugging
                    logger.info(f"Running scenario command: {ui_commands_list[0][1]}")
                                    
                    # Prepare env to include per-test log path for pytest
                    try:
                        if test_dict.get('test_logs_path'):
                            env['DMF_TEST_LOGS_PATH'] = test_dict['test_logs_path']
                            env['DMF_TEST_NAME'] = test_dict.get('name', 'unnamed')
                    except Exception:
                        pass

                    output2 = subprocess.Popen(
                        ui_commands_list[0][1], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        cwd=PYTEST_ROOT_DIR,
                        shell=True,
                        env=env
                    )
                    LoggerMethods.dsrs_scenario_verification(
                        test_dict, 
                        DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME, 
                        output2, 
                        DSRS_SCENARIO_TYPE, 
                        ui_automation_start_event, 
                        ui_automation_end_event,
                        timeout=scenario_timeout  # Pass custom timeout
                    )                
                
                # Start the scenario launch thread (SAME FOR BOTH MODES)
                thread2 = threading.Thread(target=scenario_launch)
                thread2.daemon = True
                thread2.start()
                
                # Wait for the scenario thread to complete or end event - Use custom timeout
                scenario_start = time.time()
                
                while thread2.is_alive() and time.time() - scenario_start < scenario_timeout:
                    # Check if end event is set (indicating failure)
                    if ui_automation_end_event.is_set():
                        logger.warning(f"[{test_dict['name']}] End event detected during scenario launch")
                        break
                    time.sleep(1)
                
                # Check if scenario timed out - Use custom timeout
                if thread2.is_alive() and time.time() - scenario_start >= scenario_timeout:
                    logger.error(f"[{test_dict['name']}] Scenario launch timed out after {scenario_timeout}s")
                    ui_automation_end_event.set()  # Signal to end
                    result.status = TestStatus.FAILED
                    result.error_message = f"Scenario launch timed out after {scenario_timeout}s"
                    test_dict['verdicts']['process-specific-errors'] = f"Scenario launch timed out"
                    
                    # Set a timeout for joining the thread
                    thread2.join(timeout=10)
                
                # STOP SCREEN RECORDING AFTER SCENARIO COMPLETION
                if ffmpeg_process:
                    logger.info(f"[{test_dict['name']}] Scenario completed - stopping screen recording")
                    try:
                        from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                        PretestAnalysisCallerMethods.windows_stop_ffmpeg_recording(ffmpeg_process)
                        logger.info(f"[{test_dict['name']}] Screen recording stopped successfully")
                    except Exception as e:
                        logger.error(f"[{test_dict['name']}] Error stopping screen recording: {e}")
                
                # If end event was set, it means there was a failure
                if ui_automation_end_event.is_set():
                    if result.status != TestStatus.FAILED:  # Only set if not already set
                        result.status = TestStatus.FAILED
                        result.error_message = "DSRS scenario verification failed, see logs for details"
                        test_dict['verdicts']['process-specific-errors'] = "DSRS scenario verification failed"
                else:
                    # If no end event and no timeout, scenario completed successfully
                    result.status = TestStatus.COMPLETED
                
        except Exception as e:
            error_msg = f"DSRS failed: {str(e)}"
            logger.error(f"[{test_dict['name']}] {error_msg}")
            
            # STOP SCREEN RECORDING ON EXCEPTION
            if 'ffmpeg_process' in locals() and ffmpeg_process:
                logger.info(f"[{test_dict['name']}] Exception occurred - stopping screen recording")
                try:
                    from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                    PretestAnalysisCallerMethods.windows_stop_ffmpeg_recording(ffmpeg_process)
                    logger.info(f"[{test_dict['name']}] Screen recording stopped due to exception")
                except Exception as recording_error:
                    logger.error(f"[{test_dict['name']}] Error stopping screen recording during exception handling: {recording_error}")
            
            test_dict['verdicts']['process-specific-errors'] = error_msg
            result.error_message = error_msg
            result.status = TestStatus.FAILED
            
            # Ensure end event is set to unblock any processes
            if 'ui_automation_end_event' in locals() and not ui_automation_end_event.is_set():
                ui_automation_end_event.set()
        
        # Calculate total execution time
        end_time = time.time()
        execution_time = end_time - start_time
        result.metrics['total_execution_time'] = execution_time
        
        # Add logs analysis entry
        result.logs_analysis['dsrs_execution'] = {
            'status': result.status.name,
            'execution_time': execution_time,
            'commands': [cmd for sublist in ui_commands_list for cmd in sublist] if ui_commands_list else []
        }
        
        # Increment new_count if we found new items
        if hasattr(result, 'logs_analysis') and 'new_items' in result.logs_analysis:
            result.new_count = len(result.logs_analysis['new_items'])
        
        logger.info(f"[{test_dict['name']}] DSRS runner completed with status: {result.status.name}")
        
        return ui_commands_list

    @staticmethod
    def map2sim_runner(test_dict: dict, result: TestResult):
        """
        This function is used to run MAP2SIM commands
        
        Supports multiple execution modes:
        - Normal Mode: Launches MAP2SIM app and runs scenario
        - Develop Mode: Uses existing MAP2SIM process (via skip_map2sim_process_launch)
        - CLI Mode: Skips app launch entirely and runs scenario directly (via --enable_cli_mode flag)
        
        Args:
            test_dict: Dictionary containing test information
            result: TestResult object to store execution results
            
        Returns:
            ui_commands_list: List of MAP2SIM commands executed
        """
        # Get timeout values (custom or default)
        timeout_values = CommandRunnerMethods._get_timeout_values(test_dict, 'MAP2SIM')
        launch_timeout = timeout_values['launch_timeout']
        scenario_timeout = timeout_values['scenario_timeout']
        varc.sim_terminal_log_path = f"{test_dict['test_logs_path']}/{MAP2SIM_LAUNCH_LOG_FILE_NAME}"
        varc.sim_scenario_log_path = f"{test_dict['test_logs_path']}/{MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME}"

        # Set up environment variables for colored output
        env = os.environ.copy()
        env['FORCE_COLOR'] = '1'
        env['PY_COLORS'] = '1'
        ui_commands_list = None
        
        # Mark as running and store start time
        result.status = TestStatus.RUNNING
        start_time = time.time()
        
        try:
            logger.info(f"[{test_dict['name']}] Starting MAP2SIM runner with timeouts - Launch: {launch_timeout}s, Scenario: {scenario_timeout}s")
            
            ui_automation_start_event = threading.Event()
            ui_automation_end_event = threading.Event()
            ui_automation_timeout_event = threading.Event()
            
            # Generate commands
            ui_commands_list = CommandGeneratorMethods.map2sim_command_generator(test_dict)
            varc.test_command_dict["map2sim_commands_list"] = ui_commands_list
            
            # Store commands in result object
            result.commands_executed.extend([cmd[0] for cmd in ui_commands_list[0]])
            
            logger.info(f"Executing MAP2SIM commands --- {ui_commands_list[0][0]} and {ui_commands_list[0][1]}")
            
            # At the top of the map2sim_runner method:
            output1 = None
            output2 = None
            
            # CHECK FOR CLI MODE OR DEVELOP MODE - SKIP PROCESS LAUNCH
            cli_mode_enabled = CommandRunnerMethods._is_cli_mode_enabled(test_dict)
            develop_mode_enabled = hasattr(varc, 'skip_map2sim_process_launch') and varc.skip_map2sim_process_launch
            
            if cli_mode_enabled:
                logger.info(f"[{test_dict['name']}] CLI Mode: Skipping MAP2SIM app launch, running CLI scenario directly")
                
                # Create CLI mode log
                from generic_utils.cli_mode_handler import CLIModeHandler
                CLIModeHandler.create_cli_test_log(test_dict, varc.sim_terminal_log_path or f"{test_dict['test_logs_path']}/cli_mode.log")
                
                # Set the start event to indicate "launch" is complete
                ui_automation_start_event.set()
                launch_successful = True
                
                # Record minimal launch time since we're skipping
                result.metrics['launch_time'] = 0.0
                
            elif develop_mode_enabled:
                logger.info(f"[{test_dict['name']}] Windows Develop Mode: Skipping MAP2SIM app launch, using existing app process")
                
                # Ensure a launch log exists with a clear develop mode header
                try:
                    if varc.sim_terminal_log_path:
                        with open(varc.sim_terminal_log_path, 'a', encoding='utf-8') as f:
                            f.write(f"=== MAP2SIM DEVELOP MODE: Skipping app launch at {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                except Exception as e:
                    logger.warning(f"Failed to write develop mode header to launch log: {e}")

                # Set the start event to indicate "launch" is complete
                ui_automation_start_event.set()
                launch_successful = True
                
                # Record minimal launch time since we're skipping
                result.metrics['launch_time'] = 0.0
                
            else:
                # NORMAL MODE - FULL LAUNCH FLOW
                logger.info(f"[{test_dict['name']}] Normal Mode: Launching MAP2SIM app")
                
                # Then in the build_launch function:
                def build_launch():
                    nonlocal output1  # Access the outer variable
                    logger.info(f"[{test_dict['name']}] Launching MAP2SIM App")
                    output1 = subprocess.Popen(
                        ui_commands_list[0][0], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        cwd=varc.cwd, 
                        shell=True,
                        bufsize=0,  # Force unbuffered output
                        universal_newlines=True,
                        encoding='utf-8',
                        errors='ignore'  # Text mode improves line handling
                    )
                    LoggerMethods.map2sim_launch_verification(
                        test_dict, 
                        output1, 
                        MAP2SIM_SCENARIO_TYPE, 
                        start_event=ui_automation_start_event,
                        end_event=ui_automation_end_event,
                        timeout_event=ui_automation_timeout_event,
                        timeout=launch_timeout  # Pass custom timeout
                    )
                
                # Start the MAP2SIM launch thread
                thread1 = threading.Thread(target=build_launch)
                thread1.daemon = True
                thread1.start()
                
                # Wait for either start event (success) or end event (failure)
                launch_start = time.time()
                last_status_report = time.time()  # For periodic status updates
                logger.info(f"[{test_dict['name']}] Waiting for MAP2SIM app launch events...")

                # --- Check Status and Perform Fallback Logic ---
                launch_successful = False
                
                # Continuously check events while thread is running
                while thread1.is_alive():
                    current_time = time.time()
                    elapsed = current_time - launch_start
                    
                    # Provide periodic status updates (every 10 seconds)
                    if current_time - last_status_report > 10:
                        logger.info(f"[{test_dict['name']}] Still waiting for MAP2SIM launch - elapsed: {elapsed:.1f}s")
                        logger.info(f"[{test_dict['name']}] Event status - start: {ui_automation_start_event.is_set()}, end: {ui_automation_end_event.is_set()}, timeout: {ui_automation_timeout_event.is_set()}")
                        last_status_report = current_time
                    
                    # Check for success
                    if ui_automation_start_event.is_set():
                        launch_successful = True
                        logger.info(f"[{test_dict['name']}] MAP2SIM launch confirmed via stdout.")
                        break
                    
                    # Check for failure
                    if ui_automation_end_event.is_set():
                        logger.error(f"[{test_dict['name']}] MAP2SIM launch failed (end_event set).")
                        result.error_message = "MAP2SIM launch verification failed"
                        result.status = TestStatus.FAILED
                        test_dict['verdicts']['process-specific-errors'] = result.error_message
                        return ui_commands_list
                    
                    # Check for timeout - if timeout, try fallback
                    if ui_automation_timeout_event.is_set():
                        logger.warning(f"[{test_dict['name']}] Timeout event set, trying fallback check in Kit log.")
                        
                        # Check Kit log as fallback
                        if LogsSaverMethods.check_kit_log_for_app_ready(test_dict, MAP2SIM_LAUNCH_LOG_FILE_NAME, 'MAP2SIM'):
                            launch_successful = True
                            logger.info(f"[{test_dict['name']}] Fallback successful: 'app ready' found in Kit log.")
                            break
                        else:
                            logger.error(f"[{test_dict['name']}] Fallback check failed: 'app ready' not found in Kit log.")
                            result.error_message = "MAP2SIM launch failed: 'app ready' not found in stdout or Kit log"
                            result.status = TestStatus.FAILED
                            test_dict['verdicts']['process-specific-errors'] = result.error_message
                            return ui_commands_list
                    
                    # Handle main timeout (don't rely on timeout_event) - Use custom timeout
                    if elapsed > launch_timeout:
                        logger.warning(f"[{test_dict['name']}] Launch timeout reached ({launch_timeout}s), checking Kit log directly.")
                        
                        # Try fallback check in Kit log
                        if LogsSaverMethods.check_kit_log_for_app_ready(test_dict, MAP2SIM_LAUNCH_LOG_FILE_NAME, 'MAP2SIM'):
                            launch_successful = True
                            logger.info(f"[{test_dict['name']}] Fallback successful: 'app ready' found in Kit log.")
                            break
                        else:
                            logger.error(f"[{test_dict['name']}] Fallback check failed: 'app ready' not found in Kit log.")
                            result.error_message = f"MAP2SIM launch failed: 'app ready' not found within {launch_timeout}s timeout or in Kit log"
                            result.status = TestStatus.FAILED
                            test_dict['verdicts']['process-specific-errors'] = result.error_message
                            return ui_commands_list
                    
                    # Sleep briefly to avoid CPU spinning
                    time.sleep(1)

                # Record launch time for normal mode
                if launch_successful:
                    launch_time = time.time() - start_time
                    result.metrics['launch_time'] = launch_time
                    logger.info(f"[{test_dict['name']}] MAP2SIM launch completed in {launch_time:.2f} seconds")
                    # Adding temp sleep to avoid race condition(current issue is app ready not getting detected in terminal log)
                    # Skip this sleep in CLI mode as there's no app to wait for
                    if not cli_mode_enabled:
                        time.sleep(60)

            # --- Proceed if Launch Successful (ALL MODES) ---
            if launch_successful:
                logger.info(f"[{test_dict['name']}] MAP2SIM ready - proceeding with scenario execution")
                
                # Skip UI-related setup in CLI mode
                if not cli_mode_enabled:
                    # Give app a moment to fully render its window before recording
                    logger.info(f"[{test_dict['name']}] Waiting 5 seconds for app window to be fully ready...")
                    time.sleep(5)
                else:
                    logger.info(f"[{test_dict['name']}] CLI Mode: Skipping UI setup, proceeding directly to scenario")
                
                # START SCREEN RECORDING AFTER APP IS READY (Skip in CLI mode)
                ffmpeg_process = None
                screen_recording_requested = "--record-screen" in test_dict['automation_flags_dict'] or "--record-screen" in test_dict['automation_suite_flags_dict']
                
                if screen_recording_requested:
                    if cli_mode_enabled:
                        logger.warning(f"[{test_dict['name']}] Screen recording requested but CLI mode is enabled - skipping screen recording")
                    else:
                        logger.info(f"[{test_dict['name']}] App is ready - starting screen recording")
                        try:
                            from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                            ffmpeg_process = PretestAnalysisCallerMethods.windows_ffmpeg_recorder_caller(test_dict)
                            if ffmpeg_process:
                                logger.info(f"[{test_dict['name']}] Screen recording started successfully with PID: {ffmpeg_process.pid}")
                                # Store in varc so it can be accessed later for cleanup
                                varc.ffmpeg_process = ffmpeg_process
                            else:
                                # FAIL THE TEST if recording was requested but failed to start
                                error_msg = "Screen recording FAILED to start when --record-screen flag was specified"
                                logger.error(f"[{test_dict['name']}] {error_msg}")
                                result.status = TestStatus.FAILED
                                result.error_message = error_msg
                                test_dict['verdicts']['process-specific-errors'] = error_msg
                                ui_automation_end_event.set()  # Signal to end
                                return ui_commands_list
                        except Exception as e:
                            # FAIL THE TEST if recording was requested but encountered an exception
                            error_msg = f"Screen recording FAILED with exception when --record-screen flag was specified: {str(e)}"
                            logger.error(f"[{test_dict['name']}] {error_msg}")
                            result.status = TestStatus.FAILED
                            result.error_message = error_msg
                            test_dict['verdicts']['process-specific-errors'] = error_msg
                            ui_automation_end_event.set()  # Signal to end
                            return ui_commands_list
                
                # Thread function for launching scenario (DIFFERENT FOR CLI MODE)
                def scenario_launch():
                    nonlocal output2  # Access the outer variable
                    
                    if cli_mode_enabled:
                        logger.info(f"[{test_dict['name']}] Launching MAP2SIM CLI Scenario...")
                        
                        # Generate CLI-specific pytest command
                        from generic_utils.cli_mode_handler import CLIModeHandler
                        cli_pytest_command = CLIModeHandler.generate_cli_pytest_command(test_dict)
                        
                        logger.info(f"Running CLI scenario command: {cli_pytest_command}")
                        
                        # Execute CLI test with enhanced reporting
                        try:
                            test_result, report_file = CLIModeHandler.execute_cli_test_with_reporting(test_dict, cli_pytest_command)
                            
                            # Update result with CLI test results
                            if test_result['verdict'] == 'PASS':
                                result.status = TestStatus.COMPLETED
                                ui_automation_end_event.set()  # Signal successful completion
                            elif test_result['verdict'] == 'FAIL':
                                result.status = TestStatus.FAILED
                                result.error_message = test_result.get('error_output', 'CLI test failed')
                                ui_automation_end_event.set()  # Signal completion (even if failed)
                            
                            # Store CLI-specific data in test_dict for reporting
                            test_dict['cli_test_result'] = test_result
                            test_dict['cli_report_file'] = report_file
                            test_dict['verdicts']['execution-mode'] = 'CLI'
                            test_dict['verdicts']['final-verdict'] = test_result['verdict']
                            
                            logger.info(f"[{test_dict['name']}] CLI Mode: Test execution completed with verdict: {test_result['verdict']}")
                            
                        except Exception as e:
                            error_msg = f"CLI test execution failed: {str(e)}"
                            logger.error(f"[{test_dict['name']}] {error_msg}")
                            result.status = TestStatus.FAILED
                            result.error_message = error_msg
                            test_dict['verdicts']['final-verdict'] = 'FAIL'
                            test_dict['verdicts']['process-specific-errors'] = error_msg
                            ui_automation_end_event.set()  # Signal completion
                    else:
                        logger.info(f"[{test_dict['name']}] Launching MAP2SIM UI Scenario...")
                        
                        logger.debug(f"pytest root path: {PYTEST_ROOT_DIR}")
                                        
                        # Print the scenario command for debugging
                        logger.info(f"Running scenario command: {ui_commands_list[0][1]}")
                                        
                        # Prepare env to include per-test log path for pytest
                        try:
                            if test_dict.get('test_logs_path'):
                                env['DMF_TEST_LOGS_PATH'] = test_dict['test_logs_path']
                                env['DMF_TEST_NAME'] = test_dict.get('name', 'unnamed')
                        except Exception:
                            pass

                        output2 = subprocess.Popen(
                            ui_commands_list[0][1], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT, 
                            cwd=PYTEST_ROOT_DIR,
                            shell=True,
                            env=env
                        )
                        LoggerMethods.map2sim_scenario_verification(
                            test_dict,
                            output2,
                            MAP2SIM_SCENARIO_TYPE, 
                            ui_automation_start_event, 
                            ui_automation_end_event,
                            timeout=scenario_timeout  # Pass custom timeout
                        )                
                
                # Start the scenario launch thread (SAME FOR BOTH MODES)
                thread2 = threading.Thread(target=scenario_launch)
                thread2.daemon = True
                thread2.start()
                
                # Wait for the scenario thread to complete or end event - Use custom timeout
                scenario_start = time.time()
                
                while thread2.is_alive() and time.time() - scenario_start < scenario_timeout:
                    # Check if end event is set (indicating failure)
                    if ui_automation_end_event.is_set():
                        logger.warning(f"[{test_dict['name']}] End event detected during scenario launch")
                        break
                    time.sleep(1)
                
                # Check if scenario timed out - Use custom timeout
                if thread2.is_alive() and time.time() - scenario_start >= scenario_timeout:
                    logger.error(f"[{test_dict['name']}] Scenario launch timed out after {scenario_timeout}s")
                    ui_automation_end_event.set()  # Signal to end
                    result.status = TestStatus.FAILED
                    result.error_message = f"Scenario launch timed out after {scenario_timeout}s"
                    test_dict['verdicts']['process-specific-errors'] = f"Scenario launch timed out"
                    
                    # Set a timeout for joining the thread
                    thread2.join(timeout=10)
                
                # STOP SCREEN RECORDING AFTER SCENARIO COMPLETION
                if ffmpeg_process:
                    logger.info(f"[{test_dict['name']}] Scenario completed - stopping screen recording")
                    try:
                        from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                        PretestAnalysisCallerMethods.windows_stop_ffmpeg_recording(ffmpeg_process)
                        logger.info(f"[{test_dict['name']}] Screen recording stopped successfully")
                    except Exception as e:
                        logger.error(f"[{test_dict['name']}] Error stopping screen recording: {e}")
                
                # If end event was set, it typically indicates a failure in UI mode.
                # In CLI mode, the end event is also used to signal completion, so do not override the CLI result.
                if ui_automation_end_event.is_set():
                    from fwk.shared.variables_util import varc as _varc  # local import to avoid circulars at module load
                    cli_mode_active = getattr(_varc, 'cli_mode_enabled', False)
                    if cli_mode_active:
                        logger.info(f"[{test_dict['name']}] CLI Mode: End event observed - treating as normal completion, not a failure")
                    else:
                        if result.status != TestStatus.FAILED:  # Only set if not already set
                            result.status = TestStatus.FAILED
                            result.error_message = "MAP2SIM scenario verification failed, see logs for details"
                            test_dict['verdicts']['process-specific-errors'] = "MAP2SIM scenario verification failed"
                else:
                    # If no end event and no timeout, scenario completed successfully
                    result.status = TestStatus.COMPLETED

        except Exception as e:
            error_msg = f"MAP2SIM failed: {str(e)}"
            logger.error(f"[{test_dict['name']}] {error_msg}")
            
            # STOP SCREEN RECORDING ON EXCEPTION
            if 'ffmpeg_process' in locals() and ffmpeg_process:
                logger.info(f"[{test_dict['name']}] Exception occurred - stopping screen recording")
                try:
                    from generic_utils.analysis_caller_util import PretestAnalysisCallerMethods
                    PretestAnalysisCallerMethods.windows_stop_ffmpeg_recording(ffmpeg_process)
                    logger.info(f"[{test_dict['name']}] Screen recording stopped due to exception")
                except Exception as recording_error:
                    logger.error(f"[{test_dict['name']}] Error stopping screen recording during exception handling: {recording_error}")
            
            test_dict['verdicts']['process-specific-errors'] = error_msg
            result.error_message = error_msg
            result.status = TestStatus.FAILED
            
            # Ensure end event is set to unblock any processes
            if 'ui_automation_end_event' in locals() and not ui_automation_end_event.is_set():
                ui_automation_end_event.set()
        
        # Calculate total execution time
        end_time = time.time()
        execution_time = end_time - start_time
        result.metrics['total_execution_time'] = execution_time
        
        # Add logs analysis entry (execution metadata)
        result.logs_analysis['map2sim_execution'] = {
            'status': result.status.name,
            'execution_time': execution_time,
            'commands': [cmd for sublist in ui_commands_list for cmd in sublist] if ui_commands_list else []
        }
        
        # Increment new_count if we found new items
        if hasattr(result, 'logs_analysis') and 'new_items' in result.logs_analysis:
            result.new_count = len(result.logs_analysis['new_items'])
        
        logger.info(f"[{test_dict['name']}] MAP2SIM runner completed with status: {result.status.name}")
                
        return ui_commands_list
