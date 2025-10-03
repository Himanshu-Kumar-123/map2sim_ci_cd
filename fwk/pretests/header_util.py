# Standard imports
import os
import datetime
import subprocess
import platform
from typing import Optional, Dict, Any

try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False

try:
    import pygit2
    PYGIT2_AVAILABLE = True
except ImportError:
    PYGIT2_AVAILABLE = False

# Local imports
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger("HEADER_UTIL")

class HeaderUtil:
    """Windows-focused header utility for DMF framework"""
    
    @staticmethod
    def create_header():
        """Main entry point to create header information"""
        logger.info("Creating header information for DMF framework")
        
        # Initialize header dict if not exists
        if not hasattr(varc, 'header_dict'):
            varc.header_dict = {}
        
        # Create header dictionary
        HeaderUtil.create_header_dict()
        
        logger.info("Header information created successfully")

    @staticmethod
    def create_header_dict():
        """
        Creates a comprehensive header dictionary for Windows DMF framework
        containing system details, build info, and component-specific configurations
        """
        logger.info("Building comprehensive header dictionary")
        
        # Initialize header dict
        varc.header_dict = {}
        
        # Get system and GPU information
        system_details = HeaderUtil._get_system_details()
        varc.header_dict['System Details'] = system_details
        
        # Get build information
        build_info = HeaderUtil._get_build_info()
        varc.header_dict['Build'] = build_info
        
        # Get component-specific information
        component_info = HeaderUtil._get_component_info()
        varc.header_dict.update(component_info)
        
        # Add common framework information
        HeaderUtil._add_framework_info()
        
        logger.debug(f"Header dictionary created with {len(varc.header_dict)} sections")

    @staticmethod
    def _get_system_details() -> Optional[Dict[str, Any]]:
        """Get Windows system and GPU details"""
        logger.debug("Collecting Windows system details")
        
        try:
            if not PYNVML_AVAILABLE:
                logger.warning("pynvml not available, skipping GPU info")
                return {
                    'OS': platform.system(),
                    'OS Version': platform.version(),
                    'Architecture': platform.architecture()[0],
                    'GPU Info': 'pynvml not available'
                }
            
            # Initialize NVIDIA ML
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            
            # Get GPU information from the primary device (last device for constellation)
            handle = pynvml.nvmlDeviceGetHandleByIndex(device_count - 1)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            driver_version = pynvml.nvmlSystemGetDriverVersion()
            
            # Adjust device count for constellation setup
            adjusted_device_count = 8 if device_count == 10 else device_count
            
            # Get platform info from configuration
            platform_info = None
            if hasattr(varc, 'platform_name_dict'):
                platform_info = varc.platform_name_dict.get(gpu_name, gpu_name)
            
            # Get CUDA version using nvidia-smi (Windows-safe approach)
            cuda_version = HeaderUtil._get_cuda_version()
            
            system_details = {
                'OS': platform.system(),
                'OS Version': platform.version(),
                'Architecture': platform.architecture()[0],
                'Processor': platform.processor(),
                'GPU Count': adjusted_device_count,
                'GPU Name': gpu_name,
                'Driver Version': driver_version,
                'CUDA Version': cuda_version,
                'Platform': platform_info
            }
            
            logger.debug(f"System details collected: {gpu_name}, Driver: {driver_version}")
            return system_details
            
        except Exception as e:
            logger.exception(f"Error collecting system details: {e}")
            return {
                'OS': platform.system(),
                'Error': str(e),
                'Fallback Info': 'System details collection failed'
            }

    @staticmethod
    def _get_cuda_version() -> str:
        """Get CUDA version using nvidia-smi (Windows-safe)"""
        try:
            # Use Windows-safe subprocess approach
            process = subprocess.Popen(
                ["nvidia-smi"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=False,  # More secure
                text=True
            )
            
            for line in process.stdout:
                line = line.strip()
                if 'CUDA Version' in line:
                    cuda_version = line.split('CUDA Version: ')[1].split()[0]
                    logger.debug(f"Detected CUDA Version: {cuda_version}")
                    return cuda_version
            
            return "Not detected"
            
        except Exception as e:
            logger.warning(f"Could not detect CUDA version: {e}")
            return "Unknown"

    @staticmethod
    def _get_build_info() -> str:
        """Get build information based on component and configuration"""
        logger.debug("Collecting build information")
        
        try:
            # For DMF framework, we typically use local builds rather than Docker
            if 'BUILD' in varc.toml_dict and 'name' in varc.toml_dict['BUILD']:
                build_name = varc.toml_dict['BUILD']['name']
                logger.debug(f"Using build name from TOML: {build_name}")
                return build_name
            
            # Fallback: try to get git information if available
            if PYGIT2_AVAILABLE:
                git_info = HeaderUtil._get_git_info()
                if git_info:
                    return git_info
            
            # Final fallback
            return "Unknown Build"
            
        except Exception as e:
            logger.warning(f"Error getting build info: {e}")
            return "Build Info Error"

    @staticmethod
    def _get_git_info() -> Optional[str]:
        """Get git branch and commit information"""
        try:
            repo = pygit2.Repository(".")
            
            # Try to get branch from environment variables (CI/CD)
            branch = (os.environ.get("CI_COMMIT_BRANCH") or 
                     os.environ.get("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"))
            
            if not branch:
                # Fallback to current branch
                branch = repo.head.shorthand if not repo.head_is_unborn else "main"
            
            # Get commit ID
            commit_id = str(repo.revparse_single("HEAD").id)[:8]  # Short commit ID
            
            git_info = f"{branch}_{commit_id}"
            logger.debug(f"Git info: {git_info}")
            return git_info
            
        except Exception as e:
            logger.debug(f"Could not get git info: {e}")
            return None

    @staticmethod
    def _get_component_info() -> Dict[str, Any]:
        """Get component-specific information"""
        component = getattr(varc, 'component', 'Unknown')
        logger.debug(f"Collecting info for component: {component}")
        
        component_info = {
            'Component': component,
            'Framework': 'DMF (DriveSim Management Framework)'
        }
        
        # Component-specific details
        if component == 'DSRS':
            component_info.update({
                'Component Type': 'DSRS (DriveSim Ready Studio)',
                'Server Type': 'S3 Bucket',
                'S3 Bucket': varc.toml_dict.get('SERVER', {}).get('s3_bucket', 'Not specified')
            })
            
        elif component == 'MAP2SIM':
            component_info.update({
                'Component Type': 'MAP2SIM (Map to Simulation)',
                'Pipeline': 'Asset Mapping and Validation',
                'Content Path': varc.toml_dict.get('BUILD', {}).get('local_content_path', 'Not specified')
            })
        
        return component_info

    @staticmethod
    def _add_framework_info():
        """Add common framework information"""
        logger.debug("Adding framework information")
        
        # Test suite information
        varc.header_dict.update({
            'Testsuite Name': getattr(varc, 'test_suite_name', 'Not set'),
            'Log Directory': getattr(varc, 'test_suite_path', 'Not set'),
            'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Framework Version': 'DMF v1.0',
            'Python Version': platform.python_version()
        })
        
        # Add test count if available
        if hasattr(varc, 'tests_list'):
            varc.header_dict['Total Tests'] = len(varc.tests_list)
        
        # Add TOML file information
        if hasattr(varc, 'args') and hasattr(varc.args, 'toml'):
            varc.header_dict['TOML File'] = varc.args.toml

    @staticmethod
    def get_header_summary() -> Dict[str, Any]:
        """Get a summary of header information for logging"""
        if not hasattr(varc, 'header_dict'):
            return {'Status': 'Header not created'}
        
        summary = {
            'System': varc.header_dict.get('System Details', {}).get('OS', 'Unknown'),
            'GPU': varc.header_dict.get('System Details', {}).get('GPU Name', 'Unknown'),
            'Component': varc.header_dict.get('Component', 'Unknown'),
            'Build': varc.header_dict.get('Build', 'Unknown'),
            'Test Suite': varc.header_dict.get('Testsuite Name', 'Unknown')
        }
        
        return summary

    @staticmethod
    def validate_system_requirements() -> bool:
        """Validate that system meets DMF requirements"""
        logger.info("Validating system requirements")
        
        issues = []
        
        # Check Windows
        if platform.system() != 'Windows':
            issues.append(f"DMF requires Windows, detected: {platform.system()}")
        
        # Check GPU availability
        if not PYNVML_AVAILABLE:
            issues.append("pynvml not available - GPU monitoring limited")
        else:
            try:
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count == 0:
                    issues.append("No NVIDIA GPUs detected")
            except Exception as e:
                issues.append(f"GPU check failed: {e}")
        
        # Check Python version
        python_version = platform.python_version()
        major, minor = python_version.split('.')[:2]
        if int(major) < 3 or (int(major) == 3 and int(minor) < 8):
            issues.append(f"Python 3.8+ required, detected: {python_version}")
        
        if issues:
            logger.warning("System requirement issues found:")
            for issue in issues:
                logger.warning(f"  - {issue}")
            return False
        else:
            logger.info("System requirements validation passed")
            return True