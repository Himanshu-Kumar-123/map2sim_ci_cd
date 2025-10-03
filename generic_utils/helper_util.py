# Standard library imports
import re
import os
import ast
import sys
import time
import json
import psutil
import shutil
import tomli_w
import threading
import subprocess
try:
    import tomllib # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib
import tkinter as tk
import platform
import stat
from pathlib import Path

# Local imports
from generic_utils.googledrive_upload_util import GoogleDriveUploadMethods
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger(__name__, varc.framework_logs_path)


class HelperMethods:
    '''This class consist of methods that support core engine in some operations'''
                
    @staticmethod
    def test_command_dict_updater(test_dict):
        '''This function is used to update commands.txt file'''
        
        # Open the file in append mode
        with open(f"{test_dict['test_path']}/commands.txt", "a") as file:
            # Write the dictionary string to the file
            test_command_dict_str = str(varc.test_command_dict)
            file.write(test_command_dict_str + "\n")

    @staticmethod
    def sr_killer(test_dict):
        '''This function is used to kill dsrs or map2sim process'''
        
        # Windows PowerShell command to kill Sim Ready process
        timeout_kill_sim_command = 'Stop-Process -Name "*drivesim*" -Force'
        varc.test_command_dict[f"timeout_kill_sim_command"] = timeout_kill_sim_command
        try:
            subprocess.run(['powershell', '-Command', timeout_kill_sim_command], shell=True)
        except Exception as e:
            logger.info('\n')
            logger.error(f"[DMF_RUNNER] : [{test_dict['name']}] : Failed to kill Sim Ready process. Exception: {e}")
            logger.info('\n')
                
    
    @staticmethod
    def kill_process_by_command_part(command_part, kill=True):
        '''This function is used to kill processes - Windows-only version'''
        
        if "ffmpeg" in command_part:
            parts = command_part.split()
            try:
                parent_pid = int(parts[-1])
                parent = psutil.Process(parent_pid)
                children = parent.children(recursive=True)

                if children:
                    ffmpeg_pid = children[0].pid
                    
                    if kill:
                        # Windows: Force kill ffmpeg process
                        subprocess.run(["taskkill", "/F", "/PID", str(ffmpeg_pid)], 
                                     check=False, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        logger.info(f"ffmpeg process with pid {ffmpeg_pid} has been force killed.")
                    else:
                        # Windows: Graceful termination (send WM_CLOSE)
                        subprocess.run(["taskkill", "/PID", str(ffmpeg_pid)], 
                                     check=False, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        logger.info(f"ffmpeg process with pid {ffmpeg_pid} has been terminated.")
                    
                    # Wait for proper ffmpeg cleanup
                    if hasattr(varc, 'skip_docker_launch') and varc.skip_docker_launch:
                        message = "Press Enter to continue. If you need the video to be saved properly, please wait for 30 seconds before pressing Enter."
                        HelperMethods.print_message(message,'blue')
                        input()
                    else:
                        time.sleep(30)
                        
            except (psutil.NoSuchProcess, ValueError, IndexError) as e:
                logger.error(f"Error handling ffmpeg process: {e}")
            except Exception as e:
                logger.error(f"Unexpected error with ffmpeg process: {e}")
        else:
            # Find all processes matching the command_part
            matching_processes = []
            try:
                for process in psutil.process_iter(['pid', 'cmdline', 'name']):
                    try:
                        # Check both cmdline and process name
                        cmdline_match = (process.info['cmdline'] and 
                                       any(command_part.lower() in str(arg).lower() for arg in process.info['cmdline']))
                        name_match = (process.info['name'] and 
                                    command_part.lower() in process.info['name'].lower())
                        
                        if cmdline_match or name_match:
                            matching_processes.append(process)
                            
                    except (psutil.AccessDenied, psutil.ZombieProcess):
                        # Skip processes we can't access (common on Windows)
                        continue

                if matching_processes:
                    for process in matching_processes:
                        try:
                            pid = process.pid
                            process_name = process.info.get('name', 'Unknown')
                            
                            if kill:
                                # Windows: Force kill process tree (/T flag kills child processes too)
                                result = subprocess.run(["taskkill", "/F", "/PID", str(pid), "/T"], 
                                                      check=False, capture_output=True, text=True,
                                                      creationflags=subprocess.CREATE_NO_WINDOW)
                                
                                if result.returncode == 0:
                                    logger.info(f"Process '{process_name}' with command containing '{command_part}' and pid {pid} has been force killed.")
                                else:
                                    logger.warning(f"Could not force kill process {pid}: {result.stderr.strip()}")
                            else:
                                # Windows: Graceful termination (no /F flag)
                                result = subprocess.run(["taskkill", "/PID", str(pid), "/T"], 
                                                      check=False, capture_output=True, text=True,
                                                      creationflags=subprocess.CREATE_NO_WINDOW)
                                
                                if result.returncode == 0:
                                    logger.info(f"Process '{process_name}' with command containing '{command_part}' and pid {pid} has been terminated.")
                                else:
                                    logger.warning(f"Could not terminate process {pid}: {result.stderr.strip()}")
                                    
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            logger.warning(f"Could not access process {process.pid}: {e}")
                        except Exception as e:
                            logger.error(f"Unexpected error with process {process.pid}: {e}")
                else:
                    logger.info(f"No processes found with command containing '{command_part}'.")
                
            except Exception as e:
                logger.error(f"Error searching for processes: {e}")

    @staticmethod
    def kill_process_by_name(process_name, kill=True):
        '''Windows-specific helper to kill processes by name'''
        try:
            if kill:
                # Force kill all processes with this name
                result = subprocess.run(["taskkill", "/F", "/IM", process_name, "/T"], 
                                      check=False, capture_output=True, text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Graceful termination
                result = subprocess.run(["taskkill", "/IM", process_name, "/T"], 
                                      check=False, capture_output=True, text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                logger.info(f"Successfully {'killed' if kill else 'terminated'} all '{process_name}' processes.")
            elif "not found" in result.stderr.lower():
                logger.info(f"No '{process_name}' processes found to {'kill' if kill else 'terminate' }.")
            else:
                logger.warning(f"Error {'killing' if kill else 'terminating'} '{process_name}': {result.stderr.strip()}")
            
        except Exception as e:
            logger.error(f"Exception while {'killing' if kill else 'terminating'} '{process_name}': {e}")

    @staticmethod
    def kill_kit_process(process_name):
        '''
        Kill a specific process by name with detailed logging (Windows)
        This is the reusable version of the startup cleanup logic
        
        Args:
            process_name (str): Name of the process to kill (e.g., "kit.exe")
        '''
        try:
            logger.info(f"Attempting to kill process: {process_name}")
            kill_command = ["taskkill", "/F", "/IM", process_name]
            result = subprocess.run(
                kill_command, 
                capture_output=True, 
                text=True, 
                check=False, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Check stderr for "not found" error specifically
            if "ERROR: The process" in result.stderr and "not found" in result.stderr:
                logger.debug(f"Process {process_name} not found, likely already closed.")
                return True
            elif "SUCCESS:" in result.stdout:
                logger.info(f"Successfully terminated process {process_name}.")
                logger.debug(f"Taskkill output for {process_name}: {result.stdout.strip()}")
                return True
            else:
                logger.warning(f"Unexpected output from taskkill for {process_name}. ReturnCode: {result.returncode}, Stdout: '{result.stdout.strip()}', Stderr: '{result.stderr.strip()}'")
                return False
                
        except Exception as e:
            logger.error(f"Error killing process {process_name}: {e}")
            return False

    @staticmethod
    def get_resolution(test_dict):
        '''This function is used to get screen resolution'''
        
        try:
            # Set the DISPLAY environment variable
            os.environ['DISPLAY'] = ':0.0'
            root = tk.Tk()
            varc.width = root.winfo_screenwidth()
            varc.height = root.winfo_screenheight()
            root.destroy()

        except Exception as e:
            logger.warning(f"[DMF_RUNNER] : [{test_dict['name']}] Screen Resoultion fetch failed. Proceeding with default resolution. Exception: {e}")
            test_dict['dmf_warnings'].append(f'Screen Resoultion fetch failed. Im proceeding with default resolution. exception I captured is {e}')
            varc.width = "1920"
            varc.height = "1080"
            
    @staticmethod
    def print_message(message, color="default", bold=False, start_new_line=False):
        '''Deprecated: route print-style messages to the framework logger for consistency.'''
        # Map legacy colors to log levels
        level = {
            "red": "ERROR",
            "blue": "INFO",
            "green": "INFO",
            "default": "INFO"
        }.get(color, "INFO")
        if level == "ERROR":
            logger.error(message)
        else:
            logger.info(message)
        
    @staticmethod
    def sim_input(test_dict):
        '''This function sends input to Windows simulation processes'''
        
        try:
            # Find Kit/DSRS processes on Windows
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Look for simulation processes
                    if (proc.info['name'] and 'kit' in proc.info['name'].lower()) or \
                       (proc.info['cmdline'] and any('drivesim' in str(arg).lower() for arg in proc.info['cmdline'])):
                        
                        pid = proc.info['pid']
                        logger.debug(f"Found simulation process: {proc.info['name']} (PID: {pid})")
                        
                        # Windows equivalent would be sending window messages or using named pipes
                        # This is application-specific and would need to be implemented
                        # based on how the Windows simulation process accepts input
                        
                        # Example: Send keyboard input to process window (if it has GUI)
                        # This would require win32api or similar Windows-specific libraries
                        
                except (psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                
        except Exception as e:
            logger.info('\n')
            logger.error(f"[DMF_RUNNER] : [{test_dict['name']}] : sending input to sim failed, Exception: {e}")
            logger.info('\n')

    @staticmethod
    def update_file_permission(permission: str, file_path: str):
        """This function is used to change the permissions of a file on Windows.

        Args:
            permission (str): The permission to be set. 
                             For Windows: 'read', 'write', 'full', 'modify', or octal like '755'
            file_path (str): The file path for which the permission is to be changed.

        Returns:
            bool: True if the file permission was successfully changed, False if the permission change failed.
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"[DMF] : File does not exist: {file_path}")
                return False
            
            # Convert permission string to Windows-compatible format
            if permission.lower() == 'read':
                # Read-only permission
                file_path.chmod(stat.S_IREAD)
                logger.info(f"[DMF] : Successfully set read-only permission for {file_path}")
                return True
            
            elif permission.lower() in ['write', 'full', 'modify']:
                # Full permissions (read, write, execute)
                file_path.chmod(stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
                logger.info(f"[DMF] : Successfully set full permissions for {file_path}")
                return True
            
            elif permission.isdigit() and len(permission) == 3:
                # Handle octal permissions (like 755, 644, etc.)
                octal_perm = int(permission, 8)
                
                # Convert octal to Windows stat flags
                mode = 0
                if octal_perm & 0o400:  # Owner read
                    mode |= stat.S_IREAD
                if octal_perm & 0o200:  # Owner write  
                    mode |= stat.S_IWRITE
                if octal_perm & 0o100:  # Owner execute
                    mode |= stat.S_IEXEC
                
                file_path.chmod(mode)
                logger.info(f"[DMF] : Successfully set permissions {permission} for {file_path}")
                return True
            
            else:
                # Use Windows icacls command for advanced permissions
                return HelperMethods._update_file_permission_icacls(permission, str(file_path))
            
        except Exception as e:
            logger.error(f"[DMF] : Failed to change file permission of {file_path}. Error: {e}")
            return False

    @staticmethod
    def _update_file_permission_icacls(permission: str, file_path: str):
        """Use Windows icacls command for advanced file permissions"""
        try:
            # Map common permission strings to Windows icacls format
            permission_map = {
                'full': 'F',           # Full control
                'modify': 'M',         # Modify
                'read': 'R',           # Read
                'write': 'W',          # Write
                'execute': 'X',        # Execute
                'readonly': 'R',       # Read only
                'readwrite': 'RW'      # Read + Write
            }
            
            icacls_perm = permission_map.get(permission.lower(), permission)
            
            # Grant permission to current user
            import getpass
            current_user = getpass.getuser()
            
            # Windows icacls command
            icacls_command = f'icacls "{file_path}" /grant {current_user}:{icacls_perm}'
            
            result = subprocess.run(icacls_command, capture_output=True, text=True, 
                                  shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                logger.info(f"[DMF] : Successfully changed file permission of {file_path} using icacls")
                return True
            else:
                logger.error(f"[DMF] : Failed to change file permission of {file_path}. icacls error: {result.stderr}")
                return False
            
        except Exception as e:
            logger.error(f"[DMF] : Failed to use icacls for {file_path}. Error: {e}")
            return False

    @staticmethod
    def update_directory_permissions(permission: str, directory_path: str, recursive: bool = True):
        """Windows-specific method to update directory permissions"""
        try:
            dir_path = Path(directory_path)
            
            if not dir_path.exists():
                logger.warning(f"[DMF] : Directory does not exist: {dir_path}")
                return False
            
            import getpass
            current_user = getpass.getuser()
            
            # Windows icacls command for directories
            if recursive:
                icacls_command = f'icacls "{dir_path}" /grant {current_user}:F /T'
            else:
                icacls_command = f'icacls "{dir_path}" /grant {current_user}:F'
            
            result = subprocess.run(icacls_command, capture_output=True, text=True, 
                                  shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                logger.info(f"[DMF] : Successfully updated directory permissions for {dir_path}")
                return True
            else:
                logger.error(f"[DMF] : Failed to update directory permissions for {dir_path}. icacls error: {result.stderr}")
                return False
            
        except Exception as e:
            logger.error(f"[DMF] : Failed to update directory permissions for {directory_path}. Error: {e}")
            return False

    @staticmethod
    def make_file_executable(file_path: str):
        """Windows-specific method to make a file executable"""
        try:
            file_path = Path(file_path)
            
            # On Windows, executability is determined by file extension
            if file_path.suffix.lower() not in ['.exe', '.bat', '.cmd', '.ps1']:
                logger.warning(f"[DMF] : Warning: {file_path} may not be executable on Windows (no .exe/.bat/.cmd/.ps1 extension)")
            
            # Set full permissions
            file_path.chmod(stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
            logger.info(f"[DMF] : Made file executable: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"[DMF] : Failed to make file executable: {file_path}. Error: {e}")
            return False

    @staticmethod
    def remove_readonly_attribute(file_path: str):
        """Windows-specific method to remove read-only attribute"""
        try:
            # Windows attrib command to remove read-only attribute
            attrib_command = f'attrib -R "{file_path}"'
            
            result = subprocess.run(attrib_command, capture_output=True, text=True, 
                                  shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                logger.info(f"[DMF] : Successfully removed read-only attribute from {file_path}")
                return True
            else:
                logger.error(f"[DMF] : Failed to remove read-only attribute from {file_path}")
                return False
            
        except Exception as e:
            logger.error(f"[DMF] : Error removing read-only attribute: {e}")
            return False

    @staticmethod
    def print_debug_commands():
        """Print helpful debugging commands and information for PDB."""
        
        HelperMethods.print_message("========================= PDB Debugging Commands ==============================", "red", bold=True, start_new_line=True)
        HelperMethods.print_message("Navigation:", "red", bold=True)
        HelperMethods.print_message("n or next: Execute the current line and move to the next line in the current function.", "red")
        HelperMethods.print_message("s or step: Step into the current function call.", "red")
        HelperMethods.print_message("c or continue: Continue execution until the next breakpoint is encountered.", "red")
        HelperMethods.print_message("r or return: Continue execution until the current function returns.", "red")
        HelperMethods.print_message("q or quit: Quit the debugger and exit the program.", "red")
        HelperMethods.print_message("Inspection:", "red", bold=True)
        HelperMethods.print_message("l or list: Show the current position in the source code.", "red")
        HelperMethods.print_message("p <expression> or print <expression>: Print the value of an expression.", "red")
        HelperMethods.print_message("pp <expression> or pprint <expression>: Pretty-print the value of an expression.", "red")
        HelperMethods.print_message("args: Print the arguments of the current function.", "red")
        HelperMethods.print_message("locals: Print the local variables in the current scope.", "red")
        HelperMethods.print_message("globals: Print the global variables.", "red")
        HelperMethods.print_message("Setting breakpoints:", "red", bold=True)
        HelperMethods.print_message("b <line_number> or break <line_number>: Set a breakpoint at the specified line number.", "red")
        HelperMethods.print_message("b <function_name> or break <function_name>: Set a breakpoint at the first line of the specified function.", "red")
        HelperMethods.print_message("b <file_name>:<line_number>: Set a breakpoint at a specific line in a file.", "red")
        HelperMethods.print_message("tbreak <expression>: Set a temporary breakpoint based on the given expression.", "red")
        HelperMethods.print_message("Conditional breakpoints:", "red", bold=True)
        HelperMethods.print_message("break <line_number> if <condition>: Set a breakpoint at the specified line only if the condition is true.", "red")
        HelperMethods.print_message("condition <breakpoint_number> <condition>: Set a condition for an existing breakpoint.", "red")
        HelperMethods.print_message("Skipping code:", "red", bold=True)
        HelperMethods.print_message("skip: Skip the current breakpoint.", "red")
        HelperMethods.print_message("Stack inspection:", "red", bold=True)
        HelperMethods.print_message("w or where: Show the current call stack.", "red")
        HelperMethods.print_message("u or up: Move up one level in the call stack.", "red")
        HelperMethods.print_message("d or down: Move down one level in the call stack.", "red")
        HelperMethods.print_message("Other:", "red", bold=True)
        HelperMethods.print_message("! <statement>: Execute a Python statement in the current context.", "red")
        HelperMethods.print_message("run: Restart the program from the beginning.", "red")
        HelperMethods.print_message("restart: Restart the debugger and re-run the current script.", "red")
        HelperMethods.print_message("help: Show a list of available commands.", "red")
        HelperMethods.print_message("================================================================================", "red")
