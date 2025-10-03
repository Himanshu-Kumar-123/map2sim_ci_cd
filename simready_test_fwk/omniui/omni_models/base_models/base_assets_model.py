# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Assets Model class
   This module contains the base methods for Assets window
"""
import random
from omni_remote_ui_automator.driver.waits import Wait
from ..base_models.base_model import BaseModel


class BaseAssetsModel(BaseModel):
    """Base model class for Assets window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _assets_window = "NVIDIA Assets//Frame/VStack[0]"
    all_assets = "NVIDIA Assets//Frame/**/ThumbnailView[0]/Frame[*]/HStack[0]"
    _assets_slider = "NVIDIA Assets//Frame/**/IntSlider[0]"
    _loading_spinner = "NVIDIA Assets//Frame/**/SceneView[*]"
    _all_category_btn = "NVIDIA Assets//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[1]/Label[0]"
    _search_asset_field = "NVIDIA Assets//Frame/**/HStack[0]/StringField[0]"
    _asset_label = "NVIDIA Assets//Frame/**/ThumbnailView[0]/**/Label[0].text=='{}'"

    def navigate_to_assets(self, timeout=120):
        """Navigates to assets window"""
        assets_window = self.omni_driver.find_element(self._assets_window)
        assets_window.click()
        self.screenshot("navigated_to_assets")
        wait = Wait(timeout=timeout)
        wait.element_to_be_invisible(self.omni_driver, self._loading_spinner)

    def select_asset_and_drop_to_position(self, position):
        """Selects asset from window and drag to viewport center

        Args:
            position (Float): X and Y position of destination co ordinate

        Returns:
            Asset Name: Returns the asset name
        """
        assets = self.omni_driver.find_elements(self.all_assets)
        rand_value = random.randrange(0, len(assets))
        assets_label = assets[rand_value].find_element("**/Label[0]").get_text()
        self.set_asset_slider()
        assets[rand_value].drag_and_drop(position[0], position[1])
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
        self.screenshot("asset_drag_and_dropped")
        return assets_label

    def select_asset_and_double_click(self):
        """Selects asset from window and double clicks on it

        Returns:
            Material Name: Returns the material name of applied material
        """
        assets = self.omni_driver.find_elements(self.all_assets)
        rand_value = random.randrange(0, len(assets))
        assets_label = assets[rand_value].find_element("**/Label[0]").get_text()
        self.set_asset_slider()
        self.omni_driver.wait_frames(5)
        assets[rand_value].double_click()
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(300)
        return assets_label

    def add_asset_webrtc(self):
        """Navigates to assets window"""
        assets = self.omni_driver.find_elements(self.all_assets)
        rand_value = 4
        # assets_label = assets[rand_value].find_element("**/Label[0]").get_text()
        # self.omni_driver.find_element(self._assets_slider).send_keys(5)
        # self.omni_driver.wait(2)
        # self.omni_driver.wait_for_stage_load()
        # self.omni_driver.wait_frames(5)
        return assets[rand_value].get_widget_center()

    def set_asset_slider(self, set_value: int = 5):
        """Set asset window slider

        Args:
            set_value (int): Value to set
        """
        self.omni_driver.find_element(self._assets_slider).send_keys(set_value)
        self.omni_driver.wait(2)
        self.omni_driver.find_element(self._assets_slider).send_keys(set_value)
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
    
    def add_asset_by_double_click(self, asset_name: str):
        """Finds the asset under all category and add it to viewport by double click

        Args:
        asset_name(str): name of the asset
        """
        self._select_all_category()
        self.omni_driver.wait(1)
        search_example_scene = self.omni_driver.find_element(self._search_asset_field, True)
        search_example_scene.send_keys(asset_name)
        asset_locator = self._asset_label.format(asset_name)
        asset_label = self.wait.element_to_be_located(self.omni_driver, asset_locator)
        asset_label.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
        self.screenshot("add_asset_by_double_click")
        return asset_label

    def add_asset_by_double_click(self, asset_name: str):
        """Finds the asset under all category and add it to viewport by double click

        Args:
        asset_name(str): name of the asset
        """
        self._select_all_category()
        self.omni_driver.wait(1)
        search_example_scene = self.omni_driver.find_element(self._search_asset_field, True)
        search_example_scene.send_keys(asset_name)
        asset_locator = self._asset_label.format(asset_name)
        asset_label = self.wait.element_to_be_located(self.omni_driver, asset_locator)
        asset_label.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
        self.screenshot("add_asset_by_double_click")
        return asset_label

    def search_and_drop_asset_from_all(self, asset_name: str, position: tuple):
        """Finds the asset under all category and add it to viewport

        Args:
        asset_name(str): name of the asset
        position(tuple): position in viewport
        """
        self._select_all_category()
        self.omni_driver.wait(1)
        search_example_scene = self.omni_driver.find_element(self._search_asset_field, True)
        search_example_scene.send_keys(asset_name)
        asset_locator = self._asset_label.format(asset_name)
        asset_label = self.wait.element_to_be_located(self.omni_driver, asset_locator)
        asset_label.drag_and_drop(position[0], position[1])
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
        self.screenshot("asset_drag_and_dropped")
        return asset_label

    def _select_all_category(self):
        """Select ALL submenu from NVIDIA Assets window"""
        all_category_btn = self.omni_driver.find_element(self._all_category_btn)
        all_category_btn.double_click()
        self.log_info_with_screenshot("Navigated to All Category", "navigated_to_all_category")
