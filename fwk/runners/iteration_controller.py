# fwk/runners/iteration_controller.py - Adapted from Linux Reference

# Standard library imports
import subprocess
import re
import os
from pathlib import Path
from copy import deepcopy

# Local imports
from fwk.shared.variables_util import varc
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger(__name__)

class IterationController:
    """This class is used to control the iteration of tests"""

    def __init__(self):
        self.iteration = 0  # Current iteration number
        self.max_iterations = 3  # Default to 3 unless --iterate flag is specified

    def should_continue_iterations(self, needs_retry, test_dict):
        """Determine if we should continue iterating this test.
        
        Args:
            needs_retry: Boolean indicating if the test should be retried
            test_dict: Dictionary containing test information
            
        Returns:
            Boolean indicating if the test should continue iterating
        """
        iterate_number = None
        
        # Parse --iterate flag from string format like "--iterate 3"
        iterate_number1 = self._parse_iterate_from_dict(test_dict.get('automation_suite_flags_dict', {}))
        iterate_number2 = self._parse_iterate_from_dict(test_dict.get('automation_flags_dict', {}))
        iterate_number = iterate_number1 or iterate_number2
        
        if iterate_number is not None:
            return self.iteration < int(iterate_number)
        
        # If --iterate is not specified, allow retry within max_iterations
        return needs_retry and self.iteration < self.max_iterations

    def _parse_iterate_from_dict(self, flags_dict):
        """Parse --iterate flag from automation flags dict.
        
        Args:
            flags_dict: Dictionary containing automation flags
            
        Returns:
            str or None: Iteration number if found, None otherwise
        """
        # Check if --iterate is a direct key
        if '--iterate' in flags_dict:
            return flags_dict['--iterate']
        
        # Check in the flags list for string format like "--iterate 3"
        for key, value in flags_dict.items():
            if isinstance(key, str) and key.startswith('--iterate'):
                if ' ' in key:
                    parts = key.split(' ', 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        return parts[1]
                elif '=' in key:
                    parts = key.split('=', 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        return parts[1]
        
        return None

    def handle_test_result(self, test_dict, test_queue, current_test_index):
        """Handle test completion and determine next steps.
        
        Args:
            test_dict: Dictionary containing test information
            test_queue: The deque containing test items
            current_test_index: Current test index in the queue
        """
        # DMF-specific retry conditions (adapt as needed)
        needs_retry = (
            hasattr(varc, 'p0_functional_iter') and varc.p0_functional_iter or
            hasattr(varc, 'p0_platform') and varc.p0_platform or 
            hasattr(varc, 'skip_remaining_blocks_freeze') and varc.skip_remaining_blocks_freeze or
            hasattr(varc, 'p0_setup_iter') and varc.p0_setup_iter
        )
  
        self.iteration += 1

        # Continue iterations if --iterate is specified or if retry is needed within max_iterations
        if self.should_continue_iterations(needs_retry, test_dict):
            # Update current test directory name to include iteration number
            test_dict['updated_name'] = f"{test_dict['name']}_iteration_{self.iteration}"
            self.rename_test_directory(test_dict)
            
            # Create copy for next iteration
            test_dict_copy = deepcopy(test_dict)
            
            # Insert copy at current_index + 1 to maintain proper order
            from fwk.runners.dsrs_runner import TestResult
            iteration_test_item = {
                'test_dict': test_dict_copy,
                'result': TestResult()
            }
            test_queue.insert(current_test_index + 1, iteration_test_item)
            
            # Reset fields for the next iteration
            iteration_test = test_queue[current_test_index + 1]['test_dict']
            self.reset_test_fields(iteration_test)
            
            logger.info(f"Created iteration {self.iteration + 1} for test '{test_dict['name']}'")
            
        else:
            # Reset iteration counter for next test
            self.iteration = 0

    def get_iteration_info(self):
        """Get current iteration information, better to call at start of test"""
        return {
            'iteration': self.iteration
        }

    def rename_test_directory(self, test_dict):
        """Renames test directory and updates all paths in test_dict.
        
        Args:
            test_dict: Dictionary containing test information
        """
        try:
            # Get old and new paths
            old_path = Path(test_dict['test_path'])
            new_name = f"{test_dict['updated_name']}"
            new_path = old_path.parent / new_name

            # Rename directory
            old_path.rename(new_path)

            # Update all paths in test_dict
            for key in test_dict:
                if key.endswith('_path'):
                    old_value = Path(test_dict[key])
                    new_value = str(new_path / old_value.relative_to(old_path))
                    test_dict[key] = new_value

            logger.info(f"Renamed test directory from {old_path.name} to {new_path.name}")

        except Exception as e:
            logger.exception(f"Failed to rename directory: {e}")

    def reset_test_fields(self, iteration_test):
        """
        Resets test fields for a new iteration.
        
        Args:
            iteration_test: Test dictionary to reset fields in
        """
        iteration_test['updated_name'] = f"{iteration_test['name']}_iteration_{self.iteration + 1}"

        # Reset verdicts (using DMF format)
        iteration_test['verdicts'] = {
            "final-verdict": None,
            "logs-errors": None,
            "process-specific-errors": None,
            "launch-time": None,
            "execution-time": None
        }

        # Reset analysis fields
        iteration_test['detailed_analysis'] = {
            "logs": None,
            "kit_logs": None,
            "pytest_logs": None
        }

        # Reset tracking
        iteration_test['subtest_dict'] = {}
        if 'dmf_warnings' in iteration_test:
            iteration_test['dmf_warnings'] = []

        # Reset upload storage IDs
        iteration_test['upload_storage'] = {
            'share_point': {"test_artifacts_id": None}
        }

        logger.debug(f"Reset fields for iteration test: {iteration_test['updated_name']}")
        
        # Note: Paths will be overwritten by directory_creator_for_iterative_tests 