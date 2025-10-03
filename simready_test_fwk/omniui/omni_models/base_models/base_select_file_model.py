# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Select File Model class
   This module contains the base methods for Select File modal
   Select File modal appears from File-> Import
"""
import os

from omni_remote_ui_automator.common.enums import ScrollAxis, ScrollAmount

from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BaseSelectFileModel(BaseModel):
    """Base model class for Select File model

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _window_name = "Select File"
    _directory_path_picker = (
        "Select File//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    )
    _file_type_combobox = "Select File//Frame/VStack[0]/HStack[2]/ZStack[1]/ComboBox[0]"
    _content_item_label = (
        "Select File//Frame/**/TreeView[0]/**/Label[0].text=='__name__'"
    )
    _import_button = "Select File//Frame/VStack[0]/HStack[2]/Button[0]"
    _import_destination_path = (
        "Select File//Frame/**/CollapsableFrame[1]/**/StringField[0]"
    )
    _slider = "Select File//Frame/**/IntSlider[0]"
    _file_or_folder_label = (
        "Select File//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    )
    _server_added = "Select File//Frame/**/Label[*].text=='__server__'"
    _search_bar_folder_btn = "Select File//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    _tessellation_level = "Select File//Frame/**/combo_tessellation"
    _default_import_selection = (
        "Select File//Frame/VStack[0]/HStack[1]/**/RadioButton[*].checked==True"
    )
    _import_type = "Select File//Frame/**/Label[*].text == '{}'"

    def get_tessellation_level_options(self):
        """Returns all the tessellation level from the combobox
        Returns:
            list: list of tessellation level
        """
        try:
            tessellation_level = self.omni_driver.find_element(
                self._tessellation_level, refresh=True
            )
        except ElementNotFound:
            self.log.info("Tessellation Level not found")
        else:
            tessellation_info = tessellation_level.get_combobox_info()
            self.log.info(tessellation_info)
            return tessellation_info["all_options"]
        return None

    def set_tessellation_level_options(self, option: str):
        """
        Sets the tessellation level from the combobox
        """
        self.select_item_from_stack_combo_box(self._tessellation_level, name=option)
        self.omni_driver.wait(2)

    def is_window_visible(self):
        """Method to check if Select File is visible"""
        self.omni_driver.wait(2)
        return self._window_name in self.omni_driver.get_windows()["visible_windows"]

    def launch_import_window(self):
        """
        Opens the import window
        """
        self.omni_driver.select_menu_option("File/Import")
        self.omni_driver.wait(2)

    def close_select_file_window(self):
        """Closes extension window"""
        self.omni_driver.close_window("Select File")
        self.omni_driver.wait(2)

    def set_output_format(self, name: str):
        """Sets the output format for capture

        Args:
            format (str): File format
        """
        self.select_item_by_name_from_combo_box(self._file_type_combobox, name)

    def set_output_by_index(self, index: int):
        """Sets the output format for capture

        Args:
            index (int)
        """
        self.select_item_by_index_from_combo_box(self._file_type_combobox, index)

    def import_destination(self, path):
        """
        Uses the option dropdown to choose where the file import destination is
        """
        element = self.omni_driver.find_element(
            self._import_destination_path, refresh=True
        )
        self.omni_driver.wait(1)
        element.send_keys(path)

    def click_import_button(self):
        """
        Clicks the import button
        """
        self.find_and_click(self._import_button)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait(10)

    def set_slider(self, value: int):
        """Set the slider value

        Args:
            value (int): Value to set the slider to
        """
        self.omni_driver.find_element(self._slider).send_keys(value)
        self.omni_driver.wait(2)

    def select_file(self, file_name: str):
        """Selects a file from the window

        Args:
            file_name (str): Name of the file to select
        """
        _file_element = self.omni_driver.find_element(
            self._content_item_label.replace("__name__", file_name)
        )
        self.omni_driver.click_at(*_file_element.get_widget_center())
        self.omni_driver.wait(2)

    def open_file_folder(
        self,
        directory: str,
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
            usd_file.click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(
                    self._file_or_folder_label.replace("__name__", item)
                )
                self.omni_driver.wait(1)
        self.omni_driver.wait(2)

    def enter_path_and_navigate(self, path: str, assert_file_or_folder: str):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
            assert_file_or_folder (str): To check file/folder present in path for successful navigation
        """
        path = path.replace(os.sep, "/")
        # self.wait_for_loader()
        retry = 0
        while retry < 3:
            if not self._do_path_exists(directory_path=path):
                retry += 1
                continue
            # self.wait_for_loader()
            self.wait.element_to_be_located(
                self.omni_driver,
                self._file_or_folder_label.replace("__name__", assert_file_or_folder),
            )
            return
        raise RuntimeError(f"Could not navigate to {path}")

    def _do_path_exists(self, directory_path: str):
        """
        Verifies if the path exists

        :param directory_path:
        :return:
        """
        search_bar = self.omni_driver.find_element(
            self._directory_path_picker, refresh=True
        )
        search_bar.send_keys(directory_path)
        self.omni_driver.wait(5)
        folders = directory_path.replace("omniverse://", "").split("/")
        try:
            for folder in folders:
                self.omni_driver.find_element(
                    self._search_bar_folder_btn.replace("__folder__", folder)
                )
            return True
        except:
            return False

    def get_supported_file_formats(self):
        """Get Supported File Formats for Import"""
        _file_type_locator = self.omni_driver.find_element(
            self._file_type_combobox, refresh=True
        )
        return _file_type_locator.get_combobox_info()["all_options"]

    def get_default_import_selection(self):
        """Get default selection for Import"""
        try:
            default_import_element = self.omni_driver.find_element(
                self._default_import_selection, refresh=True
            )
        except ElementNotFound:
            self.log.info("Import Selection not found")
        else:
            parent_path = default_import_element.find_parent_element_path()
            selected_option_element = self.omni_driver.find_element(
                f"{parent_path}/Label[0]", refresh=True
            )
            return selected_option_element.get_text()
        return None

    def select_import_type(self, import_type):
        """
        Selects the import type on the select file model
        """
        element = self.omni_driver.find_element(self._import_type.format(import_type))
        radio_btn_locator = "/".join(
            element.find_parent_element_path().split("/") + ["RadioButton[0]"]
        )
        radio_btn_ele = self.omni_driver.find_element(radio_btn_locator, refresh=True)
        radio_btn_ele.click()
        self.omni_driver.wait(2)

    def select_server(self, server: str):
        """Clicks on Server

        Args:
            server (str): server name
        """
        server_label = self._server_added.replace("__server__", server)
        self.wait.element_to_be_located(self.omni_driver, server_label)
        server_element = self.find_and_scroll_element_into_view(
            server_label, ScrollAxis.Y, ScrollAmount.CENTER, True
        )
        server_element.click()
        self.omni_driver.wait(2)
