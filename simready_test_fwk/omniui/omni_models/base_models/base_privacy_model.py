# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Privacy class
   This module contains the base methods for Privacy window available at startup
"""

from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BasePrivacyModel(BaseModel):
    """Base model class for Privacy window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Common locators
    _privacy_checkbox = "Privacy//Frame/**/CheckBox[*]"
    _privacy_ok_btn = "Privacy//Frame/**/Button[*]"

    def handle_privacy_window(self):
        """Method to handle and accept privacy window after app is launched"""
        try:
            privacy_button = self.omni_driver.find_element(self._privacy_ok_btn)
            privacy_button.click()
            self.omni_driver.wait(2)
            self.log.info("Clicked and handled privacy window.")
            self.screenshot("handled_privacy_window")
        except ElementNotFound:
            self.log.warning("Privacy window not present.")
            self.screenshot("privacy_window_not_present")
