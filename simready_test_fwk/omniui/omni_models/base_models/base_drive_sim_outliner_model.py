# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimOutliner class
   This module contains the base methods for DriveSimOutliner window
"""
from omni_remote_ui_automator.driver.omnielement import OmniElement

from ..base_models.base_model import BaseModel


class BaseDriveSimOutlinerModel(BaseModel):
    """Base model class for DriveSimOutliner window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Stage window
    _window_name = "Drivesim Scenario Outliner"
    _stage_window = _window_name + "//Frame/VStack[0]"
    _light_dropdown = _window_name + "//Frame/Frame[*]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[5]"
    _light_type = _window_name + "//Frame/**/Label[*].text=='__light__'"
    _asset_path = _window_name + "//Frame/**/Label[*].text=='__name__'"
    _asset_path_search_results = _window_name + "//Frame/**/TreeView[1]/**/Label[*].text=='__name__'"
    _asset_search_result_labels = _window_name + "//Frame/**/TreeView[1]/**/Label[*]"
    _stage_label = _window_name + "//Frame/**/TreeView[0]/HStack[6]/**/Label[0]"
    _stage_search = _window_name + "//Frame/VStack[0]/Frame[0]/Frame[0]/VStack[0]/HStack[0]/ZStack[1]/StringField[0]"
    __world_default_prim = _window_name + "//Frame/**/TreeView[0]/**/Label[*].text=='World (defaultPrim)'"
    _looks_expand = _window_name + "//Frame/**/TreeView[0]/HStack[1]"
    _all_images = _window_name + "//Frame/**/TreeView[0]/HStack[*]/Image[0]"
    _expand_environment = _window_name + "//Frame/**/ScrollingFrame[0]/**/TreeView[0]/**/HStack[1]"
    _main_treeview = _window_name + "//Frame/**/TreeView[0]"
    _options_btn = _window_name + "//Frame/**/Button[0].name == 'options'"

    def navigate_to_stage(self):
        """Navigates to stage window"""
        stage_window = self.omni_driver.find_element(self._stage_window)
        stage_window.click()
        self.screenshot("navigated_to_stage")

    def assert_item_exits(self, name: str, search: bool = False):
        """Asserts if a specified item exists in stage

        Args:
            name (str): Asset name
        """
        if search:
            assert self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name)
            ), f"Asset not present in stage Expected: '{name}'"
        else:
            assert self.omni_driver.find_element(
                self._asset_path.replace("__name__", name)
            ), f"Asset not present in stage Expected: '{name}'"
        self.log.info(f"Asset {name} is present in stage")

    def get_stage_label(self):
        element = self.omni_driver.find_element(self._stage_label, refresh=True)
        return element.get_text()

    def select_all_assets(self):
        """Selects all assets in stage"""
        self.find_and_click(self.__world_default_prim)

    def select_asset(self, name: str, search: bool = False):
        """Selects  assets in stage

        Args:
            name (str): Name of asset
            search (bool): True if the asset is to be searched

        Returns:
            OmniElement: Reference of asset item
        """
        if search:
            asset: OmniElement = self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name), True
            )

        else:
            asset: OmniElement = self.omni_driver.find_element(self._asset_path.replace("__name__", name), True)
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

    def search_asset(self, asset_name):
        """Search assets in stage
        Args:
            asset_name (str): Name of asset
        """
        self.find_and_enter_text(self._stage_search, asset_name)
        self.wait.element_to_be_located(
            self.omni_driver,
            locator=self._asset_path_search_results.replace("__name__", asset_name),
        )

    def search_and_select_asset(self, asset_name):
        """Searchs and Selects asset in stage
        Args:
            asset_name (str): Name of asset
        """
        self.search_asset(asset_name)
        self.omni_driver.wait(3)
        return self.select_asset(asset_name, search=True)
