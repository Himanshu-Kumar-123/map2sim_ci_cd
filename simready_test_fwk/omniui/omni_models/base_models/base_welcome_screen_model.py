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

from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import (
    ElementNotFound,
    PropertyRetrieveFailed,
)
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait
from ...utils.omni_ui_utils import wait_for_scene_load
from omniui.utils.enums import ViewportMode
from omni_remote_ui_automator.common.constants import KeyboardConstants

class BaseWelcomeScreenModel(BaseModel):
    """BaseWelcomeScreen class for apps like Code containing common methods"""

    # Widget Locators
    _welcomescr_window = "Welcome Screen"
    _open_stage_frame_btn = "Welcome Screen//Frame/**/RadioButton[0].text=='STAGE'"
    _open_sample_frame_btn = "Welcome Screen//Frame/**/RadioButton[1].text=='SAMPLES'"
    _sample_usd = "Welcome Screen//Frame/**/Label[0].text=='{}'"
    _open_file_frame_btn = "Welcome Screen//Frame/**/RadioButton[*].text=='FILE'"
    _open_default_stage_btn = "Welcome Screen//Frame/**/Label[0].text=='default stage'"
    _open_menu_btn = "Welcome Screen//Frame/HStack[0]/VStack[0]/Button[0]"
    _whatsnew_menu_btn = "Welcome Screen//Frame/HStack[0]/VStack[0]/Button[1]"
    _learn_menu_btn = "Welcome Screen//Frame/HStack[0]/VStack[0]/Button[2]"
    _about_menu_btn = "Welcome Screen//Frame/HStack[0]/VStack[0]/Button[3]"
    _open_file_btn = "Welcome Screen//Frame/**/Button[*].text=='Open File'"
    _please_wait_window = "Please Wait//Frame"
    _add_new_connection = "Open File//Frame/**/Label[*].text=='Add New Connection ...'"
    _server_added = "Open File//Frame/**/Label[*].text=='__server__'"
    _new_connection_server_name_txtbox = "Add Nucleus connection//Frame/**/StringField[0]"
    _new_connection_server_ok_btn = "Add Nucleus connection//Frame/**/Button[*].text=='Ok'"
    _file_or_folder_label = "Welcome Screen//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"

    _file_filepicker = "Welcome Screen//Frame/**/filepicker_directory_path"
    _file_folder_content = (
        "Welcome Screen//Frame/**/Frame[2]/**/ZStack[0]/HStack[0]/HStack[0]/ZStack[1]/**/None_grid_view"
    )
    _file_filepicker_btn = (
        "Welcome Screen//Frame/**/Frame[2]/**/HStack[1]/VStack[0]/HStack[0]/ZStack[0]/ZStack[0]/**/Button[*]"
    )
    _open_original_file = "Opening a Read Only File//Frame/VStack[0]/VStack[0]/HStack[1]/Button[0]"
    _file_url_path_txtbox = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[1]/ZStack[0]/StringField[0]"
    _open_link_btn = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[1]/ZStack[1]/HStack[0]/Label[0]"
    _welcomescr_new_btn = (
        "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/ImageWithProvider[0]"
    )
    _welcomescr_learn_btn = (
        "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[2]/ZStack[0]/ImageWithProvider[0]"
    )
    _welcomescr_close_btn = "Welcome//Frame/VStack[0]/ZStack[0]/HStack[0]/VStack[0]/ZStack[0]/Placer[1]/Image[0]"
    _welcomescr_open_btn_txt = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[0]/HStack[0]/Label[0]"
    _welcomescr_new_btn_txt = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[1]/HStack[0]/Label[0]"
    _welcomescr_open_learn_txt = "Welcome//Frame/VStack[0]/ZStack[1]/VStack[0]/HStack[0]/VStack[2]/HStack[0]/Label[0]"

    # save this stage dialog window
    _save_this_stage_dialog_window = """__exclamation_glyph__"""
    _save_this_stage_dialog_save_btn = """__exclamation_glyph__//Frame/**/Button[*].text=="Save" """
    _save_this_stage_dialog_dont_save_btn = """__exclamation_glyph__//Frame/**/Button[*].text=="Don't Save" """
    _save_this_stage_dialog_cancel_btn = """__exclamation_glyph__//Frame/**/Button[*].text=="Cancel" """

    def open(self, timeout: int = 300, polling_freq: int = 1):
        """Opens Stage from Welcome Screen to Omniverse model by clicking on Open and Default Stage"""

        self.find_and_click(self._open_menu_btn)
        self.find_and_click(self._open_stage_frame_btn)
        default_stage = self.omni_driver.find_element(self._open_default_stage_btn)
        default_stage.double_click()
        self.omni_driver.wait(2)
        default_stage.double_click()
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

    def open_sample_from_welcomescr(
        self,
        timeout: int = 300,
        polling_freq: int = 1,
        sample_scene: str = "Automotive_Material_Library",
    ):
        """Opens Sample scene from Welcome Screen to Omniverse model by clicking on Open and Samples"""
        self.find_and_click(self._open_menu_btn)
        self.find_and_click(self._open_sample_frame_btn)
        default_sample = self.omni_driver.find_element(self._sample_usd.format(sample_scene))
        default_sample.double_click()
        self.omni_driver.wait(2)
        default_sample.double_click()
        target_fps = 60
        end = time.time() + timeout
        while time.time() < end:
            self.log.info(f"Wait for viewport FPS to stabilize. Target FPS: {target_fps}")
            frame_info = self.omni_driver.get_viewport_info()["frame_info"]
            fps = frame_info.get("fps")
            if fps is None:
                fps = 0
            if fps >= target_fps:
                self.log.info("Application has loaded with sample scene {_sample_usd} and is ready to use.")
                return
            time.sleep(polling_freq)
        assert False, f"App did not load in {timeout} time."

    def wait_for_app_ready(self, timeout: int = 300, polling_freq: int = 1):
        """Waits for the app to be ready by checking if we are able to query any widget

        Args:
            driver (OmniDriver): Object reference of Omnidriver
            timeout (int, optional):Timeout to wait for app ready. Defaults to 300.
            polling_freq (int, optional): Frequency of API calls. Defaults to 1.
        """
        self.wait.timeout = timeout
        self.wait.polling_interval = polling_freq
        self.wait.element_to_be_located(self.omni_driver, self._welcomescr_window)
        # self.open()

    def is_open_file_window_visible(self):
        """returns True if Open File Window is visible,
        False otherwise"""
        self.omni_driver.wait(2)
        open_file_model = self.omni_driver.find_element(self._open_file_frame_btn)
        return open_file_model.is_visible()

    def switch_to_file_tab(self):
        """Switches to File Tab in Open Menu"""
        self.find_and_click(self._open_menu_btn)
        self.wait.element_to_be_located(self.omni_driver, self._open_file_frame_btn)
        self.find_and_click(self._open_file_frame_btn)

    def handle_save_this_stage_pop_up(self, response: str):
        """Handles the Save Pop up dialog"""
        try:
            window: OmniElement = self.wait.element_to_be_located(
                self.omni_driver,
                self._save_this_stage_dialog_window.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
            )
            self.wait.visibility_of_element(window)
        except (ElementNotFound, PropertyRetrieveFailed):
            self.log.info("'Save this stage' pop up did not appear")
            return
        self.log.info("Found 'Save this stage' pop up")
        if response.lower() == "save":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_save_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Save'")
        elif response.lower() == "don't save":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_dont_save_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Don't Save'")
        if response.lower() == "cancel":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_cancel_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Cancel'")
        self.wait.invisibility_of_element(window)
        self.log.info("'Save this stage' pop up handled")

    def _do_path_exists(self, directory_path: str, is_local_storage: bool = False):
        """Verifies if path exists"""
        if is_local_storage:
            path = directory_path
        else:
            path = self._updated_path(directory_path)
        search_bar: OmniElement = self.omni_driver.find_element(self._file_filepicker)
        search_bar.click(bring_to_front=True)
        self.omni_driver.wait(3)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)
        folders = path.replace("omniverse://", "").split("/")
        try:
            for folder in folders:
                self.omni_driver.find_element(self._file_filepicker_btn.replace("__folder__", folder))
            return True
        except ElementNotFound:
            return False

    def file_tab_open_file_folder(
        self,
        file_name: str,
        folder_path: str,
        is_local_storage: bool = False,
        is_readonly: bool = False,
        handle_dont_save: bool = False,
        timeout: int = 200,
    ):
        """Opens File or Folder from FIle Tab"""
        retry = 3
        while retry:
            if self._do_path_exists(directory_path=folder_path, is_local_storage=is_local_storage):
                break
            retry -= 1
        if retry == 0:
            self.log.error("%s path does not exists", folder_path)
            raise RuntimeError("Failed to navigate to path")

        query_target = self._file_folder_content + f"/**/Label[0].text=='{file_name}'"

        target: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
        target.double_click()

        if is_readonly:
            original_file = self.wait.element_to_be_located(self.omni_driver, self._open_original_file)
            original_file.click()
        if handle_dont_save:
            self.handle_save_this_stage_pop_up("don't save")
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(timeout=timeout)

    def enter_path_and_navigate(self, path: str, assert_file_or_folder: str):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
            assert_file_or_folder (str): To check file/folder present in path for successful navigation
        """
        self.switch_to_file_tab()
        self.find_and_enter_text(self._file_filepicker, path)
        self.wait.element_to_be_located(
            self.omni_driver,
            self._file_folder_content.replace("__name__", assert_file_or_folder),
        )
        self.omni_driver.wait(2)

    def open_file_folder(
        self,
        directory: str,
        stage_load_timeout: int = 60,
        isreadonly: bool = False,
        handle_dont_save: bool = False,
    ):
        """Opens a specified file

        Args:
            directory (str): Directory of folder/file to locate
            stage_load_timeout (int, optional): Timeout for stage to finish loading. Defaults to 60.
        """
        path = directory.split("/")
        if len(path) == 1:
            usd_file = self.omni_driver.find_element(
                self._file_or_folder_label.replace("__name__", path[0]), refresh=True
            )
            self.omni_driver.wait(1)
            usd_file.click()
            self.omni_driver.wait(1)
            self.find_and_click(self._open_file_btn)
        if len(path) > 1:
            for item in path:
                self.find_and_click(self._file_or_folder_label.replace("__name__", item))
                self.omni_driver.wait(1)
        if isreadonly:
            original_file = self.wait.element_to_be_located(self.omni_driver, self._open_original_file)
            original_file.click()

        self.omni_driver.wait(2)
        if handle_dont_save:
            self.handle_save_this_stage_pop_up("don't save")
        self.omni_driver.wait(5)
        self.wait.timeout = 120
        self.wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)
        self.omni_driver.wait_for_stage_load(stage_load_timeout)

    def add_new_connection(self, server_name: str):
        "Adds new connection"
        self._click_add_connection()
        self._enter_new_connection_server(server_name)

    def _click_add_connection(self):
        """Clicks on add new connection option"""
        self.find_and_click(self._add_new_connection)

    def _enter_new_connection_server(self, server_name: str):
        """Enter the connection details for the serer

        Args:
            server_name (str): Server name
        """
        self.omni_driver.find_element(self._new_connection_server_name_txtbox).send_keys(server_name)
        self.screenshot("Entered_Server_details")
        self.omni_driver.find_element(self._new_connection_server_ok_btn).click()

    def verify_server_added(self, server: str):
        """Verifies if server has been successfully added or not

        Args:
            server (str): server name
        """
        server_label = self._server_added.replace("__server__", server)
        self.wait.element_to_be_located(self.omni_driver, server_label)

    def open_about(self):
        """Opens About modal by clicking on About"""
        about_button = self.omni_driver.find_element(self._about_menu_btn)
        about_button.click()

    def open_welcome_screen_window(self):
        """Opens welcome screen window through Layout/window"""
        preference_path = "Window/Welcome Window"
        self.omni_driver.select_menu_option(menupath=preference_path)
        self.omni_driver.wait(seconds=2)
        assert self.find(self._welcomescr_new_btn), "Welcome screen window is not present"
        self.omni_driver.wait(2)

    def open_usd_file_by_url(
        self,
        path: str,
        handle_dont_save: bool = True,
        please_wait_timeout=120,
    ):
        """Opens a specified file from content browser

        Args:
            directory (str): Directory of folder/file to locate
            stage_load_timeout (int, optional): Timeout for stage to finish loading. Defaults to 60.
        """
        self.open_welcome_screen_window()
        self.find_and_enter_text(self._file_url_path_txtbox, path)
        self.omni_driver.wait(1)
        assert self.find_and_click(self._open_link_btn, refresh=True), "Open link button not found"
        self.omni_driver.wait(1)

        if handle_dont_save:
            self.handle_save_this_stage_pop_up("don't save")
        self.omni_driver.wait(2)
        wait = Wait(please_wait_timeout)
        wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)
        wait_for_scene_load(self.omni_driver.baseurl, self.log)

    def open_empty_scene(self):
        "Opens empty scene into the viewport"
        self.omni_driver.wait(2)
        path = "File/New"
        self.omni_driver.select_menu_option(menupath=path), "Unable to open new scene"
        self.omni_driver.wait(seconds=2)
        self.handle_save_this_stage_pop_up("don't save")
        self.omni_driver.wait(2)

    def welcome_screen_new_scene_load(self):
        """Opens new scene by clicking on new button of Welcome Screen"""
        self.open_welcome_screen_window()
        assert self.find_and_click(self._welcomescr_new_btn, refresh=True), "New button not found"
        self.omni_driver.wait(2)
        self.handle_save_this_stage_pop_up("don't save")
        self.viewport_screenshot("new scene by welcome screen")
        self.omni_driver.wait_for_stage_load()
        cnt = len(self.omni_driver.get_stage())
        self.omni_driver.wait(2)
        assert cnt == 12, "Failed to load new scene"

    def welcome_screen_open_learn(self, driver):
        """Opens learning resourses link in browser by clicking on new learn buton of Welcome Screen"""
        self.open_welcome_screen_window()
        assert self.find_and_click(self._welcomescr_learn_btn, refresh=True), "Learn button not found"
        self.omni_driver.wait(5)
     
    def verify_welcome_src_names_and_buttons(self):
        """OTo verify all names and button are present on Welcome Screen"""
        self.open_welcome_screen_window()
        open_name = self.omni_driver.find_element(self._welcomescr_open_btn_txt, refresh=True).get_text()
        new_name = self.omni_driver.find_element(self._welcomescr_new_btn_txt, refresh=True).get_text()
        learn_name = self.omni_driver.find_element(self._welcomescr_open_learn_txt, refresh=True).get_text()

        assert open_name == "Open", "Open name is not present ON Welcome Screen"
        assert new_name == "New", "New name is not present ON Welcome Screen"
        assert learn_name == "Learn", "Learn name is not present ON Welcome Screen"
        self.find_and_click(self._welcomescr_close_btn, refresh=True)
        self.omni_driver.wait(2)

    def open_live_session_by_url(
        self,
        handle_dont_save: bool = True,
        please_wait_timeout=120,
    ):
        """Opens a specified file from content browser

        Args:
            directory (str): Directory of folder/file to locate
            stage_load_timeout (int, optional): Timeout for stage to finish loading. Defaults to 60.
        """
        self.open_welcome_screen_window()
        element = self.find_and_click(self._file_url_path_txtbox, refresh=True, double_click=True)
        self.omni_driver.emulate_key_combo_press("CTRL+" + KeyboardConstants.v_key)
        self.omni_driver.wait(1)
        url = element.get_text()
        paste_val_len = len(url)
        self.log.info(f"Live session URL = {url}")

        assert paste_val_len > 0, "Link paste Failure"
        self.omni_driver.wait(1)
        assert self.find_and_click(self._open_link_btn, refresh=True), "Open link button not found"
        self.omni_driver.wait(2)
