# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimMaps Model Class
   This module contains the base methods for MAP section
"""
from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait


class BaseDriveSimV2MapsModel(BaseModel):
    """Base model class for DriveSimMaps window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """
    # Locators
    _map_section_btn = "DRIVE Sim Asset Explorer//Frame/VStack[0]/Frame[0]/VStack[0]/Stack[0]/ZStack[0]/Frame[0]/HStack[0]/ZStack[0]/VStack[0]/ScrollingFrame[0]/CategoryView[0]/HStack[7]/Label[0]"
    _asset_search_field = "DRIVE Sim Asset Explorer//Frame/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/Frame[0]/HStack[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/HStack[0]/StringField[0]"
    _select_all_payloads_checkbox = "Select Payloads To Load//Frame/**/HStack[0]/CheckBox[0]"
    _selected_payloads_confirm_btn = "Select Payloads To Load//Frame/**/Button[0].text == 'Ok'"
    _select_result_image = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/HStack[0]/VStack[0]/ThumbnailView[0]/Frame[*]/**/Label[0]"
    _select_option_btn = "DRIVE Sim Asset Explorer//Frame/**/HStack[0]/settings_icon"
    
    def map_selection(self):
        """Select MAP from DRIVE Sim Asset Explorer"""
        self.find_and_click(self._map_section_btn, refresh=True)

    def enter_search_field(self, text: str):
        """Enter text in search field

        Args:
            text (str): Name of scenario
        """
        self.find_and_enter_text(self._asset_search_field, text)

    def set_as_active_map(self, current_map_selection):
        """Set As Active Map"""
        current_map = self.omni_driver.find_element(current_map_selection)
        self.omni_driver.wait(2)
        current_map.right_click()
        self.omni_driver.select_context_menu_option("Set As Active Map")

    def select_payloads(self, payload_option: str):
        """Select Payloads

        Args:
            payload_option (str): 'All' or 'None'
        """
        if payload_option == 'All':
            self.find_and_click(self._select_all_payloads_checkbox, bring_to_front=False)
        if payload_option == 'None':
            pass

    def confirm_payloads_selection(self):
        """Click on Ok to confirm payloads"""
        self.find_and_click(self._selected_payloads_confirm_btn, bring_to_front=False)

    def wait_for_map_selection_button(self, timeout=600):
        """Waits for map mode button to be invisible

        Args:
            timeout (int): Time to wait in seconds
        """
        wait = Wait(timeout)
        wait.element_to_be_located(self.omni_driver, self._map_section_btn)
        self.omni_driver.wait(2)
        wait.element_to_be_enabled(self.find(self._map_section_btn, True))

    def select_experimental_assets(self):
        """Select show experimental assets"""
        self.find_and_click(self._select_option_btn, refresh=True)
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Show Experimental Assets")

    def search_and_open_scene(self, scene: str, experimental_asset: bool, wait_time=10):
        """Search and open's a scenario from main window

        Args:
            scene (str): name of map
            wait_time (int): waiting for time
            experimental_asset (bool): experimental assets to be shown
        """
        if experimental_asset:
            self.select_experimental_assets()
        self.enter_search_field(scene)
        self.omni_driver.wait(2)
        current_result_image = "{}.text=='{}'".format(self._select_result_image, scene)
        self.set_as_active_map(current_result_image)
        self.omni_driver.wait(wait_time)