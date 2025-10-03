# 🧙‍♂️ CONFTEST.PY - The Pytest Magic Behind The Scenes, pytest automatically discovers and loads conftest.py files

# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

# Standard imports
import os
import sys
import json
import pytest
import logging
from datetime import datetime
from pathlib import Path

# Configure Python path for framework imports EARLY, before any package imports
# This ensures all test files can import framework modules correctly
current_dir = os.path.dirname(os.path.abspath(__file__))  # simready_test_fwk directory
parent_dir = os.path.dirname(current_dir)  # Repo root directory

# Add both directories to Python path if not already present
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)  # For local package imports under simready_test_fwk
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)   # For top-level absolute imports

# Absolute import (avoid relative imports in conftest context)
from simready_test_fwk.utils.logging_util import get_test_logger

# 3rd party imports  
# Note: UI automator imports are intentionally not imported at module level
# to avoid import errors during CLI-only runs.

def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="127.0.0.1", help="IP address")
    parser.addoption("--port", action="store", default="8080", help="Port number")
    parser.addoption("--output_path", action="store", help="Output path")
    parser.addoption("--json_data", action="store", default=None, help="JSON data for UI automation")
    parser.addoption("--json_data_b64", action="store", default=None, help="Base64 encoded JSON data for UI automation")
    # CLI-only flag (does not affect UI tests if not used)
    parser.addoption("--cli_mode", action="store", default="false", help="Enable CLI mode for headless testing")
    
@pytest.fixture(scope="function", autouse=True)
def configure_logging(request):
    """This function will configure the logging for the test run with a unique folder name"""
    # Skip heavy UI logging setup in CLI mode
    cli_mode_opt = request.config.getoption("--cli_mode", default="false")
    if isinstance(cli_mode_opt, str):
        cli_mode_enabled = cli_mode_opt.lower() == "true"
    else:
        cli_mode_enabled = bool(cli_mode_opt)
    if cli_mode_enabled:
        # Let CLI tests manage their own lightweight logging
        yield
        return
    # Get the current test name
    test_name = request.node.name
    date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    global log_folder
    log_folder = test_name + "_" + date_string 
    source_path = request.config.getoption("--output_path")
    
    # Create unique folders for each test run using log_folder
    os.makedirs(f"{source_path}/pytest_results/{log_folder}/test_logs/", exist_ok=True)
    os.makedirs(f"{source_path}/pytest_results/{log_folder}/images/", exist_ok=True)
    os.makedirs(f"{source_path}/pytest_results/{log_folder}/kit_logs/", exist_ok=True)
    os.makedirs(f"{source_path}/pytest_results/{log_folder}/node_details/", exist_ok=True)
    # Configure the logging format with the test name
    logging.basicConfig(
        level=logging.INFO,
        format=(
            f"%(asctime)s [%(name)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)s] - {test_name} -"
            " %(message)s"
        ),
        handlers=[
            logging.FileHandler(
                f"{source_path}/pytest_results/{log_folder}/test_logs/test_log.log",
                mode="a",
                delay=True,
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )
    # Yield control back to the test
    yield

@pytest.fixture(scope="function", autouse=True)
def import_corrections(request):
    """This function will replace the original BaseModel init function with a patched one that uses the log_folder variable"""
    # Skip UI-specific BaseModel patching in CLI mode
    cli_mode_opt = request.config.getoption("--cli_mode", default="false")
    if isinstance(cli_mode_opt, str):
        cli_mode_enabled = cli_mode_opt.lower() == "true"
    else:
        cli_mode_enabled = bool(cli_mode_opt)
    if cli_mode_enabled:
        return
    output_path = request.config.getoption("--output_path")
    from omniui.omni_models.base_models.base_model import BaseModel
    
    def patched_init(self, omni_driver, wait_timeout=60, polling_frequency=0.5, **kwargs):
        import logging
        from omni_remote_ui_automator.driver.waits import Wait
        from omni_remote_ui_automator.driver.omnidriver import OmniDriver
        
        self.omni_driver: OmniDriver = omni_driver # type: ignore
        
        # Use log_folder for consistent screenshot directory
        global log_folder
        if 'log_folder' in globals() and log_folder:
            self.ss_dir = f"{output_path}/pytest_results/{log_folder}/"
        else:
            # Fallback to generic folder if log_folder not available
            self.ss_dir = f"{output_path}/pytest_results/"
            
        self.log = kwargs.get("logger", None)
        if self.log is None:
            self.log = logging.getLogger()
        self.wait = Wait(wait_timeout, polling_frequency)
        self.glyph_codes = dict()
    # 🎯 THE MAGIC HAPPENS HERE:
    BaseModel.__init__ = patched_init # ← This REPLACES the original __init__ method


@pytest.fixture(autouse=True)
def per_test_logger_setup(request):
    """Attach a per-test file handler if DMF_TEST_LOGS_PATH is provided via env.
    This runs for every test automatically and does not change test behavior.
    """
    import re
    test_logs_path = os.environ.get('DMF_TEST_LOGS_PATH')
    raw_test_name = os.environ.get('DMF_TEST_NAME') or request.node.name
    # Sanitize test name for Windows-safe filenames
    test_name = re.sub(r'[<>:"/\\|?*]+', '_', raw_test_name)

    # Initialize module logger for the test module
    logger = get_test_logger(request.module.__name__, per_test_file=bool(test_logs_path), test_logs_path=test_logs_path)

    # Also attach a file handler at root if desired
    if test_logs_path:
        try:
            Path(test_logs_path).mkdir(parents=True, exist_ok=True)
            file_path = str(Path(test_logs_path) / f"{test_name}.log")
            handler = logging.FileHandler(file_path, encoding='utf-8')
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('\n[DMF_TEST] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root_logger = logging.getLogger()
            root_logger.addHandler(handler)
            # Ensure we don't duplicate handlers excessively across tests
            request.addfinalizer(lambda: root_logger.removeHandler(handler))
        except Exception:
            # Silent fallback - don't break tests due to logging issues
            pass

    return logger


@pytest.fixture(autouse=True)
def cli_autosetup(request):
    """In CLI mode, automatically invoke setup_cli_mode on test instances.
    Has no effect for UI tests (when --cli_mode is false or absent).
    """
    try:
        cli_mode_opt = request.config.getoption("--cli_mode", default="false")
    except Exception:
        return
    if isinstance(cli_mode_opt, str):
        cli_mode_enabled = cli_mode_opt.lower() == "true"
    else:
        cli_mode_enabled = bool(cli_mode_opt)
    if not cli_mode_enabled:
        return
    instance = getattr(request, "instance", None)
    if instance is not None and hasattr(instance, "setup_cli_mode"):
        instance.setup_cli_mode(request)
