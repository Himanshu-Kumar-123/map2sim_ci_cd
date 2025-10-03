# Standard imports
import datetime
import os
import sys
from pathlib import Path
# Local imports
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger

# Initialize logger - will get file logging when varc.framework_logs_path is available
logger = get_logger('DIRECTORY_HELPER')

class DirectoryCreatorMethods():
    """The method of this class is used to build output directory"""
    
    @staticmethod 
    def output_directory_creator():
        """This function is used to create main output directory structure"""
        
        # Use the already-created base path from pre_framework_initialization
        # If not created yet, fall back to creating it (for backward compatibility)
        if hasattr(varc, 'test_suite_path') and varc.test_suite_path:
            base_path = Path(varc.test_suite_path)
            logger.debug(f"Using existing base path: {base_path}")
        else:
            # Fallback: create the base path (backward compatibility)
            logger.warning("Base path not found, creating it now (this should not happen normally)")
            directory_name = Path(varc.args.toml).stem
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            varc.test_suite_name = f"{directory_name}_{date_string}"
            base_path = Path(varc.toml_dict['AUTOMATION_SUITE']['automation_files_dump_path']) / 'Outputs' / varc.test_suite_name
            base_path.mkdir(parents=True, exist_ok=True)
            varc.test_suite_path = str(base_path)
        
        try:
            
            # Define directory structure (test_suite_path already set in pre_framework_initialization)
            directory_structure = {
                'test_dump_path': base_path / 'isolated_dump',
                'test_temp_files_path': base_path / 'temp_files'
            }

            # Define isolated dump subdirectories
            isolated_dump_structure = {
                'test_freeze_issue_logs_path': base_path / 'isolated_dump' / 'freeze_issue_logs',
                'test_p0_platform_path': base_path / 'isolated_dump' / 'p0_platform_issue_logs',
                'test_p0_functional_iter_path': base_path / 'isolated_dump' / 'p0_functional_iter_issue_logs',
                'test_ui_data_path': base_path / 'isolated_dump' / 'ui_data'
            }

            # Component-specific directories
            component_specific = {}
            if varc.component == 'DSRS':
                component_specific.update({
                    'dsrs_metadata_path': base_path / 'dsrs_metadata',
                })
            elif varc.component == 'MAP2SIM':
                component_specific.update({
                    'map2sim_metadata_path': base_path / 'map2sim_metadata',
                })

            # Combine all directory structures
            all_directories = {**directory_structure, **isolated_dump_structure, **component_specific}

            # Create directories and update varc
            for key, path in all_directories.items():
                path.mkdir(parents=True, exist_ok=True)
                setattr(varc, key, str(path))  # Convert Path to string for compatibility
                
            logger.info(f"Created output directory structure: {varc.test_suite_path}")
            logger.debug(f"Created {len(all_directories)} directories for {varc.component} component")
                
        except Exception as e:
            logger.exception(f"Failed to create output directory structure: {e}")
            sys.exit(1)

    @staticmethod
    def directory_creator_for_iterative_tests(test_dict):
        """
        Creates structured output directory hierarchy for iterative tests.
        
        Args:
            test_dict: Dictionary containing test information and will be updated with paths
        """
        try:
            # Define directory structure relative to test path
            test_name = test_dict['name']
            base_path = Path(varc.test_suite_path) / test_name
            
            # Base directories for all tests
            directory_structure = {
                'test_path': base_path,
                'test_logs_path': base_path / 'logs',
                'test_videos_path': base_path / 'videos',
                'test_raw_data_path': base_path / 'raw_data',
                'test_perf_data_path': base_path / 'perf_data',
            }

            # Component-specific directories
            component_directories = {}
            
            if varc.component == 'DSRS':
                # DSRS-specific directories
                component_directories.update({
                    'test_pp_data_path': base_path / 'pp_data',
                    'test_raw_videos_path': base_path / 'videos' / 'raw_data_videos',
                    'test_pp_videos_path': base_path / 'videos' / 'pp_data_videos',
                    'test_dsrs_output_path': base_path / 'dsrs_output'
                })
                
                # Type-specific directories for DSRS
                test_type = test_dict.get('type', '')
                if test_type == 'DSRS_CHARACTERS':
                    component_directories['test_character_metrics_path'] = base_path / 'character_metrics'
                elif test_type == 'DSRS_VEHICLES':
                    component_directories['test_vehicle_metrics_path'] = base_path / 'vehicle_metrics'
                elif test_type == 'DSRS_PROPS':
                    component_directories['test_props_metrics_path'] = base_path / 'props_metrics'
                elif test_type == 'DSRS_SCENES':
                    component_directories['test_scenes_metrics_path'] = base_path / 'scenes_metrics'
                    
            elif varc.component == 'MAP2SIM':
                # MAP2SIM-specific directories
                component_directories.update({
                    'test_map2sim_output_path': base_path / 'map2sim_output',
                    'test_mapping_data_path': base_path / 'mapping_data',
                    'test_validation_results_path': base_path / 'validation_results'
                })

            # Combine all directory structures
            all_directories = {**directory_structure, **component_directories}

            # Create directories and update test_dict
            for key, path in all_directories.items():
                path.mkdir(parents=True, exist_ok=True)
                test_dict[key] = str(path)  # Convert Path to string for compatibility

            logger.debug(f"Created directory structure for test: {test_name} ({test_dict.get('type', 'unknown type')})")

        except Exception as e:
            logger.exception(f"Failed to create directory structure for test {test_dict.get('name', 'unknown')}: {e}")
            raise

    @staticmethod
    def directory_creator():
        """
        Creates complete directory structure for test suite
        This method combines output_directory_creator and directory_creator_for_iterative_tests
        """
        logger.info("Creating complete directory structure for test suite")
        
        # Create main output directories
        DirectoryCreatorMethods.output_directory_creator()
        
        # Create directories for each test
        if hasattr(varc, 'tests_list') and varc.tests_list:
            for test_dict in varc.tests_list:
                DirectoryCreatorMethods.directory_creator_for_iterative_tests(test_dict)
            
            logger.info(f"Successfully created directory structure for {len(varc.tests_list)} tests")
        else:
            logger.warning("No tests found in varc.tests_list - only main directories created")

    @staticmethod
    def update_framework_log_file_path():
        """
        Update the logger with framework log file path once directories are created
        This should be called after output_directory_creator()
        Note: This is now only used as a fallback - main_runner.py handles framework logging setup
        """
        # Check if framework logging is already set up
        if hasattr(varc, 'framework_logs_path') and varc.framework_logs_path:
            logger.debug(f"Framework logging already configured: {varc.framework_logs_path}")
            return
            
        if hasattr(varc, 'test_suite_path'):
            # Create framework logs directory
            framework_logs_dir = Path(varc.test_suite_path) / 'framework_logs'
            framework_logs_dir.mkdir(exist_ok=True)
            
            # Set framework log file path
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            varc.framework_logs_path = str(framework_logs_dir / f"dmf_framework_{timestamp}.log")
            
            # Update logger with file path
            from fwk.fwk_logger.fwk_logging import DMFLogger
            DMFLogger.set_framework_log_file(varc.framework_logs_path)
            
            logger.info(f"Framework logging updated with file: {varc.framework_logs_path}")
        else:
            logger.warning("Cannot update framework log file - test_suite_path not set")

    @staticmethod
    def get_directory_summary():
        """
        Get a summary of created directories for logging/debugging
        
        Returns:
            dict: Summary of created directories
        """
        summary = {
            'test_suite_name': getattr(varc, 'test_suite_name', 'Not set'),
            'test_suite_path': getattr(varc, 'test_suite_path', 'Not set'),
            'component': getattr(varc, 'component', 'Not set'),
            'framework_logs_path': getattr(varc, 'framework_logs_path', 'Not set'),
            'tests_count': len(getattr(varc, 'tests_list', []))
        }
        
        return summary
