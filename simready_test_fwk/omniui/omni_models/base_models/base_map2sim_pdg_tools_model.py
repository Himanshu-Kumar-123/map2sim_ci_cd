# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Map2simPDGTool Model class
   This module contains the base methods for Map2simPDGTool window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis

class BaseMap2simPDGToolModel(BaseModel):
    """Base model class for Map2simPDGTool window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _pdg_tool_combo = (
        "Map2Sim PDG Tools//Frame/VStack[0]/HStack[0]/ComboBox[0]"
    )
    
    _pdg_initialize_button = (
        "Map2Sim PDG Tools//Frame/VStack[0]/HStack[1]/Button[0]"
    )
    
    _pdg_assets_combo = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[0]/HStack[1]/VStack[0]/HStack[0]/ComboBox[0]"
    )
    
    _pdg_create_assets_button = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[0]/HStack[1]/Button[0]"
    )
    
    _pdg_houdini_assets_node_scene_settings = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/HStack[0]/Label[0]"
    )
    
    _pdg_houdini_assets_node_country_search = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[4]/HStack[0]/HStack[0]/StringField[0]"
    )
    
    _pdg_houdini_assets_node_scene_search = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[5]/HStack[0]/HStack[0]/StringField[0]"
    )
    
    _pdg_load_usd_to_stage_checkbox = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/CheckBox[0]"
    )
    
    _pdg_cook_output_button = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/Button[0]"
    )

    _pdg_generate_buildings_checkbox = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[1]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[2]/HStack[0]/Frame[0]/CheckBox[0]"
    )
    
    _pdg_download_buildings_checkbox = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[1]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[1]/HStack[0]/Frame[0]/CheckBox[0]"
    )

    _pdg_user_options_settings = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[1]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/HStack[0]/Label[0]"
    )

    _pdg_use_usd_in_user_options_settings = (
        "Houdini PDG Driver - Blackshark Buildings Generation//Frame/VStack[0]/VStack[1]/HDAParmsFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[1]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[9]/HStack[0]/Frame[0]/CheckBox[0]"
    )

    _open_scene_for_editing_button = (
        "Map2Sim Content Generation//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[1]"
    )

    def select_pdg_tool(self, pdg_tool):
        """Selects a PDG tool from the combo box

        Args:
            pdg_tool (str): Name of the PDG tool to select
        """
        self.select_item_by_name_from_combo_box(self._pdg_tool_combo, pdg_tool)

    def initialize_pdg(self):
        """Initializes the PDG"""
        self.find_and_click(self._pdg_initialize_button, refresh=True)

    def select_pdg_assets(self, assets):
        """Selects a PDG asset from the combo box

        Args:
            assets (str): Name of the PDG asset to select
        """
        self.verify_combo_box_selection(self._pdg_assets_combo, assets)
    
    def create_pdg_assets(self):
        """Creates the PDG assets"""
        self.find_and_click(self._pdg_create_assets_button, refresh=True)
    
    def select_pdg_houdini_assets_node_scene_settings(self):
        """Selects the PDG Houdini assets node scene settings"""
        self.find_and_click(self._pdg_houdini_assets_node_scene_settings, refresh=True)
    
    def select_pdg_houdini_assets_node_country(self, country):
        """Selects the PDG Houdini assets node country

        Args:
            country (str): Name of the country to select
        """
        self.find_and_enter_text(self._pdg_houdini_assets_node_country_search, country)
        self.wait.element_to_be_located(
            self.omni_driver,
            locator=self._pdg_houdini_assets_node_country_search.replace("__name__", country),
        )
    
    def select_pdg_houdini_assets_node_scene(self, scene):
        """Selects the PDG Houdini assets node scene

        Args:
            scene (str): Name of the scene to select
        """
        self.find_and_enter_text(self._pdg_houdini_assets_node_scene_search, scene)
        self.wait.element_to_be_located(
            self.omni_driver,
            locator=self._pdg_houdini_assets_node_scene_search.replace("__name__", scene),
        )

    def toggle_load_usd_to_stage(self):
        """Toggles the load USD to stage checkbox"""
        checkbox_element = self.find_and_scroll_element_into_view(
            self._pdg_load_usd_to_stage_checkbox,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
            refresh=True
        )
        current_state = checkbox_element.is_checked()
        if current_state:
            self.log.info(f"Auto load USD file to stage is already enabled, Disabling it")
            self.find_and_click(self._pdg_load_usd_to_stage_checkbox, refresh=True)
        else:
            self.log.info(f"Auto load USD file to stage is already disabled")
    
    def select_cook_output(self):
        """Selects the cook output button"""
        scroll_pdg_cook_output_button=self.find_and_scroll_element_into_view(
            self._pdg_cook_output_button,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
            refresh=True
        )
        scroll_pdg_cook_output_button.click()
    
    def generate_buildings_checkbox(self, enable=True):
        """
        Toggles the Generate Buildings checkbox.
        By default, enables the checkbox (enable=True). Set enable=False to disable it.
        """
        checkbox_element = self.find_and_scroll_element_into_view(
            self._pdg_generate_buildings_checkbox,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
            refresh=True
        )
        current_state = checkbox_element.is_checked()
        if enable:
            if not current_state:
                self.log.info("Enabling Generate Buildings checkbox")
                self.find_and_click(self._pdg_generate_buildings_checkbox, refresh=True)
            else:
                self.log.info("Generate Buildings checkbox is already enabled")
        else:
            if current_state:
                self.log.info("Disabling Generate Buildings checkbox")
                self.find_and_click(self._pdg_generate_buildings_checkbox, refresh=True)
            else:
                self.log.info("Generate Buildings checkbox is already disabled")

    def download_buildings_checkbox(self, enable=True):
        """
        Toggles the Download Buildings checkbox.
        By default, enables the checkbox (enable=True). Set enable=False to disable it.
        """
        checkbox_element = self.find_and_scroll_element_into_view(
            self._pdg_download_buildings_checkbox,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
            refresh=True
        )
        current_state = checkbox_element.is_checked()
        if enable:
            if not current_state:
                self.log.info("Enabling Download Buildings checkbox")
                self.find_and_click(self._pdg_download_buildings_checkbox, refresh=True)
            else:
                self.log.info("Download Buildings checkbox is already enabled")
        else:
            if current_state:
                self.log.info("Disabling Download Buildings checkbox")
                self.find_and_click(self._pdg_download_buildings_checkbox, refresh=True)
            else:
                self.log.info("Download Buildings checkbox is already disabled")

    def click_user_options_settings(self):
        """Selects the PDG Houdini assets node scene settings"""
        self.find_and_click(self._pdg_user_options_settings, refresh=True)

    def select_open_scene_for_editing(self):
        """Opens scene for editing"""
        self.find_and_click(self._open_scene_for_editing_button, refresh=True)