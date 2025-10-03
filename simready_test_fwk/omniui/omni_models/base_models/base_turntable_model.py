# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Turntable model class
   This module contains the base methods for Turntable Model for actions to perform
"""
import os
from ..base_models.base_model import BaseModel



class BaseTurntableModel(BaseModel):
    """BaseTurntableModel class containing common methods"""

    # Widget Locators
    _turntable_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/ZStack[0]/Placer[0]"
    _speed_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/HStack[0]/ZStack[0]/Placer[1]"
    _backward_rotate_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/HStack[0]/ZStack[1]/Placer[1]"
    _forward_rotate_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/HStack[0]/ZStack[2]/Placer[1]"
    _close_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/ZStack[1]/Placer[1]"
    _turntable_text = "Turntable//Frame/**/Label[0].text=='Select object(s) to put on turntable'"
    _ok_btn = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/HStack[0]/ZStack[0]/Placer[0]"
    _circle = "Turntable//Frame/**/OpaqueZStack[0]/Placer[1]/Circle[0].name == 'cursor'"
    _slider = "Turntable//Frame/ZStack[0]/VStack[0]/HStack[0]/HStack[0]/OpaqueZStack[0]/Placer[1]"

    def close_turntable_toolbar(self):
        """
        Close the turntable toolbar
        """
        close_btn_element = self.omni_driver.find_element(self._close_btn)
        close_btn_element.click()
        self.omni_driver.wait(2)

    def change_speed(self, speed):
        """
        Updates the rotation speed
        Args:
            speed: Rotation Speed to be set
        """
        speed_btn_element = self.omni_driver.find_element(self._speed_btn)
        match_speed = False
        retry = 6

        while not match_speed and retry > 0:
            speed_btn_element.click()
            self.omni_driver.wait(2)
            new_speed = self.get_current_speed
            self.omni_driver.wait(2)
            match_speed = new_speed == speed
            retry -= 1
        if retry == 0:
            self.log.error(f"Failed to change speed to {speed}")
            raise RuntimeError(f"Failed to change speed to {speed}")

    @property
    def get_current_speed(self):
        """
        Finds the current speed of the Turntable
        Returns: Speed of the Turntable
        """
        speed_btn_element = self.omni_driver.find_element(self._speed_btn + "/Image[0]",
                                                          refresh=True)
        source = speed_btn_element.image_source()
        speed = os.path.split(source)[-1].split('_')[1]
        return speed

    @property
    def is_displayed(self):
        """Returns whether turntable toolbar is displayed"""
        return self.omni_driver.find_element(self._turntable_text).is_visible()

    def approve_turntable_selection(self):
        """Approves the turntable selection"""
        ok_btn_element = self.omni_driver.find_element(self._ok_btn)
        ok_btn_element.click()
        self.omni_driver.wait(2)

    def click_rotate(self, forward=True):
        """Clicks the forward rotate button by default
        Args:
            forward(bool): True for forward rotate, False for backward rotate
        """
        if forward:
            rotate_btn_element = self.omni_driver.find_element(self._forward_rotate_btn)
        else:
            rotate_btn_element = self.omni_driver.find_element(self._backward_rotate_btn)
        rotate_btn_element.click()
        self.omni_driver.wait(2)

    def click_pause(self, forward=True):
        """Clicks the pause button"""
        locator = self._forward_rotate_btn if forward else self._backward_rotate_btn
        pause_btn_element = self.omni_driver.find_element(locator)
        pause_btn_element.click()
        self.omni_driver.wait(2)

    def rotate_by_slider(self, direction="left"):
        """Rotates the object by slider"""
        circle = self.omni_driver.find_element(self._circle)
        circle_center = circle.get_widget_center()
        rectangle = self.omni_driver.find_element(self._slider)
        x1_to = rectangle.get_size_and_position("screen_position_x")
        if direction == "left":
            self.omni_driver.drag_from_and_drop_to(circle_center[0], circle_center[1], x1_to,
                                                   circle_center[1])
            self.omni_driver.wait(2)
        else:
            x2_to = x1_to + rectangle.get_size_and_position("computed_width")
            self.omni_driver.drag_from_and_drop_to(circle_center[0], circle_center[1], x2_to,
                                                   circle_center[1])
            self.omni_driver.wait(2)
