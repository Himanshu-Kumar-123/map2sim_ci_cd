# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Load Definition Model class
   This module contains the base methods for Load Definition modal
"""


import os
from ..base_models.base_model import BaseModel


class BaseLoadDefinitionModel(BaseModel):
    """Base model class for Load Definition modal

    Args:
        BaseLoadDefinitionModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for Load Definition modal
    _directory_path_picker = (
        "Load Definition//Frame/**/StringField[*].identifier == 'filepicker_directory_path'"
    )
    _load_button = "Load Definition//Frame/VStack[0]/HStack[2]/Button[0]"
    _search_bar_folder_btn = "Load Definition//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    _file_or_folder_label = (
        "Load Definition//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    )

    def select_and_load_file(self, file: str):
        """
        Selects and loads the preset file
        Args:
            file: File to be loaded
        """
        self.find_and_click(locator=self._file_or_folder_label.replace("__name__", file),refresh=True)
        self.omni_driver.wait(2)
        self.find_and_click(self._load_button)
        self.omni_driver.wait(2)

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
