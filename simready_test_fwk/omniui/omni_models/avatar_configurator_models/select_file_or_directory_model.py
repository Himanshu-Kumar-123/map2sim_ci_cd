# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Select File or Directory Model class
   This module contains the base methods for Select File or Directory window
"""
from omniui.omni_models.base_models.base_select_file_model import BaseSelectFileModel


class SelectFileOrDirectoryModel(BaseSelectFileModel):
    """Model class for Select File or Directory window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _window_name = "Select File or Directory"
    _file_or_folder_label = (
        _window_name + "//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    )
    _directory_path_picker = (
        _window_name
        + "//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    )
    _search_bar_folder_btn = (
        _window_name
        + "//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    )
    _ok_button = _window_name + "//Frame/VStack[0]/HStack[2]/Button[0]"

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
            usd_file.double_click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(
                    self._file_or_folder_label.replace("__name__", item)
                )
                self.omni_driver.wait(1)
        self.omni_driver.wait(2)

    def click_ok_button(self):
        """
        Clicks the ok button
        """
        self.find_and_click(self._ok_button)
        self.omni_driver.wait(10)
