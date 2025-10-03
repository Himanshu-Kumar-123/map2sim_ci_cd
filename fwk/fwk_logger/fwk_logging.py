# logger.py - Clean DMF Framework Logger Implementation
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from fwk.shared.constants import (
    DSRS_LAUNCH_LOG_FILE_NAME, 
    MAP2SIM_LAUNCH_LOG_FILE_NAME,
    DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME,
    MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME,
    DSRS_SCENARIO_TYPE,
    MAP2SIM_SCENARIO_TYPE
)

class DMFLogger:
    """
    Dedicated logger class for DMF Framework
    Maintains single framework log file with component-based console logging
    """
    
    # Class-level storage
    _framework_log_file: Optional[str] = None
    _console_log_level: str = 'DEBUG'
    _created_loggers: Dict[str, logging.Logger] = {}
    
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    @staticmethod
    def use_logger(module_name: str, file_path: Optional[str] = None, console_log_level: str = 'DEBUG') -> logging.Logger:
        """
        Create or get logger for a module with console and optional file logging
        
        Args:
            module_name: Name of the module (e.g., 'DSRS', 'MAP2SIM', 'MAIN')
            file_path: Path to the framework log file (if provided, updates all loggers)
            console_log_level: Log level for console output ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            
        Returns:
            Logger instance for the module
        """
        
        # Create logger name with DMF prefix
        logger_name = f"DMF.{module_name}"
        logger = logging.getLogger(logger_name)
        
        # If logger already exists and has handlers, return it (unless we need to update file path)
        if logger.handlers and not file_path:
            return logger
        
        # Set logger level to DEBUG (handlers will control actual output levels)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False  # Don't propagate to root logger
        
        # Store console log level for updates
        DMFLogger._console_log_level = console_log_level.upper()
        
        # Always create/update console handler
        DMFLogger._setup_console_handler(logger, console_log_level)
        
        # Handle file logging
        if file_path:
            # Update framework log file path and add file handler to all loggers
            DMFLogger.set_framework_log_file(file_path)
        elif DMFLogger._framework_log_file:
            # Add file handler using existing framework log file
            DMFLogger._add_file_handler(logger, DMFLogger._framework_log_file)
        
        # Store reference to created logger
        DMFLogger._created_loggers[module_name] = logger
        
        return logger
    
    @staticmethod
    def _setup_console_handler(logger: logging.Logger, console_log_level: str):
        """Setup or update console handler for a logger"""
        
        # Remove existing console handlers
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
                handler.close()
        
        # Create new console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(DMFLogger.LOG_LEVELS.get(console_log_level.upper(), logging.INFO))
        
        # Set formatter with DMF_RUNNER prefix
        formatter = logging.Formatter('\n[DMF_RUNNER] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    @staticmethod
    def _add_file_handler(logger: logging.Logger, file_path: str):
        """Add or update file handler for a logger"""
        
        # Remove any existing file handlers
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
                handler.close()
        
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Add new file handler
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # File gets all levels
        
        # Set formatter with DMF_RUNNER prefix
        formatter = logging.Formatter('\n[DMF_RUNNER] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    @staticmethod
    def set_framework_log_file(file_path: str):
        """
        Set the framework log file path and update all existing loggers
        
        Args:
            file_path: Path to the single framework log file
        """
        DMFLogger._framework_log_file = file_path
        
        # Update all existing loggers with the new file handler
        DMFLogger._update_all_file_handlers(file_path)
    
    @staticmethod
    def _update_all_file_handlers(file_path: str):
        """Update all existing loggers with new file path"""
        
        # Update all DMF loggers we've created
        for logger in DMFLogger._created_loggers.values():
            DMFLogger._add_file_handler(logger, file_path)
        
        # Also update any other DMF loggers that might exist in the logging registry
        for name, logger in logging.root.manager.loggerDict.items():
            if isinstance(logger, logging.Logger) and name.startswith('DMF.'):
                DMFLogger._add_file_handler(logger, file_path)
    
    @staticmethod
    def get_framework_log_file() -> Optional[str]:
        """Get the current framework log file path"""
        return DMFLogger._framework_log_file
    
    @staticmethod
    def set_console_log_level(console_log_level: str):
        """
        Update console log level for all existing loggers
        
        Args:
            console_log_level: New console log level
        """
        DMFLogger._console_log_level = console_log_level.upper()
        
        # Update console handlers for all existing loggers
        for logger in DMFLogger._created_loggers.values():
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(DMFLogger.LOG_LEVELS.get(console_log_level.upper(), logging.INFO))
    
    @staticmethod
    def list_active_loggers() -> Dict[str, str]:
        """Get list of active DMF loggers and their status"""
        status = {}
        for module_name, logger in DMFLogger._created_loggers.items():
            console_handlers = sum(1 for h in logger.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler))
            file_handlers = sum(1 for h in logger.handlers if isinstance(h, logging.FileHandler))
            status[module_name] = f"Console: {console_handlers}, File: {file_handlers}"
        return status
    
    @staticmethod
    def shutdown():
        """Clean shutdown of all loggers and handlers"""
        for logger in DMFLogger._created_loggers.values():
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        
        DMFLogger._created_loggers.clear()
        DMFLogger._framework_log_file = None

# Convenience functions for easy usage
def get_logger(module_name: str, file_path: Optional[str] = None, console_log_level: str = 'INFO') -> logging.Logger:
    """
    Convenience function to get a DMF logger
    
    Args:
        module_name: Name of the module
        file_path: Optional path to framework log file
        console_log_level: Console log level
        
    Returns:
        Logger instance
    """
    return DMFLogger.use_logger(module_name, file_path, console_log_level)

def setup_framework_logging(log_dir: str, log_filename: str = None) -> str:
    """
    Setup framework-wide logging with a single log file
    
    Args:
        log_dir: Directory for log files
        log_filename: Custom log filename (if None, generates timestamp-based name)
        
    Returns:
        Path to the created log file
    """
    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate log filename if not provided
    if not log_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"dmf_framework_{timestamp}.log"
    
    # Create full path
    log_file_path = str(Path(log_dir) / log_filename)
    
    # Set framework log file (this will update all existing loggers)
    DMFLogger.set_framework_log_file(log_file_path)
    
    return log_file_path

def update_console_log_level(level: str):
    """Update console log level for all loggers"""
    DMFLogger.set_console_log_level(level)

def get_framework_log_file() -> Optional[str]:
    """Get current framework log file path"""
    return DMFLogger.get_framework_log_file()

def get_component_log_file(component, log_type='launch'):
    """Get appropriate log file name based on component and log type"""
    if component == DSRS_SCENARIO_TYPE:
        return DSRS_LAUNCH_LOG_FILE_NAME if log_type == 'launch' else DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME
    elif component == MAP2SIM_SCENARIO_TYPE:
        return MAP2SIM_LAUNCH_LOG_FILE_NAME if log_type == 'launch' else MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME
    else:
        return f"{component.lower()}_logs.txt"
