# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base USD paths Model class
   This module contains the base methods for USD paths window
"""
from ..base_models.base_model import BaseModel


class BaseUSDPathsModel(BaseModel):
    """Base model class for USD paths window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to USD paths window
    _regex_button = "USD Paths//Frame/**/Button[0].text=='Regex'"
    _search_field = "USD Paths//Frame/VStack[0]/VStack[0]/HStack[0]/ZStack[0]/StringField[0]"
    _reload_path_button = "USD Paths//Frame/**/Button[0].text==' Reload paths '"
    _preview_button = "USD Paths//Frame/**/Button[1].text==' Preview '"
    _apply_button = "USD Paths//Frame/**/Button[2].text==' Apply '"
    _reloaded_path = "USD Paths//Frame/**/ScrollingFrame[0]/**/StringField[0]"

    def _search_path(self, path: str):
        """Enters given path in search field

        Args:
            path (str): path to be searched
        """
        search_field = self.omni_driver.find_element(self._search_field)
        search_field.send_keys(path)

    def _reload_path(self):
        """Reloads paths"""
        self.find_and_click(self._reload_path_button)
        self.wait.element_to_be_located(self.omni_driver, self._reloaded_path)

    def _apply(self):
        """Applies paths"""
        self.find_and_click(self._apply_button)
        self.omni_driver.wait(5)
        self.omni_driver.wait_for_stage_load()

    def _toggle_regex(self, enabled: bool):
        """Toggles regex

        Args:
            enabled (bool): state of regex
        """
        regex_button = self.omni_driver.find_element(self._regex_button)
        if enabled:
            if not regex_button.is_checked():
                regex_button.click()
        else:
            if regex_button.is_checked():
                regex_button.click()

    
    def navigate_to_usd_path(self):
        """Opens USD paths window"""
        self.omni_driver.select_menu_option("Window/Utilities/USD Paths")

    
    def apply_paths(self, path: str, regex: bool):
        """Searches for a path, reloads it and applies it

        Args:
            path (str): path to be applied
            regex (bool): Whether regex should be enabled or disabled
        """
        self._search_path(path)
        self._toggle_regex(True)
        self._toggle_regex(True)
        self._reload_path()
        self.find_and_click(self._preview_button)
        self._apply()
