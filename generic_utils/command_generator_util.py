# Standard imports
import os
import json
import subprocess
import sys
import datetime
from typing import List
# Local imports
from fwk.fwk_logger.fwk_logging import get_logger
from fwk.shared.variables_util import varc
from fwk.shared.constants import AUTOMATOR_VERSION

logger = get_logger(__name__, varc.framework_logs_path)

class CommandGeneratorMethods():
    '''This class is intended to generate different DSRS and Map2Sim commands'''

    @staticmethod
    def _get_python_executable():
        """
        Get the appropriate Python executable with version checking.
        Prioritizes default python3, then falls back to TOML configuration.
        Returns the python executable path after verifying it's 3.8 or newer.
        """        
        def check_python_version(python_cmd):
            """Check if the python executable is version 3.8 or newer"""
            try:
                result = subprocess.run([python_cmd, '--version'], 
                                      capture_output=True, text=True, check=True)
                version_output = result.stdout.strip()
                logger.info(f"Python version output: {version_output}")
                
                # Parse version from output like "Python 3.9.7"
                if version_output.startswith('Python '):
                    version_str = version_output.split()[1]
                    version_parts = version_str.split('.')
                    major = int(version_parts[0])
                    minor = int(version_parts[1])
                    
                    if major == 3 and minor >= 8:
                        logger.info(f"Python version {version_str} meets requirement (>= 3.8)")
                        return True
                    else:
                        logger.warning(f"Python version {version_str} does not meet requirement (>= 3.8)")
                        return False
                else:
                    logger.error(f"Unexpected version output format: {version_output}")
                    return False
                    
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to get version for {python_cmd}: {e}")
                return False
            except (ValueError, IndexError) as e:
                logger.error(f"Failed to parse version for {python_cmd}: {e}")
                return False
            except FileNotFoundError:
                logger.warning(f"Python executable not found: {python_cmd}")
                return False
        
        # First, try to use default python3
        logger.info("Attempting to use default python3...")
        if check_python_version('python3'):
            logger.info("Using default python3")
            # Prefer the current interpreter to avoid PATH/AppAlias issues
            return sys.executable
        
        # If python3 is not available or doesn't meet version requirement, try python
        logger.info("python3 not available or doesn't meet version requirement, trying 'python'...")
        if check_python_version('python'):
            logger.info("Using default python")
            # Prefer the current interpreter to avoid PATH/AppAlias issues
            return sys.executable
        
        # Fall back to TOML configuration if it exists
        logger.warning("Default python3/python not available or doesn't meet version requirement")
        toml_python = varc.toml_dict.get('ENVIRONMENT', {}).get('PYTHONEXE')
        if toml_python:
            logger.info(f"Falling back to TOML configured Python: {toml_python}")
            if check_python_version(toml_python):
                logger.info(f"TOML configured Python {toml_python} meets version requirement")
                return toml_python
            else:
                logger.error(f"TOML configured Python {toml_python} does not meet version requirement (>= 3.8)")
                raise RuntimeError(f"Python version requirement not met. Need Python 3.8 or newer, but {toml_python} does not meet this requirement.")
        
        # If nothing works, raise an error
        logger.error("No suitable Python executable found. Need Python 3.8 or newer.")
        raise RuntimeError("No suitable Python executable found. Please ensure Python 3.8 or newer is installed and available as 'python3' or 'python', or specify a valid PYTHONEXE in the TOML configuration.")

    @staticmethod
    def dsrs_command_generator(test_dict) -> List[str]:
        '''This function is used to generate command for dsrs'''
        logger.info(f"Generating DSRS commands for test: {test_dict.get('name', 'unnamed')}")
                    
        varc.control_block['post_processing'] = False
        varc.control_block['pp_directory_check'] = False
        varc.control_block['pp_data_transfer'] = False
        varc.control_block['pp_ffmpeg'] = False

        if "--ui-automator-version" in test_dict['automation_suite_flags_dict']:
            automator_version = test_dict['automation_suite_flags_dict']["--ui-automator-version"]
        else:
            automator_version = AUTOMATOR_VERSION
               
        # Construct the full path to the DSRS application
        app = varc.toml_dict['app']  # Application name from TOML
        build_path = varc.toml_dict['BUILD']['local_build_path']
        app_full_path = os.path.join(build_path, app)
        
        logger.info(f"DSRS application path: {app_full_path}")
        
        # Start building the kit command with the full application path
        kit_command = f'"{app_full_path}"'
        
        # Add required flags in the exact order as provided in the sample
        kit_command += " --allow-root"
        kit_command += " --/app/file/ignoreUnsavedStage=true"
        kit_command += " --/exts/omni.services.transport.server.http/port=9682"
        kit_command += ' --/exts/omni.kit.registry.nucleus/registries/2/name="kit/default"'
        kit_command += ' --/exts/omni.kit.registry.nucleus/registries/2/url="omniverse://kit-extensions.ov.nvidia.com/exts/kit/default"'
        kit_command += " --enable omni.kit.remote_ui_automator"
        
        # Add kit suite flags if they exist
        if 'kit_suite_flags' in test_dict and test_dict['kit_suite_flags']:
            for flags in test_dict['kit_suite_flags']:
                if flags.strip():  # Only add non-empty flags
                    kit_command += " " + flags
                
        # Add kit flags if they exist
        if 'kit_flags' in test_dict and test_dict['kit_flags']:
            for flags in test_dict['kit_flags']:
                if flags.strip():  # Only add non-empty flags
                    kit_command += " " + flags
        
        # Get Python executable with version checking
        try:
            python_exe = CommandGeneratorMethods._get_python_executable()
            logger.info(f"Using Python executable for pytest: {python_exe}")
        except RuntimeError as e:
            logger.error(f"Failed to get suitable Python executable: {e}")
            raise
        
        # Get script path from test dictionary (set during pretest)
        dsrs_scripts_path = test_dict['script_path']
        
        # Store the script path in varc for the runner to use
        varc.test_command_dict["dsrs_scripts_path"] = dsrs_scripts_path
        
        # Get the scenario field and create full path
        scenario_name = test_dict['scenario']
        scenario_full_path = os.path.join(dsrs_scripts_path, scenario_name)
        logger.info(f"Using full scenario path: {scenario_full_path}")
        
        # Use the full path to the scenario file with connection parameters
        # Extract port from detected develop-mode process if available; fallback to default 9682
        kit_port = str(varc.kit_http_port) if getattr(varc, 'kit_http_port', None) else "9682"
        ip = "127.0.0.1"
        pytest_command = f"{python_exe} -m pytest -s {scenario_full_path} --ip={ip} --port={kit_port} --output_path={test_dict['test_path']}"
        
        ui_automation_flags_dict = {}
        
        # Add automation suite flags
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            for key, value in test_dict['automation_suite_flags_dict'].items():
                # Filter for DSRS specific flags and debug mode
                if key.startswith("--dsrs") or key == "--ui_debug_mode":
                    ui_automation_flags_dict[key] = value
                
        # Add automation flags
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            for key, value in test_dict['automation_flags_dict'].items():
                # Filter for DSRS specific flags and debug mode
                if key.startswith("--dsrs") or key == "--ui_debug_mode":
                    ui_automation_flags_dict[key] = value

        if ui_automation_flags_dict:
            # Serialize dictionary to JSON and encode as base64 to avoid shell escaping issues
            import base64
            ui_automation_flags_json = json.dumps(ui_automation_flags_dict)
            encoded_json = base64.b64encode(ui_automation_flags_json.encode('utf-8')).decode('ascii')
            pytest_command += f" --json_data_b64 {encoded_json}"
        
        # Create list of commands to run
        run_commands = [kit_command, pytest_command]
        
        # Save commands to commands.txt file in test output directory
        try:
            commands_file_path = os.path.join(test_dict['test_path'], 'commands.txt')
            os.makedirs(test_dict['test_path'], exist_ok=True)  # Ensure directory exists
            
            with open(commands_file_path, 'w', encoding='utf-8') as f:
                f.write("DSRS Test Commands\n")
                f.write("==================\n\n")
                f.write(f"Test Name: {test_dict.get('name', 'unnamed')}\n")
                f.write(f"Test Type: {test_dict.get('type', 'unknown')}\n")
                f.write(f"Component: DSRS\n")
                f.write(f"Script Path: {dsrs_scripts_path}\n")
                f.write(f"Scenario: {test_dict['scenario']}\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("1. Kit Application Launch Command:\n")
                f.write("-" * 50 + "\n")
                f.write(f"{kit_command}\n\n")
                
                f.write("2. Pytest Test Execution Command:\n")
                f.write("-" * 50 + "\n")
                f.write(f"{pytest_command}\n\n")
                
                f.write("Command Execution Order:\n")
                f.write("-" * 50 + "\n")
                f.write("1. Launch Kit application (run in background)\n")
                f.write("2. Wait for application to be ready\n")
                f.write("3. Execute pytest command\n")
                
            logger.info(f"Commands saved to: {commands_file_path}")
            
        except Exception as e:
            logger.warning(f"Failed to save commands to file: {str(e)}")
        
        # Log the exact commands that will be executed
        logger.info(f"Generated DSRS commands:")
        logger.info(f"Kit command: {kit_command}")
        logger.info(f"Pytest command: {pytest_command}")
        logger.info(f"Scripts path: {dsrs_scripts_path}")
        
        # Return commands wrapped in a list for consistency with other command generators
        return [run_commands]

    @staticmethod
    def map2sim_command_generator(test_dict) -> List[str]:
        '''This function is used to generate command for map2sim'''
        logger.info(f"Generating MAP2SIM commands for test: {test_dict.get('name', 'unnamed')}")
                    
        varc.control_block['post_processing'] = False
        varc.control_block['pp_directory_check'] = False
        varc.control_block['pp_data_transfer'] = False
        varc.control_block['pp_ffmpeg'] = False
        varc.control_block['pp_videos_merge'] = False

        if "--ui-automator-version" in test_dict['automation_suite_flags_dict']:
            automator_version = test_dict['automation_suite_flags_dict']["--ui-automator-version"]
        else:
            automator_version = AUTOMATOR_VERSION
               
        # Construct the full path to the MAP2SIM application
        app = varc.toml_dict['app']  # "omni.drivesim.map2sim.app"
        build_path = varc.toml_dict['BUILD']['local_build_path']
        app_full_path = os.path.join(build_path, app)
        
        logger.info(f"MAP2SIM application path: {app_full_path}")
        
        # Start building the kit command with the full application path
        kit_command = f'"{app_full_path}"'
        
        # Add required flags in the exact order as provided in the sample
        kit_command += " --allow-root"
        kit_command += " --/app/window/width=1920"
        kit_command += " --/app/window/height=1080"
        kit_command += " --/app/window/fullscreen=true"
        kit_command += " --/app/file/ignoreUnsavedStage=true"
        kit_command += " --/exts/omni.services.transport.server.http/port=9682"
        kit_command += ' --/exts/omni.kit.registry.nucleus/registries/2/name="kit/default"'
        kit_command += ' --/exts/omni.kit.registry.nucleus/registries/2/url="omniverse://kit-extensions.ov.nvidia.com/exts/kit/default"'
        kit_command += " --enable omni.kit.remote_ui_automator"
        
        # Add kit suite flags if they exist
        if 'kit_suite_flags' in test_dict and test_dict['kit_suite_flags']:
            for flags in test_dict['kit_suite_flags']:
                if flags.strip():  # Only add non-empty flags
                    kit_command += " " + flags
                
        # Add kit flags if they exist
        if 'kit_flags' in test_dict and test_dict['kit_flags']:
            for flags in test_dict['kit_flags']:
                if flags.strip():  # Only add non-empty flags
                    kit_command += " " + flags
        
        # Get Python executable with version checking
        try:
            python_exe = CommandGeneratorMethods._get_python_executable()
            logger.info(f"Using Python executable for pytest: {python_exe}")
        except RuntimeError as e:
            logger.error(f"Failed to get suitable Python executable: {e}")
            raise
        
        # Get script path from test dictionary (set during pretest)
        map2sim_scripts_path = test_dict['script_path']
        
        # Store the script path in varc for the runner to use
        varc.test_command_dict["map2sim_scripts_path"] = map2sim_scripts_path
        
        # Get the scenario field and create full path
        scenario_name = test_dict['scenario']
        scenario_full_path = os.path.join(map2sim_scripts_path, scenario_name)
        logger.info(f"Using full scenario path: {scenario_full_path}")
        
        # Use the full path to the scenario file with connection parameters
        # Extract port from kit command (default to 9682 if not found)
        kit_port = "9682"  # Default port used in kit command above
        ip = "127.0.0.1"
        pytest_command = f"{python_exe} -m pytest -s {scenario_full_path} --ip={ip} --port={kit_port} --output_path={test_dict['test_path']}"
        
        ui_automation_flags_dict = {}
        
        # Add automation suite flags
        if 'automation_suite_flags_dict' in test_dict and test_dict['automation_suite_flags_dict']:
            for key, value in test_dict['automation_suite_flags_dict'].items():
                # Filter for Map2Sim specific flags and debug mode
                if key.startswith("--m2s") or key == "--ui_debug_mode":
                    ui_automation_flags_dict[key] = value
                
        # Add automation flags
        if 'automation_flags_dict' in test_dict and test_dict['automation_flags_dict']:
            for key, value in test_dict['automation_flags_dict'].items():
                # Filter for Map2Sim specific flags and debug mode
                if key.startswith("--m2s") or key == "--ui_debug_mode":
                    ui_automation_flags_dict[key] = value

        if ui_automation_flags_dict:
            # Serialize dictionary to JSON and encode as base64 to avoid shell escaping issues
            import base64
            ui_automation_flags_json = json.dumps(ui_automation_flags_dict)
            encoded_json = base64.b64encode(ui_automation_flags_json.encode('utf-8')).decode('ascii')
            pytest_command += f" --json_data_b64 {encoded_json}"
        
        # Create list of commands to run
        run_commands = [kit_command, pytest_command]
        
        # Save commands to commands.txt file in test output directory
        try:
            commands_file_path = os.path.join(test_dict['test_path'], 'commands.txt')
            os.makedirs(test_dict['test_path'], exist_ok=True)  # Ensure directory exists
            
            with open(commands_file_path, 'w', encoding='utf-8') as f:
                f.write("MAP2SIM Test Commands\n")
                f.write("=====================\n\n")
                f.write(f"Test Name: {test_dict.get('name', 'unnamed')}\n")
                f.write(f"Test Type: {test_dict.get('type', 'unknown')}\n")
                f.write(f"Component: MAP2SIM\n")
                f.write(f"Script Path: {map2sim_scripts_path}\n")
                f.write(f"Scenario: {test_dict['scenario']}\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("1. Kit Application Launch Command:\n")
                f.write("-" * 50 + "\n")
                f.write(f"{kit_command}\n\n")
                
                f.write("2. Pytest Test Execution Command:\n")
                f.write("-" * 50 + "\n")
                f.write(f"{pytest_command}\n\n")
                
                f.write("Command Execution Order:\n")
                f.write("-" * 50 + "\n")
                f.write("1. Launch Kit application (run in background)\n")
                f.write("2. Wait for application to be ready\n")
                f.write("3. Execute pytest command\n")
                
            logger.info(f"Commands saved to: {commands_file_path}")
            
        except Exception as e:
            logger.warning(f"Failed to save commands to file: {str(e)}")
        
        # Log the exact commands that will be executed
        logger.info(f"Generated MAP2SIM commands:")
        logger.info(f"Kit command: {kit_command}")
        logger.info(f"Pytest command: {pytest_command}")
        logger.info(f"Scripts path: {map2sim_scripts_path}")
        
        # Return commands wrapped in a list for consistency with other command generators
        return [run_commands]

