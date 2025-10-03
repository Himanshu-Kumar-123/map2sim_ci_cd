# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Save Layout Model class
   This module contains the base methods for Save Layout window
"""


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BaseSelectFileToSaveLayout(BaseModel):
    """Base model class for Save Layout

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for Save Layout
    _save_button = "Select File to Save Layout//Frame/VStack[0]/HStack[2]/Button[0]"
    _file_name_textarea = "Select File to Save Layout//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]"
    _directory_path_picker = (
        "Select File to Save Layout//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    )
    _overwrite_ok_button = r" Overwrite//Frame/VStack[0]/HStack[1]/Button[0]"
    _extension_btn = "Select File to Save Layout//Frame/VStack[0]/HStack[2]/ZStack[2]/Button[0]"

    # Locators for Load Layout
    _load_layout_file_name_textarea = (
        "Select File to Load Layout//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]"
    )
    _load_button = "Select File to Load Layout//Frame/VStack[0]/HStack[2]/Button[0]"
    _load_layout_directory_path_picker = (
        "Select File to Load Layout//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    )



    
    def save_changes(
        self,
        file_name,
        folder_path="",
        overwrite=False,
    ):
        """
        Saves the layout

        :param overwrite: True if changes to be saved in existing file, False otherwise
        :param file_name: file name to be saved
        :param folder_path: path of the folder to save the file to
        :return: None
        """
        element = self.omni_driver.find_element(self._file_name_textarea)
        self.clear(locator=self._file_name_textarea)
        element.send_keys(file_name)

        if folder_path:
            folder_path = self._updated_path(folder_path) if not folder_path.startswith("file") else folder_path
            for i in range(2):
                path_field = self.omni_driver.find_element(self._directory_path_picker)
                path_field.click(bring_to_front=True)
                self.omni_driver.wait(2)
                path_field.send_keys(folder_path)

        self.find_and_click(self._save_button)
        if overwrite:
            try:
                self.wait.element_to_be_located(self.omni_driver, self._overwrite_ok_button)
                self.find_and_click(self._overwrite_ok_button)
                self.log.info("Overwritten existing file.")
            except ElementNotFound:
                self.log.info("File was not present, saved it for first time.")

    
    def load_layout(
        self,
        file_name,
        folder_path="",
    ):
        """
        Loads the layout

        :param file_name: file name to be load
        :param folder_path: path of the folder to load the file
        :return: None
        """

        if folder_path:
            folder_path = self._updated_path(folder_path) if not folder_path.startswith("file") else folder_path
            for i in range(2):
                path_field = self.omni_driver.find_element(self._load_layout_directory_path_picker)
                path_field.click(bring_to_front=True)
                self.omni_driver.wait(2)
                path_field.send_keys(folder_path)
                element = self.omni_driver.find_element(self._load_layout_file_name_textarea)
                self.clear(locator=self._load_layout_file_name_textarea)
                element.send_keys(file_name)
        self.find_and_click(self._load_button)
