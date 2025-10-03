# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""View Content Model class
   This module contains the methods for View Content Window
"""
from ..base_models.base_content_model import BaseContentModel


class ContentModel(BaseContentModel):
    """View model class for Content window

    Args:
        ViewContentModel (BaseContentModel): BaseContentModel class for base Content Window
    """

    # Locators for widgets
    _directory_path_picker = "Open File//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _search_bar_folder_btn = "Open File//Frame/**/Frame[*]/**/Button[*].text=='__folder__'"
    _add_new_connection = "Open File//Frame/**/Label[*].text=='Add New Connection ...'"
    _server_added = "Open File//Frame/**/Label[*].text=='__server__'"
    _content_window = "Open File//Frame/VStack[0]"
