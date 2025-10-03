# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Physics Authoring Toolbar Model class
   This module contains the base methods for Physics Authoring Toolbar
"""
from enum import Enum
import os

from ..base_models.base_model import BaseModel


class BasePhysicsAuthoringToolbarModel(BaseModel):
    """Base model class for Physics Authoring Toolbar

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _window_name = "Physics Authoring"
    _physics_authoring_toolbar = "Physics Authoring//Frame/VStack[0]"
    _toolbar_all_buttons = "Physics Authoring//Frame/**/Button[*]"

    _rigid_body_selection = "Physics Authoring//Frame/VStack[0]/VStack[0]/Button[0]"

    _remove_physics = "Physics Authoring//Frame/VStack[0]/VStack[0]/Button[1]"
    _set_static_collider = (
        "Physics Authoring//Frame/VStack[0]/VStack[0]/ZStack[0]/Button[0]"
    )
    _set_dynamic_collider = (
        "Physics Authoring//Frame/VStack[0]/VStack[0]/ZStack[1]/Button[0]"
    )
    _automatic_collider_generation = (
        "Physics Authoring//Frame/VStack[0]/VStack[0]/Button[2]"
    )
    _mass_distribution_manipulator = (
        "Physics Authoring//Frame/VStack[0]/VStack[0]/Button[3]"
    )
    _settings_main = "Physics Authoring//Frame/VStack[0]/VStack[0]/Button[4]"

    class Buttons(Enum):
        """Enum class for all buttons in Physics Authoring Toolbar"""

        RIGID_BODY_SELECTION = "Rigid Body Selection"
        REMOVE_PHYSICS = "Remove Physics"
        SET_STATIC_COLLIDER = "Set Static Collider"
        SET_DYNAMIC_COLLIDER = "Set Dynamic Collider"
        AUTOMATIC_COLLIDER_GENERATION = "Automatic Collider Generation"
        MASS_DISTRIBUTION_MANIPULATOR = "Mass Distribution Manipulator"

    class Settings(Enum):
        """Enum class for all Settings in Physics Authoring Toolbar"""

        PHYSICS_INSPECTOR = "Physics Inspector"

    def is_window_visible(self):
        """Method to check if Physics Authoring Toolbar is visible"""
        self.omni_driver.wait(2)
        return self._window_name in self.omni_driver.get_windows()["visible_windows"]

    def get_button_tooltip_and_images(self):
        """Method to get Tooltip and Images data"""
        # TODO Add Tooltip data
        self.log.warning(
            "Tooltip data check is yet to be implemented for Physics Authoring Toolbar"
        )
        _all_buttons = self.omni_driver.find_elements(self._toolbar_all_buttons)
        ret_data = {}
        for index, _current_button in enumerate(_all_buttons):
            ret_data[str(index)] = {}
            ret_data[str(index)]["tooltip"] = str(index)
            ret_data[str(index)]["img_src"] = os.path.split(
                _current_button.image_source()
            )[-1]
        return ret_data

    def toggle_button_status(self, button: Buttons, status: bool):
        """
        Method to toggle buttons in Physics Authoring Toolbar

        Args:
            button_name (Buttons): Enum value of button to be toggled
            status (bool): Boolean to set status of button
        """
        _button_locator = None
        if button == self.Buttons.RIGID_BODY_SELECTION:
            _button_locator = self._rigid_body_selection
        elif button == self.Buttons.REMOVE_PHYSICS:
            _button_locator = self._remove_physics
        elif button == self.Buttons.SET_STATIC_COLLIDER:
            _button_locator = self._set_static_collider
        elif button == self.Buttons.SET_DYNAMIC_COLLIDER:
            _button_locator = self._set_dynamic_collider
        elif button == self.Buttons.AUTOMATIC_COLLIDER_GENERATION:
            _button_locator = self._automatic_collider_generation
        elif button == self.Buttons.MASS_DISTRIBUTION_MANIPULATOR:
            _button_locator = self._mass_distribution_manipulator

        _button_element = self.omni_driver.find_element(_button_locator)
        self.omni_driver.emulate_mouse_move(*_button_element.get_widget_center())
        self.omni_driver.wait(2)
        if _button_element.is_checked() ^ status:
            _button_element.click()
        self.log_info_with_screenshot(f"{button.name.lower()}_{str(status).lower()}")

    def toggle_settings(self, setting_name: Settings, status: bool):
        """
        Method to toggle Settings in Physics Authoring Toolbar

        Args:
            setting_name (Settings): Enum value of setting to be toggled
            status (bool): Boolean to set status of setting
        """
        _button_element = self.omni_driver.find_element(self._settings_main)
        _button_element.click()
        self.omni_driver.wait(2)

        _setting_label = self.omni_driver.find_element(
            f"SupportUI Settings//Frame/**/Label[*].text=='{setting_name.value}'"
        )
        _setting_checkbox = self.omni_driver.find_element(
            f"{_setting_label.find_parent_element_path()}/**/CheckBox[0]"
        )
        if _setting_checkbox.is_checked() ^ status:
            _setting_checkbox.click()
        self.log_info_with_screenshot(
            f"{setting_name.value.lower()}_{str(status).lower()}"
        )
