'''This module contains methods to analyze logs, capture terminal logs, and save logs'''

# Standard library imports
import shutil
import signal
import subprocess
import threading
import time
from strip_ansi import strip_ansi
import os
import sys
from datetime import datetime
import re
import select
import logging
# Local imports
from fwk.shared.constants import SCENARIO_SUCCESS_MESSAGE_LIST
from fwk.shared.variables_util import varc
from generic_utils.helper_util import HelperMethods
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger(__name__, varc.framework_logs_path)


class ValidateLogsMethod():
    '''This class is used to analyze logs'''
    
    @staticmethod
    def analyze_frame_generation_logs(file_path,test_dict):
        '''This function is used to analyze frame generation logs'''
        
        dict = {'verdict':"",'severity':"",'reason':[]}
            
        with open(file_path, "r") as f:
            for line in f:
                line=line.strip()
                
                if any(string in line for string in varc.p1_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p1'
                    dict['reason'].append(f'P1 issue found here : {line}')
                
                if any(string in line for string in varc.p1_ignore_issue_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p1_ignored_issue'
                    dict['reason'].append(f'P1 ignored issue found here : {line}')
                    break
                
                if any(string in line for string in varc.p0_platform_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p0_platform'
                    dict['reason'].append(f'p0 platform issue found here : {line}')
                    if "--wait-after-platform-crash" in test_dict['automation_suite_flags_dict']:
                        input("Pausing DMF here as you have added --wait-after-platform-crash flag in automation_suite_flags of input TOML, press enter to continue") 
                    break
                
                if any(string in line for string in varc.p0_functional_iter_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p0_functional_iter'
                    dict['reason'].append(f'P0 functional iter issue found here : {line}')
                    break
                
                if any(string in line for string in varc.p0_functional_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p0_functional'
                    dict['reason'].append(f'P0 functional issue found here : {line}')
                    break    
                                
        return dict

    @staticmethod
    def analyze_kit_logs(file_path,test_dict):
        '''This function is used to analyze kit logs'''

        dict = {'verdict':"",'severity':"",'reason':[]}
            
        with open(file_path, "r") as f:
            for line in f:
                line=line.strip()

                if any(string in line for string in varc.p1_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p1'
                    dict['reason'].append(f'P1 issue found here : {line}')

        return dict

    @staticmethod
    def analyze_pytest_logs(file_path,test_dict):
        '''This function is used to analyze pytest logs'''
        
        dict = {'verdict':"",'severity':"",'reason':[]}
        in_summary_section = False
            
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if any(string in line for string in varc.pytest_p1_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p1'
                    dict['reason'].append(f'pytest P1 issue found here : {line}')
                                
                if any(string in line for string in varc.pytest_p0_functional_list):
                    dict['verdict'] = 'fail'
                    dict['severity'] = 'p0_functional'
                    in_summary_section = True
                    dict['reason'].append(f'\npytest P0 functional issue found here:')
                    continue
                    #dict['reason'].append(f'pytest P0 functional issue found here : {line}')
                    #break    
                 
                if in_summary_section:
                    if line.startswith('==='):  # End of summary section
                        dict['reason'].append(f'{line}')
                        dict['reason'].append('\nplease check pytest logs for more details')
                        break
                    if line.strip():  # Only append non-empty lines
                        dict['reason'].append(f'{line}')

        return dict

class LoggerMethods:
    '''This class consist of methods that help capture terminal logs'''
            

    @staticmethod
    def dsrs_launch_verification(test_dict, output, type, start_event=None, end_event=None, timeout_event=None, timeout=150):
        '''This function is used to verify dsrs launch, check freeze issues, capture logs, continue or stop the run'''
        logger.info(f"Starting launch verification process for {varc.sim_terminal_log_path} (Timeout: {timeout}s)")
        varc.skip_remaining_blocks_freeze = False
        line_count = 0
        last_status_report = time.time()
        launch_start_time = time.time()
        app_ready_found = False
        
        # Open log file once and keep it open
        with open(varc.sim_terminal_log_path, "a", encoding='utf-8') as f:
            f.write(f"=== DSRS LAUNCH VERIFICATION (STDOUT Only) STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.flush()
            
            # Set up non-blocking timeout checker in separate thread
            def timeout_checker():
                checker_start = time.time()
                while not app_ready_found:
                    elapsed = time.time() - checker_start
                    if elapsed > timeout:
                        logger.error(f"TIMEOUT EXCEEDED after {elapsed:.1f}s waiting for 'app ready' in stdout.")
                        f.write(f"=== TIMEOUT EXCEEDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                        f.flush()
                        timeout_event.set()
                        logger.info(f"Timeout event has been set due to timeout")
                        return
                    time.sleep(1)
                    
            # Start timeout checker
            timeout_thread = threading.Thread(target=timeout_checker)
            timeout_thread.daemon = True  # This one can be daemon as it's just for timeout
            timeout_thread.start()
            
            # Direct line-by-line processing with explicit readline call
            try:
                for line in iter(output.stdout.readline, ''):  # Use b'' for bytes mode
                    # Process the current line
                    current_time = time.time()
                    elapsed = current_time - launch_start_time
                    
                    # Process the line
                    if not line:  # Skip empty lines
                        continue
                        
                    line_str = line.strip()
                    logger.debug(line_str)
                    
                    # Clean and log the line
                    clean_line = strip_ansi(line_str)
                    f.write(clean_line + "\n")
                    f.flush()  # Ensure immediate write to file
                    line_count += 1
                    
                    # Periodic status reporting
                    if current_time - last_status_report > 10:
                        logger.info(f"Still monitoring stdout... ({elapsed:.1f}s elapsed, {line_count} lines processed)")
                        last_status_report = current_time
                    
                    # Check for app ready message (critical priority)
                    if type == 'DSRS' and 'app ready' in clean_line.lower():
                        app_ready_found = True
                        success_msg = f"APP READY detected in stdout after {elapsed:.1f} seconds!"
                        logger.info(success_msg)
                        f.write(f"=== APP READY DETECTED (STDOUT) AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                        f.flush()
                        
                        # Set event IMMEDIATELY
                        start_event.set()
                        logger.info(f"Start event has been set, continuing to monitor output")
                    
                # If loop exits normally (EOF), log it
                elapsed = time.time() - launch_start_time
                logger.warning(f"Output stream ended after {elapsed:.1f}s without detecting 'app ready' in stdout.")
                f.write(f"=== OUTPUT STREAM ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                f.flush()
                
                # Only set end_event if app_ready wasn't found
                if not app_ready_found:
                    end_event.set()
                    logger.info(f"End event has been set due to output stream ending without 'app ready'")
                
            except Exception as e:
                # Log any errors that occur
                elapsed = time.time() - launch_start_time
                error_msg = f"Error reading output at {elapsed:.1f}s: {str(e)}"
                logger.error(error_msg, exc_info=True)
                f.write(f"=== ERROR READING OUTPUT AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)} ===\n")
                f.flush()
                
                # Only set end_event if app_ready wasn't found
                if not app_ready_found:
                    end_event.set()
                    logger.info(f"End event has been set due to error, but continuing to monitor output")
                
                # Continue monitoring despite errors
                time.sleep(0.5)


    @staticmethod
    def dsrs_scenario_verification(test_dict, output, type, start_event=None, end_event=None, timeout=300):
        '''Verify DSRS scenario using pytest process exit code; capture stdout to logs'''
        logger.info(f"Starting scenario verification process for {varc.sim_terminal_log_path} (Timeout: {timeout}s)")
        varc.skip_remaining_blocks_freeze = False
        line_count = 0
        last_status_report = time.time()
        scenario_start_time = time.time()
        scenario_success_found = False
        
        # List of error patterns to detect (still recorded to file, but not decisive)
        error_patterns = [
            "ERRORS",
            "Traceback (most recent call last)"
        ]
        
        # Open log file once and keep it open
        with open(varc.sim_terminal_log_path, "a", encoding='utf-8') as f:
            f.write(f"=== DSRS SCENARIO VERIFICATION STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.flush()
            
            # Set up non-blocking timeout checker in separate thread
            def timeout_checker():
                checker_start = time.time()
                while not scenario_success_found:
                    elapsed = time.time() - checker_start
                    if elapsed > timeout:
                        logger.error(f"TIMEOUT EXCEEDED after {elapsed:.1f}s waiting for scenario success")
                        f.write(f"=== SCENARIO TIMEOUT EXCEEDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                        f.flush()
                        if end_event:
                            end_event.set()
                        logger.info(f"End event has been set due to scenario timeout")
                        return
                    time.sleep(1)
            # Start timeout checker
            timeout_thread = threading.Thread(target=timeout_checker)
            timeout_thread.daemon = True
            timeout_thread.start()
            
            try:
                for line in iter(output.stdout.readline, b''):
                    current_time = time.time()
                    elapsed = current_time - scenario_start_time
                    if not line:
                        continue
                    line_str = line.decode(errors='ignore').strip()
                    logger.debug(line_str)
                    clean_line = strip_ansi(line_str)
                    f.write(clean_line + "\n")
                    f.flush()
                    line_count += 1
                    if current_time - last_status_report > 10:
                        logger.info(f"Still monitoring scenario output... ({elapsed:.1f}s elapsed, {line_count} lines processed)")
                        last_status_report = current_time
                    # Keep logging errors but do not decide success/failure here
                    for error_pattern in error_patterns:
                        if error_pattern in clean_line:
                            logger.error(f"ERROR DETECTED: '{error_pattern}' after {elapsed:.1f}s")
                            f.write(f"=== ERROR DETECTED: '{error_pattern}' AFTER {elapsed:.1f}s ===\n")
                            f.flush()
                # EOF
                elapsed = time.time() - scenario_start_time
                logger.warning(f"Scenario output stream ended after {elapsed:.1f}s")
                f.write(f"=== SCENARIO OUTPUT STREAM ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                
                # Decide based on pytest exit code
                try:
                    output.wait(timeout=1)
                except Exception:
                    pass
                if hasattr(output, 'returncode') and output.returncode == 0:
                    scenario_success_found = True
                    success_msg = "SCENARIO SUCCESSFUL inferred from pytest return code 0"
                    logger.info(success_msg)
                    f.write(f"=== {success_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                    if start_event:
                        start_event.set()
                else:
                    if end_event:
                        end_event.set()
                    logger.info(f"End event has been set due to non-zero pytest return code")
                f.flush()
            except Exception as e:
                elapsed = time.time() - scenario_start_time
                error_msg = f"Error reading scenario output at {elapsed:.1f}s: {str(e)}"
                logger.error(error_msg, exc_info=True)
                f.write(f"=== ERROR READING SCENARIO OUTPUT AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)} ===\n")
                f.flush()
                if not scenario_success_found and end_event:
                    end_event.set()
                    logger.info(f"End event has been set due to error reading scenario output")
            time.sleep(0.5)

    @staticmethod
    def map2sim_launch_verification(test_dict, output, type, start_event=None, end_event=None, timeout_event=None, timeout=150):
        '''This function is used to verify map2sim launch, check freeze issues, capture logs, continue or stop the run'''
        logger.info(f"Starting launch verification process for {varc.sim_terminal_log_path} (Timeout: {timeout}s)")
        varc.skip_remaining_blocks_freeze = False
        line_count = 0
        last_status_report = time.time()
        launch_start_time = time.time()
        app_ready_found = False
        
        # Open log file once and keep it open
        with open(varc.sim_terminal_log_path, "a", encoding='utf-8') as f:
            f.write(f"=== MAP2SIM LAUNCH VERIFICATION (STDOUT Only) STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.flush()
            
            # Set up non-blocking timeout checker in separate thread
            def timeout_checker():
                checker_start = time.time()
                while not app_ready_found:
                    elapsed = time.time() - checker_start
                    if elapsed > timeout:
                        logger.error(f"TIMEOUT EXCEEDED after {elapsed:.1f}s waiting for 'app ready' or 'map2sim app started' in stdout.")
                        f.write(f"=== TIMEOUT EXCEEDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                        f.flush()
                        timeout_event.set()
                        logger.info(f"Timeout event has been set due to timeout")
                        return
                    time.sleep(1)
                    
            # Start timeout checker
            timeout_thread = threading.Thread(target=timeout_checker)
            timeout_thread.daemon = True  # This one can be daemon as it's just for timeout
            timeout_thread.start()
            
            # Direct line-by-line processing with explicit readline call
            try:
                for line in iter(output.stdout.readline, ''):  # Use b'' for bytes mode
                    # Process the current line
                    current_time = time.time()
                    elapsed = current_time - launch_start_time
                    
                    # Process the line
                    if not line:  # Skip empty lines
                        continue
                        
                    line_str = line.strip()
                    logger.debug(line_str)
                    
                    # Clean and log the line
                    clean_line = strip_ansi(line_str)
                    f.write(clean_line + "\n")
                    f.flush()  # Ensure immediate write to file
                    line_count += 1
                    
                    # Periodic status reporting
                    if current_time - last_status_report > 10:
                        logger.info(f"Still monitoring stdout... ({elapsed:.1f}s elapsed, {line_count} lines processed)")
                        last_status_report = current_time
                    
                    # Check for app ready message (critical priority)
                    if type == 'MAP2SIM' and ('app ready' in clean_line.lower() or 'map2sim app started' in clean_line.lower()):
                        app_ready_found = True
                        if 'app ready' in clean_line.lower():
                            success_msg = f"APP READY detected in stdout after {elapsed:.1f} seconds!"
                            log_msg = f"=== APP READY DETECTED (STDOUT) AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n"
                        else:
                            success_msg = f"MAP2SIM APP STARTED detected in stdout after {elapsed:.1f} seconds!"
                            log_msg = f"=== MAP2SIM APP STARTED DETECTED (STDOUT) AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n"
                        
                        logger.info(success_msg)
                        f.write(log_msg)
                        f.flush()
                        
                        # Set event IMMEDIATELY
                        start_event.set()
                        logger.info(f"Start event has been set, continuing to monitor output")
                    
                # If loop exits normally (EOF), log it
                elapsed = time.time() - launch_start_time
                logger.warning(f"Output stream ended after {elapsed:.1f}s without detecting 'app ready' or 'map2sim app started' in stdout.")
                f.write(f"=== OUTPUT STREAM ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                f.flush()
                
                # Only set end_event if app_ready wasn't found
                if not app_ready_found:
                    end_event.set()
                    logger.info(f"End event has been set due to output stream ending without 'app ready' or 'map2sim app started'")
                
            except Exception as e:
                # Log any errors that occur
                elapsed = time.time() - launch_start_time
                error_msg = f"Error reading output at {elapsed:.1f}s: {str(e)}"
                logger.error(error_msg, exc_info=True)
                f.write(f"=== ERROR READING OUTPUT AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)} ===\n")
                f.flush()
                
                # Only set end_event if app_ready wasn't found
                if not app_ready_found:
                    end_event.set()
                    logger.info(f"End event has been set due to error, but continuing to monitor output")
                
                # Continue monitoring despite errors
                time.sleep(0.5)

    @staticmethod
    def map2sim_scenario_verification(test_dict, output, type, start_event=None, end_event=None, timeout=300):
        '''Verify MAP2SIM scenario using pytest process exit code; capture stdout to logs'''
        logger.info(f"Starting scenario verification process for {varc.sim_scenario_log_path} (Timeout: {timeout}s)")
        varc.skip_remaining_blocks_freeze = False
        line_count = 0
        last_status_report = time.time()
        scenario_start_time = time.time()
        scenario_success_found = False
        
        # List of error patterns to detect (still recorded to file, but not decisive)
        error_patterns = [
            "ERRORS",
            "Traceback (most recent call last)"
        ]
        
        # Open log file once and keep it open
        with open(varc.sim_scenario_log_path, "a", encoding='utf-8') as f:
            f.write(f"=== MAP2SIM SCENARIO VERIFICATION STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.flush()
            
            # Set up non-blocking timeout checker in separate thread
            def timeout_checker():
                checker_start = time.time()
                while not scenario_success_found:
                    elapsed = time.time() - checker_start
                    if elapsed > timeout:
                        logger.error(f"TIMEOUT EXCEEDED after {elapsed:.1f}s waiting for scenario success")
                        f.write(f"=== SCENARIO TIMEOUT EXCEEDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                        f.flush()
                        if end_event:
                            end_event.set()
                        logger.info(f"End event has been set due to scenario timeout")
                        return
                    time.sleep(1)
            # Start timeout checker
            timeout_thread = threading.Thread(target=timeout_checker)
            timeout_thread.daemon = True
            timeout_thread.start()
            
            try:
                for line in iter(output.stdout.readline, b''):
                    current_time = time.time()
                    elapsed = current_time - scenario_start_time
                    if not line:
                        continue
                    line_str = line.decode(errors='ignore').strip()
                    logger.debug(line_str)
                    clean_line = strip_ansi(line_str)
                    f.write(clean_line + "\n")
                    f.flush()
                    line_count += 1
                    if current_time - last_status_report > 10:
                        logger.info(f"Still monitoring scenario output... ({elapsed:.1f}s elapsed, {line_count} lines processed)")
                        last_status_report = current_time
                    # Keep logging errors but do not decide success/failure here
                    for error_pattern in error_patterns:
                        if error_pattern in clean_line:
                            logger.error(f"ERROR DETECTED: '{error_pattern}' after {elapsed:.1f}s")
                            f.write(f"=== ERROR DETECTED: '{error_pattern}' AFTER {elapsed:.1f}s ===\n")
                            f.flush()
                # EOF
                elapsed = time.time() - scenario_start_time
                logger.warning(f"Scenario output stream ended after {elapsed:.1f}s")
                f.write(f"=== SCENARIO OUTPUT STREAM ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (after {elapsed:.1f}s) ===\n")
                
                # Decide based on pytest exit code
                try:
                    output.wait(timeout=1)
                except Exception:
                    pass
                if hasattr(output, 'returncode') and output.returncode == 0:
                    scenario_success_found = True
                    success_msg = "SCENARIO SUCCESSFUL inferred from pytest return code 0"
                    logger.info(success_msg)
                    f.write(f"=== {success_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                    if start_event:
                        start_event.set()
                else:
                    if end_event:
                        end_event.set()
                    logger.info(f"End event has been set due to non-zero pytest return code")
                f.flush()
            except Exception as e:
                elapsed = time.time() - scenario_start_time
                error_msg = f"Error reading scenario output at {elapsed:.1f}s: {str(e)}"
                logger.error(error_msg, exc_info=True)
                f.write(f"=== ERROR READING SCENARIO OUTPUT AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)} ===\n")
                f.flush()
                if not scenario_success_found and end_event:
                    end_event.set()
                    logger.info(f"End event has been set due to error reading scenario output")
            time.sleep(0.5)

    @staticmethod
    def map2sim_cli_scenario_verification(test_dict, output, type, start_event=None, end_event=None, timeout=300):
        '''Verify MAP2SIM CLI scenario using pytest process exit code; capture stdout to logs'''
        logger.info(f"Starting CLI scenario verification process for {varc.sim_scenario_log_path} (Timeout: {timeout}s)")
        varc.skip_remaining_blocks_freeze = False
        line_count = 0
        last_status_report = time.time()
        scenario_start_time = time.time()
        scenario_success_found = False
        
        # CLI-specific success patterns
        cli_success_patterns = [
            "CLI Mode: Test setup completed",
            "CLI Mode: Test completed successfully",
            "PASSED",
            "test passed"
        ]
        
        # CLI-specific error patterns
        cli_error_patterns = [
            "CLI Mode: Test failed",
            "FAILED",
            "test failed",
            "ERROR",
            "Traceback (most recent call last)"
        ]
        
        # Open log file once and keep it open
        with open(varc.sim_scenario_log_path, "a", encoding='utf-8') as f:
            f.write(f"=== MAP2SIM CLI SCENARIO VERIFICATION STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"CLI Mode: No UI automator required\n")
            f.write(f"Timeout: {timeout} seconds\n")
            f.write("=" * 80 + "\n")
            
            while time.time() - scenario_start_time < timeout:
                try:
                    # Read output line by line
                    line = output.stdout.readline()
                    if line:
                        line = line.decode('utf-8', errors='ignore').strip()
                        line_count += 1
                        
                        # Write to log file
                        f.write(f"[{line_count:04d}] {line}\n")
                        
                        # Check for CLI success patterns
                        for pattern in cli_success_patterns:
                            if pattern.lower() in line.lower():
                                scenario_success_found = True
                                success_msg = f"CLI SCENARIO SUCCESSFUL: Found pattern '{pattern}'"
                                logger.info(success_msg)
                                f.write(f"=== {success_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                                if start_event:
                                    start_event.set()
                                break
                        
                        # Check for CLI error patterns
                        for pattern in cli_error_patterns:
                            if pattern.lower() in line.lower():
                                error_msg = f"CLI SCENARIO ERROR: Found pattern '{pattern}'"
                                logger.warning(error_msg)
                                f.write(f"=== {error_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                                if end_event:
                                    end_event.set()
                                break
                        
                        # Status report every 30 seconds
                        if time.time() - last_status_report > 30:
                            elapsed = time.time() - scenario_start_time
                            logger.info(f"CLI scenario still running... {elapsed:.1f}s elapsed, {line_count} lines processed")
                            last_status_report = time.time()
                    
                    # Check if process has finished
                    if output.poll() is not None:
                        elapsed = time.time() - scenario_start_time
                        logger.info(f"CLI scenario process finished after {elapsed:.1f}s")
                        
                        # Check return code
                        try:
                            return_code = output.returncode
                            logger.info(f"CLI scenario return code: {return_code}")
                        except Exception:
                            return_code = -1
                        
                        if return_code == 0:
                            scenario_success_found = True
                            success_msg = "CLI SCENARIO SUCCESSFUL: pytest return code 0"
                            logger.info(success_msg)
                            f.write(f"=== {success_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                            if start_event:
                                start_event.set()
                        else:
                            error_msg = f"CLI SCENARIO FAILED: pytest return code {return_code}"
                            logger.error(error_msg)
                            f.write(f"=== {error_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                            if end_event:
                                end_event.set()
                        break
                    
                    f.flush()
                    
                except Exception as e:
                    elapsed = time.time() - scenario_start_time
                    error_msg = f"Error reading CLI scenario output at {elapsed:.1f}s: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    f.write(f"=== ERROR READING CLI SCENARIO OUTPUT AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)} ===\n")
                    f.flush()
                    if not scenario_success_found and end_event:
                        end_event.set()
                        logger.info(f"End event has been set due to error reading CLI scenario output")
                time.sleep(0.5)
            
            # Final timeout check
            if not scenario_success_found and time.time() - scenario_start_time >= timeout:
                timeout_msg = f"CLI SCENARIO TIMEOUT: {timeout}s elapsed without success"
                logger.error(timeout_msg)
                f.write(f"=== {timeout_msg} AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                if end_event:
                    end_event.set()
            
            f.write(f"=== MAP2SIM CLI SCENARIO VERIFICATION ENDED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"Total lines processed: {line_count}\n")
            f.write(f"Success found: {scenario_success_found}\n")
            f.write("=" * 80 + "\n")


class LogsSaverMethods:
    '''This class consist of methods that isolate  different type of test data in automation output directory'''
    
    @staticmethod
    def logs_saver(test_dict):
        '''
        This function is used to save different type of logs like kit,nv-gpu dump etc for each test.

        Args:
            test_dict: Dictionary containing test information
        '''
        
        def extract_logs_file_names(file_path):
            file_names = {'kit_log_file':'','gpu_dump_file':'','nvdbg_file':'','version_number':'','log_path':'','nvgpu_dump_path':'','nvdbg_path':''}
            with open(file_path, 'r') as f:
                contents = f.read()
                
                version_match = re.search(r'\/omni\.drivesim\.e2e(\.\w+)?\/(\d+\.\d+)\/', contents)
                #Extract the path (e.g., /localhome/local-mohaali/kit/kit/_build/linux-x86_64/release)
                log_path_match = re.search(r'Logging to file: (.+?)(/logs/Kit/omni\.drivesim\.e2e/\d+\.\d+/\S+\.log)', contents)
                nvgpu_dump_path_match = re.search(r'Crash dump is written into: (.+?)(/logs/Kit/omni\.drivesim\.e2e/\d+\.\d+/\S+\.nv-gpudmp)', contents)
                nvdbg_path_match = re.search(r'Shader debug is written into: (.+?)(/logs/Kit/omni\.drivesim\.e2e/\d+\.\d+/\S+\.nvdbg)', contents)
                    
                if version_match:
                    file_names['version_number'] = version_match.group(2)
                    
                kit_log_match = re.search(r'[\w-]+\.log', contents)
                if kit_log_match:
                    file_names['kit_log_file']=kit_log_match.group()
                
                nvgpu_dump_match = re.search(r'[\w-]+\.nv-gpudmp', contents)
                if nvgpu_dump_match:
                    file_names['gpu_dump_file']=nvgpu_dump_match.group()
                
                nvdbg_match = re.search(r'[\w-]+\.nvdbg', contents)
                if nvdbg_match:
                    file_names['nvdbg_file']=nvdbg_match.group()
                    
                if log_path_match:
                    file_names['log_path']=log_path_match.group(1)

                if nvgpu_dump_path_match:
                    file_names['nvgpu_dump_path']=nvgpu_dump_path_match.group(1)
                            
                if nvdbg_path_match:
                    file_names['nvdbg_path']=nvdbg_path_match.group(1)
            
            return file_names
        
        try:
            # dump and kit logs transfer logic
            returned_dict = extract_logs_file_names(f"{test_dict['test_logs_path']}/sim_terminal_logs.txt")
            version_number=returned_dict['version_number']
            home=os.path.expanduser("~")
            if "--dsse" in test_dict['automation_flags_dict'] or "--dsse" in test_dict['automation_suite_flags_dict']:
                app = 'dsse'
            else:
                app='e2e'
              
            if returned_dict['kit_log_file']:
                
                varc.kit_file_name=returned_dict['kit_log_file'] #will be used later for analysis
                kit_log_file_core_name=returned_dict['kit_log_file'][:-4]
                to_path=f"{test_dict['test_logs_path']}/{kit_log_file_core_name}.log"
                                
                if "--docker-run" in test_dict['automation_suite_flags_dict']:
                    kit_logs_transfer_command = f"docker cp ds2:/drivesim-ov/.nvidia-omniverse/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['kit_log_file']} {to_path}"
                    varc.test_command_dict[f"kit_logs_transfer_command"] = kit_logs_transfer_command
                    subprocess.run(kit_logs_transfer_command,check=True,shell=True)        
                else:
                    kit_logs_transfer_command = f"cp {returned_dict['log_path']}/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['kit_log_file']} {to_path}"
                    varc.test_command_dict[f"kit_logs_transfer_command"] = kit_logs_transfer_command
                    subprocess.run(kit_logs_transfer_command,check=True,shell=True)
            
            if returned_dict['gpu_dump_file']:
                
                gpu_dump_file_core_name=returned_dict['gpu_dump_file'][:-10]
                to_path=f"{test_dict['test_logs_path']}/{gpu_dump_file_core_name}.nv-gpudmp"
                
                if "--docker-run" in test_dict['automation_suite_flags_dict']:
                    gpu_crash_dump_logs_transfer_command = f"docker cp ds2:/drivesim-ov/.nvidia-omniverse/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['gpu_dump_file']} {to_path}"
                    varc.test_command_dict["gpu_crash_dump_logs_transfer_command"] = gpu_crash_dump_logs_transfer_command
                    subprocess.run(gpu_crash_dump_logs_transfer_command,check=True,shell=True)
                else:
                    gpu_crash_dump_logs_transfer_command = f"cp {returned_dict['nvgpu_dump_path']}/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['gpu_dump_file']} {to_path}"     
                    varc.test_command_dict["gpu_crash_dump_logs_transfer_command"] = gpu_crash_dump_logs_transfer_command
                    subprocess.run(gpu_crash_dump_logs_transfer_command,check=True,shell=True)
            
            if returned_dict['nvdbg_file']:
                
                nvdbg_file_core_name=returned_dict['nvdbg_file'][:-6]
                to_path=f"{test_dict['test_logs_path']}/{nvdbg_file_core_name}.nvdbg"
                
                if "--docker-run" in test_dict['automation_suite_flags_dict']:
                    nvdbg_file_transfer_command = f"docker cp ds2:/drivesim-ov/.nvidia-omniverse/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['nvdbg_file']} {to_path}"
                    varc.test_command_dict["nvdbg_file_transfer_command"] = nvdbg_file_transfer_command
                    subprocess.run(nvdbg_file_transfer_command,check=True,shell=True)
                else:
                    nvdbg_file_transfer_command = f"cp {returned_dict['nvdbg_path']}/logs/Kit/omni.drivesim.{app}/{version_number}/{returned_dict['nvdbg_file']} {to_path}"
                    varc.test_command_dict["nvdbg_file_transfer_command"] = nvdbg_file_transfer_command
                    subprocess.run(nvdbg_file_transfer_command,check=True,shell=True)
                
            if "--debug" in test_dict['automation_suite_flags_dict']:
                to_path=f"{test_dict['test_logs_path']}/gdb_logs.txt"
                    
                if "--docker-run" in test_dict['automation_suite_flags_dict']:
                    gpu_crash_dump_logs_transfer_command = f"docker cp ds2:/drivesim-ov/gdb_logs.txt {to_path}"
                    varc.test_command_dict["gpu_crash_dump_logs_transfer_command"] = gpu_crash_dump_logs_transfer_command
                    subprocess.run(gpu_crash_dump_logs_transfer_command, check=True,shell=True)      
                else:
                    gpu_crash_dump_logs_transfer_command = f"cp {varc.drivesimov_path}/gdb_logs.txt {to_path}"
                    varc.test_command_dict["gpu_crash_dump_logs_transfer_command"] = gpu_crash_dump_logs_transfer_command
                    subprocess.run(gpu_crash_dump_logs_transfer_command, check=True,shell=True)

                if varc.dump_directory:
                    path = test_dict['test_path']
                    if "--docker-run" in test_dict['automation_suite_flags_dict']:
                        driver_dump_transfer_command = f"docker cp ds2:{varc.dump_directory} {path}"
                        varc.test_command_dict["driver_dump_transfer_command"] = driver_dump_transfer_command
                        subprocess.run(driver_dump_transfer_command, check=True,shell=True)
                    else:
                        driver_dump_transfer_command = f"cp -r {varc.dump_directory} {path}"
                        varc.test_command_dict["driver_dump_transfer_command"] = driver_dump_transfer_command
                        subprocess.run(driver_dump_transfer_command, check=True,shell=True)
                    
        except Exception as e:
            logger.info(f"[{test_dict['name']}] : Something broke while copying test files. Exception I captured is {e}")
            test_dict['verdicts']["process_specific_errors"] = f"Something broke while copying test files. Exception I captured is {e}"


    @staticmethod
    def check_kit_log_for_app_ready(test_dict, launch_log_filename, component='DSRS'):
        """
        Searches the actual Kit log file for the 'app ready' message.
        It first finds the Kit log path from the launch logs.
        Returns True if 'app ready' is found, False otherwise.
        """
        logger.info("Fallback: Checking Kit log file for 'app ready' message.")

        kit_log_path = None
        try:
            # --- Step 1: Find the Kit Log Path from Launch Logs ---
            launch_logs_path = os.path.join(test_dict['test_logs_path'], launch_log_filename)

            if not os.path.exists(launch_logs_path):
                logger.warning(f"{component} launch log file '{launch_logs_path}' not found. Cannot extract Kit log path.")
                return False # Cannot perform check without launch logs

            # Regex to find the specific log line and capture the path
            log_pattern = re.compile(r"\[(?:Info|info)\]\s+\[carb\]\s+Logging to file:\s*([^\s]+(?:kit.*?\.log))", re.IGNORECASE)

            logger.info(f"Searching for Kit log path within: {launch_logs_path}")
            with open(launch_logs_path, 'r', encoding='utf-8', errors='ignore') as f_launch:
                for line in f_launch:
                    match = log_pattern.search(line)
                    if match:
                        kit_log_path = match.group(1).strip()
                        kit_log_path = os.path.normpath(kit_log_path) # Normalize path
                        logger.info(f"Found potential Kit log path via launch logs: {kit_log_path}")
                        break # Stop after finding the first match

            if not kit_log_path:
                logger.warning(f"Could not find Kit log path line (e.g., '[Info] [carb] Logging to file:') in {launch_logs_path}.")
                # Optionally add searches in default locations here if needed as a further fallback
                return False

            if not os.path.exists(kit_log_path):
                logger.warning(f"Extracted Kit log file path does not exist: {kit_log_path}")
                return False
            # --- Kit Log Path Found ---

            # --- Step 2: Search the actual Kit Log File ---
            logger.info(f"Reading Kit log file: {kit_log_path}")
            # Use a buffer to avoid reading huge files entirely into memory if possible
            buffer_size = 8192 # Increased buffer size
            found_app_ready = False
            found_message_type = ""
            with open(kit_log_path, 'r', encoding='utf-8', errors='ignore') as kit_log_file:
                while True:
                    chunk = kit_log_file.read(buffer_size)
                    if not chunk:
                        break # End of file
                    
                    chunk_lower = chunk.lower()
                    if 'app ready' in chunk_lower:
                        found_app_ready = True
                        found_message_type = "app ready"
                        break # Found it, no need to read further
                    elif component == 'MAP2SIM' and 'map2sim app started' in chunk_lower:
                        found_app_ready = True
                        found_message_type = "map2sim app started"
                        break # Found it, no need to read further

            if found_app_ready:
                 logger.info(f"Found '{found_message_type}' message in Kit log file during fallback check.")
                 return True
            else:
                 if component == 'MAP2SIM':
                     logger.info("Did not find 'app ready' or 'map2sim app started' message in Kit log file during fallback check.")
                 else:
                     logger.info("Did not find 'app ready' message in Kit log file during fallback check.")
                 return False
            # --- End Search ---

        except Exception as e:
            logger.error(f"Error during fallback check in Kit log (Path: {kit_log_path if kit_log_path else 'Not Found'}): {e}")
            return False

    @staticmethod
    def copy_kit_logs(test_dict, component='DSRS'):
        """Find and copy kit log files to the test logs directory (supports DSRS and MAP2SIM)"""
        logger.info(f"Searching for Kit log path in: {test_dict['test_logs_path']} (component={component})")
        
        try:
            # Path to the launch logs file which should contain the kit log path
            launch_file = "dsrs_sim_launch_logs.txt" if component != 'MAP2SIM' else "map2sim_launch_logs.txt"
            launch_logs_path = os.path.join(test_dict['test_logs_path'], launch_file)
            
            kit_log_path = None
            
            if os.path.exists(launch_logs_path):
                # Regex to find the specific log line and capture the path
                log_pattern = re.compile(r"\[(?:Info|info)\]\s+\[carb\]\s+Logging to file:\s*([^\s]+(?:kit.*?\.log))", re.IGNORECASE)

                with open(launch_logs_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        match = log_pattern.search(line)
                        if match:
                            kit_log_path = match.group(1).strip()
                            # Normalize path separators just in case
                            kit_log_path = os.path.normpath(kit_log_path)
                            logger.info(f"Found potential Kit log path: {kit_log_path}")
                            break # Stop after finding the first match
            else:
                logger.warning(f"Launch log file not found at {launch_logs_path}, attempting fallback discovery")
            
            # Fallback discovery for develop mode or missing 'Logging to file' line
            if not kit_log_path or not os.path.exists(kit_log_path):
                try:
                    base_local = os.path.join(os.path.expanduser("~"), "AppData", "Local")
                    candidate_roots = [
                        os.path.join(base_local, "ov", "Kit", "logs", "Kit"),
                        os.path.join(base_local, "ov", "logs", "Kit"),
                    ]
                    newest_file = None
                    newest_mtime = -1
                    for root in candidate_roots:
                        if not os.path.isdir(root):
                            continue
                        for dirpath, _, filenames in os.walk(root):
                            for name in filenames:
                                if name.lower().endswith('.log') and ('omni' in name.lower() or 'kit' in name.lower()):
                                    full = os.path.join(dirpath, name)
                                    try:
                                        mtime = os.path.getmtime(full)
                                        if mtime > newest_mtime:
                                            newest_mtime = mtime
                                            newest_file = full
                                    except Exception:
                                        continue
                    if newest_file and os.path.exists(newest_file):
                        kit_log_path = newest_file
                        logger.info(f"Fallback selected Kit log: {kit_log_path}")
                except Exception as disc_err:
                    logger.warning(f"Fallback discovery of Kit log failed: {disc_err}")
            
            if not kit_log_path or not os.path.exists(kit_log_path):
                logger.warning("Could not find a Kit log to copy.")
                return
            
            # Copy to the test logs directory
            destination = os.path.join(test_dict['test_logs_path'], "kit_application.log")
            try:
                shutil.copy2(kit_log_path, destination)
                # Store file name for later analysis
                try:
                    from fwk.shared.variables_util import varc
                    varc.kit_file_name = os.path.basename(kit_log_path)
                except Exception:
                    pass
                logger.info(f"Successfully copied Kit log from {kit_log_path} to {destination}")
            except Exception as copy_err:
                logger.error(f"Failed to copy Kit log file {kit_log_path} to {destination}: {copy_err}")

        except Exception as e:
            logger.error(f"Error occurred while trying to copy kit logs: {str(e)}")
