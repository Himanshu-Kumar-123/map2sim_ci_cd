"""Property Model class
   This module contains the base methods for Property Window
"""
import random
from omni_remote_ui_automator.common.constants import KeyboardConstants
from ..base_models.base_property_model import BasePropertyModel


class PropertyModel(BasePropertyModel):
    """Property model class for Property Window

    Args:
        BasePropertyModel: BasePropertyModel class parent to
        Property window class.
    """

    transform_translate_x = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[0]/HStack[1]/HStack[0]/HStack[0]/ZStack[1]/value"
    transform_translate_y = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[0]/HStack[1]/HStack[0]/HStack[1]/ZStack[1]/value"
    transform_translate_z = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[0]/HStack[1]/HStack[0]/HStack[2]/ZStack[1]/value"
    _tranform_rotate_x = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[__index__]/HStack[0]/HStack[0]/HStack[0]/ZStack[1]/value"
    _tranform_rotate_y = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[__index__]/HStack[0]/HStack[0]/HStack[1]/ZStack[1]/value"
    _tranform_rotate_z = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/frame_v_stack/HStack[__index__]/HStack[0]/HStack[0]/HStack[2]/ZStack[1]/value"

    def transform_translate(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z translate values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        self._add_transform_if_not_present()
        if x is not None:
            self.set_transform_values(x, self.transform_translate_x)
        if y is not None:
            self.set_transform_values(y, self.transform_translate_y)
        if z is not None:
            self.set_transform_values(z, self.transform_translate_z)
        self.log_info_with_screenshot(
            "All translate values set.", "translate_values_set"
        )

    def set_transform_values(self, coord_value, locator):
        """
        Enters a random value in transform edit boxes if not value is provided
        Args:
            coord_value (int, optional): Value to input. Defaults to 0.
            locator (str): Locator of coordinate to set.
        Returns:
            None
        """
        coord_element = self.omni_driver.find_element(locator, refresh=True)
        coord_element.double_click()
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_press(KeyboardConstants.backspace)
        self.omni_driver.wait(1)
        if coord_value is None:
            rand_value = random.randrange(0, 100)
            coord_element.send_keys(rand_value)
        else:
            coord_element.send_keys(coord_value)

    def transform_rotate(self, rotate_value: list, widget_index: int = 1):
        """Adds X, Y and Z rotate values
        :param rotate_value: list containing x, y and z values
        :param widget_index: index of 'Rotate' section in 'Transform' collapsable"""
        if len(rotate_value) != 3:
            assert (
                False
            ), f"Please send X, Y and Z values for Rotation. Received was {rotate_value}"
        self._open_transform_settings()
        self.set_transform_values(rotate_value[0], self._tranform_rotate_x.replace("__index__", f"{widget_index}"))
        self.set_transform_values(rotate_value[1], self._tranform_rotate_y.replace("__index__", f"{widget_index}"))
        self.set_transform_values(rotate_value[2], self._tranform_rotate_z.replace("__index__", f"{widget_index}"))
        self.log_info_with_screenshot("added_rotation_values")
