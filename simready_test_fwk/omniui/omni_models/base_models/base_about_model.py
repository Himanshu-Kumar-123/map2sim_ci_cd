# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base About Model class
   This module contains the base methods for About modal that
    appears from File-> About
"""
import re


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.waits import Wait
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import ElementNotFound, PropertyRetrieveFailed


class BaseAboutModel(BaseModel):
    """Base model class for About modal

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for about modal
    _version = "About//Frame/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/VStack[0]/HStack[0]/ZStack[0]/" \
               "HStack[0]/VStack[2]/Label[1]"
    _loaded_plugins = "About//Frame/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Label[0]"
    _kit = "About//Frame/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/VStack[0]/Label[0]"
    _client_lib = "About//Frame/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/VStack[0]/Label[1]"
    _list_of_plugins = "About//Frame/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/ScrollingFrame[0]/VStack[0]/Label[*]"
    _close_btn = "About//Frame/ZStack[0]/VStack[0]/HStack[0]/Button[0]"

    def get_version(self):
        version = self.omni_driver.find_element(self._version)
        return version.get_text()

    def get_kit_value(self):
        kit = self.omni_driver.find_element(self._kit)
        return kit.get_text()

    def get_client_lib_value(self):
        client_lib = self.omni_driver.find_element(self._client_lib)
        return client_lib.get_text()

    def close(self):
        self.omni_driver.find_element(self._close_btn).click()

    def get_plugins(self):
        plugins_header = self.omni_driver.find_element(self._loaded_plugins).get_text()

        plugins_list = self.omni_driver.find_elements(self._list_of_plugins)
        plugins = [plugin.get_text() for plugin in plugins_list]
        pattern = r'\[[^\]]*\]'
        plugin_names = [re.sub(pattern, '', plugin) for plugin in plugins]
        return plugins_header, len(plugins_list), plugin_names
