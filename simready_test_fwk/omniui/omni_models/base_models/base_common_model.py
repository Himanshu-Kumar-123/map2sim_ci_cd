# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
"""Base Common model
    This module contains the base methods for small common windows
"""
from ..base_models.base_model import BaseModel


class BaseCommonModel(BaseModel):
    """Base model class for small common windows

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _new_edit_layer_button = "Opening a Read Only File//Frame/VStack[0]/VStack[0]/HStack[0]/Button[0]"
    _original_file_button = "Opening a Read Only File//Frame/VStack[0]/VStack[0]/HStack[1]/Button[0]"

    def handle_read_only_file(self, open_new_layer=False):
        """Handles Read only file prompt. Opens Original file by default.

        Args:
            open_new_layer (bool, optional): Opens file with new edit layer. Defaults to False.
        """
        if open_new_layer:
            self.find_and_click(self._new_edit_layer_button)
        else:
            self.find_and_click(self._original_file_button)
