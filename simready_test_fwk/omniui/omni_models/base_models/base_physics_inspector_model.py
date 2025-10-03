# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Physics Inspector Model class
   This module contains the base methods for Physics Inspector
"""
from ..base_models.base_model import BaseModel


class BasePhysicsInspectorModel(BaseModel):
    """Base model class for Physics Inspector

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _window_name_prefix = "Physics Inspector: "
    _window_name_suffix = "###PhysicsInspector1"

    def is_window_visible(self, stage_object_path):
        """Method to check if Physics Inspector is visible

        Args:
            stage_object_path (str): Stage object path

        Returns:
            bool: True if Physics Inspector is visible"""
        self.omni_driver.wait(2)
        self._window_name = (
            self._window_name_prefix + stage_object_path + self._window_name_suffix
        )
        return self._window_name in self.omni_driver.get_windows()["visible_windows"]

    def get_drive_target_position_info(self):
        """Method to get Drive Target Position info

        Returns:
            dict: Drive Target Position info"""
        _locator = f"{self._window_name}//Frame/**/TreeView[0]/ZStack[1]/FloatSlider[0]"
        _element = self.omni_driver.find_element(_locator)
        return _element.get_size_and_position("all")
