# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Welcome to Omniverse model class
   This module contains the base methods for Share Omniverse USD Path Model for actions to perform
"""
from ..base_models.base_model import BaseModel


class BaseShareOmniverseUSDPathModel(BaseModel):
    """BaseShareOmniverseUSDPathModel class containing common methods"""

    # Widget Locators
    _copy_path_to_clipboard = \
        "Share Omniverse USD Path//Frame/**/Button[0].text=='Copy Path to Clipboard'"
    _share_omniverse_usd_path_window = "Share Omniverse USD Path"

    def click_copy_path_to_clipboard(self):
        """Method to click copy the usd path to clipboard"""
        copy_path_button = self.omni_driver.find_element(self._copy_path_to_clipboard)
        copy_path_button.click()
        self.omni_driver.wait(2)
        self.log.info("Clicked Copy Path to Clipboard button.")
        self.screenshot("after_clicking_copy_path_to_clipboard")
        share_omniverse_usd_path_window = \
            self.omni_driver.find_element(self._share_omniverse_usd_path_window)
        self.wait.invisibility_of_element(share_omniverse_usd_path_window)
