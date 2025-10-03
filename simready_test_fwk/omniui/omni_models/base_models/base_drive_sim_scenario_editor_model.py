# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimScenarioEditor Model class
   This module contains the base methods for DriveSimScenarioEditor window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait

class BaseDriveSimScenarioEditorModel(BaseModel):
    """Base model class for DriveSimScenarioEditor window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _placer_tab = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/**/TreeView[0]/HStack[*]/**/Label[0].text=='Placer'"
    )

    _data_Studio_tab = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/**/TreeView[0]/HStack[*]/**/Label[0].text=='Data Studio'"
    )
    
    _vehicle_section = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/**/ScrollingFrame[0]/TreeView[0]/HStack[*]/Label[0].text"
        " == 'Vehicles (68)'"
    )

    _ego_section = "Drivesim Scenario Editor Tools Manager Window//Frame/**/Label[0].text=='Ego vehicles (8)'"
        
    _pedestrian_section = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/**/ScrollingFrame[0]/TreeView[0]/HStack[*]/Label[0].text"
        " == 'Pedestrians (53)'"
    )
    _search_results_thumbnails = (
        "Drivesim Scenario Editor Tools Manager"
        " Window//Frame/**/ScrollingFrame[0]/ZStack[0]/Frame[0]/VGrid[0]/ZStack[*]/**/Frame[0]/Image[0]"
    )

    _vehicle_base_path = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/**/Frame[0]/Title"
    )

    _pedestrian_base_path = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/VStack[0]/ZStack[0]/ScrollingFrame[0]/ZStack[0]/Frame[0]/VGrid[0]/ZStack[0]/HStack[0]/VStack[0]/VStack[0]/Frame[0]/Title"
    )

    _search_asset_textarea = (
        "Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/Frame[0]/VStack[0]/VStack[0]/Frame[0]/VStack[0]/ZStack[0]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/ZStack[1]/HStack[0]/Search"
    )

    _script_editor_textarea = (
        "Script Editor//Frame/ScriptEditorWidget[0]"
    )

    _driving_state_combo = ("Property//Frame/VStack[0]/canvas/main_v_stack/groupFrame/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/subFrame/frame_v_stack/subFrame/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/frame_v_stack/HStack[21]/ZStack[0]/token_action:forward:refTrafficModelVehicle:drivingState")
    
    def open_placer_menu(self):
        """Clicks on Placer menu"""
        self.find_and_click(self._placer_tab, refresh=True)

    def open_data_studio_tab(self):
        """Clicks on Data Studio Tab"""
        self.find_and_click(self._data_Studio_tab, refresh=True)

    def click_on_vehicle_section(self):
        """Clicks on Vehicles section"""
        self.find_and_click(self._vehicle_section, refresh=True)

    def click_on_pedestrians_section(self):
        """Clicks on Vehicles section"""
        self.find_and_click(self._vehicle_section, refresh=True)
    
    def click_on_ego_section(self, wait_time=180):
        """Clicks on Ego section
        
        Args:
            wait_time(int): waiting for time until ego section is visible
        """
        wait = Wait(wait_time)
        wait.element_to_be_located(self.omni_driver,self._ego_section)
        self.find_and_click(self._ego_section, refresh=True)

    def click_on_pedestrian_section(self):
        """Clicks on Pedestrian section"""
        self.find_and_click(self._pedestrian_section, refresh=True)

    def get_search_results_thumbnails(self):
        """Returns list of thumbnails visible in search result"""
        return self.omni_driver.find_elements(self._search_results_thumbnails)

    def vehicle_to_place(self, vehicle_name):
        """Returns the Vehicle to be spawned"""

        _vehicle_name = f"{self._vehicle_base_path}.text=='{vehicle_name}'"

        return self.omni_driver.find_element(_vehicle_name)
    
    def pedestrian_to_place(self, pedestrian_name):
        """Returns the pedestrian to be spawned"""

        _pedestrian_name = f"{self._pedestrian_base_path}.text=='{pedestrian_name}'"

        return self.omni_driver.find_element(_pedestrian_name)
    
    def search_asset_from_placer(self, search_asset_name):
        """Inputs the name of asset to be searched"""

        element = self.omni_driver.find_element(self._search_asset_textarea)
        element.double_click()
        self.omni_driver.wait(2)

        self.omni_driver.emulate_char_press(search_asset_name)

    def enter_script_editor(self, api_script):
        """Inputs the script in the script editor"""

        element = self.omni_driver.find_element(self._script_editor_textarea)
        element.double_click()
        self.omni_driver.wait(2)

        self.omni_driver.emulate_char_press(api_script)

    def get_entity_driving_list(self):
        """Clicks on load button to load a toml"""
        combobox_element = self.omni_driver.find_element(self._driving_state_combo)
        combobox_dict = combobox_element.get_combobox_info()
        combobox_list = combobox_dict["all_options"]
        return combobox_list
 
    def select_entity_driving_state(self, driving_state_name):
        """Clicks on ComboBox button to load a driving state with index"""
        combobox_list = self.get_entity_driving_list()
        driving_state_index = combobox_list.index(driving_state_name)
        self.select_item_from_stack_combo_box(self._driving_state_combo, driving_state_index)