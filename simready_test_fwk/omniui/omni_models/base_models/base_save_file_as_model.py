# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Save File As Model class
   This module contains the base methods for Open File modal
   Open File modal appears from File-> Save as or CTRL+Shift+S
"""
import time
from omni_remote_ui_automator.driver.waits import Wait
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BaseSaveFileAsModel(BaseModel):
    """Base model class for Save File as modal

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for open file modal
    _save_button = "Save Scenario//Frame/VStack[0]/HStack[2]/Button[0]"
    _open_button = "Scenario Filepicker//Frame/VStack[0]/HStack[2]/Button[0]"
    _file_name_textarea = "Save Scenario//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"
    _directory_path_picker = "Save Scenario//Frame/VStack[0]/HStack[0]/**/HStack[0]/filepicker_directory_path"
    _overwrite_ok_button = r"__exclamation_glyph__ Overwrite//Frame/VStack[0]/HStack[1]/Button[0]"
    _save_fail_ok_btn = " Save Layer(s) Failed//Frame/VStack[0]/HStack[1]/Button[0]"
    _save_fail_label = " Save Layer(s) Failed//Frame/VStack[0]/HStack[0]/Label[0]"
    _extension_btn = "Save File As...//Frame/VStack[0]/HStack[2]/ZStack[2]/Button[0]"
    _extension_combobox_options = "ComboBoxMenu//Frame/ZStack[0]/HStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[{}]/Button[0]"
    _please_wait_window = "Please Wait"
    _map_button = "Drivesim ModeBar//Frame/ZStack[0]/HStack[1]/ImageWithProvider[0]"
    _back_button = "Drivesim Scenario Maps Window//Frame/ZStack[0]/**/HStack[0]/Back"
    _open_scenario = "Drivesim Scenario Maps Window//Frame/ZStack[0]/Frame[1]/**/ZStack[1]/Open"    

    def save_changes(
        self,
        file_name,
        extension: str,
        folder_path="",
        overwrite=False,
        please_wait_timeout=120
    ):
        """
        Saves the changes done in viewport

        :param overwrite: True if changes to be saved in existing file, False otherwise
        :param file_name: file name to be saved
        :param folder_path: path of the folder to save the file to
        :return: None
        """
        self.omni_driver.emulate_key_combo_press(
            f"{KeyboardConstants.shift}+{KeyboardConstants.control}+{KeyboardConstants.s_key}"
        )
        element = self.omni_driver.find_element(self._file_name_textarea)
        element.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(file_name)
        self.omni_driver.wait(2)

        if folder_path:
            folder_path = self._updated_path(folder_path) if not folder_path.startswith("file") else folder_path
            for i in range(2):
                path_field = self.omni_driver.find_element(self._directory_path_picker)
                path_field.click(bring_to_front=True)
                self.omni_driver.wait(2)
                path_field.send_keys(folder_path)

        if extension:
            ext_btn = self.find_and_click(self._extension_btn)
            center = ext_btn.get_widget_center()
            if extension.lower() == "usd":
                self.find_and_click(self._extension_combobox_options.format("0"))
            elif extension.lower() == "usda":
                self.find_and_click(self._extension_combobox_options.format("1"))
            elif extension.lower() == "usdc":
                self.find_and_click(self._extension_combobox_options.format("2"))
            else:
                assert (
                    False
                ), f"Incorrect extension name provided, Provided was {extension}, available options usd, usda and usdc"
        self.find_and_click(self._save_button)
        if overwrite:
            try:
                btn = self.wait.element_to_be_located(self.omni_driver, self._overwrite_ok_button.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")))
                btn.click()
                self.log.info("Overwritten existing file.")
            except ElementNotFound:
                self.log.info("File was not present, saved it for first time.")

        wait = Wait(please_wait_timeout)
        wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)

    def save_with_failure(
        self,
        file_name,
        folder_path="",
        overwrite=False,
    ):
        """
        Saves the changes done in viewport and expects failure

        :param overwrite: True if changes to be saved in existing file, False otherwise
        :param file_name: file name to be saved
        :param folder_path: path of the folder to save the file to
        :return: None
        """
        self.save_changes(file_name=file_name, folder_path=folder_path, overwrite=overwrite)
        self.wait.element_to_be_located(self.omni_driver, self._save_fail_label)
        windows = self.omni_driver.get_windows()["visible_windows"]
        header = " Save Layer(s) Failed"
        assert header in windows, "Save Layer Failed pop up not appeared"
        self.handle_save_failed()

    def handle_save_failed(self):
        save_layer_info = self.omni_driver.find_element(self._save_fail_label)
        expected = "Failed to save layers. Please check console for error."
        assert save_layer_info.get_text() == expected, f"Info: {save_layer_info.get_text()} mismatched with {expected}"
        ok_button = self.omni_driver.find_element(self._save_fail_ok_btn)
        ok_button.click()

    def save_scenario(
        self,
        file_name,
        folder_path=""
    ):
        """
        Saves the changes done in viewport

        :param overwrite: True if changes to be saved in existing file, False otherwise
        :param file_name: file name to be saved
        :param folder_path: path of the folder to save the file to
        :return: None
        """
        self.omni_driver.emulate_key_combo_press(
            f"{KeyboardConstants.shift}+{KeyboardConstants.control}+{KeyboardConstants.s_key}"
        )
        element = self.omni_driver.find_element(self._file_name_textarea)
        element.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(file_name)
        self.omni_driver.wait(2)
     
        path_field = self.omni_driver.find_element(self._directory_path_picker)
        path_field.click(bring_to_front=True)
        self.omni_driver.wait(2)

        path_field.send_keys(folder_path)
        self.omni_driver.wait(1)

        self.find_and_click(self._save_button)
        self.omni_driver.wait(2)

        self.omni_driver.emulate_key_press(KeyboardConstants.enter) 

    def open_scenario(
        self,
        file_name,
        folder_path=""
    ):
        """
        Saves the changes done in viewport

        :param overwrite: True if changes to be saved in existing file, False otherwise
        :param file_name: file name to be saved
        :param folder_path: path of the folder to save the file to
        :return: None
        """
        map_button_element = self.omni_driver.find_element(self._map_button)
        map_button_element.click()
        self.omni_driver.wait(1)

        back_button_element = self.omni_driver.find_element(self._back_button)
        back_button_element.click()
        self.omni_driver.wait(1)

        open_scenario_element = self.omni_driver.find_element(self._open_scenario)
        open_scenario_element.click()
        self.omni_driver.wait(1)

        self.omni_driver.emulate_key_press(KeyboardConstants.escape)

        element = self.omni_driver.find_element(self._file_name_textarea)
        element.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(file_name)
        self.omni_driver.wait(2)
     
        path_field = self.omni_driver.find_element(self._directory_path_picker)
        path_field.click(bring_to_front=True)
        self.omni_driver.wait(2)

        path_field.send_keys(folder_path)
        self.omni_driver.wait(1)

        self.find_and_click(self._open_button)
        self.omni_driver.wait(2)