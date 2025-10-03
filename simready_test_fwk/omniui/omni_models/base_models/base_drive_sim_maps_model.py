# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimMaps Model class
   This module contains the base methods for DriveSimMaps window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait


class BaseDriveSimMapsModel(BaseModel):
    """Base model class for DriveSimMaps window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for DriveSimMaps window
    _create_scenario = "Drivesim Scenario Maps Window//Frame/**/Label[0].text == 'Create a new scenario'"
    _search_field = (
        "Drivesim Scenario Maps"
        " Window//Frame/ZStack[0]/Frame[0]/**/HStack[0]/ZStack[0]/HStack[0]/ZStack[1]/StringField[0]"
    )

    _search_results_images = "Drivesim Scenario Maps Window//Frame/**/VGrid[0]/ZStack[*]/**/Frame[0]/Image[0]"
    _open_selected_map_btn = "Drivesim Scenario Maps Window//Frame/**/Label[0].text == 'Open selected map'"

    _loading_btn = "Loading"
    _selected_payloads_confirm_btn = "Select Payloads To Load//Frame/**/Button[0].text == 'Ok'"
    _show_experimental_btn = "Drivesim Scenario Maps Window//Frame/ZStack[0]/Frame[0]/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/VStack[0]/HStack[1]/VStack[0]/CheckBox[0]"
    
    def create_new_scenario(self):
        """Click on create new scenario Button"""
        self.find_and_click(self._create_scenario, refresh=True)

    def enter_search_field(self, text: str):
        """Enter text in search field

        Args:
            text (str): Name of scenario
        """
        self.find_and_enter_text(self._search_field, text)

    def click_open_selected_map_btn(self):
        """Click on open Selected Map Button"""
        self.find_and_click(self._open_selected_map_btn)

    def confirm_payloads_selection(self):
        """Click on Confirm payloads Button"""
        self.find_and_click(self._selected_payloads_confirm_btn, bring_to_front=False)

    def wait_for_loading_button(self, timeout=180):
        """Wait's for loading button to be invisible

        Args:
            timeout (int): Time to wait in seconds
        """
        wait = Wait(timeout)
        wait.invisibility_of_element(self.find(self._loading_btn, True))

    def search_and_open_scene(self, scene: str, index=0, wait_time=180):
        """Search and open's a scenario from main window

        Args:
            scene (str): Name of scene
            index (int): Search result index to open
            wait_time(int): waiting for time until searched scene is visible
        """
        self.find_and_click(self._show_experimental_btn, refresh=True)
        self.enter_search_field(scene)
        self.omni_driver.wait(10)
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._search_results_images)
        results = self.omni_driver.find_elements(self._search_results_images)
        results[index].click()
        self.omni_driver.wait(1)

        self.click_open_selected_map_btn()

        self.wait.element_to_be_located(self.omni_driver, self._selected_payloads_confirm_btn)
        self.confirm_payloads_selection()
    
    def wait_for_create_button(self, timeout=600):
        """Wait's for create scenario button to be invisible

        Args:
            timeout (int): Time to wait in seconds
        """
        wait = Wait(timeout)
        wait.element_to_be_located(self.omni_driver, self._create_scenario)
        self.omni_driver.wait(2)
        # wait.element_to_be_enabled(self.find(self._create_scenario, True))