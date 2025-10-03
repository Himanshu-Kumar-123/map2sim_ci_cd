# Standard imports
import os
import sys
import psutil
import subprocess
from typing import List, Optional

# Local imports
from fwk.shared.variables_util import varc
from generic_utils.helper_util import HelperMethods

class WindowsDevelopMode():
    '''This class consists of methods that help in Windows develop mode for Kit-based applications (DSRS/MAP2SIM)'''
    
    @staticmethod
    def check_kit_process(test_dict: dict, component_name: str = "map2sim") -> None:
        '''This method checks if Kit process is running with UI automator flag on Windows'''
        
        try:
            # Look for Kit-based processes (works for both DSRS and MAP2SIM)
            matching_processes = WindowsDevelopMode._find_kit_processes()
            
            if matching_processes:
                # Check each process for UI automator flag
                for process_info in matching_processes:
                    if WindowsDevelopMode._has_ui_automator_flag(process_info):
                        # Found a suitable process, set skip flag
                        varc.skip_process_launch = True
                        varc.kit_process_info = process_info
                        # Try to extract HTTP port from process cmdline for develop mode usage
                        try:
                            cmdline = process_info.get('cmdline', [])
                            detected_port = WindowsDevelopMode._extract_http_port_from_cmdline(cmdline)
                            if detected_port is not None:
                                varc.kit_http_port = detected_port
                                HelperMethods.print_message(
                                    f"[{test_dict['name']}] : Detected Kit HTTP port: {detected_port}",
                                    'green'
                                )
                        except Exception:
                            pass
                        HelperMethods.print_message(
                            f"[{test_dict['name']}] : Found running {component_name} process with UI automator: PID {process_info['pid']}", 
                            'green'
                        )
                        return
            
            # No suitable process found
            raise Exception(f"No suitable {component_name} process with UI automator found.")
                            
        except Exception as e:            
            warning_message = f""" 
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

[{test_dict['name']}] : WARNING: Windows Develop Mode Issue

Exception captured: {e}

ISSUE: You have enabled Windows develop mode using the --windows-develop-mode flag, but no suitable {component_name.upper()} process with UI automator is currently running.

SOLUTION: Please start the {component_name.upper()} application manually with the UI automator enabled using this exact command:

{WindowsDevelopMode._get_sample_kit_command(test_dict, component_name)}

REQUIREMENTS:
✓ UI automator must be enabled (--enable omni.kit.remote_ui_automator)
✓ HTTP server must be enabled (--/exts/omni.services.transport.server.http/port=9682)
✓ Application must be running and accessible before starting the framework

STEPS:
1. Copy and run the command above in a separate terminal/command prompt
2. Wait for the {component_name.upper()} application to fully load
3. Run the DMF framework again with the same parameters

╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

Exiting framework..."""
            HelperMethods.print_message(warning_message, 'blue')
            sys.exit()

    @staticmethod
    def _find_kit_processes() -> List[dict]:
        '''Find all running Kit-based processes (DSRS, MAP2SIM, etc.)'''
        matching_processes = []
        
        # Process names to look for (covers both DSRS and MAP2SIM)
        target_process_names = [
            'kit.exe',  # Generic Kit application
            'dsrs.exe',
            'omni.drivesim.dsrs.exe', 
            'drivesim.exe',
            'map2sim.exe',
            'omni.drivesim.map2sim.exe',
            'omni.map2sim.exe',
            # Add other possible executable names
        ]
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info.get('name', '').lower()
                    
                    # Check if process name matches our targets
                    if any(target.lower() in proc_name for target in target_process_names):
                        matching_processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cmdline': proc_info.get('cmdline', []),
                            'exe': proc_info.get('exe', '')
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process might have terminated or we don't have access
                    continue
                    
        except Exception as e:
            HelperMethods.print_message(f"Error while scanning processes: {e}", 'red')
            
        return matching_processes

    @staticmethod
    def _has_ui_automator_flag(process_info: dict) -> bool:
        '''Check if a process has UI automator flag in its command line'''
        cmdline = process_info.get('cmdline', [])
        
        if not cmdline:
            return False
            
        # Join command line arguments into a single string for easier searching
        cmd_string = ' '.join(cmdline)
        
        # Look for UI automator flags
        ui_automator_patterns = [
            '--enable omni.kit.remote_ui_automator',
            'omni.kit.remote_ui_automator-',
            '--/exts/omni.services.transport.server.http',
        ]
        
        for pattern in ui_automator_patterns:
            if pattern in cmd_string:
                HelperMethods.print_message(f"Found UI automator pattern '{pattern}' in process {process_info['pid']}", 'green')
                return True
                
        return False

    @staticmethod
    def _extract_http_port_from_cmdline(cmdline: List[str]) -> Optional[int]:
        """Extract the Kit HTTP port from a process cmdline list if present.
        Looks for patterns like '--/exts/omni.services.transport.server.http/port=<PORT>'.
        """
        try:
            for arg in cmdline or []:
                if not isinstance(arg, str):
                    continue
                if '--/exts/omni.services.transport.server.http/port=' in arg:
                    try:
                        port_str = arg.split('=')[-1].strip().strip('"')
                        port_val = int(port_str)
                        return port_val
                    except Exception:
                        continue
            return None
        except Exception:
            return None

    @staticmethod
    def _get_sample_kit_command(test_dict, component_name) -> str:
        '''Generate a sample command for running Kit application with UI automator'''
        
        # Get application path from TOML - construct the exact same way as command_generator_util.py
        app_path = "kit.exe"  # Default fallback
        
        if hasattr(varc, 'toml_dict') and varc.toml_dict:
            if 'BUILD' in varc.toml_dict and 'local_build_path' in varc.toml_dict['BUILD']:
                build_path = varc.toml_dict['BUILD']['local_build_path']
                if 'app' in varc.toml_dict:
                    app_name = varc.toml_dict['app']
                    app_path = os.path.join(build_path, app_name)
        
        # Generate the exact command format as used in command_generator_util.py
        sample_command = f'"{app_path}" --allow-root --/app/window/width=1920 --/app/window/height=1080 --/app/window/fullscreen=true --/app/file/ignoreUnsavedStage=true --/exts/omni.services.transport.server.http/port=9682 --/exts/omni.kit.registry.nucleus/registries/2/name="kit/default" --/exts/omni.kit.registry.nucleus/registries/2/url="omniverse://kit-extensions.ov.nvidia.com/exts/kit/default" --enable omni.kit.remote_ui_automator'
        
        return sample_command

    @staticmethod
    def kill_kit_processes(test_dict, process_name_patterns: Optional[List[str]] = None):
        '''Kill Kit-based processes (optional cleanup method)'''
        
        if process_name_patterns is None:
            process_name_patterns = [
                'kit.exe', 'dsrs.exe', 'omni.drivesim.dsrs.exe', 'drivesim.exe',
                'map2sim.exe', 'omni.drivesim.map2sim.exe', 'omni.map2sim.exe'
            ]
        
        killed_processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(pattern.lower() in proc_name for pattern in process_name_patterns):
                        proc.terminate()  # Try graceful termination first
                        killed_processes.append(proc.info)
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Wait a bit and force kill if necessary
            if killed_processes:
                import time
                time.sleep(2)
                
                for proc_info in killed_processes:
                    try:
                        proc = psutil.Process(proc_info['pid'])
                        if proc.is_running():
                            proc.kill()  # Force kill
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                        
            if killed_processes:
                HelperMethods.print_message(
                    f"Killed {len(killed_processes)} Kit processes", 
                    'yellow'
                )
                
        except Exception as e:
            HelperMethods.print_message(f"Error while killing processes: {e}", 'red')

    @staticmethod
    def is_develop_mode_enabled(test_dict) -> bool:
        '''Check if Windows develop mode is enabled in test configuration'''
        
        # Check automation_flags_dict for --develop-mode flag
        automation_flags = test_dict.get('automation_flags_dict', {})
        if '--windows-develop-mode' in automation_flags:
            return True
            
        # Check automation_suite_flags_dict for --develop-mode flag
        suite_flags = test_dict.get('automation_suite_flags_dict', {})
        if '--windows-develop-mode' in suite_flags:
            return True
            
        # Check in automation_flags list for string format
        flags_list = test_dict.get('automation_flags', [])
        for flag in flags_list:
            if isinstance(flag, str) and '--windows-develop-mode' in flag:
                return True
                
        # Check in automation_suite_flags list for string format
        suite_flags_list = test_dict.get('automation_suite_flags', [])
        for flag in suite_flags_list:
            if isinstance(flag, str) and '--windows-develop-mode' in flag:
                return True
        
        return False 