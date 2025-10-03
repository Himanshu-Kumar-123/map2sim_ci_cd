# run.py - Clean DMF Framework Entry Point (Windows-only)

# Standard imports
import sys
import os
import argparse
import subprocess
import platform
import logging
from pathlib import Path

# Initialize varc.cwd early - before importing constants that depend on it
# Set up project paths once at entry point
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize varc.cwd before importing constants
from fwk.shared.variables_util import varc
varc.cwd = str(project_root.resolve())

from fwk.shared.constants import MAIN_RUNNER_LOG_LEVEL

try:
    import tomllib # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib

# Basic imports for logging setup - proper logging will be setup in pre_framework_initialization

# Now import local modules (they will use the already-setup logging)
from fwk.fwk_logger.fwk_logging import get_logger
# Other imports moved to methods to avoid import errors before dependency installation

# Setup exception logging to capture unhandled exceptions
def setup_exception_logging(logger):
    """Setup logging for unhandled exceptions"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't log keyboard interrupts
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("Unhandled exception occurred:", exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception

class DMFRunner:
    """Main DMF (Drive SimReady Modular Framework) Runner.
    This class is used to run the DMF framework.
    It is used to parse arguments, check dependencies, setup logging, and setup variables.
    It is also used to run the tests.
    """

    def __init__(self):
        """Initialize DMF Runner with argument parsing and dependency checking"""
        # Do all pre-framework initialization first
        self.pre_framework_initialization()
        
        # Get logger after proper setup
        self.logger = get_logger('MAIN_RUNNER', console_log_level=MAIN_RUNNER_LOG_LEVEL, file_path=varc.framework_logs_path)
        
        # Setup exception logging
        setup_exception_logging(self.logger)
        
        # Load and display version information
        self._display_version_info()
        
        self.logger.info("="*60)
        self.logger.info("DMF Framework Initialized")
        self.logger.info(f"Test suite: {varc.test_suite_name}")
        self.logger.info(f"Framework log file: {varc.framework_logs_path}")
        self.logger.info("="*60)
        
        self._check_platform()
        self._check_dependencies()
        
        self.logger.info("DMF Framework initialized successfully")
        self.logger.info(f"Running component: {varc.component}")
        self.logger.info(f"TOML file: {varc.args.toml}")

    def pre_framework_initialization(self):
        """Handle all early initialization before proper logging setup"""
        # Parse arguments first
        self._parse_arguments()
        
        # Setup variables and directories 
        self._setup_variables()
        
        # Setup proper logging in correct location
        self._setup_early_logging()

    def _parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='DMF Framework - Windows Drive SimReady Modular Framework'
        )
        parser.add_argument(
            'toml',
            type=str,
            help='Name of input testsuite TOML file (should have .toml extension)',
        )
        parser.add_argument(
            '--component',
            type=str,
            choices=['DSRS', 'MAP2SIM'],
            default='DSRS',
            help='Component type to run tests for (DSRS or MAP2SIM)',
        )
        parser.add_argument(
            '--install',
            action='store_true',
            help='Install dependencies (quick if already satisfied)'
        )
        parser.add_argument(
            '--force-install',
            action='store_true',
            help='Force reinstall all dependencies'
        )
        
        varc.args = parser.parse_args()

    def _check_platform(self):
        """Ensure we're running on Windows"""
        if platform.system() != 'Windows':
            print("ERROR: DMF Framework is designed for Windows only.")
            print(f"Current platform: {platform.system()}")
            sys.exit(1)

    def _check_dependencies(self):
        """Check and install dependencies based on flags"""
        component = varc.args.component.upper()
        
        if varc.args.force_install:
            print(f"Force installing dependencies for {component}...")
            self._install_dependencies(component, force=True)
        elif varc.args.install:
            print(f"Installing dependencies for {component}...")
            self._install_dependencies(component, force=False)
        else:
            print("Skipping dependency installation (use --install or --force-install if needed)")

    def _install_dependencies(self, component, force=False):
        """Install main dependencies"""
        # Build pip command with force flag if specified
        pip_args = [sys.executable, "-m", "pip", "install"]
        if force:
            pip_args.extend(["--force-reinstall", "--no-deps"])
            print("Installing essential dependencies (force mode)...")
        else:
            print("Installing essential dependencies...")
        
        # Install essential packages first
        essential_packages = [
            "google-auth", "google-auth-oauthlib", "google-auth-httplib2",
            "google-api-python-client", "msal", "tomli_w", "psutil",
            "strip_ansi", "colorama", "ansimarkup", "tomli", "pynvml"
        ]
        
        try:
            subprocess.check_call(pip_args + essential_packages)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install essential dependencies: {e}")
            sys.exit(1)

        # Install main requirements
        self._install_main_requirements(force)
        
        # Install UI requirements for DSRS and MAP2SIM
        if component in ['DSRS', 'MAP2SIM']:
            self._install_ui_dependencies(force)

    def _install_main_requirements(self, force=False):
        """Install main requirements from requirements.txt"""
        requirements_file = Path.cwd() / "requirements.txt"
        if requirements_file.exists():
            pip_args = [sys.executable, "-m", "pip", "install"]
            if force:
                pip_args.extend(["--force-reinstall", "--no-deps"])
                print("Installing main requirements (force mode)...")
            else:
                print("Installing main requirements...")
            
            pip_args.extend(["-r", str(requirements_file)])
            
            try:
                subprocess.check_call(pip_args)
            except subprocess.CalledProcessError as e:
                print(f"Failed to install main requirements: {e}")
                sys.exit(1)

    def _install_ui_dependencies(self, force=False):
        """Install UI-specific dependencies"""
        ui_requirements_file = Path.cwd() / "ui_requirements.txt"
        if ui_requirements_file.exists():
            pip_args = [sys.executable, "-m", "pip", "install"]
            if force:
                pip_args.extend(["--force-reinstall", "--no-deps"])
                print("Installing UI requirements (force mode)...")
            else:
                print("Installing UI requirements...")
            
            pip_args.extend(["-r", str(ui_requirements_file)])
            
            try:
                subprocess.check_call(pip_args)
            except subprocess.CalledProcessError as e:
                print(f"Failed to install UI requirements: {e}")
                sys.exit(1)

    def _setup_variables(self):
        """Setup framework variables and create base directory structure"""
        # varc.cwd is already set during early initialization
        # Set up remaining paths based on cwd
        varc.toml_path = varc.cwd + '/TOML/' + varc.args.toml
        varc.dmf_config_path = varc.cwd + '/dmf_config.toml'
        varc.component = varc.args.component.upper()
        
        # Load TOML minimally for directory creation
        self._load_toml_for_directories()
        
        # Create base directory with proper naming
        self._create_base_directory()

    def _load_toml_for_directories(self):
        """Load TOML file early to get directory configuration"""
        try:
            with open(varc.toml_path, 'rb') as f:
                toml_data = tomllib.load(f)
            
            # Store the full dict for later use
            varc.toml_dict = toml_data
            
            # Set default automation files dump path if not specified
            automation_suite = toml_data.get('AUTOMATION_SUITE', {})
            if not automation_suite.get('automation_files_dump_path'):
                automation_suite['automation_files_dump_path'] = varc.cwd
                varc.toml_dict['AUTOMATION_SUITE'] = automation_suite
            
        except FileNotFoundError:
            print(f"ERROR: TOML file not found: {varc.toml_path}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Error loading TOML: {e}")
            sys.exit(1)

    def _create_base_directory(self):
        """Create base directory structure with proper TOML-based naming"""
        try:
            import datetime
            
            # Extract directory name from TOML file (same logic as output_directory_creator)
            directory_name = Path(varc.args.toml).stem  # Modern way to get filename without extension
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            varc.test_suite_name = f"{directory_name}_{date_string}"
            
            # Define base path
            base_path = Path(varc.toml_dict['AUTOMATION_SUITE']['automation_files_dump_path']) / 'Outputs' / varc.test_suite_name
            
            # Create the base directory
            base_path.mkdir(parents=True, exist_ok=True)
            varc.test_suite_path = str(base_path)
            
            # Create framework logs directory immediately
            framework_logs_dir = base_path / 'framework_logs'
            framework_logs_dir.mkdir(exist_ok=True)
            
        except Exception as e:
            print(f"ERROR: Failed to create base directory: {e}")
            sys.exit(1)

    def _setup_early_logging(self):
        """Setup proper framework logging in the correct location"""
        try:
            import datetime
            
            # Set framework log file path (base directory already created)
            framework_logs_dir = Path(varc.test_suite_path) / 'framework_logs'
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            varc.framework_logs_path = str(framework_logs_dir / f"dmf_framework_{timestamp}.log")
            
            # Update logger with file path
            from fwk.fwk_logger.fwk_logging import DMFLogger
            DMFLogger.set_framework_log_file(varc.framework_logs_path)
            
        except Exception as e:
            print(f"ERROR: Failed to setup logging: {e}")
            sys.exit(1)

    def _display_version_info(self):
        """Display version information"""
        try:
            import cicd_scripts.version as version
            version_info = version.get_version_info()
            
            print("="*60)
            print("DMF FRAMEWORK VERSION INFORMATION")
            print("="*60)
            print(f"Version: {version_info['version']}")
            
            build_info = version_info['build_info']
            print(f"Build Date: {build_info.get('build_date', 'unknown')}")
            print(f"Commit Hash: {build_info.get('commit_hash', 'unknown')}")
            print(f"Branch: {build_info.get('branch', 'unknown')}")
            
            if build_info.get('mr_number'):
                print(f"MR Number: {build_info['mr_number']}")
            
            if build_info.get('is_release'):
                print("Type: Release Version")
            elif version.is_mr_version():
                print("Type: MR Version (Temporary)")
            elif version.is_dev_version():
                print("Type: Development Version")
            else:
                print("Type: Unknown")
            
            print("="*60)
            
            # Also log to file if logger is available
            if hasattr(self, 'logger'):
                self.logger.info(f"DMF Framework Version: {version_info['version']}")
                self.logger.info(f"Build Info: {build_info}")
                
        except Exception as e:
            print(f"WARNING: Could not load version information: {e}")
            if hasattr(self, 'logger'):
                self.logger.warning(f"Could not load version information: {e}")
        
    def testsuite_pre_steps(self):
        """This function prepares engine for test execution based on component type"""
        self.logger.info(f"Starting pre-steps for {varc.component} component")
        
        try:
            # Import here after dependencies are installed
            from fwk.pretests.dmf_pretest import run_pretest, dmf_config_loader
            from fwk.pretests.header_util import HeaderUtil
            
            # Load ATF configuration first
            dmf_config_loader()
            
            # Run component-agnostic pretest (handles everything including header creation)
            processor = run_pretest()
            
            # Log system summary for reference
            header_summary = HeaderUtil.get_header_summary()
            self.logger.info(f"System Summary: {header_summary}")
            
            self.logger.debug(f"TOML dict: {varc.toml_dict}")
            self.logger.debug(f"Tests list: {varc.tests_list}")
            
            self.logger.info("Pre-steps completed successfully")
            
        except Exception as e:
            self.logger.error(f"Pre-steps failed: {str(e)}")
            raise
      
    def command_runner(self):
        """Entry point that delegates to component-specific runners"""
        self.logger.info(f"Starting command runner for {varc.component} component")
        
        try:
            if varc.component == 'DSRS':
                self._run_dsrs_tests()
            elif varc.component == 'MAP2SIM':
                self._run_map2sim_tests()
            else:
                self.logger.error(f"Unsupported component type: {varc.component}")
                return
                
            self.logger.info("Command runner completed successfully")
            
        except Exception as e:
            self.logger.error(f"Command runner failed: {str(e)}")
            raise

    def _run_dsrs_tests(self):
        """DSRS component - implement queue-based approach"""
        self.logger.info("Running DSRS tests")
        
        # Import DSRS runner from fwk directory
        from fwk.runners.dsrs_runner import DSRSRunner
        dsrs_runner = DSRSRunner()
            
        # Run the tests directly within this if block
        results = dsrs_runner.run_tests(varc.tests_list)
            
        # Process the results directly within this if block
        success_count = sum(1 for r in results if r['status'] == 'COMPLETED')
        failed_count = sum(1 for r in results if r['status'] == 'FAILED')
        skipped_count = sum(1 for r in results if r['status'] == 'SKIPPED')
            
        self.logger.info(f"DSRS Test Summary:")
        self.logger.info(f"  Total tests: {len(results)}")
        self.logger.info(f"  Successful: {success_count}")
        self.logger.info(f"  Failed: {failed_count}")
        self.logger.info(f"  Skipped: {skipped_count}")

    def _run_map2sim_tests(self):
        """MAP2SIM component - implement queue-based approach"""
        self.logger.info("Running MAP2SIM tests")
        
        # Import MAP2SIM runner from fwk directory
        from fwk.runners.map2sim_runner import MAP2SIMRunner
        map2sim_runner = MAP2SIMRunner()
        
        # Run the tests
        results = map2sim_runner.run_tests(varc.tests_list)
        
        # Process the results
        success_count = sum(1 for r in results if r['status'] == 'COMPLETED')
        failed_count = sum(1 for r in results if r['status'] == 'FAILED')
        skipped_count = sum(1 for r in results if r['status'] == 'SKIPPED')
        
        self.logger.info(f"MAP2SIM Test Summary:")
        self.logger.info(f"  Total tests: {len(results)}")
        self.logger.info(f"  Successful: {success_count}")
        self.logger.info(f"  Failed: {failed_count}")
        self.logger.info(f"  Skipped: {skipped_count}")
        
    def testsuite_post_step(self):
        """Post-test cleanup and reporting - simplified single step"""
        self.logger.info(f"Starting post-steps for {varc.component} component")
        
        try:
            # Import here after dependencies are installed
            from generic_utils.reporting_util import ReportingMethods
            
            # Single post step - report generation
            ReportingMethods.txt_report_printer()
            
            self.logger.info("Test suite execution completed")
            
        except Exception as e:
            self.logger.error(f"Post-steps failed: {str(e)}")
            # Don't raise here as we want to continue with cleanup

    def run(self):
        """Main execution flow"""
        self.logger.info("Starting DMF Framework execution")
        
        try:
            # Execute main flow
            self.testsuite_pre_steps()
            self.command_runner()
            self.testsuite_post_step()
            
            self.logger.info("DMF Framework execution completed successfully")
            
        except Exception as e:
            self.logger.error(f"DMF Framework execution failed: {str(e)}", exc_info=True)
            self.logger.error("Check logs for detailed error information")
            sys.exit(1)
        
        finally:
            # Always log completion
            self.logger.info("="*60)
            self.logger.info("DMF Framework Execution Finished")
            self.logger.info("="*60)
            
            # Flush all handlers to ensure logs are written
            for handler in logging.getLogger().handlers:
                handler.flush()


def main():
    """Main entry point"""
    try:
        # Create and run DMF Framework
        dmf_runner = DMFRunner()
        dmf_runner.run()
        
    except KeyboardInterrupt:
        print("\nDMF Framework interrupted by user")
        # Also log to file if logger is available
        try:
            logger = get_logger('MAIN')
            logger.warning("DMF Framework interrupted by user")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        # Also log to file if logger is available
        try:
            logger = get_logger('MAIN')
            logger.critical(f"Fatal error in main(): {str(e)}", exc_info=True)
        except:
            pass
        sys.exit(1)


if __name__ == '__main__':
    main()
