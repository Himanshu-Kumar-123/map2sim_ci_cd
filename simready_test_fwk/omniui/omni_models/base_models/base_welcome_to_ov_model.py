# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Welcome to Omniverse model class
   This module contains the base methods for Welcome to Omniverse Model for actions to perform as soon as app opens
"""
import time


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BaseWelcomeToOmniverseModel(BaseModel):
    """BaseWelcomeToOmniverseModel class containing common methods"""

    # Widget Locators
    _open_folder_btn = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[0]/ZStack[0]/ImageWithProvider[0]"
    _about_btn = "Welcome//Frame/**/welcome_window_about_action_btn"
    _open_file_window = "Open File//Frame/VStack[0]"
    _welcome_window = "Welcome"
    _all_recent_usd = "Welcome//Frame/**/HGrid[0]/ZStack[*]"
    _create_new_mode_btn = (
        "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/ImageWithProvider[0]"
    )

    def open(self, timeout: int = 300, polling_freq: int = 1, usd_name: str = None):
        """Opens Content Browser from Welcome to Omniverse model by clicking on Open"""
        flag = False
        if not usd_name:
            open_button = self.omni_driver.find_element(self._open_folder_btn)
            open_button.click(bring_to_front=False)
            self.wait.timeout = timeout
            self.wait.polling_interval = polling_freq
            self.wait.element_to_be_located(self.omni_driver, self._open_file_window)
        else:
            recent_files = self.omni_driver.find_elements(self._all_recent_usd)
            for file in recent_files:
                label = file.find_element("**/Label[0]")
                label_text = label.get_text()
                if usd_name in label_text:
                    file.double_click()
                    self.omni_driver.wait(2)
                    flag = True
        return flag

    def wait_for_app_ready(self, timeout: int = 300, polling_freq: int = 1):
        """Waits for the app to be ready by checking if we are able to query any widget

        Args:
            driver (OmniDriver): Object reference of Omnidriver
            timeout (int, optional):Timeout to wait for app ready. Defaults to 300.
            polling_freq (int, optional): Frequency of API calls. Defaults to 1.
        """
        self.wait.timeout = timeout
        self.wait.polling_interval = polling_freq
        self.wait.element_to_be_located(self.omni_driver, self._welcome_window)
        target_fps = 60
        end = time.time() + timeout
        while time.time() < end:
            self.log.info(f"Wait for viewport FPS to stabilize. Target FPS: {target_fps}")
            frame_info = self.omni_driver.get_viewport_info()["frame_info"]
            fps = frame_info.get("fps")
            if fps is None:
                fps = 0
            if fps >= target_fps:
                self.log.info("Application has loaded and is ready to use.")
                return
            time.sleep(polling_freq)
        assert False, f"App did not load in {timeout} time."

    def is_open_file_window_visible(self):
        """returns True if Open File Window is visible,
        False otherwise"""
        self.omni_driver.wait(2)
        open_file_model = self.omni_driver.find_element(self._open_file_window)
        return open_file_model.is_visible()

    def is_welcome_window_visible(self):
        """returns True if Welcome Window is visible,
        False otherwise"""
        self.omni_driver.wait(2)
        welcome_window = self.omni_driver.find_element(self._welcome_window)
        return welcome_window.is_visible()

    def get_recently_opened_usd(self, usd_name: str):
        """Fetches recently opened usd from the list

        Args:
        usd_name(str): name of the usd
        """
        self.wait.element_to_be_located(self.omni_driver, self._welcome_window)
        recent_files = self.omni_driver.find_elements(self._all_recent_usd)
        for file in recent_files:
            label = file.find_element("**/Label[0]")
            label_text = label.get_text()
            if usd_name in label_text:
                file.double_click()
                self.omni_driver.wait(2)
        raise ValueError(f"Failed to find {usd_name} in the recent list")

    def open_about(self):
        """Opens About modal by clicking on About"""
        about_button = self.omni_driver.find_element(self._about_btn)
        about_button.click()

    def close_if_present(self):
        """Closes window if present in UI"""
        self.omni_driver.wait(1)
        try:
            self.omni_driver.find_element(self._welcome_window)
            self.omni_driver.close_window(self._welcome_window)
            self.log.info("Closed welcome window.")
        except ElementNotFound:
            self.log.info("Welcome window not present.")

    def create_new_mode(self):
        """Directs user to modify mode in viewport by clicking on New button"""
        about_button = self.omni_driver.find_element(self._create_new_mode_btn)
        about_button.click()

    def _click_open_btn(self):
        """Clicks on the Open button in Welcome window"""
        self.find_and_click(self._open_folder_btn)
