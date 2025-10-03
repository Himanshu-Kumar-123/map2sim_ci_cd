# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Main toolbar class
   This module contains the base methods for Base toolbar window
"""
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from ..base_models.base_model import BaseModel


class BaseMainToolBarModel(BaseModel):
    """Base model class for Main toolbar window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _play_btn = "Main ToolBar//Frame/VStack[0]/ToolButton[5]"
    _stop_btn = "Main ToolBar//Frame/VStack[0]/Button[0]"
    _select_prim_btn = "Main ToolBar//Frame/VStack[0]/ToolButton[0]"
    _drive_sim_scenario_editor = "Main ToolBar//Frame/VStack[0]/ToolButton[6]"
    _zerogravity_btn = "Main ToolBar//Frame/**/ToolButton[*].name=='zerogravity'"
    _Creation_btn = "Main ToolBar//Frame/VStack[0]/creation"

    def play_animation(self):
        """Method to click on start animation button"""
        play = self.omni_driver.find_element(self._play_btn)
        play.click()

    def is_animation_playing(self):
        """Returns whether animation is playing"""
        play_btn = self.omni_driver.find_element(self._play_btn, True)
        return play_btn.is_enabled() and play_btn.tool_button_is_checked()

    def stop_animation(self):
        """Method to click on stop animation button"""
        stop = self.omni_driver.find_element(self._stop_btn)
        stop.click()

    def toggle_select_prim(self, status: bool = True):
        """Toggles select prim"""
        select_prim = self.omni_driver.find_element(self._select_prim_btn, refresh=True)
        if status == True:
            if not select_prim.tool_button_is_checked():
                select_prim.click()
        else:
            if select_prim.tool_button_is_checked():
                select_prim.click()

    def toggle_drive_sim_scenario_editor(self, status: bool = True):
        """Toggles select prim"""
        scenario_tool = self.omni_driver.find_element(
            self._drive_sim_scenario_editor, refresh=True
        )
        if status == True:
            if not scenario_tool.tool_button_is_checked():
                scenario_tool.click()
        else:
            if scenario_tool.tool_button_is_checked():
                scenario_tool.click()

    def is_zerogravity_button_visible(self):
        """Method to check if zerogravity button is visible"""
        try:
            self.omni_driver.find_element(self._zerogravity_btn, refresh=True)
            self.log.info("Zero gravity button is visible")
            return True
        except ElementNotFound:
            self.log.info("Zero gravity button is not visible")
            return False

    def click_zerogravity_button(self):
        """Method to click on zerogravity button"""
        self.omni_driver.find_element(self._zerogravity_btn).click()

    def click_creation(self):
        """Method to click on creation button"""
        self.omni_driver.find_element(self._Creation_btn).click()

