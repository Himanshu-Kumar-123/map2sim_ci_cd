# -*- coding: utf-8 -*-
# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""
File Assertion Utilities

This module provides utility functions for file existence and validation assertions
in test cases.
"""

import os
import logging
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def assert_file_exists(file_path: str, description: str = "Required file") -> None:
    """
    Assert that a file exists, failing the test if it doesn't.
    
    Args:
        file_path (str): Path to the file to check
        description (str): Description of the file for error message
        
    Raises:
        AssertionError: If the file does not exist
        
    Example:
        >>> assert_file_exists("/path/to/file.usda", "Main scenario file")
    """
    if not os.path.exists(file_path):
        error_msg = f"{description} does not exist: {file_path}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    
    logger.info(f"{description} exists: {file_path}")


def assert_files_exist(file_paths: List[str], description: str = "Required files") -> None:
    """
    Assert that multiple files exist, failing the test if any don't exist.
    
    Args:
        file_paths (List[str]): List of file paths to check
        description (str): Description of the files for error message
        
    Raises:
        AssertionError: If any file does not exist
        
    Example:
        >>> assert_files_exist(["/path/file1.usda", "/path/file2.usda"], "Scene files")
    """
    missing_files = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        error_msg = f"{description} do not exist: {', '.join(missing_files)}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    
    logger.info(f"All {description.lower()} exist: {len(file_paths)} files verified")


def assert_directory_exists(dir_path: str, description: str = "Required directory") -> None:
    """
    Assert that a directory exists, failing the test if it doesn't.
    
    Args:
        dir_path (str): Path to the directory to check
        description (str): Description of the directory for error message
        
    Raises:
        AssertionError: If the directory does not exist
        
    Example:
        >>> assert_directory_exists("/path/to/scene", "Scene directory")
    """
    if not os.path.isdir(dir_path):
        error_msg = f"{description} does not exist: {dir_path}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    
    logger.info(f"{description} exists: {dir_path}")


def assert_file_not_empty(file_path: str, description: str = "Required file") -> None:
    """
    Assert that a file exists and is not empty, failing the test if it doesn't exist or is empty.
    
    Args:
        file_path (str): Path to the file to check
        description (str): Description of the file for error message
        
    Raises:
        AssertionError: If the file does not exist or is empty
        
    Example:
        >>> assert_file_not_empty("/path/to/log.txt", "Log file")
    """
    assert_file_exists(file_path, description)
    
    if os.path.getsize(file_path) == 0:
        error_msg = f"{description} is empty: {file_path}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    
    logger.info(f"{description} exists and is not empty: {file_path}")


def assert_file_extension(file_path: str, expected_extensions: List[str], 
                         description: str = "Required file") -> None:
    """
    Assert that a file exists and has one of the expected extensions.
    
    Args:
        file_path (str): Path to the file to check
        expected_extensions (List[str]): List of expected file extensions (e.g., ['.usda', '.usd'])
        description (str): Description of the file for error message
        
    Raises:
        AssertionError: If the file does not exist or has wrong extension
        
    Example:
        >>> assert_file_extension("/path/file.usda", ['.usda', '.usd'], "USD file")
    """
    assert_file_exists(file_path, description)
    
    file_extension = Path(file_path).suffix.lower()
    expected_extensions = [ext.lower() for ext in expected_extensions]
    
    if file_extension not in expected_extensions:
        error_msg = f"{description} has wrong extension. Expected {expected_extensions}, got {file_extension}: {file_path}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    
    logger.info(f"{description} has correct extension {file_extension}: {file_path}")
