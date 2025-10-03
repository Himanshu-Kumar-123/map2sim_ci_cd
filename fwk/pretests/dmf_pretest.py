"""DMF framework pretest processing"""

# Standard imports
import os
import sys
import copy
from pathlib import Path
from collections import deque
from typing import Dict, List, Any, Optional
try:
    import tomllib # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib

# Local imports
from fwk.shared.variables_util import varc
from generic_utils.directory_helper_util import DirectoryCreatorMethods
from generic_utils.reporting_util import ReportingMethods
from fwk.fwk_logger.fwk_logging import get_logger
from fwk.pretests.header_util import HeaderUtil

logger = get_logger('DMF_PRETEST')


def dmf_config_loader():
    """This function is used to load all configuration settings from dmf_config.toml into varc variables"""

    with open(varc.dmf_config_path, 'rb') as f:
        config = tomllib.load(f)
    
    varc.control_block=config['settings']['control_block']
    varc.check_words=config['logs']['check_words']
    varc.p0_functional_list=config['logs']['p0_functional_list']
    varc.p0_functional_iter_list=config['logs']['p0_functional_iter_list']
    varc.p0_platform_list=config['logs']['p0_platform_list']
    varc.p1_list=config['logs']['p1_list']
    varc.p1_ignore_issue_list=config['logs']['p1_ignore_issue_list']
    varc.pytest_p0_functional_list=config['logs']['pytest_p0_functional_list']
    varc.pytest_p1_list=config['logs']['pytest_p1_list']
    varc.platform_name_dict = config['platform_name_dict']
    varc.verdict_decider_list = config['settings']['verdict_decider_list']
    # Optional sections
    varc.overwrite_log_level = config.get('settings', {}).get('overwrite_log_level', None)


class DMFPreTestRunner:
    """
    Modern DMF PreTest Runner for DSRS and MAP2SIM components
    Handles TOML loading, validation, and pretest preparation
    
    Supports standardized TOML format:
    [COMPONENT]  # e.g., [MAP2SIM] or [DSRS]
        [TEST_TYPE.test_name]  # e.g., [ASSET_MAPPING.test_asset_mapping_table]
        script_path = "ui_tests\\path"
        scenario = "test_file.py"
        automation_flags = ["--flag1", "--flag2"]
        kit_flags = [""]
    """
    
    # Supported test types for DMF framework
    SUPPORTED_TEST_TYPES = {
        'DSRS': ['DSRS_PROPS', 'DSRS_VEHICLES', 'DSRS_CYCLIST', 'DSRS_CHARACTERS', 'DSRS_SCENES'],
        'MAP2SIM': ['MAP_PREPROCESSING', 'ASSET_MAPPING', 'NONMAP_CONTENT_CREATION', 'SCENES_VALIDATION', "E2E_TESTING", 
                    "BATCH_CONTENT_GENERATION", "IMPORT_IMAGEFILE_BILLBOARD", "AUTO_GENERATE_INTERSECTION", "PRESET_VALIDATION", 
                    "CREATE_SCENE", "TEST_FRAMEWORK", "PRESET_CREATION", "INTERSECTION_VALIDATION", "ASSET_REMAPPING", "BUILD_MAPPING_TABLE", 
                    "CREATE_CUTOUTS_GT", "CREATE_EXTENDED_PAYLOADS", "DOWNLOAD_SUPPLIMENTAL_DATA", "DSSR", "CUSTOM_SIGN", "DEM_DOWNLOAD", 
                    "OMNIMAP_CONVERSION", "SCENE_API", "INTERSECTION_TEST", "CLI_TEST"]
    }
    
    # Required fields for each component
    COMPONENT_REQUIRED_FIELDS = {
        'DSRS': ['scenario', 'script_path'],
        'MAP2SIM': ['scenario', 'script_path']  # Can be extended later
    }
    
    # Flag types that need to be parsed into dictionaries
    FLAG_TYPES = [
        'automation_flags',
        'automation_suite_flags',
        'kit_flags',
        'kit_suite_flags',
        'post_processing_flags'
    ]

    def __init__(self):
        """Initialize the DMF pretest runner"""
        logger.info(f"Initializing DMF PreTest Runner for component: {varc.component}")
        
        # Initialize variables
        varc.tests_list = []
        varc.toml_dict = {}
        
        # Process TOML
        self.load_toml()
        self.validate_toml_structure()
        self.create_test_instances()
        self.update_flags_dictionaries()
        self.create_tests_deque()
        
        # Create directories and reports
        self.setup_directories_and_reports()
        
        logger.info(f"DMF PreTest Runner initialized successfully with {len(varc.tests_list)} tests")

    def load_toml(self):
        """Load and parse TOML file"""
        logger.info(f"Loading TOML file: {varc.toml_path}")
        
        try:
            with open(varc.toml_path, 'rb') as f:
                varc.toml_dict = tomllib.load(f)
            logger.debug("TOML file loaded successfully")
            logger.debug(f"TOML top-level sections: {list(varc.toml_dict.keys())}")
            
        except FileNotFoundError:
            logger.exception(f"TOML file not found: {varc.toml_path}")
            sys.exit(1)
        except tomllib.TomlDecodeError as e:
            logger.exception(f"TOML decoding error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.exception(f"Unexpected error loading TOML: {e}")
            sys.exit(1)

    def validate_toml_structure(self):
        """Validate TOML structure and required sections"""
        logger.info("Validating TOML structure")
        
        # Check required top-level sections
        required_sections = ['BUILD', 'AUTOMATION_SUITE', 'SERVER', 'ENVIRONMENT']
        missing_sections = [section for section in required_sections 
                          if section not in varc.toml_dict]
        
        if missing_sections:
            logger.error(f"Missing required TOML sections: {missing_sections}")
            sys.exit(1)
        
        # Validate server credentials
        server_section = varc.toml_dict.get('SERVER', {})
        required_server_fields = ['s3_bucket', 'username', 'password']
        
        missing_server_fields = [field for field in required_server_fields 
                               if not server_section.get(field)]
        
        if missing_server_fields:
            logger.error(f"Missing or empty server fields: {missing_server_fields}")
            sys.exit(1)
        
        # Set default automation files dump path if not specified
        automation_suite = varc.toml_dict.get('AUTOMATION_SUITE', {})
        if not automation_suite.get('automation_files_dump_path'):
            automation_suite['automation_files_dump_path'] = varc.cwd
            logger.info(f"Set default automation_files_dump_path: {varc.cwd}")
        
        logger.debug("TOML structure validation completed")

    def _process_test_sections(self, supported_test_types: List[str], test_sections: Dict[str, Dict[str, Any]], common_config: Dict[str, Any]):
        """Process test sections grouped by test type"""
        # Process each test type group
        for test_type, tests in test_sections.items():
            if test_type in supported_test_types:
                logger.info(f"Processing test type: {test_type}")
                for test_name, test_config in tests.items():
                    logger.debug(f"Processing test: {test_name}")
                    
                    # Create test instance
                    test_instance = {
                        'name': test_name,
                        'updated_name': test_name,
                        'type': test_type,
                        **copy.deepcopy(common_config),
                        **copy.deepcopy(test_config)
                    }
                    
                    # Validate required fields
                    if self._validate_test_instance(test_instance):
                        varc.tests_list.append(test_instance)
                        logger.debug(f"Added test: {test_name}")
                    else:
                        logger.warning(f"Skipped invalid test: {test_name}")
            else:
                logger.warning(f"Found unsupported test type '{test_type}' (will be ignored)")

    def _check_for_unsupported_test_types(self, supported_test_types: List[str], test_sections: Dict[str, Dict[str, Any]]):
        """Check for unsupported test types and warn user"""
        unsupported_types = []
        
        for test_type in test_sections.keys():
            if test_type not in supported_test_types:
                unsupported_types.append(test_type)
        
        if unsupported_types:
            logger.warning(f"Found unsupported test types (will be ignored): {unsupported_types}")
            logger.warning(f"Supported test types for component '{varc.component}': {supported_test_types}")
            logger.warning("Please use only supported test types for proper test execution")

    def create_test_instances(self):
        """Create test instances based on component type"""
        logger.info(f"Creating test instances for component: {varc.component}")
        
        # Get component-specific test types
        test_types = self.SUPPORTED_TEST_TYPES.get(varc.component, [])
        if not test_types:
            logger.error(f"No supported test types for component: {varc.component}")
            sys.exit(1)
        
        # Create common configuration template
        common_config = self._create_common_config()
        
        # Process tests from standardized format: [COMPONENT] then [TEST_TYPE.test_name] sections
        logger.info(f"Processing tests for component: {varc.component}")
        
        # Find all test sections - these are top-level sections that are test types
        test_sections = {}
        logger.debug(f"All TOML sections found: {list(varc.toml_dict.keys())}")
        
        for section_name, section_content in varc.toml_dict.items():
            logger.debug(f"Processing section: {section_name}, content type: {type(section_content)}")
            
            # Skip configuration sections and non-dict sections
            if section_name in {'BUILD', 'AUTOMATION_SUITE', 'SERVER', 'ENVIRONMENT', varc.component, 'app'}:
                logger.debug(f"Skipping config section: {section_name}")
                continue
            
            # Check if this is a test type section (should be a dict with test configurations)
            if isinstance(section_content, dict) and section_content:
                logger.debug(f"Found potential test type section: {section_name}")
                test_sections[section_name] = section_content
            else:
                logger.debug(f"Section '{section_name}' is not a valid test type section")
        
        logger.debug(f"Final test_sections found: {test_sections}")
        
        if not test_sections:
            logger.error("No test configurations found in TOML file")
            logger.error("Please add test configurations using the format:")
            logger.error(f"[{varc.component}]")
            logger.error("    [TEST_TYPE.test_name]")
            logger.error("    script_path = \"ui_tests\\\\path\"")
            logger.error("    scenario = \"test_file.py\"")
            logger.error("    automation_flags = [\"--flag1\", \"--flag2\"]")
            logger.error("    kit_flags = [\"\"]")
            sys.exit(1)
        
        logger.info(f"Found test sections for test types: {list(test_sections.keys())}")
        self._process_test_sections(test_types, test_sections, common_config)
        
        # Check for any unsupported test types and warn user
        self._check_for_unsupported_test_types(test_types, test_sections)
        
        if not varc.tests_list:
            logger.error("No valid tests found in TOML file")
            logger.error(f"Supported test types for component '{varc.component}': {test_types}")
            logger.error("Please add test configurations using the standardized format:")
            logger.error(f"[{varc.component}]")
            logger.error("    [TEST_TYPE.test_name]")
            logger.error("    script_path = \"ui_tests\\\\path\"")
            logger.error("    scenario = \"test_file.py\"")
            logger.error("    automation_flags = [\"--flag1\", \"--flag2\"]")
            logger.error("    kit_flags = [\"\"]")
            sys.exit(1)
        else:
            logger.info(f"Created {len(varc.tests_list)} test instances")

    def _create_common_config(self) -> Dict[str, Any]:
        """Create common configuration applied to all tests"""
        return {
            # Server details
            's3_bucket': varc.toml_dict['SERVER']['s3_bucket'],
            'username': varc.toml_dict['SERVER']['username'], 
            'password': varc.toml_dict['SERVER']['password'],
            
            # Environment
            'python_exe': varc.toml_dict.get('ENVIRONMENT', {}).get('PYTHONEXE', sys.executable),
            
            # Suite-level flags
            'automation_suite_flags': varc.toml_dict['AUTOMATION_SUITE'].get('automation_suite_flags', []),
            'kit_suite_flags': varc.toml_dict['AUTOMATION_SUITE'].get('kit_suite_flags', []),
            
            # Build information
            'build_name': varc.toml_dict['BUILD'].get('name', ''),
            'local_build_path': varc.toml_dict['BUILD'].get('local_build_path', ''),
            'local_content_path': varc.toml_dict['BUILD'].get('local_content_path', ''),
            # Common build-related files
            'project_config_file': varc.toml_dict['BUILD'].get('project_config_file', ''),
            # Suite-level default batch file for CLI tests (can be overridden per test)
            'batch_file_path': varc.toml_dict['BUILD'].get('batch_file_path', ''),
            # Suite-level default batch args for CLI tests
            'batch_args': varc.toml_dict['BUILD'].get('batch_args', []),
            
            # Test tracking and results
            'verdicts': {
                'final-verdict': None,
                'logs-errors': None,
                'process-specific-errors': None,
                'execution-time': None
            },
            
            'detailed_analysis': {
                'logs': None,
                'kit_logs': None,
                'pytest_logs': None
            },
            
            'metrics': {
                'start_time': None,
                'end_time': None,
                'duration': None
            },
            
            # Component tracking
            'component': varc.component,
            
            # Initialize empty test-level flags (will be populated from test-specific config)
            'kit_flags': [],
            
            # Suite-level file updaters (if present)
            'files_updater_suite_level': varc.toml_dict['AUTOMATION_SUITE'].get('files_updater_suite_level', {}),
            
            # Upload storage tracking (SharePoint integration)
            'upload_storage': {
                'share_point': {'test_artifacts_id': None}
            },
            
            # Timing information
            
            
            # Framework warnings and subtest tracking
            'dmf_warnings': [],
            'subtest_dict': {}
        }

    def _process_test_type(self, test_type: str, common_config: Dict[str, Any]):
        """Process all tests of a specific type"""
        test_section = varc.toml_dict[test_type]
        
        for test_name, test_config in test_section.items():
            logger.debug(f"Processing test: {test_name}")
            
            # Create test instance
            test_instance = {
                'name': test_name,
                'updated_name': test_name,  # Can be modified during execution
                'type': test_type,
                **copy.deepcopy(common_config),  # Deep copy to avoid reference issues
                **copy.deepcopy(test_config)     # Test-specific configuration
            }
            
            # Validate required fields
            if self._validate_test_instance(test_instance):
                varc.tests_list.append(test_instance)
                logger.debug(f"Added test: {test_name}")
            else:
                logger.warning(f"Skipped invalid test: {test_name}")

    def _validate_test_instance(self, test_instance: Dict[str, Any]) -> bool:
        """Validate individual test instance"""
        test_name = test_instance['name']
        component = test_instance['component']
        
        # Get required fields for this component
        required_fields = self.COMPONENT_REQUIRED_FIELDS.get(component, [])
        
        # Check if all required fields are present and non-empty
        missing_fields = []
        for field in required_fields:
            if field not in test_instance or not test_instance[field]:
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Missing required fields: {missing_fields}"
            logger.error(f"Test {test_name}: {error_msg}")
            
            # Set failure verdict
            test_instance['verdicts']['final-verdict'] = 'FAIL'
            test_instance['verdicts']['process-specific-errors'] = error_msg
            return False
        
        return True

    def update_flags_dictionaries(self):
        """Parse flags into dictionaries for easier access"""
        logger.info("Updating flags dictionaries for all tests")
        
        for test in varc.tests_list:
            test_name = test['name']
            logger.debug(f"Processing flags for test: {test_name}")
            
            for flag_type in self.FLAG_TYPES:
                if flag_type in test and test[flag_type]:
                    dict_key = f'{flag_type}_dict'
                    test[dict_key] = {}
                    
                    for flag in test[flag_type]:
                        if not flag.strip():  # Skip empty flags
                            continue
                            
                        # Split flag into key-value pair
                        parts = flag.split(' ', 1)  # Split only on first space
                        key = parts[0]
                        value = parts[1] if len(parts) > 1 else None
                        test[dict_key][key] = value
                    
                    logger.debug(f"Processed {len(test[dict_key])} flags for {flag_type}")

    def create_tests_deque(self):
        """Convert tests list to deque for efficient queue operations"""
        logger.info("Creating tests deque for queue-based execution")
        varc.tests_deque = deque(varc.tests_list)
        logger.debug(f"Tests deque created with {len(varc.tests_deque)} tests")

    def setup_directories_and_reports(self):
        """Setup directories and initialize reporting"""
        logger.info("Setting up directories and reports")
        
        try:
            # Create directory structure
            DirectoryCreatorMethods.directory_creator()
            
            # Framework logging already set up in main_runner.py, no need to update again
            
            # Create header information
            HeaderUtil.create_header()
            
            # Validate system requirements
            HeaderUtil.validate_system_requirements()
            
            # Create report.txt, atfp_report.txt & report.json
            ReportingMethods.report_creator()
            
            logger.info("Setup completed successfully")
            
        except Exception as e:
            logger.exception(f"Setup failed: {e}")
            raise

    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of processed tests"""
        summary = {
            'total_tests': len(varc.tests_list),
            'component': varc.component,
            'test_types': list(set(test['type'] for test in varc.tests_list)),
            'test_suite_name': getattr(varc, 'test_suite_name', 'Not set'),
            'test_suite_path': getattr(varc, 'test_suite_path', 'Not set')
        }
        
        # Count tests by type
        type_counts = {}
        for test in varc.tests_list:
            test_type = test['type']
            type_counts[test_type] = type_counts.get(test_type, 0) + 1
        
        summary['tests_by_type'] = type_counts
        return summary


# Convenience functions for different components
def run_dsrs_pretest():
    """Run DSRS-specific pretest processing"""
    logger.info("Starting DSRS pretest processing")
    processor = DMFPreTestRunner()
    
    summary = processor.get_test_summary()
    logger.info(f"DSRS pretest completed: {summary}")
    
    return processor

def run_map2sim_pretest():
    """Run MAP2SIM-specific pretest processing"""
    logger.info("Starting MAP2SIM pretest processing")
    processor = DMFPreTestRunner()
    
    summary = processor.get_test_summary()
    logger.info(f"MAP2SIM pretest completed: {summary}")
    
    return processor

def run_pretest():
    """Run component-appropriate pretest processing"""
    logger.info(f"Starting pretest processing for component: {varc.component}")
    
    if varc.component == 'DSRS':
        return run_dsrs_pretest()
    elif varc.component == 'MAP2SIM':
        return run_map2sim_pretest()
    else:
        logger.error(f"Unsupported component: {varc.component}")
        sys.exit(1)