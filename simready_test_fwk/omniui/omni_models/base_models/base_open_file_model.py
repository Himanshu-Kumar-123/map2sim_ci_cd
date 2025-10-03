# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Open File Model class
   This module contains the base methods for Open File modal
   Open File modal appears from File-> Open or CTRL+O
"""


import os
from ..base_models.base_model import BaseModel
from ...utils.omni_ui_utils import wait_for_scene_load
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.waits import Wait
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import (
    ElementNotFound,
    PropertyRetrieveFailed,
)


class BaseOpenFileModel(BaseModel):
    """Base model class for Open File modal

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for open file modal
    _directory_path_picker = (
        "Open File//Frame/**/StringField[*].identifier == 'filepicker_directory_path'"
    )
    _checkpoints_list = "Open File//Frame/VStack[0]/HStack[1]/**/CollapsableFrame[2]/**/VStack[1]/ZStack[0]/TreeView[0]/ZStack[*]"
    _open_file_button = "Open File//Frame/VStack[0]/HStack[2]/Button[0]"
    _search_bar_folder_btn = "Open File//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    _file_or_folder_label = (
        "Open File//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    )
    _please_wait_window = "Please Wait"
    _add_new_connection = "Open File//Frame/**/Label[*].text=='Add New Connection ...'"
    _content_window = "Open File//Frame/VStack[0]"
    _server_added = "Open File//Frame/**/Label[*].text=='__server__'"
    _new_connection_server_name_txtbox = (
        "Add Nucleus connection//Frame/**/StringField[0]"
    )
    _new_connection_server_ok_btn = (
        "Add Nucleus connection//Frame/**/Button[*].text=='Ok'"
    )
    _new_connection_server_cancel_btn = (
        "Add Nucleus connection//Frame/**/Button[*].text=='Cancel'"
    )

    # Opening a Read Only File
    _open_original_file = (
        "Opening a Read Only File//Frame/VStack[0]/VStack[0]/HStack[1]/Button[0]"
    )
    _please_wait_window = "Please Wait"

    # Progress bar for loading file content
    _loader = "Open File//Frame/VStack[0]/HStack[1]/ZStack[0]/HStack[0]/HStack[0]/ZStack[1]/Frame[0]"

    # save this stage dialog window
    _save_this_stage_dialog_window = """__exclamation_glyph__"""
    _save_this_stage_dialog_save_btn = (
        """__exclamation_glyph__//Frame/**/Button[*].text=="Save" """
    )
    _save_this_stage_dialog_dont_save_btn = (
        """__exclamation_glyph__//Frame/**/Button[*].text=="Don't Save" """
    )
    _save_this_stage_dialog_cancel_btn = (
        """__exclamation_glyph__//Frame/**/Button[*].text=="Cancel" """
    )

    # SRS App locators
    _open_folder_source = "Open folder//Frame/VStack[0]/HStack[1]/ZStack[0]/HStack[0]/HStack[0]/ZStack[1]/ScrollingFrame[0]/VStack[0]/VGrid[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/ZStack[0]/Frame[0]/ImageWithProvider[0]"
    _open_folder_select = (
        "Open folder//Frame/VStack[0]/HStack[2]/Button[0].text=='Select'"
    )

    def launch(self, launch_with="keyboard"):
        """
        Launches Open File Modal
        :param launch_with: keyboard/file menu
        :return:
        """
        if launch_with == "keyboard":
            self.omni_driver.emulate_key_combo_press(
                KeyboardConstants.control + KeyboardConstants.o_key
            )
        # Todo: launch from file menu

    def _do_path_exists(self, directory_path: str, is_local_path: bool = False):
        """
        Verifies if the path exists

        :param directory_path:
        :return:
        """
        if not is_local_path:
            path = self._updated_path(directory_path)
        else:
            path = directory_path.replace(os.sep, "/")
        search_bar = self.omni_driver.find_element(self._directory_path_picker)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)
        folders = path.replace("omniverse://", "").split("/")
        try:
            for folder in folders:
                self.omni_driver.find_element(
                    self._search_bar_folder_btn.replace("__folder__", folder)
                )
            return True
        except:
            return False

    def step_verify_file_exists(self, path: str, file_or_folder: str):
        """
        Verifies the file/folder exists in given Path
        :param path: path where the file resides
        :param file_or_folder: file/folder name to be searched
        """
        self._do_path_exists(directory_path=path)

        try:
            target = self.omni_driver.find_element(
                locator=self._file_or_folder_label.replace("__name__", file_or_folder),
                refresh=True,
            )
            return target
        except:
            return False

    def select_file(self, directory_path: str, file: str):
        """
        Navigates to the directory and selects the file

        :param directory_path: path where the file can be found
        :param file: file to be selected
        """
        self._do_path_exists(directory_path=directory_path)
        file_context = self.step_verify_file_exists(directory_path, file)
        file_context.click()

    def open_checkpoint(self, open_with_index: int):
        """Opens checkpoint

        Args:
            open_with_index (int): Index of checkpoint to open
        """
        checkpoints = self.has_checkpoints(locator=self._checkpoints_list)
        checkpoints[open_with_index].click()
        self.find_and_click(self._open_file_button)
        self.omni_driver.wait_for_stage_load()

    def enter_path_and_navigate(
        self, path: str, assert_file_or_folder: str, is_local_path: bool = False
    ):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
            assert_file_or_folder (str): To check file/folder present in path for successful navigation
            is_local_path (bool): For local Paths
        """
        # self.wait_for_loader()
        retry = 0
        while retry < 3:
            if not self._do_path_exists(
                directory_path=path, is_local_path=is_local_path
            ):
                retry += 1
                continue
            # self.wait_for_loader()
            self.wait.element_to_be_located(
                self.omni_driver,
                self._file_or_folder_label.replace("__name__", assert_file_or_folder),
            )
            return
        raise RuntimeError(f"Could not navigate to {path}")

    def open_file_folder(
        self,
        directory: str,
        stage_load_timeout: int = 240,
        isreadonly: bool = False,
        handle_dont_save: bool = False,
        please_wait_timeout=120,
    ):
        """Opens a specified file from content browser

        Args:
            directory (str): Directory of folder/file to locate
            stage_load_timeout (int, optional): Timeout for stage to finish loading. Defaults to 60.
        """
        path = directory.split("/")
        if len(path) == 1:
            usd_file = self.omni_driver.find_element(
                self._file_or_folder_label.replace("__name__", path[0]), refresh=True
            )
            self.omni_driver.wait(2)
            usd_file.double_click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(
                    self._file_or_folder_label.replace("__name__", item)
                )
                self.omni_driver.wait(1)
        if isreadonly:
            original_file = self.wait.element_to_be_located(
                self.omni_driver, self._open_original_file
            )
            original_file.click()

        self.omni_driver.wait(1)
        if handle_dont_save:
            self.handle_save_this_stage_pop_up("don't save")
        self.omni_driver.wait(2)

        wait = Wait(please_wait_timeout)
        wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)
        wait_for_scene_load(self.omni_driver.baseurl, self.log, stage_load_timeout)

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
        self.omni_driver.find_element(
            self._new_connection_server_name_txtbox
        ).send_keys(server_name)
        self.screenshot("Entered_Server_details")
        self.omni_driver.find_element(self._new_connection_server_ok_btn).click()

    def verify_server_added(self, server: str):
        """Verifies if server has been successfully added or not

        Args:
            server (str): server name
        """
        server_label = self._server_added.replace("__server__", server)
        self.wait.element_to_be_located(self.omni_driver, server_label)

    def wait_for_loader(self, timeout: int = 60):
        """Waits for loader to complete"""
        wait = Wait(timeout)
        try:
            loader = self.omni_driver.find_element(self._loader, True)
            wait.invisibility_of_element(loader)
        except PropertyRetrieveFailed as exc:
            raise RuntimeError("Loader did not complete in given time") from exc
        except ElementNotFound:
            self.log.info("Loader not found")
        self.omni_driver.wait(1)

    def handle_save_this_stage_pop_up(self, response: str):
        try:
            window: OmniElement = self.wait.element_to_be_located(
                self.omni_driver,
                self._save_this_stage_dialog_window.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
            )
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

    def wait_for_scene_load(self, timeout: int = 240):
        self.wait.timeout = 120
        self.wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)
        self.omni_driver.wait_for_stage_load(timeout)

    def find_and_click_select(self):
        """Find and clicks required icon"""
        self.find_and_click(self._open_folder_select)

    def select_download(self, file_or_folder_name: str):
        """Clicks on download option from context menu for a specified file or folder

        Args:
            file_or_folder_name (str): File or folder name to be downloaded
        """
        item = self.omni_driver.find_element(
            self._file_or_folder_label.replace("__name__", file_or_folder_name)
        )
        item.right_click()
        self.omni_driver.select_context_menu_option("Download")
        self.log.info("Clicked on download option from context menu")

    def navigate(self, path: str):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
        """
        search_bar = self.omni_driver.find_element(self._directory_path_picker)
        search_bar.send_keys(path)
        self.omni_driver.wait(2)
        folders = path.replace("omniverse://", "").split("/")

        for folder in folders:
            self.omni_driver.find_element(
                self._search_bar_folder_btn.replace("__folder__", folder)
            )
        return True

    def open_folder(
        self,
        directory: str,
    ):
        """Opens a specified file from content browser by double clicking from UI

        Args:
            directory (str): Directory of folder/file to locate
        """
        path = directory.split("/")
        if len(path) == 1:
            usd_file = self.omni_driver.find_element(
                self._file_or_folder_label.replace("__name__", path[0]), refresh=True
            )
            self.log.info("Element found : %s", directory)
            self.omni_driver.wait(2)
            usd_file.double_click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(
                    self._file_or_folder_label.replace("__name__", item),
                    refresh=True,
                    double_click=True,
                )
                self.omni_driver.wait(1)

    def open_file_from_path(self, path:str, file:str):
        """Opens a specified file from specified path

        Args:
            path (str): Path to the folder.
            file (str): File to be opened.
        """
        search_bar = self.omni_driver.find_element(self._directory_path_picker)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)

        file_context = self.omni_driver.find_element(
                locator=self._file_or_folder_label.replace("__name__", file),
                refresh=True,
            )
        file_context.click()
        self.omni_driver.wait(5)
        self.find_and_click(self._open_file_button)
