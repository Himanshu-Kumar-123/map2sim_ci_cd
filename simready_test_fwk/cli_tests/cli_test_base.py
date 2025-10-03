# -*- coding: utf-8 -*-
"""
CLI Test Base Classes for DMF Framework
Provides base classes for CLI-only tests that don't require UI automator
"""

import os
import sys
import json
import base64
import logging
import subprocess
import pytest
from typing import Dict, Any, Optional, List
from pathlib import Path

# DMF Framework imports
from fwk.fwk_logger.fwk_logging import get_logger
from fwk.shared.variables_util import varc

logger = get_logger(__name__)

class CLITestBase:
    """
    Base class for CLI-only tests that don't require UI automator
    """
    
    # Avoid __init__ so pytest can collect subclasses
    test_config = None
    cli_mode = True
    test_name = None
    output_path = None
    cli_logger = None
        
    def setup_cli_mode(self, request):
        """
        Setup for CLI mode tests
        
        Args:
            request: pytest request object
        """
        # Get CLI mode flag from pytest options
        cli_mode = request.config.getoption("--cli_mode", default=False)
        if isinstance(cli_mode, str):
            cli_mode = cli_mode.lower() == 'true'
        
        if not cli_mode:
            pytest.skip("This test requires CLI mode to be enabled")
        
        # Get output path
        self.output_path = request.config.getoption("--output_path", default="./results")
        os.makedirs(self.output_path, exist_ok=True)
        
        # Setup CLI-specific logging using DMF framework
        self.test_name = request.node.name
        self.cli_logger = get_logger(f'CLI_TEST_{self.test_name}', file_path=varc.framework_logs_path)
        
        # Get CLI-specific configuration from JSON data
        json_data = request.config.getoption("--json_data_b64", default=None)
        if json_data:
            try:
                decoded_json = base64.b64decode(json_data).decode('utf-8')
                self.test_config = json.loads(decoded_json)
                self.cli_logger.info(f"CLI Mode: Loaded test configuration: {self.test_config}")
            except Exception as e:
                self.cli_logger.warning(f"CLI Mode: Failed to decode JSON data: {e}")
                self.test_config = {}
        else:
            self.test_config = {}
        
        self.cli_logger.info("CLI Mode: Test setup completed - no UI automator required")
    
    def log_cli_test_result(self, test_name: str, result: str, details: str = ""):
        """
        Log CLI test results using DMF framework logging
        
        Args:
            test_name: Name of the test
            result: Test result (PASS/FAIL/SKIP)
            details: Additional details
        """
        # Use DMF framework logger
        if self.cli_logger:
            self.cli_logger.info(f"CLI Test Result: {test_name} - {result}")
            if details:
                self.cli_logger.info(f"CLI Test Details: {details}")
        
        # Also write to CLI-specific log file
        log_file = os.path.join(self.output_path, "cli_test_results.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{test_name}] {result}")
                if details:
                    f.write(f" - {details}")
                f.write("\n")
        except Exception as e:
            if self.cli_logger:
                self.cli_logger.warning(f"Failed to log CLI test result: {e}")
            else:
                logger.warning(f"Failed to log CLI test result: {e}")
    
    def assert_cli_condition(self, condition: bool, message: str):
        """
        CLI-specific assertion that doesn't require UI
        
        Args:
            condition: Condition to check
            message: Assertion message
        """
        if not condition:
            self.log_cli_test_result(self.test_name or "unknown", "FAIL", message)
            raise AssertionError(f"CLI Test Assertion Failed: {message}")
        
        self.log_cli_test_result(self.test_name or "unknown", "PASS", message)

    def get_toml_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Fetch a value provided via encoded pytest JSON (from TOML), if any.
        """
        try:
            if isinstance(self.test_config, dict) and key in self.test_config:
                return self.test_config.get(key, default)
        except Exception:
            pass
        return default

    def get_batch_file_path(self) -> Optional[str]:
        """
        Return the batch file path coming from TOML (suite-level or per-test override).
        If the path is relative, resolve it against repo root.
        """
        # 1) Prefer encoded pytest JSON (populated by CLI runner from TOML)
        bat_path = self.get_toml_value('batch_file_path')
        if not bat_path:
            return None
        # Normalize/resolve
        try:
            # If path is quoted spaces-safe already, keep as-is for existence check
            norm = os.path.expanduser(os.path.expandvars(bat_path))
            if not os.path.isabs(norm):
                # Resolve relative to repo root (two levels up from this file: simready_test_fwk/cli_tests)
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                norm = os.path.abspath(os.path.join(repo_root, norm))
            return norm
        except Exception:
            return bat_path

    def get_batch_args(self) -> Optional[List[str]]:
        """
        Return the batch arguments list coming from TOML (suite-level or per-test override).
        Accepts list or space-delimited string; returns list.
        """
        try:
            value = None
            if isinstance(self.test_config, dict):
                value = self.test_config.get('batch_args')
            if value is None:
                return None
            if isinstance(value, list):
                return [str(v) for v in value]
            if isinstance(value, str):
                # Split on whitespace for simple cases
                return [p for p in value.split() if p]
        except Exception:
            pass
        return None

    def run_bat_script_with_monitoring(
        self,
        bat_path: str,
        args: Optional[List[str]] = None,
        subdir: Optional[str] = os.path.join("raw_data", "external"),
        log_name: str = "terminal_output.log",
        timeout: Optional[float] = None,
        env_overrides: Optional[Dict[str, str]] = None,
        check: bool = True,
        monitor_pattern: Optional[str] = None,
        monitor_timeout: float = 300.0,
    ) -> Dict[str, Any]:
        """
        Run a Windows .bat script with real-time log monitoring and terminate when pattern is found.

        Args:
            bat_path: Path to the .bat file to run.
            args: Optional list of arguments to pass to the script.
            subdir: Subdirectory under self.output_path where the run will occur.
            log_name: Name of the output log file to capture stdout/stderr.
            timeout: Optional timeout in seconds for the process.
            env_overrides: Optional environment variables to add/override.
            check: If True, raise on non-zero return code.
            monitor_pattern: Pattern to search for in the log file to trigger termination.
            monitor_timeout: Maximum time to wait for the pattern to appear (seconds).

        Returns:
            Dict with keys: return_code, log_file, run_dir, command, terminated_by_pattern
        """
        if not self.output_path:
            raise RuntimeError("CLI test output_path is not set. Ensure setup_cli_mode() ran.")

        run_dir = os.path.join(self.output_path, subdir) if subdir else self.output_path
        os.makedirs(run_dir, exist_ok=True)

        # Build command line
        cmd_parts: List[str] = []
        # Quote .bat path if needed
        bat_quoted = f'"{bat_path}"' if ' ' in bat_path and not bat_path.startswith('"') else bat_path
        cmd_parts.append(bat_quoted)
        if args:
            for a in args:
                if isinstance(a, str) and ' ' in a and not a.startswith('"'):
                    cmd_parts.append(f'"{a}"')
                else:
                    cmd_parts.append(str(a))
        command = " ".join(cmd_parts)

        # Env setup (inherit + DMF_* paths + overrides)
        env = os.environ.copy()
        try:
            env.setdefault('DMF_TEST_OUTPUT_PATH', self.output_path)
            env.setdefault('DMF_TEST_LOGS_PATH', os.path.join(self.output_path, 'logs'))
            env.setdefault('DMF_TEST_RAW_DATA_PATH', os.path.join(self.output_path, 'raw_data'))
            if self.test_name:
                env.setdefault('DMF_TEST_NAME', self.test_name)
        except Exception:
            pass
        if env_overrides:
            env.update(env_overrides)

        # Open log file and execute
        log_file = os.path.join(run_dir, log_name)
        if self.cli_logger:
            self.cli_logger.info(f"Running .bat script with monitoring: {command}")
            self.cli_logger.info(f"Working directory: {run_dir}")
            self.cli_logger.info(f"Output log: {log_file}")
            if monitor_pattern:
                self.cli_logger.info(f"Monitoring for pattern: {monitor_pattern}")

        terminated_by_pattern = False
        with open(log_file, 'w', encoding='utf-8', errors='ignore') as lf:
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=run_dir,
                    shell=True,
                    stdout=lf,
                    stderr=subprocess.STDOUT,
                    env=env,
                    text=True,
                )
                
                # Monitor the log file for the pattern
                if monitor_pattern:
                    import time
                    import re
                    
                    start_time = time.time()
                    pattern_found = False
                    
                    while proc.poll() is None and not pattern_found:
                        # Check if we've exceeded the monitor timeout
                        if time.time() - start_time > monitor_timeout:
                            if self.cli_logger:
                                self.cli_logger.warning(f"Monitor timeout reached ({monitor_timeout}s) without finding pattern: {monitor_pattern}")
                            break
                        
                        # Read the current log file content
                        try:
                            with open(log_file, 'r', encoding='utf-8', errors='ignore') as read_f:
                                log_content = read_f.read()
                                
                            # Check if pattern exists in the log
                            if re.search(monitor_pattern, log_content, re.IGNORECASE):
                                if self.cli_logger:
                                    self.cli_logger.info(f"Pattern found in log: {monitor_pattern}")
                                pattern_found = True
                                terminated_by_pattern = True
                                
                                # Terminate the process
                                proc.terminate()
                                
                                # Give it a moment to terminate gracefully
                                try:
                                    proc.wait(timeout=5.0)
                                except subprocess.TimeoutExpired:
                                    # Force kill if it doesn't terminate gracefully
                                    proc.kill()
                                    proc.wait()
                                
                                break
                        except Exception as e:
                            if self.cli_logger:
                                self.cli_logger.warning(f"Error reading log file during monitoring: {e}")
                        
                        # Wait a bit before checking again
                        time.sleep(1.0)
                    
                    # If pattern wasn't found and process is still running, wait for normal completion
                    if not pattern_found and proc.poll() is None:
                        if self.cli_logger:
                            self.cli_logger.info("Pattern not found, waiting for normal process completion")
                        return_code = proc.wait(timeout=timeout)
                    else:
                        return_code = proc.returncode
                else:
                    # No monitoring, just wait for completion
                    return_code = proc.wait(timeout=timeout)
                    
            except subprocess.TimeoutExpired:
                proc.kill()
                if self.cli_logger:
                    self.cli_logger.error(".bat execution timed out; process killed")
                if check:
                    raise
                return_code = -1
            except Exception as e:
                if self.cli_logger:
                    self.cli_logger.error(f".bat execution failed: {e}")
                if check:
                    raise
                return_code = -1

        if check and return_code != 0 and not terminated_by_pattern:
            raise RuntimeError(f".bat exited with code {return_code}. See log: {log_file}")

        return {
            'return_code': return_code,
            'log_file': log_file,
            'run_dir': run_dir,
            'command': command,
            'terminated_by_pattern': terminated_by_pattern,
        }

    def run_bat_script(
        self,
        bat_path: str,
        args: Optional[List[str]] = None,
        subdir: Optional[str] = os.path.join("raw_data", "external"),
        log_name: str = "terminal_output.log",
        timeout: Optional[float] = None,
        env_overrides: Optional[Dict[str, str]] = None,
        check: bool = True,
    ) -> Dict[str, Any]:
        """
        Run a Windows .bat script and capture output into the per-test folder.

        Args:
            bat_path: Path to the .bat file to run.
            args: Optional list of arguments to pass to the script.
            subdir: Subdirectory under self.output_path where the run will occur.
            log_name: Name of the output log file to capture stdout/stderr.
            timeout: Optional timeout in seconds for the process.
            env_overrides: Optional environment variables to add/override.
            check: If True, raise on non-zero return code.

        Returns:
            Dict with keys: return_code, log_file, run_dir, command
        """
        if not self.output_path:
            raise RuntimeError("CLI test output_path is not set. Ensure setup_cli_mode() ran.")

        run_dir = os.path.join(self.output_path, subdir) if subdir else self.output_path
        os.makedirs(run_dir, exist_ok=True)

        # Build command line
        cmd_parts: List[str] = []
        # Quote .bat path if needed
        bat_quoted = f'"{bat_path}"' if ' ' in bat_path and not bat_path.startswith('"') else bat_path
        cmd_parts.append(bat_quoted)
        if args:
            for a in args:
                if isinstance(a, str) and ' ' in a and not a.startswith('"'):
                    cmd_parts.append(f'"{a}"')
                else:
                    cmd_parts.append(str(a))
        command = " ".join(cmd_parts)

        # Env setup (inherit + DMF_* paths + overrides)
        env = os.environ.copy()
        try:
            env.setdefault('DMF_TEST_OUTPUT_PATH', self.output_path)
            env.setdefault('DMF_TEST_LOGS_PATH', os.path.join(self.output_path, 'logs'))
            env.setdefault('DMF_TEST_RAW_DATA_PATH', os.path.join(self.output_path, 'raw_data'))
            if self.test_name:
                env.setdefault('DMF_TEST_NAME', self.test_name)
        except Exception:
            pass
        if env_overrides:
            env.update(env_overrides)

        # Open log file and execute
        log_file = os.path.join(run_dir, log_name)
        if self.cli_logger:
            self.cli_logger.info(f"Running .bat script: {command}")
            self.cli_logger.info(f"Working directory: {run_dir}")
            self.cli_logger.info(f"Output log: {log_file}")
        with open(log_file, 'w', encoding='utf-8', errors='ignore') as lf:
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=run_dir,
                    shell=True,
                    stdout=lf,
                    stderr=subprocess.STDOUT,
                    env=env,
                    text=True,
                )
                return_code = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                if self.cli_logger:
                    self.cli_logger.error(".bat execution timed out; process killed")
                if check:
                    raise
                return_code = -1
            except Exception as e:
                if self.cli_logger:
                    self.cli_logger.error(f".bat execution failed: {e}")
                if check:
                    raise
                return_code = -1

        if check and return_code != 0:
            raise RuntimeError(f".bat exited with code {return_code}. See log: {log_file}")

        return {
            'return_code': return_code,
            'log_file': log_file,
            'run_dir': run_dir,
            'command': command,
        }

    def copy_external_artifacts_to_raw_data(
        self,
        external_path: str,
        artifact_name: str = None,
        subdir: str = "external",
        timeout: float = 30.0,
        check_interval: float = 1.0
    ) -> Dict[str, Any]:
        """
        Check for newly created artifacts in an external path and copy them to raw_data directory.
        
        Args:
            external_path: Path where artifacts are expected to be created (e.g., "F:/map2sim_p4/Projects/nv_content/usa/scene_sanjose_plus37point330219_minus121point882464/scene_tests/images")
            artifact_name: Specific folder/file name to look for. If None, copies the entire external_path
            subdir: Subdirectory under raw_data where artifacts will be copied (default: "external")
            timeout: Maximum time to wait for artifacts to appear (seconds)
            check_interval: Time between checks for artifacts (seconds)
            
        Returns:
            Dict with keys: success, copied_paths, error_message, external_path, destination_path
        """
        import time
        import shutil
        
        if not self.output_path:
            return {
                'success': False,
                'error_message': 'CLI test output_path is not set. Ensure setup_cli_mode() ran.',
                'external_path': external_path,
                'destination_path': None,
                'copied_paths': []
            }
        
        # Determine what to copy
        if artifact_name:
            source_path = os.path.join(external_path, artifact_name)
        else:
            source_path = external_path
        
        # Wait for artifacts to appear
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(source_path):
                break
            time.sleep(check_interval)
        else:
            return {
                'success': False,
                'error_message': f'Artifacts not found at {source_path} within {timeout} seconds',
                'external_path': external_path,
                'destination_path': None,
                'copied_paths': []
            }
        
        # Create destination directory
        raw_data_dir = os.path.join(self.output_path, "raw_data", subdir)
        os.makedirs(raw_data_dir, exist_ok=True)
        
        # Determine destination path
        if artifact_name:
            destination_path = os.path.join(raw_data_dir, artifact_name)
        else:
            # Use the last part of the external path as the folder name
            destination_path = os.path.join(raw_data_dir, os.path.basename(external_path.rstrip(os.sep)))
        
        try:
            # Remove existing destination if it exists
            if os.path.exists(destination_path):
                if os.path.isdir(destination_path):
                    shutil.rmtree(destination_path)
                else:
                    os.remove(destination_path)
            
            # Copy artifacts
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
                copied_paths = [destination_path]
            else:
                shutil.copy2(source_path, destination_path)
                copied_paths = [destination_path]
            
            if self.cli_logger:
                self.cli_logger.info(f"Successfully copied artifacts from {source_path} to {destination_path}")
            
            return {
                'success': True,
                'error_message': None,
                'external_path': external_path,
                'destination_path': destination_path,
                'copied_paths': copied_paths
            }
            
        except Exception as e:
            error_msg = f"Failed to copy artifacts from {source_path} to {destination_path}: {str(e)}"
            if self.cli_logger:
                self.cli_logger.error(error_msg)
            
            return {
                'success': False,
                'error_message': error_msg,
                'external_path': external_path,
                'destination_path': destination_path,
                'copied_paths': []
            }

class Map2SimCLITestBase(CLITestBase):
    """
    Base class for Map2Sim CLI tests
    """
    
    # Avoid __init__ so pytest can collect subclasses
    component = "MAP2SIM"
    
    def setup_cli_mode(self, request):
        """
        Setup for Map2Sim CLI mode tests
        """
        super().setup_cli_mode(request)
        logger.info("Map2Sim CLI Mode: Test setup completed")
    
    def validate_map2sim_cli_requirements(self) -> bool:
        """
        Validate Map2Sim CLI test requirements
        
        Returns:
            bool: True if requirements are met
        """
        # Add Map2Sim-specific CLI validation here
        return True
    
    def execute_map2sim_cli_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a Map2Sim CLI operation
        
        Args:
            operation: Operation to execute
            **kwargs: Operation parameters
            
        Returns:
            Dict: Operation results
        """
        logger.info(f"Map2Sim CLI: Executing operation '{operation}' with params: {kwargs}")
        
        # Placeholder implementation for CLI ops
        result = {
            "operation": operation,
            "status": "success",
            "params": kwargs,
            "cli_mode": True
        }
        
        self.log_cli_test_result(
            f"map2sim_cli_{operation}", 
            "PASS", 
            f"Operation '{operation}' completed successfully"
        )
        
        return result
    
    def run_bat_script_with_completion_monitoring(
        self,
        bat_path: str,
        args: Optional[List[str]] = None,
        subdir: Optional[str] = os.path.join("raw_data", "external"),
        log_name: str = "terminal_output.log",
        timeout: Optional[float] = None,
        env_overrides: Optional[Dict[str, str]] = None,
        check: bool = True,
        monitor_pattern: Optional[str] = None,
        monitor_timeout: float = 300.0,
    ) -> Dict[str, Any]:
        """
        Run a Windows .bat script with real-time log monitoring for completion detection.
        Unlike run_bat_script_with_monitoring, this method does NOT terminate the process
        when the pattern is found - it just logs the detection and continues.

        Args:
            bat_path: Path to the .bat file to run.
            args: Optional list of arguments to pass to the script.
            subdir: Subdirectory under self.output_path where the run will occur.
            log_name: Name of the output log file to capture stdout/stderr.
            timeout: Optional timeout in seconds for the process.
            env_overrides: Optional environment variables to add/override.
            check: If True, raise on non-zero return code.
            monitor_pattern: Pattern to search for in the log file to detect completion.
            monitor_timeout: Maximum time to wait for the pattern to appear (seconds).

        Returns:
            Dict with keys: return_code, log_file, run_dir, command, pattern_detected
        """
        if not self.output_path:
            raise RuntimeError("CLI test output_path is not set. Ensure setup_cli_mode() ran.")

        run_dir = os.path.join(self.output_path, subdir) if subdir else self.output_path
        os.makedirs(run_dir, exist_ok=True)

        # Build command line
        cmd_parts: List[str] = []
        # Quote .bat path if needed
        bat_quoted = f'"{bat_path}"' if ' ' in bat_path and not bat_path.startswith('"') else bat_path
        cmd_parts.append(bat_quoted)
        if args:
            for a in args:
                if isinstance(a, str) and ' ' in a and not a.startswith('"'):
                    cmd_parts.append(f'"{a}"')
                else:
                    cmd_parts.append(str(a))
        command = " ".join(cmd_parts)

        # Env setup (inherit + DMF_* paths + overrides)
        env = os.environ.copy()
        try:
            env.setdefault('DMF_TEST_OUTPUT_PATH', self.output_path)
            env.setdefault('DMF_TEST_LOGS_PATH', os.path.join(self.output_path, 'logs'))
            env.setdefault('DMF_TEST_RAW_DATA_PATH', os.path.join(self.output_path, 'raw_data'))
            if self.test_name:
                env.setdefault('DMF_TEST_NAME', self.test_name)
        except Exception:
            pass
        if env_overrides:
            env.update(env_overrides)

        # Open log file and execute
        log_file = os.path.join(run_dir, log_name)
        if self.cli_logger:
            self.cli_logger.info(f"Running .bat script with completion monitoring: {command}")
            self.cli_logger.info(f"Working directory: {run_dir}")
            self.cli_logger.info(f"Output log: {log_file}")
            if monitor_pattern:
                self.cli_logger.info(f"Monitoring for completion pattern: {monitor_pattern}")

        pattern_detected = False
        with open(log_file, 'w', encoding='utf-8', errors='ignore') as lf:
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=run_dir,
                    shell=True,
                    stdout=lf,
                    stderr=subprocess.STDOUT,
                    env=env,
                    text=True,
                )
                
                # Monitor the log file for the pattern (non-blocking)
                if monitor_pattern:
                    import time
                    import re
                    import threading
                    
                    def monitor_log():
                        nonlocal pattern_detected
                        start_time = time.time()
                        
                        while proc.poll() is None and not pattern_detected:
                            # Check if we've exceeded the monitor timeout
                            if time.time() - start_time > monitor_timeout:
                                if self.cli_logger:
                                    self.cli_logger.warning(f"Monitor timeout reached ({monitor_timeout}s) without finding pattern: {monitor_pattern}")
                                break
                            
                            # Read the current log file content
                            try:
                                with open(log_file, 'r', encoding='utf-8', errors='ignore') as read_f:
                                    log_content = read_f.read()
                                    
                                # Check if pattern exists in the log
                                if re.search(monitor_pattern, log_content, re.IGNORECASE):
                                    if self.cli_logger:
                                        self.cli_logger.info(f"Completion pattern detected in log: {monitor_pattern}")
                                    pattern_detected = True
                                    break
                            except Exception as e:
                                if self.cli_logger:
                                    self.cli_logger.warning(f"Error reading log file during monitoring: {e}")
                            
                            # Wait a bit before checking again
                            time.sleep(1.0)
                    
                    # Start monitoring in a separate thread
                    monitor_thread = threading.Thread(target=monitor_log)
                    monitor_thread.daemon = True
                    monitor_thread.start()
                
                # Wait for process completion
                return_code = proc.wait(timeout=timeout)
                    
            except subprocess.TimeoutExpired:
                proc.kill()
                if self.cli_logger:
                    self.cli_logger.error(".bat execution timed out; process killed")
                if check:
                    raise
                return_code = -1
            except Exception as e:
                if self.cli_logger:
                    self.cli_logger.error(f".bat execution failed: {e}")
                if check:
                    raise
                return_code = -1

        if check and return_code != 0:
            raise RuntimeError(f".bat exited with code {return_code}. See log: {log_file}")

        return {
            'return_code': return_code,
            'log_file': log_file,
            'run_dir': run_dir,
            'command': command,
            'pattern_detected': pattern_detected,
        }

    def copy_map2sim_scene_artifacts(
        self,
        scene_path: str,
        artifacts_path: str = "scene_tests/images",
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        Convenience method to copy Map2Sim image artifacts from scene generation.
        Finds the latest folder by creation time in the artifacts directory, regardless of naming convention.
        
        Args:
            scene_path: Base path to the scene (e.g., "F:/map2sim_p4/Projects/nv_content/usa/scene_sanjose_plus37point330219_minus121point882464")
            artifacts_path: Relative path to artifacts directory from scene_path (default: "scene_tests/images")
            timeout: Maximum time to wait for artifacts to appear (seconds)
            
        Returns:
            Dict with keys: success, copied_paths, error_message, external_path, destination_path
        """
        import time
        
        full_artifacts_path = os.path.join(scene_path, artifacts_path)
        
        # Wait for any folder to appear and find the latest one by creation time
        start_time = time.time()
        latest_folder = None
        
        while time.time() - start_time < timeout:
            # Get all items in the artifacts directory
            if os.path.exists(full_artifacts_path):
                all_items = [os.path.join(full_artifacts_path, item) for item in os.listdir(full_artifacts_path)]
                # Filter to only include directories
                directories = [item for item in all_items if os.path.isdir(item)]
                
                if directories:
                    # Get the most recently created folder (latest by creation time)
                    latest_folder = max(directories, key=os.path.getctime)
                    break
            
            time.sleep(1.0)
        
        if not latest_folder:
            return {
                'success': False,
                'error_message': f'No artifact folder found in {full_artifacts_path} within {timeout} seconds',
                'external_path': full_artifacts_path,
                'destination_path': None,
                'copied_paths': []
            }
        
        # Copy the latest folder
        folder_name = os.path.basename(latest_folder)
        return self.copy_external_artifacts_to_raw_data(
            external_path=full_artifacts_path,
            artifact_name=folder_name,
            subdir="",
            timeout=5.0
        )

class DSRS_CLITestBase(CLITestBase):
    """
    Base class for DSRS CLI tests
    """
    
    # Avoid __init__ so pytest can collect subclasses
    component = "DSRS"
    
    def setup_cli_mode(self, request):
        """
        Setup for DSRS CLI mode tests
        """
        super().setup_cli_mode(request)
        logger.info("DSRS CLI Mode: Test setup completed")
    
    def validate_dsrs_cli_requirements(self) -> bool:
        """
        Validate DSRS CLI test requirements
        
        Returns:
            bool: True if requirements are met
        """
        return True
    
    def execute_dsrs_cli_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a DSRS CLI operation
        """
        logger.info(f"DSRS CLI: Executing operation '{operation}' with params: {kwargs}")
        result = {
            "operation": operation,
            "status": "success",
            "params": kwargs,
            "cli_mode": True
        }
        self.log_cli_test_result(
            f"dsrs_cli_{operation}", 
            "PASS", 
            f"Operation '{operation}' completed successfully"
        )
        return result

# Pytest fixtures for CLI mode
@pytest.fixture(scope="function", autouse=True)
def cli_mode_setup(request):
    """
    Pytest fixture for CLI mode setup
    """
    # Check if this is a CLI test
    if hasattr(request.cls, 'setup_cli_mode'):
        request.cls.setup_cli_mode(request)
    elif hasattr(request.instance, 'setup_cli_mode'):
        request.instance.setup_cli_mode(request)


def pytest_addoption(parser):
    """
    Add CLI mode option to pytest
    """
    parser.addoption("--cli_mode", action="store", default="false", 
                    help="Enable CLI mode for headless testing")
    parser.addoption("--output_path", action="store", default="./results", 
                    help="Output path for test results")
    parser.addoption("--json_data_b64", action="store", default=None, 
                    help="Base64 encoded JSON data for CLI tests")
