# -*- coding: utf-8 -*-
# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""
NVIDIA Omniverse Map2Sim App Tests
"""
# To get type hints since we are creating instance of class dynamically
from omniui.omni_models.base_models import *
from omniui.utils.utility_functions import  get_window_model
from omniui.utils.omni_models import OmniModel
from utils.configuration_loader import get_config
from omni_remote_ui_automator.driver.omnidriver import OmniDriver
import pytest

class TestMap2Sim_Test():
    """
    Test Class for Map2Sim Map Preprocessing
    """
    app = "SimReady Studio"

    def set_connection_details(self) -> str:
        """Implemented Connection details setup"""
        self.test_config = get_config()
        self.connection_details = self.test_config.automator_kit_server["default"]
        
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        """
        Setup function.  Runs before every test.
        """
        self.set_connection_details()

        self.omni_driver = OmniDriver(
            self.connection_details.host, self.connection_details.port
        )
        self.omni_driver.status()

        self.app_name = 'SimReady Studio'
        self.srs_open_window: BaseSimreadyStudioOpenWindowModel = get_window_model(
            self.omni_driver, OmniModel.simready_studio_open_window_model, self.app_name
        )

        self.srs_test: BaseSimreadyAssetStudioTestModel = get_window_model(
            self.omni_driver, OmniModel.simready_asset_studio_test_model, self.app_name
        )
        self.srs_edit: BaseSimreadyStudioEditModel = get_window_model(
            self.omni_driver, OmniModel.simready_studio_edit_window_model, self.app_name
        )
        self.srs_mode_bar: BaseSimreadyStudioModeBarModel = get_window_model(
            self.omni_driver, OmniModel.simready_studio_modebar_model, self.app_name
        )

        self.drive_sim_base_model: BaseModel = get_window_model(
            self.omni_driver, OmniModel.model, self.app_name
        )

        self.map2sim_roads_content_generation: BaseMap2simRoadsContentGenerationModel = get_window_model(
            self.omni_driver, OmniModel.map2sim_roads_content_generation_model, self.app_name
        )

    def test_map2sim(self):
        
        self.srs_open_window.omni_driver.wait(2)

        content_path = r"D:\p4\Projects\nv_content"

        country_name = 'usa'
        scene_name = 'scene_sanjose_plus37point330219_minus121point882464'
        
        self.omni_driver.select_menu_option("DSReady Studio/Map2Sim/Map2Sim Content Generation")
        self.omni_driver.wait(2)
        
        self.map2sim_roads_content_generation.select_country_name(country_name)
        self.omni_driver.wait(2)
        
        self.map2sim_roads_content_generation.configure_new_scene()
        self.omni_driver.wait(2)

        self.omni_driver.emulate_key_press(button="ENTER")
        self.omni_driver.wait(2)

        self.map2sim_roads_content_generation.select_map_preprocessing()
        self.omni_driver.wait(2)
        
        self.map2sim_roads_content_generation.initialize_houdini()
        self.omni_driver.wait(40)
        
        self.map2sim_roads_content_generation.start_preprocessing()
        self.omni_driver.wait(400)
        
        self.map2sim_roads_content_generation.select_scene_composition()
        self.omni_driver.wait(2)        

        self.map2sim_roads_content_generation.select_setup_world_tiles()
        self.omni_driver.wait(4)

        self.map2sim_roads_content_generation.select_all_assets()
        self.omni_driver.wait(4)

        self.map2sim_roads_content_generation.terrain_road_max_resolution(0)
        self.omni_driver.wait(4)
        
        self.map2sim_roads_content_generation.select_start_content_generation()
        self.omni_driver.wait(650)
        
        self.map2sim_roads_content_generation.search_stage("pole_13688219_tree")
        self.omni_driver.wait(2)

        self.map2sim_roads_content_generation.terrain_elevation_hint_stage()
        self.omni_driver.wait(2)        