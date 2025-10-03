# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Zero Gravity Model class
   This module contains the base methods for Zero Gravity
"""
import os
from omni_remote_ui_automator.driver.exceptions import ElementNotFound

from ..base_models.base_model import BaseModel


class BaseZeroGravityModel(BaseModel):
    """Base model class for Zero Gravity

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _window_name = "Zero Gravity"
    _dynamic_btn_locator = _window_name + "//Frame/VStack[0]/VStack[0]/Button[2]"
    _drop_selected_asset_btn_locator = (
        _window_name + "//Frame/VStack[0]/VStack[0]/Button[3]"
    )
    _sweep_mode_btn_locator = _window_name + "//Frame/VStack[0]/VStack[0]/Button[4]"
    _sweep_mode_active_svg = "sweep_stop.svg"
    _sweep_mode_inactive_svg = "sweep_start.svg"

    def is_window_visible(self) -> bool:
        """Method to check if Zero Gravity Toolbar is visible

        Returns:
            bool indicating Zero Gravity Toolbar visibility"""
        self.omni_driver.wait(2)
        return self._window_name in self.omni_driver.get_windows()["visible_windows"]

    def is_sweep_mode_active(self):
        """Method to check if sweep mode is active"""
        _sweep_mode_btn_element = self.omni_driver.find_element(
            self._sweep_mode_btn_locator, refresh=True
        )
        _sweep_mode_img_src = os.path.split(_sweep_mode_btn_element.image_source())[-1]
        return _sweep_mode_img_src == self._sweep_mode_active_svg

    def is_sweep_mode_button_visible(self):
        """Method to check if sweep mode button is visible"""
        try:
            self.omni_driver.find_element(self._sweep_mode_btn_locator, refresh=True)
            self.log.info("Sweep mode button is visible")
            return True
        except ElementNotFound:
            self.log.info("Sweep mode button is not visible")
            return False

    def toggle_sweep_mode(self):
        """Method to toggle sweep mode"""
        current_sweep_mode = self.is_sweep_mode_active()
        self.log.info(f"Current sweep mode is {str(current_sweep_mode).lower()}")
        self.omni_driver.find_element(
            self._dynamic_btn_locator, refresh=True
        ).get_widget_center()
        self.omni_driver.find_element(
            self._drop_selected_asset_btn_locator, refresh=True
        ).get_widget_center()
        _sweep_mode_btn_element = self.omni_driver.find_element(
            self._sweep_mode_btn_locator, refresh=True
        )
        _sweep_mode_btn_element.get_widget_center()
        _sweep_mode_btn_element.click()
        self.omni_driver.wait(2)
        new_sweep_mode = self.is_sweep_mode_active()
        self.log_info_with_screenshot(f"sweep_mode_{str(new_sweep_mode).lower()}")
