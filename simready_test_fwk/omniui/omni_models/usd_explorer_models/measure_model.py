# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

""" Measure Modal class
   This module contains the methods for Measure Window
"""
from omni_remote_ui_automator.common.enums import MeasureMode
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


from ..base_models.base_measure_model import BaseMeasureModel
from omniui.framework_lib.softassert import SoftAssert


class MeasureModel(BaseMeasureModel):
    """Measure model class for Measure Tool

    Args:
        MeasureModel (BaseMeasureModel): BaseMeasureModel class is base class for measure window
    """

    _navigation_bar_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[0]"
    _measure_btn_navbar = "Viewport//Frame/**/Button[0].name=='measure'"
    _measure_window = "Measure"

    def _get_checkbox_widget(self, locator: str):
        """Returns Checkbox widget

        Args:
        locator(str): locator of Label
        """
        label = self.omni_driver.find_element(locator, True)
        checkbox = self.omni_driver.find_element(label.find_parent_element_path() + "/RadioButton[0]", True)
        return checkbox

    def _click_snap_mode(self, element_ref: OmniElement):
        """Clicks on the snap selection box"""
        element_ref.click()

    def verify_ui_layout_initial_state(self):
        """
        Verifies UI layout Initial State

        Verifies:
        1. Initial state of toolbar window
        2. Check visibility of Placement Tab
        3. Check collapsable frame functionality
        """
        assertion = SoftAssert()
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(MeasureMode.POINT_TO_POINT.value))
        assertion.expect(
            measure_tool.tool_button_is_checked(),
            f"Measure Mode: {MeasureMode.POINT_TO_POINT.value} is not checked by default",
        )
        for mode in list(MeasureMode)[1:-1]:
            measure_tool = self.omni_driver.find_element(self._measure_mode.format(mode.value))
            assertion.expect(
                not measure_tool.tool_button_is_checked(),
                f"Measure Mode: {mode.name} is checked by default",
            )
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(MeasureMode.SELECTED_MEASURE.value))
        assertion.expect(
            not measure_tool.is_enabled(),
            f"Measure Mode: {MeasureMode.SELECTED_MEASURE.name} is enabled by default",
        )
        placement_tab = self.omni_driver.find_element(self._placement_tab)
        assertion.expect(placement_tab.is_visible(), "Placement tab is not visible by default")
        display_tab = self.omni_driver.find_element(self._display_tab)
        assertion.expect(display_tab.is_visible(), "Display tab is not enabled by default")
        manage_tab = self.omni_driver.find_element(self.manage_tab)
        assertion.expect(manage_tab.is_visible(), "Manage tab is not enabled by default")
        assertion.expect(not placement_tab.is_collapsed(), "Placement Tab is collapsed")
        assertion.expect(not display_tab.is_collapsed(), "Display Tab is collapsed")
        assertion.expect(not manage_tab.is_collapsed(), "Manage Tab is collapsed")
        placement_tab.find_element('**/Label[0].text=="Placement"').double_click()
        display_tab.find_element('**/Label[0].text=="Display"').click()
        manage_tab.find_element('**/Label[0].text=="Manage"').click()
        assertion.expect(placement_tab.is_collapsed(), "Placement Tab is not collapsed")
        assertion.expect(display_tab.is_collapsed(), "Display Tab is not collapsed")
        assertion.expect(manage_tab.is_collapsed(), "Manage Tab is not collapsed")
        assertion.assert_all()

    def get_measure_value(self, index: int):
        """Returns measure value

        Args:
        index(int): Index of the list item starting from 0
        """
        measure = self.wait.element_to_be_located(self.omni_driver, self.measure_value.format(6 + index))
        return measure.get_text()

    def toggle_measure_mode(self, enable=True, pos_x: float = 900, pos_y=300):
        """Toggles Measure mode
        Args:
            enable(bool): Bool value to enable Measure Mode
            pos_x (float): X coordinate to be set for the Measure Window
            pos_y (float): Y coordinate to be set for the Measure Window
        """
        try:
            element = self.omni_driver.find_element(self._measure_btn_navbar, True)
        except ElementNotFound:
            self.find_and_click(self._navigation_bar_btn, refresh=True)
            element = self.omni_driver.find_element(self._measure_btn_navbar, True)

        current_state = self._measure_window in self.omni_driver.get_windows()["visible_windows"]
        self.screenshot("previous_measure_window_state")
        self.log.info("Measure tool state is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching Measure mode")
            element.click()
        self.screenshot("current_measure_window_state")
        assert enable == (
            self._measure_window in self.omni_driver.get_windows()["visible_windows"]
        ), "Failed to toggle Measure Window"

        if enable:
            measure_window: OmniElement = self.omni_driver.find_element(self._measure_window, True)
            measure_window.set_window_position(pos_x, pos_y)
