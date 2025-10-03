"""Content Model class
   This module contains the base methods for Omnidriver
"""
from omni_remote_ui_automator.common.constants import RenderEngine
from omni_remote_ui_automator.driver.omnielement import OmniElement

from ..base_models.base_content_model import BaseContentModel


class ContentModel(BaseContentModel):
    """Content model class for Content window

    Args:
        ContentModel (BaseContentModel): Content class parent to BaseContentModel
    """

    def navigate_to_content_window(self):
        """Navigates to content window"""
        property_window = self.omni_driver.find_element(self._content_window)
        property_window.click()
        self.omni_driver.wait(1)

        if self.find(self._new_connection_server_name_txtbox):
            self.omni_driver.close_window("Add Nucleus connection")
        self.screenshot("navigated_to_content_window")