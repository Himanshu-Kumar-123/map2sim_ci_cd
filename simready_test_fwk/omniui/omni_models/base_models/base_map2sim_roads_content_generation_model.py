# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Map2simRoadsContentGeneration Model class
   This module contains the base methods for Map2simRoadsContentGeneration window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait

class BaseMap2simRoadsContentGenerationModel(BaseModel):
    """Base model class for Map2simRoadsContentGeneration window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _country_combo = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/HStack[1]/ComboBox[0]"
    )

    _scene_dropdown_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[2]/VStack[0]/HStack[0]/Button[1]"
    )

    _scene_dropdown_base = (
        "SearchableComboBoxWindow//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/Label"
    )

    _configure_new_scene_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/**/HStack[0]/Button[0]"
    )

    _map_preprocessing_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/HStack[0]/RadioButton[0]"
    )

    _initialize_houdini_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[2]/HStack[0]/Button[0]"
    )

    _start_preprocessing_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[2]/VStack[0]/HStack[3]/Button[0]"
    )

    _scene_composition_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/HStack[0]/RadioButton[1]"
    )

    _utils_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/HStack[0]/RadioButton[3]"
    )

    _show_application_logs_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[5]/VStack[0]/VStack[0]/HStack[0]/Button[0]"
    )

    _collect_logs_button = (
        "Log Files Collector//Frame/VStack[0]/HStack[0]/Button[0]"
    )

    _log_file_label = (
        "Log Files Collector//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/TreeView[0]/HStack[0]/Label[0]"
    )

    _locate_in_explorer_button = (
        "Log Files Collector//Frame/VStack[0]/VStack[0]/HStack[0]/VStack[0]/Button[0]"
    )

    _setup_world_tiles_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[0]"
    )

    _generate_road_surface_checkbox1 = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[5]/CheckBox[0]"
    )

    _generate_road_surface_checkbox = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[4]/CheckBox[0]"
    )

    _generate_curbs_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[2]/CheckBox[0]"
    )

    _generate_lane_lines_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[1]/CheckBox[0]"
    )

    _generate_lane_lines_label = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[1]/Label[0]"
    )

    _generate_crosswalk_label = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/Label[0]"
    )

    _generate_crosswalk_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/CheckBox[0]"
    )

    _generate_barrier_label = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/Label[0]"
    )
    _generate_barrier_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/CheckBox[0]"
    )

    _generate_terrain_island_label = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[0]/Label[0]"
    )

    _generate_vegetation_label = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[8]/HStack[0]/Label[0]"
    )

    _generate_vegetation_checkbox = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[8]/HStack[0]/CheckBox[0]"
    )

    _generate_poles_checkbox = (
        #"Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[7]/HStack[0]/CheckBox[0]"
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[7]/HStack[0]/CheckBox[0]"
    )

    _generate_thumbnail_label = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[10]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[1]/HStack[0]/Label[0]"
    )

    _generate_intersection_system_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[9]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[0]/HStack[0]/CheckBox[0]"
    )

    _generate_terrain_island_checkbox = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[0]/CheckBox[0]"
    )

    _generate_test_scenario_label = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[12]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[0]/HStack[0]/Label[0]"
    )

    _generate_test_scenario_checkbox = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[12]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[0]/HStack[0]/CheckBox[0]"
    )

    _start_content_generation_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/HStack[0]/Button[0]"
    )

    _all_assets_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[0]"
    )

    _terrain_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[1]/Image[0]"
    )
 
    _terrain_XN1YP0_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[3]"
    )

    _terrain_XN1YP0_island_label = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[12]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_intersections_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[1]/Image[0]"
    )

    _network_tree_view = (      
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[2]/Image[0]"
    )

    _junction_14099181_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[3]/Image[0]"
    )

    _junction_14099181_tree_view_label = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[12]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _signal_48454539_label = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[60]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_foliage_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[1]/Image[0]"
    )

    _sub_foliage2_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[2]/Image[0]"
    )

    _sub_foliage_poles_tree_view = (    
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[3]/Image[0]"
    )

    _sub_foliage_pole_label = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[*]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _asset_placement_output_checkbox = (
        "Map2Sim Roads Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/HStack[0]/CheckBox[0]"
    )

    _tagging_stage_tree_view = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[17]/Image[0]"
    )

    _tagging_stage_anchor_prim = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[57]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _tagging_stage_thumb_cam = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[60]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _anchor_prim_raw_usd_properties = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[5]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/HStack[0]/Label[0]"
    )

    _anchor_prim_raw_usd_properties_semantic_type = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[5]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/HStack[0]/Label[0]"
    )

    _anchor_prim_raw_usd_properties_semantic_type_value = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[5]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/ZStack[0]/string_semantic:AnchorTags:params:semanticType"
    )

    _anchor_prim_raw_usd_properties_semantic_data_value = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[5]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/ZStack[0]/string_semantic:AnchorTags:params:semanticData"
    )

    _sub_poles_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[1]/Image[0]"
    )

    _sub_poles_create_scene_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[2]/Image[0]"
    )

    _sub_poles_poles_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[2]/Image[0]"
    )

    _sub_poles_poles_create_scene_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[3]/Image[0]"
    )

    _sub_poles_poles_label = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[*]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_stencil_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[3]/Image[0]"
    )

    _sub_stencil_crosswalk_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[7]/Image[0]"
    )

    _sub_stencil_crosswalk1_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[24]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_stencil_crosswalk2_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[27]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_stencil_crosswalk3_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[30]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _sub_stencil_crosswalk4_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[33]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _search_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ZStack[0]/HStack[0]/StringField[0]"
    )

    _mastarm_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[*]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _pipemount_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[*]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _pole_sign_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[0]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _pole_signal_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[0]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _terrain_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[0]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _map_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[16]/Image[0]"
    )

    _map_roads_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[17]/Image[0]"
    )

    _map_roads_parking_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[21]/Image[0]"
    )

    _map_roads_parking_lot_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[*]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    )

    _TerrainConcrete1_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[42]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete2_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[54]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete3_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[60]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete4_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[72]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete5_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[93]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete6_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[99]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _TerrainConcrete7_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[108]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    _generate_parking_label = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[1]/ZStack[0]/HStack[0]/Label[0]"
    )

    _road_max_resolution_combobox = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/VStack[1]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/ZStack[3]/HStack[0]/ComboBox[0]"
    )

    _terrain_elevation_hint_stage = (
        "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[1]/Frame[0]/ZStack[0]/HStack[0]/HStack[0]/Label[1]"
    )

    def select_country_name(self, country_name):
        """Clicks on ComboBox button to select a country by name
        Args:
            country_name (str): Name of the country to select
        """
        self.select_item_by_name_from_combo_box(self._country_combo, country_name)

    def select_scene_name(self, scene_name):
        """Clicks on ComboBox button to select a scene by name
        Args:
            scene_name (str): Name of the scene to select
        """
        self.find_and_click(self._scene_dropdown_button, refresh=True)

        _scene_name = f"{self._scene_dropdown_base}.text=='{scene_name}'"
        self.omni_driver.find_and_click(_scene_name)

    def configure_new_scene(self):
        """Clicks on Configure New Scene button"""
        self.find_and_click(self._configure_new_scene_button, refresh=True)

    def select_map_preprocessing(self):
        """Clicks on Map Preprocessing button"""
        self.find_and_click(self._map_preprocessing_button, refresh=True)
    
    def initialize_houdini(self):
        """Clicks on Initialize Houdini button"""
        self.find_and_click(self._initialize_houdini_button, refresh=True)

    def start_preprocessing(self):
        """Clicks on Start Preprocessing button"""

        element = self.omni_driver.find_element(self._start_preprocessing_button)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._start_preprocessing_button} and scrolled it into view.")
        self.omni_driver.wait(2)
        element.click()

    def select_scene_composition(self):
        """Clicks on Scene Composition button"""
        self.find_and_click(self._scene_composition_button, refresh=True)   

    def select_utils(self):
        """Clicks on Utils button"""
        self.find_and_click(self._utils_button, refresh=True)

    def select_show_application_log_files(self):
        """Clicks on Show Application Log Files button"""
        self.find_and_click(self._show_application_logs_button, refresh=True)

    def select_collect_logs(self):
        """Clicks on Collect Logs button"""
        self.find_and_click(self._collect_logs_button, refresh=True)

    def select_locate_in_explorer(self):
        """Clicks on Locate in Explorer button"""
        self.find_and_click(self._locate_in_explorer_button, refresh=True)

    def open_log_file(self):
        """Clicks on Log File button"""
        self.find_and_click(self._log_file_label, refresh=True, double_click=True)

    def select_setup_world_tiles(self):
        """Clicks on Setup World Tiles button"""
        self.find_and_click(self._setup_world_tiles_button, refresh=True)

    def select_generate_road_surface(self):
        """Clicks on Generate Road Surface button"""

        element = self.omni_driver.find_element(self._generate_lane_lines_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_lane_lines_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_road_surface_checkbox = self.omni_driver.find_element(self._generate_road_surface_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_road_surface_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(5)

    def select_generate_lane_lines(self):
        """Clicks on Generate Road Surface button"""

        element = self.omni_driver.find_element(self._generate_lane_lines_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_lane_lines_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_lane_lines_checkbox = self.omni_driver.find_element(self._generate_lane_lines_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_lane_lines_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(5)
 
    def select_generate_curbs(self):
        """Clicks on Generate Curbs button"""

        element = self.omni_driver.find_element(self._generate_lane_lines_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_lane_lines_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_road_surface_checkbox = self.omni_driver.find_element(self._generate_road_surface_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_road_surface_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(5)

    def select_generate_poles(self):
        """Clicks on Generate Poles button"""
        element = self.omni_driver.find_element(self._generate_vegetation_checkbox)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_vegetation_checkbox} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_poles_checkbox = self.omni_driver.find_element(self._generate_poles_checkbox, refresh=True) 
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_poles_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(2)

    def select_generate_crosswalks(self):
        """Clicks on Generate Crosswalk button"""
        element = self.omni_driver.find_element(self._generate_crosswalk_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_crosswalk_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_crosswalk_checkbox = self.omni_driver.find_element(self._generate_crosswalk_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_crosswalk_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(2)
    
    def select_generate_barrier(self):
        """Clicks on Generate Barrier button"""
        element = self.omni_driver.find_element(self._generate_barrier_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_barrier_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_barrier_checkbox = self.omni_driver.find_element(self._generate_barrier_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_barrier_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(2)

    def select_generate_terrain_island(self):
        """Clicks on Generate Terrain Island button"""
        element = self.omni_driver.find_element(self._generate_terrain_island_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_terrain_island_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_terrain_island_checkbox = self.omni_driver.find_element(self._generate_terrain_island_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_terrain_island_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(2)  

    def select_intersection_system(self):
        """Clicks on Intersection System button"""
        element = self.omni_driver.find_element(self._generate_thumbnail_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_thumbnail_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_intersection_system_checkbox = self.omni_driver.find_element(self._generate_intersection_system_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_intersection_system_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))
        self.omni_driver.wait(2)

    def select_vegetation_generation(self):
        """Clicks on Vegetation Generation button"""

        element = self.omni_driver.find_element(self._generate_vegetation_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_vegetation_label} and scrolled it into view.")
        self.omni_driver.wait(2)

        enable_generate_vegetation_checkbox = self.omni_driver.find_element(self._generate_vegetation_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_vegetation_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))

    def select_pavement_terrain_output(self):
        """Clicks on Generate Terrain Island button"""
        element = self.omni_driver.find_element(self._generate_terrain_island_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_terrain_island_label} and scrolled it into view.")

        enable_generate_terrain_island_checkbox = self.omni_driver.find_element(self._generate_terrain_island_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_terrain_island_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))

    def select_asset_placement_output(self):
        """Clicks on Asset Placement button"""

        element = self.omni_driver.find_element(self._generate_vegetation_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_vegetation_label} and scrolled it into view.")
        
        enable_asset_placement_checkbox = self.omni_driver.find_element(self._asset_placement_output_checkbox, refresh=True)
        checkbox_properties = enable_asset_placement_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))

    def select_generate_test_scenario(self):
        """Clicks on Generate Test Scenario button"""
        element = self.omni_driver.find_element(self._generate_test_scenario_label)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._generate_test_scenario_label} and scrolled it into view.")
        self.omni_driver.wait(1)

        enable_generate_test_scenario_checkbox = self.omni_driver.find_element(self._generate_test_scenario_checkbox, refresh=True)
        ''' Get all size and position attributes at once '''
        checkbox_properties = enable_generate_test_scenario_checkbox.get_size_and_position("all")
        pos_x = checkbox_properties["screen_position_x"]
        pos_y = checkbox_properties["screen_position_y"]

        self.omni_driver.click_at(pos_x+2, (pos_y))

    def select_all_assets(self):
        """Clicks on All Assets button"""
        element = self.omni_driver.find_element(self._all_assets_button)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._all_assets_button} and scrolled it into view.")
        self.omni_driver.wait(1)

        self.find_and_click(self._all_assets_button, refresh=True)

    def select_start_content_generation(self):
        """Clicks on Start Content Generation button"""

        element = self.omni_driver.find_element(self._start_content_generation_button)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._start_content_generation_button} and scrolled it into view.")
        self.omni_driver.wait(1)

        self.find_and_click(self._start_content_generation_button, refresh=True)

    def terrain_island_tree_view(self):
        """Clicks on Terrain Island tree view"""

        self.find_and_click(self._terrain_tree_view, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._terrain_XN1YP0_tree_view, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._terrain_XN1YP0_island_label, refresh=True)
        self.omni_driver.wait(1)

    def intersection_signal_tree_view(self):
        """Clicks on Intersection Signal tree view"""

        self.find_and_click(self._sub_intersections_tree_view, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._network_tree_view, refresh=True)
        self.omni_driver.wait(1)
        
        self.find_and_click(self._junction_14099181_tree_view, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._signal_48454539_label, refresh=True)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="F")

    def poles_tree_view(self):
         """Focuses on poles tree view"""
        
         self.find_and_click(self._sub_foliage_tree_view, refresh=True)
         self.omni_driver.wait(1)

         self.find_and_click(self._sub_foliage2_tree_view, refresh=True)
         self.omni_driver.wait(1)

         self.find_and_click(self._sub_foliage_poles_tree_view, refresh=True)
         self.omni_driver.wait(1)        
        
         for i in range(12, 64, 3):  
            path = self._sub_foliage_pole_label.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)    

    def sub_poles_tree_view(self):
         """Focuses on sub poles tree view"""
        
         self.find_and_click(self._sub_poles_stage, refresh=True)
         self.omni_driver.wait(1)

         self.find_and_click(self._sub_poles_poles_stage, refresh=True)
         self.omni_driver.wait(1)
           
         for i in range(9, 54, 3):
            path = self._sub_poles_poles_label.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)              

    def mastarm_tree_view(self):
         """Focuses on mastarm tree view"""
           
         for i in range(0, 61, 6):  
            path = self._mastarm_stage.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)

    def pipemount_tree_view(self):
         """Focuses on pipemount tree view"""
           
         for i in range(0, 61, 6):  
            path = self._pipemount_stage.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)              

    def check_tagging_stage_elements(self):
        """Clicks on tagging stage tree view and checks the elements"""
        
        self.find_and_click(self._tagging_stage_tree_view, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._tagging_stage_anchor_prim, refresh=True)
        self.omni_driver.wait(1)

        element = self.omni_driver.find_element(self._anchor_prim_raw_usd_properties)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._anchor_prim_raw_usd_properties} and scrolled it into view.")
        self.omni_driver.wait(1)

        self.find_and_click(self._anchor_prim_raw_usd_properties, refresh=True)
        self.omni_driver.wait(1)

        element = self.omni_driver.find_element(self._anchor_prim_raw_usd_properties_semantic_type)
        element.scroll_into_view(axis='Y', scroll_amount=1)
        self.log.info(f"Found element - {self._anchor_prim_raw_usd_properties_semantic_type} and scrolled it into view.")
        self.omni_driver.wait(1)
        
        element_id = self.omni_driver.find_element(self._anchor_prim_raw_usd_properties_semantic_type_value)
        semantic_type = element_id.get_value()
        self.log.info(f"Semantic type: {semantic_type}")
        self.omni_driver.wait(1)

        if semantic_type == "anchorTag":
            self.log.info("Semantic type is anchorTag")
        else:
            self.log.info("Semantic type is not anchorTag")
        
        element_id = self.omni_driver.find_element(self._anchor_prim_raw_usd_properties_semantic_data_value)
        semantic_data = element_id.get_value()
        self.log.info(f"Semantic data: {semantic_data}")
        self.omni_driver.wait(1)

        if semantic_data == "4way,has_signals,SimReady,poi,USA":
            self.log.info("Semantic data is 4way,has_signals,SimReady,poi,USA")
        else:
            self.log.info("Semantic data is not 4way,has_signals,SimReady,poi,USA")

        self.omni_driver.wait(2)

        self.find_and_click(self._tagging_stage_thumb_cam, refresh=True)
        self.omni_driver.wait(1)

    def check_sub_stencils_crosswalk_stage(self):
        """Clicks on sub stencils crosswalk stage"""

        self.find_and_click(self._sub_stencil_stage, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._sub_stencil_crosswalk_stage, refresh=True)
        self.omni_driver.wait(1)

        crosswalks_all = [self._sub_stencil_crosswalk1_stage, self._sub_stencil_crosswalk2_stage, self._sub_stencil_crosswalk3_stage, self._sub_stencil_crosswalk4_stage]

        for crosswalk in crosswalks_all:
            self.find_and_click(crosswalk, refresh=True)
            self.omni_driver.wait(1)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(1)

    def search_stage(self, search_text):
        """Clicks on search stage"""

        self.find_and_click(self._search_stage, refresh=True)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_char_press(search_text)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="ENTER")
        self.omni_driver.wait(1)

    def search_and_check_sign_poles_stage(self, search_text):
        """Clicks on sign poles stage"""

        self.find_and_click(self._search_stage, refresh=True)
        self.omni_driver.wait(1)

        for _ in range(20):
            self.omni_driver.emulate_key_press(button="BACKSPACE")

        self.omni_driver.emulate_char_press(search_text)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="ENTER")
        self.omni_driver.wait(1)

        self.find_and_click(self._pole_sign_stage, refresh=True)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="F")
        self.omni_driver.wait(3)

    def search_and_check_signal_poles_stage(self, search_text):
        """Clicks on signal poles stage"""

        self.find_and_click(self._search_stage, refresh=True)
        self.omni_driver.wait(1)

        for _ in range(20):
            self.omni_driver.emulate_key_press(button="BACKSPACE")

        self.omni_driver.emulate_char_press(search_text)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="ENTER")
        self.omni_driver.wait(1)

        self.find_and_click(self._pole_signal_stage, refresh=True)

        self.omni_driver.emulate_key_press(button="F")
        self.omni_driver.wait(3)

    def search_and_check_terrain_stage(self, search_text):
        """Clicks on terrain stage"""

        self.find_and_click(self._search_stage, refresh=True)
        self.omni_driver.wait(1)

        for _ in range(20):
            self.omni_driver.emulate_key_press(button="BACKSPACE")

        self.omni_driver.emulate_char_press(search_text)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="ENTER")
        self.omni_driver.wait(1)

        self.find_and_click(self._terrain_stage, refresh=True)

        self.omni_driver.emulate_key_press(button="F")
        self.omni_driver.wait(1)

    def poles_stage_view(self):
        """Clicks on poles stage tree view"""

        self.find_and_click(self._sub_poles_create_scene_stage, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._sub_poles_poles_create_scene_stage, refresh=True)
        self.omni_driver.wait(1)

        for i in range(12, 55, 3):  
            path = self._sub_poles_poles_label.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)

    def parking_stage_view(self):
        """Clicks on parking stage tree view"""

        self.find_and_click(self._map_stage, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._map_roads_stage, refresh=True)
        self.omni_driver.wait(1)

        self.find_and_click(self._map_roads_parking_stage, refresh=True)
        self.omni_driver.wait(1)

        self.omni_driver.wait(5)

        for i in range(66, 98, 3):  
            path = self._map_roads_parking_lot_stage.replace("*", str(i))
            self.find_and_click(path, refresh=True)
            self.omni_driver.emulate_key_press(button="F")
            self.omni_driver.wait(2)

    def TerrainConcrete_stage_view(self):
         """Focuses on TerrainConcrete tree view"""
         
         terrains = [self._TerrainConcrete1_stage, self._TerrainConcrete2_stage, self._TerrainConcrete3_stage, self._TerrainConcrete4_stage, self._TerrainConcrete5_stage, self._TerrainConcrete6_stage, self._TerrainConcrete7_stage]
         
         for terrain in terrains:
          self.find_and_click(terrain, refresh=True)
          self.log.info(f"Found element - {terrain} and clicked it.")
          self.omni_driver.wait(1)
         
          self.omni_driver.emulate_key_press(button="F")
          self.omni_driver.wait(2)

    def terrain_road_max_resolution(self, value):
        """Selects a value from ComboBox button for terrain road max resolution
        Args:
            value (int): Value to select
            0 - 0.25 meter, 1 - 0.5 meter, 2 - 1 meter, 3 - 2 meter, 4 - 4 meter, 5 - 8 meter
        """
        
        self.select_item_by_index_from_combo_box(self._road_max_resolution_combobox, value)

    def terrain_elevation_hint_stage(self):
        """Clicks on terrain elevation hint stage"""

        self.find_and_click(self._terrain_elevation_hint_stage, refresh=True)
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(button="F")
        self.omni_driver.wait(2)
