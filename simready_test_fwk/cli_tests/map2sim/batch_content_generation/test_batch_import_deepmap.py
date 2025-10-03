# -*- coding: utf-8 -*-
"""
CLI test that runs the Map2Sim generate_scene.bat with desired arguments
and validates it completes under the per-test output directory.
"""

import os
import pytest

from simready_test_fwk.cli_tests.cli_test_base import Map2SimCLITestBase

class TestMap2SimGenerateSceneCLI(Map2SimCLITestBase):
    def test_run_generate_scene_bat(self):

        set_project_config_bat_path = r"D:\DSRS_map2sim_builds\DSReady_Studio_Software_205332945\_build\packages\dsrs\tools\map2sim\bin\set_project_config.bat"

        if not set_project_config_bat_path or not os.path.exists(set_project_config_bat_path):
            pytest.skip(f".bat not found at: {set_project_config_bat_path}")

        result_set_config = self.run_bat_script(
            set_project_config_bat_path,
            args=["D:\\p4\\Projects\\nv_content\\project_config.toml"],
            log_name="set_project_config.log"
        )
        
        # Validate return code
        self.assert_cli_condition(result_set_config["return_code"] == 0, "set_project_config.bat completed successfully")

        bat_path = self.get_batch_file_path()

        if not bat_path or not os.path.exists(bat_path):
            pytest.skip(f".bat not found at: {bat_path}")

        result_generate_scene = self.run_bat_script(
            bat_path,
            args=self.get_batch_args(),
            log_name="generate_scene.log",
        )

        # Validate return code
        self.assert_cli_condition(result_generate_scene["return_code"] == 0, "generate_scene.bat completed successfully")