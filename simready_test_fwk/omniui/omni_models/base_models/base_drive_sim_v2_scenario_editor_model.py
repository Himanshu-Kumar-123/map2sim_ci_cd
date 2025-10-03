# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSim V2 Scenario Editor Model class
   This module contains the base methods for DriveSim V2 Scenario Editor window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait
from omni_remote_ui_automator.driver.omnielement import OmniElement

class BaseDriveSimV2ScenarioEditorModel(BaseModel):
    """Base model class for DriveSim V2 Scenario Editor window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _vehicle_section = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[*]/Label[0].text=='VEHICLE'"

    _ego_section = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[*]/Label[0].text=='EGO'"
        
    _character_section = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[*]/Label[0].text=='CHARACTER'"

    _prefab_section = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[*]/Label[0].text=='PREFAB'"

    _prop_section = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[*]/Label[0].text=='PROP'"

    _select_resultant_thumbnail = "DRIVE Sim Asset Explorer//Frame/**/ScrollingFrame[0]/HStack[0]/VStack[0]/ThumbnailView[0]/**/Image[0]"

    _search_asset_outliner = "Outliner//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[9]/ZStack[0]/HStack[0]/HStack[0]/object_name"

    _search_outliner_section = "Outliner//Frame/Frame[0]/VStack[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/HStack[0]/StringField[0]"
    
    _view_switch_section = "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[6]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Perspective"

    def click_on_vehicle_section(self, wait_time=180):
        """
        Clicks on vehicle section
        Args:
            wait_time(int): waiting for time until vehicle section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._vehicle_section)
        self.find_and_click(self._vehicle_section, refresh=True)

    def click_on_ego_section(self, wait_time=180):
        """
        Clicks on ego section
        Args:
            wait_time(int): waiting for time until ego section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._ego_section)
        self.find_and_click(self._ego_section, refresh=True)

    def click_on_character_section(self, wait_time=180):
        """
        Clicks on character section
        Args:
            wait_time(int): waiting for time until character section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._character_section)
        self.find_and_click(self._character_section, refresh=True)

    def get_resultant_thumbnail(self):
        """Click on the resultant thumbnail which is visible"""
        return self.omni_driver.find_elements(self._select_resultant_thumbnail)

    def click_on_prefab_section(self, wait_time=180):
        """
        Clicks on prefab section
        Args:
            wait_time(int): waiting for time until prefab section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._prefab_section)
        self.find_and_click(self._prefab_section, refresh=True)

    def click_on_prop_section(self, wait_time=180):
        """
        Clicks on prop section
        Args:
            wait_time(int): waiting for time until prop section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._prop_section)
        self.find_and_click(self._prop_section, refresh=True)
    
    def switch_view(self, option="Top", wait_time=180):
        """This function is to switch the view in viewport"""
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._view_switch_section)
        self.find_and_click(self._view_switch_section, refresh=True)
        self.omni_driver.wait(5)
        view = self._view_switch_section + "/" + option
        wait.element_to_be_located(self.omni_driver,view)
        self.find_and_click(view, refresh=True)

    def navigate_to_outliner_window(self):
        """Navigates to outliner window"""
        outliner_window = self.omni_driver.find_element(self._search_outliner_section)
        outliner_window.click()

    def select_asset(self, name: str):
        """
        Select asset in outliner window
        Args:
            name (str): Name of asset
        """
        asset: OmniElement = self.omni_driver.find_element(self._search_asset_outliner, True)
        self.omni_driver.wait(2)
        attempts = 0
        while not asset.is_selected():
            if attempts >= 3:
                break
            self.log.info(f"Attempting to select asset: {name}")
            asset.click()
            self.omni_driver.wait(1)
            attempts += 1
        assert asset.is_selected(), f"Failed to select asset: '{name}'"
        return asset

    def search_and_select_asset(self, asset_name):
        """
        Search and Select asset in outliner window
        Args:
            asset_name (str): Name of asset
        """
        self.find_and_enter_text(self._search_outliner_section, asset_name)
        self.omni_driver.wait(3)
        return self.select_asset(asset_name)