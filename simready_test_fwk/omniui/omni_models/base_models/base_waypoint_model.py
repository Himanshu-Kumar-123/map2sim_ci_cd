# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Waypoint class
   This module contains the base methods for Waypoint Window
"""
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound

from ..base_models.base_model import BaseModel


class BaseWaypointModel(BaseModel):
    """Base Waypoint model class for Waypoint Tool

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _add_waypoint_btn_nav_bar = "Viewport//Frame/**/Button[0].name=='waypoint'"
    _waypoint_manager_window = "Waypoints//Frame/VStack[0]"
    waypoint_list = "Waypoints//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[*]"
    _waypoint_thumbnail = "Waypoints//Frame/**/ScrollingFrame[0]/**/ZStack[{}]/**/ImageWithProvider[0]"
    _waypoint_previous_button = "Waypoints//Frame/**/Button[*].name=='previous'"
    _waypoint_play_button = "Waypoints//Frame/**/Button[*].name=='play'"
    _waypoint_next_button = "Waypoints//Frame/**/Button[*].name=='next'"
    _waypoint_pause_button = "Waypoints//Frame/**/Button[*].name=='pause'"
    _waypoint_label = "Waypoints//Frame/**/Label[0].text == '{}'"
    _waypoint_settings = "Waypoints//Frame/**/ZStack[1]"
    _waypoint_close_button = "Waypoints//Frame/**/ZStack[0]/**/Image[0]"
    _waypoint_collapsable = "Waypoints//Frame/**/ZStack[{}]/VStack[0]/CollapsableFrame[0]"
    specific_waypoint = "Waypoints//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__waypoint__]"
    _waypoint_collapse_bar = (
        "Waypoints//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__waypoint__]/**/CollapsableFrame[0]"
    )
    _edit_waypoint_btn = specific_waypoint + "/**/Button[0].name=='edit'"
    delete_waypoint_btn = specific_waypoint + "/**/Button[*].name=='delete'"

    # Edit operations
    _apply_button = specific_waypoint + "/**/Button[*].name=='apply'"
    _cancel_button = specific_waypoint + "/**/Button[*].name=='cancel'"
    _add_new_button = specific_waypoint + "/**/Button[*].name=='new'"

    # Common locators
    add_waypoint_button = "Waypoints//Frame/**/Button[0].name=='add_waypoint'"
    _waypoint_name_field = "Waypoints//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__waypoint__]/**/StringField[0]"
    _rename_waypoint_context_menu = "Rename Waypoint"
    _add_waypoint_btn_nav_bar = "Viewport//Frame/**/Button[0].name=='waypoint'"
    _waypoints_window = "Waypoints"

    @property
    def waypoints_length(self):
        """Returns Number of Waypoints"""
        try:
            return len(self.omni_driver.find_elements(self.waypoint_list))
        except ElementNotFound:
            return 0

    def get_notes_collapsable(self, name: str):
        """Returns Collapsable Frame of the Waypoint

        Args:
        name(str): Name of the Waypoint
        """
        _, index = self.get_child_element(self.waypoint_list, f"**/Label[0].text == '{name}'")
        return self.omni_driver.find_element(self._waypoint_collapsable.format(index), refresh=True)

    def add_waypoint(self):
        """Adds a new waypoint to the current scene in viewport"""
        old_len = self.waypoints_length
        self.log.info(f"Current Waypoint Length: {old_len}")
        waypoint_btn = self.omni_driver.find_element(self.add_waypoint_button)
        new_len = 0
        self.omni_driver.wait(1)
        waypoint_btn.click()
        self.omni_driver.wait(1)
        new_len = self.waypoints_length
        assert new_len - old_len == 1, f"Failed to add Waypoint, Expected: {old_len+1}, Actual: {new_len}"
        self.log.info("Added new waypoint")

    def enable_waypoint_manager(self):
        """Enables waypoint manager"""

        try:
            win = self.omni_driver.find_element(self._waypoint_manager_window)
            if win.get_widget_center() == (0, 0):
                assert False, "Waypoint manager window not visible"
        except AssertionError:
            waypoint_btn = self.omni_driver.find_element(self._add_waypoint_btn_nav_bar)
            waypoint_btn.right_click()

    def navigate_to_last_waypoint(self):
        waypoints_after = self.omni_driver.find_elements(self.waypoint_list)
        waypoint = self.find_and_scroll_element_into_view(
            self.waypoint_list.replace("ZStack[*]", f"ZStack[{len(waypoints_after)-1}]"),
            ScrollAxis.Y,
            ScrollAmount.CENTER,
        )
        waypoint.click()

    def navigate_to_waypoint(self, num: int):
        waypoint = self.find_and_scroll_element_into_view(
            self.waypoint_list.replace("ZStack[*]", f"ZStack[{num}]"),
            ScrollAxis.Y,
            ScrollAmount.CENTER,
        )
        waypoint.click()

    def verify_note(self, name: str, note: str):
        """Verify note of a given waypoint

        Args:
        name(str): Name of Waypoint
        note(str): text to be verified
        """
        frame = self.get_notes_collapsable(name)
        if frame.is_collapsed():
            frame.click()
        text_input = frame.find_element("**/StringField[0]")
        assert text_input.get_text() == note, f"Note is invalid, Expected: {note}, Actual: {text_input.get_text()}"

    def go_to_waypoint(self, name: str):
        """Clicks on specific waypoint from the list

        Args:
        name(str): Waypoint name
        """
        _, index = self.get_child_element(self.waypoint_list, f"**/Label[0].text == '{name}'")
        thumbnail = self.omni_driver.find_element(self._waypoint_thumbnail.format(index), True)
        thumbnail.click()
        self.omni_driver.wait(1)

    def add_waypoint_note(self, name: str, note: str):
        """Adds note to the waypoint

        Args:
        name(str): Waypoint name
        note(str): Note to be added
        """
        frame = self.get_notes_collapsable(name)
        if frame.is_collapsed():
            frame.click()
        text_input = frame.find_element("**/StringField[0]")
        text_input.click()
        self.omni_driver.emulate_char_press(note)
        self.go_to_waypoint(name)
        self.screenshot(f"{name}_note")
        self.log.info("[WaypointTool] Added Note {%s} for {%s}", name, note)

    def open_previous_waypoint(self):
        """Navigate to Previous Waypoint"""
        self.omni_driver.find_element(self._waypoint_previous_button, True).click()
        self.omni_driver.wait_for_stage_load()

    def play_waypoints(self):
        """Play Waypoint Playlist"""
        self.omni_driver.find_element(self._waypoint_play_button, True).click()
        self.omni_driver.wait_for_stage_load()

    def pause_waypoints(self):
        """Pause Waypoint Playlist"""
        self.omni_driver.find_element(self._waypoint_pause_button, True).click()
        self.omni_driver.wait_for_stage_load()

    def open_next_waypoint(self):
        """Navigate to Next Waypoint"""
        self.omni_driver.find_element(self._waypoint_next_button, True).click()
        self.omni_driver.wait_for_stage_load()

    def rename_waypoint(self, name: str, rename_to: str):
        """Rename the Waypoint
        Args:
        name(str): waypoint name
        rename_to(str): New name"""
        label = self.omni_driver.find_element(self._waypoint_label.format(name), True)
        self.log.info("[Waypoint Manager] Right-Clicking on Waypoint Name")
        label.right_click()
        self.omni_driver.select_context_menu_option("Rename Waypoint")
        self.log.info("[Waypoint Manager] Sending new name to input field")
        self.omni_driver.emulate_char_press(rename_to)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def collapse_note(self, name: str):
        """Collapses note of given waypoint"""
        self.find_and_click(self._waypoint_label.format(name))

    def close(self):
        """Closes Waypoint Manager"""
        self.find_and_click(self._waypoint_close_button)

    def delete_waypoint(self, waypoint_num: int):
        """Deletes waypoint from the list

        Args:
        waypoint_num(int): Waypoint number in the list
        """
        self.find_and_scroll_element_into_view(
            self.specific_waypoint.replace("__waypoint__", str(waypoint_num - 1)),
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        delete_btn = self.omni_driver.find_element(
            self.delete_waypoint_btn.replace("__waypoint__", str(waypoint_num - 1))
        )
        center = delete_btn.get_widget_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        delete_btn.click()

    def edit_waypoint(self, waypoint_num: int):
        """Edit waypoint from the list

        Args:
        waypoint_num(int): Waypoint number in the list
        """
        self.find_and_scroll_element_into_view(
            self.specific_waypoint.replace("__waypoint__", str(waypoint_num - 1)),
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        edit_btn = self.omni_driver.find_element(self._edit_waypoint_btn.replace("__waypoint__", str(waypoint_num - 1)))
        center = edit_btn.get_widget_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        edit_btn.click()

    def apply_changes(self, waypoint_num: int):
        """Apply changes in edit mode

        Args:
        waypoint_num(int): Waypoint number in the list
        """
        self.find_and_click(self._apply_button.replace("__waypoint__", str(waypoint_num - 1)))
        self.omni_driver.wait(1)

    def add_new_waypoint(self, waypoint_num: int):
        """Apply changes in edit mode

        Args:
        waypoint_num(int): Waypoint number in the list"""
        self.find_and_click(self.add_waypoint_button)
        self.omni_driver.wait(1)

    def cancel_edit_mode(self, waypoint_num: int):
        """Apply changes in edit mode

        Args:
        waypoint_num(int): Waypoint number in the list"""
        self.find_and_click(self._cancel_button.replace("__waypoint__", str(waypoint_num - 1)))
        self.omni_driver.wait(1)

    def is_edit_mode_visible(self, waypoint_num: int):
        """Returns whether edit mode is enabled

        Args:
        waypoint_num(int): Waypoint number in the list"""
        edit_operations = [
            self.omni_driver.find_element(
                self._cancel_button.replace("__waypoint__", str(waypoint_num - 1)), True
            ).is_checked(),
            self.omni_driver.find_element(
                self._add_new_button.replace("__waypoint__", str(waypoint_num - 1)),
                True,
            ).is_checked(),
            self.omni_driver.find_element(
                self._apply_button.replace("__waypoint__", str(waypoint_num - 1)), True
            ).is_checked(),
        ]
        self.log.info("Operations visibility: %s", edit_operations)
        return all(edit_operations)

    def verify_waypoint_added(self, prev_count: int):
        waypoints_after = self.omni_driver.find_elements(self.waypoint_list)
        assert len(waypoints_after) == prev_count + 1, "New waypoint was not created."

    def verify_waypoint_deleted(self, prev_count: int):
        waypoints_after = self.omni_driver.find_elements(self.waypoint_list)
        assert len(waypoints_after) == prev_count - 1, "Waypoint was not deleted."

    def get_waypoint_count(self):
        waypoints = self.omni_driver.find_elements(self.waypoint_list)
        return len(waypoints)

    def rename_waypoint(self, waypoint_num: int, new_name: str):
        """Rename the Waypoint
        Args:
        waypoint_num(str): waypoint index
        new_name(str): New name"""
        self.find_and_scroll_element_into_view(
            self.specific_waypoint.replace("__waypoint__", str(waypoint_num - 1)), ScrollAxis.Y, ScrollAmount.TOP
        )
        waypoint = self.omni_driver.find_element(
            self._waypoint_collapse_bar.replace("__waypoint__", str(waypoint_num - 1))
        )
        self.omni_driver.wait(1)
        waypoint.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option(self._rename_waypoint_context_menu)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(new_name)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.enter)
        self.omni_driver.wait(2)

    def verify_waypoint_with_name_exists(self, waypoint_name: str):
        """Verifies whether waypoint with given name exists or not

        waypoint_name(str): name of waypoint
        """
        self.omni_driver.wait(1)
        assert self.omni_driver.find_elements(
            self._waypoint_label.format(waypoint_name)
        ), f"No waypoint exists with name {waypoint_name}"

    def toggle_waypoint_manager(self, enable=True):
        """Toggles waypoint Mode

        Args:
        enable(bool): Bool value to enable waypoint Mode"""
        element = self.omni_driver.find_element(self._add_waypoint_btn_nav_bar, refresh=True)
        current_state = self._waypoints_window in self.omni_driver.get_windows()["visible_windows"]
        self.screenshot("previous_waypoint_manager_state")
        self.log.info("waypoint manager_state is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching waypoint manager_state")
            element.click()
        self.screenshot("current_waypoint_manager_state")
        assert enable == (
            self._waypoints_window in self.omni_driver.get_windows()["visible_windows"]
        ), "Failed to toggle waypoint bar"

    def is_waypoint_manager_visible(self) -> bool:
        """Gets the visibility of the waypoint manager window
        Retuns:
            bool
        """
        return self._waypoints_window in self.omni_driver.get_windows()["visible_windows"]

    def waypoint_manager_current_status(self):
        """Returns waypoint Mode current status"""
        element = self.omni_driver.find_element(self._add_waypoint_btn_nav_bar, True)
        current_state = element.tool_button_is_checked()
        self.screenshot("current_waypoint_manager_state")
        return current_state
