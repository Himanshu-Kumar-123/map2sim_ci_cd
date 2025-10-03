# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Model class
   This module contains the base methods for Omnidriver
"""
import datetime
import math
import os
import logging
import random
import subprocess
import sys
import time
import re
from typing import Tuple
from omni_remote_ui_automator.common.enums import DockPosition
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.omnidriver import OmniDriver
from omni_remote_ui_automator.driver.waits import Wait
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
import pyautogui
from pxr import Usd
from omniui.utils.utility_functions import (
    get_images_dir,
    connect_to_nucleus_server,
    get_nucleus_server_url_and_user,
    get_value_from_json,
)


class BaseModel:
    """Base Model class containing common methods for all window models"""

    def __init__(self, omni_driver, wait_timeout=60, polling_frequency=0.5, **kwargs):
        self.omni_driver: OmniDriver = omni_driver
        self.ss_dir = os.getcwd() + "/" + get_images_dir()
        self.log = kwargs.get("logger", None)
        if self.log is None:
            self.log = logging.getLogger()
        self.wait = Wait(wait_timeout, polling_frequency)
        self.glyph_codes = dict()
        self.cloud = get_value_from_json("app_type")

    def _updated_path(self, omniverse_path: str):
        """Segregates the  path"""
        input_path = omniverse_path
        if not input_path.startswith("omniverse://"):
            input_path = "omniverse://" + input_path
        input_path = input_path.replace("127.0.0.1/", "localhost/")
        self.log.info(
            "[BaseContentModel][_updated_path] %s -> %s", omniverse_path, input_path
        )
        return input_path

    def screenshot(
        self,
        name: str,
        file_format="png",
        verify=False,
        timeout=10,
        download: bool = False,
    ):
        """Method to take screenshot of entire screen

        Args:
            name (str): Name of image file
            file_format (str, optional): File format to be used for saving. Defaults to "png".
            verify (bool, optional): Should file path be verified.
            timeout (float, optional): maximum polling interval
        """
        if name.endswith(f".{file_format}"):
            path = os.path.join(self.ss_dir, name)
        else:
            path = os.path.join(self.ss_dir, f"{name}.{file_format}")
        self.omni_driver.screenshot(path, download)
        if verify:
            end = time.time() + timeout
            while time.time() < end:
                if os.path.isfile(path):
                    self.log.info(
                        f"Captured screenshot and saved at {path} Verified in {timeout - (end + time.time())} secs"
                    )
                    return
            else:
                raise FileNotFoundError(
                    f"File with path {path} could not be located within {timeout} seconds."
                )

    def viewport_screenshot(
        self,
        name: str,
        download: bool = False,
        file_format="png",
        verify=False,
        timeout=10,
    ):
        """Method for taking screenshot of viewport

        Args:
           name (str): Name of image file
           download (bool): flag to download captured image
           file_format (str, optional): File format to be used for saving. Defaults to "png".
           verify (bool, optional): Should file path be verified.
           timeout (float, optional): maximum polling interval
        """
        if name.endswith(f".{file_format}"):
            path = os.path.join(self.ss_dir, name)
        else:
            path = os.path.join(self.ss_dir, f"{name}.{file_format}")

        self.omni_driver.viewport_screenshot(path, download=download)
        if verify:
            end = time.time() + timeout
            while time.time() < end:
                if os.path.isfile(path):
                    self.log.info(
                        f"Captured viewport screenshot and saved at {path}. "
                        f"Verified in {timeout - end + time.time()} secs"
                    )
                    return
            raise FileNotFoundError(
                f"File with path {path} could not be located within {timeout} seconds."
            )

    def find(self, locator: str, refresh: bool = False):
        """Finds the widget and returns it

        Args:
            locator (str): Locator path of widget
            refresh(bool, optional): Refreshes the element index
        """
        try:
            element = self.omni_driver.find_element(locator, refresh)
            self.log.info(f"Found element - {locator}")
        except:
            element = None
            self.log.info(f"Could not find element - {locator}")
        return element

    def find_and_click(
        self,
        locator: str,
        bring_to_front: bool = True,
        refresh: bool = False,
        double_click: bool = False,
    ):
        """Finds the widget and click on it

        Args:
            locator (str): Locator path of widget
            bring_to_front (bool, optional): Brings the widget to front. Defaults to True.
            refresh (bool, optional): Flag for refreshing the elements
            double_click (bool, optional): Flag for double click
        """
        element = self.omni_driver.find_element(locator, refresh)
        # TODO: remove the mouse move step when click issue gets resolved (OM-102905)
        x, y = element.get_widget_center()
        self.omni_driver.emulate_mouse_move(x, y)
        if double_click:
            element.double_click()
        else:
            element.click(bring_to_front)
        self.log.info(f"Found element - {locator} and clicked on it")
        return element

    def find_and_focus(self, locator: str, undock: bool = False):
        """Find the widget and focus on it

        Args:
            locator (str): Locator path of widget
            undock (bool, optional): Undocks the window. Defaults to False.
        """
        element = self.omni_driver.find_element(locator)
        element.bring_to_front(undock=undock)
        self.log.info(f"Found element - {locator} and focused on it")

    def find_and_scroll_element_into_view(
        self,
        locator: str,
        axis: ScrollAxis,
        scroll_amount: ScrollAmount,
        refresh: bool = False,
    ):
        """Scroll the element into view

        Args:
            locator(str): Locator of element
            axis (ScrollAxis): Scroll in X axis or Y axis
            scroll_amount (ScrollAmount): Amount to scroll by,
                                        possible values 0:Top 0.5:Center 1:Bottom
            refresh (bool): Boolean to set refresh flag
        """
        element = self.omni_driver.find_element(locator, refresh)
        element.scroll_into_view(axis=axis.value, scroll_amount=scroll_amount.value)
        self.log.info(f"Found element - {locator} and scrolled it into view.")
        return element

    def select_value_for_slider(self, locator: str, value: int = None):
        """Enters a random value in slider if not value is provided

        Args:
            locator (str): Locator of slider
            value (int, optional): Value to input. Defaults to 0.
        """
        slider = self.omni_driver.find_element(locator, refresh=True)
        slider.click()
        self.omni_driver.wait(2)
        if value is None:
            min_value, max_value = slider.get_slider_range()
            if isinstance(min_value, int):
                rand_value = random.randrange(min_value, max_value + 1)
            if isinstance(min_value, float):
                rand_value = random.uniform(min_value, max_value)
            slider.send_keys(rand_value)
        else:
            slider.send_keys(value)
        self.omni_driver.wait(2)

    def clear(self, locator: str):
        """
        Finds the widget and clears it

        :param locator: Locator path of widget
        """
        element = self.omni_driver.find_element(locator)
        element.click()
        self.omni_driver.wait(2)
        element.send_keys(" ")
        self.log.info(f"Found element - {locator} and cleared it")

    def paste(self, locator: str):
        """
        Finds the widget and paste on it

        :param locator: Locator path of widget
        :return: paste_val: str
        """

        element = self.omni_driver.find_element(locator)
        element.click()
        self.omni_driver.emulate_key_combo_press(
            KeyboardConstants.control + KeyboardConstants.v_key
        )
        self.log.info(f"Found element - {locator} and pasted value successfully")
        paste_val = element.get_text()
        self.clear(locator=locator)
        return paste_val

    def has_checkpoints(self, locator):
        """Validates Files Checkpoints"""
        self.omni_driver.wait(2)
        try:
            checkpoints = self.omni_driver.find_elements(locator)
            return checkpoints
        except:
            return False

    def select_item_by_index_from_combo_box(self, locator: str, index: int):
        """Selects item from combo box using index

        Args:
            locator (str): Locator of combobox
            index (int): Index of item
        """
        combo_box = self.find_and_scroll_element_into_view(
            locator, ScrollAxis.Y, ScrollAmount.CENTER
        )
        combo_box.select_item_from_combo_box(index=index, name=None, stack_combo=False)

    def select_item_from_stack_combo_box(
        self, locator: str, index: int = None, name: str = None
    ):
        """Selects item from combo box using index for stack combo

        Args:
            locator (str): Locator of combobox
            index (int): Index of item
            name (str): Name of the item
        """
        combo_box = self.find_and_scroll_element_into_view(
            locator, ScrollAxis.Y, ScrollAmount.CENTER, refresh=True
        )
        if name is not None:
            combobox_info = combo_box.get_combobox_info()
            self.log.info(combobox_info)
            options = combobox_info["all_options"]
            index = options.index(name)
        combo_box.select_item_from_combo_box(index=index, name=None, stack_combo=True)

    def get_child_element(self, locator: str, key_locator: str):
        """Finds Child element

        Args:
            locator (str): Locator for Child Elements
            key_locator (str): Identify Child Element
        """
        layers = self.omni_driver.find_elements(locator)
        index_level = -1
        child = None
        for i in range(len(layers)):
            try:
                child = layers[i].find_element(key_locator)
                index_level = i
                break
            except:
                pass
        if index_level == -1:
            self.log.error("[Base Model] Child not Found")
            raise
        return child, index_level

    def open_preference_window(self):
        """Sets Drap Drop Behaviour for Viewport"""
        preference_path = "Edit/Preferences"
        self.omni_driver.select_menu_option(menupath=preference_path)
        self.omni_driver.wait(seconds=2)

    def close_window(self, window_name: str):
        """Closes the given window widget

        Args:

           window_name (str): Name of window to search and close
        """
        self.omni_driver.close_window(window_name)

    def clear_textbox(self, element):
        """Clears textbox

        Args:
            element (OmniElement): Textbox element to clear
        """
        element.click()
        self.omni_driver.emulate_key_combo_press("CTRL+" + KeyboardConstants.a_key)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.delete)
        self.omni_driver.wait(1)

    def dock_window(
        self, first_win_name: str, seconds_win_name: str, dock_position: DockPosition
    ):
        """Docks first window into seconds window from UI

        Args:
            first_win_name (str): Name of window to dock
            seconds_win_name (str): Name of window to dock into
            dock_position (DockPosition): Docking position
        """
        self.omni_driver.dock_window(
            first_win_name, seconds_win_name, dock_position.value
        )

    def find_and_enter_text(self, locator: str, text: str):
        """Finds the widget and enter text in it

        Args:
            locator (str): Locator path of widget
            text (str): Text to be entered
        """
        element = self.omni_driver.find_element(locator)
        self.omni_driver.wait(1)
        element.send_keys(text)
        self.log.info(f"Found element - {locator} and entered text {text}")

    def close_window_from_ui(self, window_name: str):
        """Closes a window by clicking on Close button in the UI
        Args:
            window_name (str): name of the window that is to be closed
        """
        window_elm: OmniElement = self.omni_driver.find_element(
            window_name, refresh=True
        )
        window_elm.bring_to_front(undock=True)
        self.omni_driver.wait(1)
        dimensions = self.omni_driver.get_window_dimensions(window_name=window_name)
        x_pos = dimensions["position_x"] + dimensions["width"] - 10
        y_pos = dimensions["position_y"] + 10
        self.omni_driver.click_at(x_pos, y_pos)

    def get_glyph_code(self, glyph_name: str):
        if not self.glyph_codes.get(glyph_name):
            self.log.info(f"Glyph code for {glyph_name} not found in local dictionary.")
            self.glyph_codes[glyph_name] = self.omni_driver.get_glyph_code(glyph_name)
        self.log.info(f"Glyph code for {glyph_name} was found in local dictionary.")
        return self.glyph_codes[glyph_name]

    def drag_drop_window_from_ui(
        self, window_name: str, to_x: float, to_y: float, tolerance: float = 1
    ):
        """Drag and drops the window to the desired position
        Args:
        window_name (str): name of the window that is to be dragged
        to_x (float): x coordinate to which the window needs to be dragged
        to_y (float): y coordinate to which the window needs to be dragged
        tolerance (float): maximum difference allowed between displacement of window and
        displacement of mouse"""

        window_elm: OmniElement = self.omni_driver.find_element(
            window_name, refresh=True
        )
        window_elm.bring_to_front(undock=True)
        self.omni_driver.wait(1)
        dimensions = self.omni_driver.get_window_dimensions(window_name=window_name)
        original_x = dimensions["position_x"]
        original_y = dimensions["position_y"]
        self.log.info(
            f"Originally the dimensions of {window_name} are x :{original_x} and y :{original_y} "
        )

        x_pos = dimensions["position_x"] + dimensions["width"] / 2
        y_pos = dimensions["position_y"] + 10
        self.omni_driver.drag_from_and_drop_to(x_pos, y_pos, to_x, to_y)

        changed_dimensions = self.omni_driver.get_window_dimensions(
            window_name=window_name
        )
        changed_x = changed_dimensions["position_x"]
        changed_y = changed_dimensions["position_y"]
        self.log.info(
            f"After dragging, the dimensions of {window_name} are x :{changed_x} and y :{changed_y}"
        )

        window_displacement_x = abs(changed_x - original_x)
        window_displacement_y = abs(changed_y - original_y)

        mouse_displacement_x = abs(x_pos - to_x)
        mouse_displacement_y = abs(y_pos - to_y)

        success = math.isclose(
            window_displacement_x, mouse_displacement_x, rel_tol=tolerance
        ) and math.isclose(
            window_displacement_y, mouse_displacement_y, rel_tol=tolerance
        )
        if success:
            self.log.info(f"SUCCESS:{window_name} dragged successfully.")
        else:
            self.log.info(f"FAIL:Error in dragging the {window_name} window.")
            return False
        return original_x, original_y, changed_x, changed_y

    def compare_window_positions(
        self, window_name: str, original_x: float, original_y: float
    ):
        """This method compares the initial and the final coordinates of the window"""

        window_elm: OmniElement = self.omni_driver.find_element(
            window_name, refresh=True
        )
        window_elm.bring_to_front(undock=False)
        dimensions = self.omni_driver.get_window_dimensions(window_name=window_name)
        final_x = dimensions["position_x"]
        final_y = dimensions["position_y"]
        if (original_x == final_x) and (original_y == final_y):
            self.log.info("The original and the current coordinates are same.")
            return True
        else:
            self.log.info("The original and the current coordinates are not same.")
            return False

    def get_dock_status(self, window_name: str):
        """Gets the dock status of window
        Returns:
        Dictionary: Docking details
        """
        win = self.omni_driver.find_element(window_name, refresh=True)
        return win.get_dock_details()

    def find_element_center(self, locator: str) -> Tuple[float, float]:
        """Closes a window by clicking on Close button in the UI
        Args:
            window_name (str): name of the window that is to be closed
        """
        element = self.omni_driver.find_element(locator=locator)
        return element.get_widget_center()

    def log_info_with_screenshot(
        self, log_msg: str, screenshot_name: str = None, viewport_ss: bool = False
    ):
        """Creates a log info entry and takes fullscreen and viewport screenshot

        Args:
            log_msg (str): Log Message
            screenshot_name (str, optional): Screenshot file name. Defaults to None.
            viewport_ss (bool, optional): Flag to set whether to take viewport screenshot or not. Defaults to False.
        """
        date_time = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y%m%d_%H%M%S"
        )
        self.log.info(log_msg)
        screenshot_name = screenshot_name if screenshot_name else log_msg
        screenshot_name_ts = date_time + "_" + screenshot_name
        self.screenshot(screenshot_name_ts)
        if viewport_ss:
            viewport_screenshot_name_ts = date_time + "_viewport_ss_" + screenshot_name
            self.viewport_screenshot(viewport_screenshot_name_ts)

    def log_error_with_screenshot(self, log_msg: str, screenshot_name: str = None):
        """Creates a log error entry and takes fullscreen and viewport screenshot

        Args:
            log_msg (str): Log Message
            screenshot_name (str, optional): Screenshot file name. Defaults to None.
        """
        self.log.error(log_msg)
        if screenshot_name:
            self.screenshot(screenshot_name)
            self.viewport_screenshot(f"viewport_ss_{screenshot_name}")
        else:
            self.screenshot(log_msg)
            self.viewport_screenshot(f"viewport_ss_{log_msg}")

    def move_to_external_window(self, window_name: str):
        """Move a window to external window

        Args:
            window_name (str): Window Name
        """
        window_elm: OmniElement = self.omni_driver.find_element(
            window_name, refresh=True
        )
        window_elm.bring_to_front(undock=True)

        dimensions = self.omni_driver.get_window_dimensions(window_name=window_name)

        x_pos = dimensions["position_x"] + dimensions["width"] / 2
        y_pos = dimensions["position_y"] + 10

        self.omni_driver.click_at(x_pos, y_pos, True)
        self.omni_driver.click_at(x_pos + 5, y_pos + 5)
        flag = False
        if sys.platform == "win32":
            for title in pyautogui.getAllTitles():
                if window_name == title:
                    flag = True
                    self.log.info("External window is present.")
                    break
        else:
            cmd_line = r"wmctrl -lxp"
            window_names = (
                subprocess.check_output(cmd_line, shell=True).decode().splitlines()
            )
            for name in window_names:
                if window_name in name:
                    flag = True
                    self.log.info("External window is present.")
        assert flag, f"External window for {window_name} not found."

    def wait_for_stable_fps(self):
        """Waits until the Viewport fps stabilizes"""
        current_fps = self.omni_driver.get_viewport_info()["frame_info"]["fps"]
        start = time.time()
        while current_fps < 35:
            self.log.info("[OmniUI] Current FPS: %s", current_fps)
            current_fps = self.omni_driver.get_viewport_info()["frame_info"]["fps"]
            self.omni_driver.wait(5)
            if time.time() - start > 120:
                self.log.error("Timeout exceeded for stable fps")
                break

    def set_window_position(self, win_name: str, x: float, y: float):
        """Sets window position to given coordinates

        Args:
            win_name (str): Name of window
            x (float): X coordinate
            y (float): Y coordinate
        """
        window: OmniElement = self.omni_driver.find_element(win_name, refresh=True)
        if window.get_dock_details()["dock_status"]:
            window.bring_to_front(True)
        window.set_window_position(x, y)

    def get_notification_text(self, timeout: int = 5):
        """Returns Notification Label

        Args:
        timeout(int): seconds for timeout
        """
        notification = self.get_notification(timeout)
        return notification.get_text()

    def get_notification(self, timeout: int = 5):
        """Returns Notification ref"""
        pattern = r"[a-z0-9-]*[a-z0-9]$"
        start_time = time.time()
        timeout = timeout + time.time()
        while time.time() <= timeout:
            windows = self.omni_driver.get_windows()["visible_windows"]
            result = re.match(pattern, windows[-1])
            self.log.info(f"[Notification] Window: {windows[-1]}")
            if result:
                self.log.info(
                    f"Time to get notification: {time.time() - start_time}",
                )
                return self.omni_driver.find_element(
                    f"{result.string}//Frame/**/Label[0]"
                )
            time.sleep(0.2)
        raise RuntimeError("Failed to find notification in viewport")

    def connect_to_server(self, server):
        """Method to add new nucleus server using server name only

        Args:
            server (str): name of the server
        """
        self.token = get_value_from_json("nucleus_connection_token_name")[server]
        self.server, svcuser = get_nucleus_server_url_and_user(server)

        self.log.info(f"Connecting to Server name:{self.server} and user: {svcuser}")

        connect_to_nucleus_server(
            server_url=self.server,
            user=svcuser,
            endpoint=self.omni_driver.baseurl,
            token=self.token,
        )

    def expand_section(self, triangle_locator, expand: bool = True):
        """
        Expands or collapses the section by clicking on triangle icon
        This method can be used in particular section which can be expanded and collapsed
        by clicking on triangle icon.
        It is generally available in Property window, Asset Validator window, Scene Optimizer window.
        Args:
            triangle_locator: Triangle element locator on which click needs to be made to expand/collapse
            expand: True to expand else False to collapse
        Returns: Expanded/collapsed section
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        ele = self.omni_driver.find_element(triangle_locator, refresh=True)
        current_state = False if ele.get_alignment() == "RIGHT_CENTER" else True
        self.log.info(f"Initial expanded state for root element: {current_state}")
        state_match = current_state == expand
        attempt = 0
        while not state_match and attempt < 3:
            attempt += 1
            ele.click()
            self.omni_driver.wait(1)
            ele = self.omni_driver.find_element(triangle_locator, refresh=True)
            new_state = False if ele.get_alignment() == "RIGHT_CENTER" else True
            self.screenshot(f"after_triangle_clicked_{attempt}")
            state_match = new_state == expand
        assert state_match, f"{triangle_locator} expanded state: {expand}"

    def verify_usda_file_content(self, file_path, content):
        """
        Verifies the specific content is present in the USDA format file
        Args:
            file_path: USDA file path
            content: Content to be verified
        Returns: True if the content is present in the USDA file else False
        Raises:
            FileNotFoundError: when USDA file does not exist
        """
        stage = Usd.Stage.Open(file_path)
        usda_content = stage.ExportToString()
        return content in usda_content

    def expand_collapsible_frame(self, locator):
        """Expands a collapsible frame if it is collapsed.

        Args:
            locator (str): The locator string of the collapsible frame.
        """
        frame = self.find_and_scroll_element_into_view(
            locator, ScrollAxis.Y, ScrollAmount.TOP, refresh=True
        )
        curr_value = frame.is_collapsed()
        attempts = 10
        attempts_made = 0
        while curr_value != False and attempts_made <= attempts:
            attempts_made = attempts_made + 1
            frame.click()
            self.omni_driver.wait(2)
            curr_value = frame.is_collapsed()

        assert (
            curr_value == False
        ), f"Collapsible Frame was not expanded. Expected: False Actual: {curr_value}"

    def set_slider_value(self, locator, value):
        """Sets the value of a slider, ensuring it is within the valid range.

        Args:
            locator (str): The locator string of the slider.
            value (float): The value to set on the slider.

        Raises:
            ValueError: If the value is outside the allowed range of the slider.
        """
        slider = self.omni_driver.find_element(locator, refresh=True)
        min_value, max_value = slider.get_slider_range()
        curr_value = slider.get_value()
        if min_value <= value <= max_value:
            attempts = 10
            attempts_made = 0
            while curr_value != value and attempts_made <= attempts:
                slider.send_keys(str(value))
                self.omni_driver.wait(2)
                curr_value = slider.get_value()
                attempts_made += 1
            assert (
                value == curr_value
            ), f"Slider value was not changed. Expected: {value} Actual: {curr_value}"
        else:
            raise ValueError(
                f"The value {value} is outside the allowed range of {min_value} to {max_value}."
            )

    def select_item_by_name_from_combo_box(self, locator: str, name: str):
        """Selects an item from a combobox by its name.

        Args:
            locator (str): The locator string of the combobox.
            name (str): The name of the item to select in the combobox.

        Raises:
            ValueError: If the value is not an option in the combobox.
        """
        combo_box = self.find_and_scroll_element_into_view(
            locator, ScrollAxis.Y, ScrollAmount.CENTER, refresh=True
        )
        combobox_info = combo_box.get_combobox_info()
        if name in combobox_info["all_options"]:
            combo_box.select_item_from_combo_box(
                index=None, name=name, stack_combo=False
            )
            self.omni_driver.wait(2)
            combo_box = self.omni_driver.find_element(locator, refresh=True)
        else:
            raise ValueError(f"{name} is not an option in the combobox.")
        curr_value = combo_box.get_combobox_info()["current_value"]
        assert (
            name == curr_value
        ), f"ComboBox value not set. Expected: {name} Actual: {curr_value}"

    def toggle_checkbox(self, checkbox_locator, check_on: bool = True):
        """
        Toggles the given checkbox to On by default
        """
        checkbox_element = self.omni_driver.find_element(checkbox_locator, refresh=True)
        current_state = checkbox_element.is_checked()
        self.log.info(
            f"Initial check box state for {checkbox_locator}: {current_state}"
        )
        self.omni_driver.wait(1)
        attempts = 10
        attempts_made = 0
        while current_state != check_on and attempts_made <= attempts:
            checkbox_element.click()
            self.omni_driver.wait(2)
            current_state = checkbox_element.is_checked()
            attempts_made += 1
        self.omni_driver.wait(1)
        new_state = checkbox_element.is_checked()
        self.log.info(
            f"After click, check box state for {checkbox_locator}: {new_state} but expected was {check_on}"
        )
        state_match = new_state == check_on
        assert state_match, f"{checkbox_locator} is not getting toggled to {check_on}"

    def find_slider_range_from_locator(self, locator):
        element = self.omni_driver.find_element(locator)
        return element.get_slider_range()
    
    def validate_prim_within_viewport(self, prim:str):
        """Validate if the prims is within viewport.

        Args:
            prim (str): Prim Path

        Return:
            True/False        
        """

        # Fill Viewport
        self.omni_driver.fill_viewport()

        # Get Viewport co-ordinates
        _viewport_element = "Viewport//Frame/ZStack[0]"
        viewport_elem = self.omni_driver.find_element(_viewport_element, True)
        viewport_width = viewport_elem.get_size_and_position("computed_width")
        viewport_height = viewport_elem.get_size_and_position("computed_height")

        # Prim coo-ordinates
        prim_coord = self.omni_driver.get_prim_screen_coordinates(prim)

        if prim_coord["x"] <= viewport_width and prim_coord["y"] <= viewport_height and prim_coord["x"] >=0 and prim_coord["y"] >=0 :
            return True
        else:
            return False

    def verify_combo_box_selection(self, combo_box_locator, expected_value):
        """
        Verify that the combo box has the expected value selected
        Args:
            combo_box_locator (str): The locator string of the combobox.
            expected_value (str): The expected value of the combobox.
        Returns:
            True/False
        Raises:
            AssertionError: If the current value does not match the expected value.
        """
        combo_box = self.omni_driver.find_element(combo_box_locator)
        current_value = combo_box.get_combobox_info()["current_value"]
        self.log.info(f"Current value: {current_value} Expected value: {expected_value}")
        assert current_value == expected_value, f"Expected {expected_value}, got {current_value}"