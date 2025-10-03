# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Add New Search Path Model class
   This module contains the base methods for Add New Search Path toolbar window
"""
from ..base_models.base_model import BaseModel


class BaseAddNewSearchPathModel(BaseModel):
    """Base model class for Add New Search Path Model window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _directory_path_picker = (
        "Add New Search Path//Frame/**/StringField[*].identifier == 'filepicker_directory_path'"
    )
    _file_or_folder_label = (
        "Add New Search Path//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    )
    _select_button = "Add New Search Path//Frame/VStack[0]/HStack[2]/Button[0]"

    def enter_path_and_select(self, path: str, assert_file_or_folder: str):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
            assert_file_or_folder (str): To check file/folder present in path for
            successful navigation
        """
        self.find_and_enter_text(self._directory_path_picker, path)
        self.wait.element_to_be_located(
            self.omni_driver,
            self._file_or_folder_label.replace("__name__", assert_file_or_folder),
        )
        self.find_and_click(self._select_button)
