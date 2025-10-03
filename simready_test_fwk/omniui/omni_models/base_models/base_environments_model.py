# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
"""Base Environments class
   This module contains the base methods for Environments window
"""
import random
import time
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omniui.utils.utility_functions import occurrence_of_string_in_logs


class BaseEnvironmentsModel(BaseModel):
    """Base model class for Environments window
    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Materials window
    _environments_window = "Environments//Frame/VStack[0]"
    _all_environments = "Environments//Frame/VStack[0]/Stack[0]/ZStack[0]/**/HStack[0]/ZStack[1]/ZStack[0]/ScrollingFrame[0]/HStack[0]/VStack[0]/ThumbnailView[0]/Frame[*]"
    _environments_slider = "Environments//Frame/**/IntSlider[0]"

    # start of Locators related to SRS environment
    _srs_enviroment_system = "Environment System"
    _srs_apply_btn = "Environment System//Frame/ScrollingFrame[0]/VStack[0]/HStack[0]/Button[0].text=='APPLY'" 
    _env_settings_sliders = ["Environment System//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/HStack[0]/FloatSlider[0]", 
                                        "Environment System//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/HStack[1]/FloatSlider[0]", 
                                        "Environment System//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/HStack[2]/FloatSlider[0]", 
                                        "Environment System//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/HStack[3]/FloatSlider[0]"]    
    # end of Locators related to SRS environment

    def navigate_to_environments(self, timeout: float = 300, log_path: str = None):
        """Navigates to environments window"""
        environments_window = self.omni_driver.find_element(self._environments_window)
        environments_window.click()

        environments_loaded_string = "End traverse https://omniverse-content-staging.s3.us-west-2.amazonaws.com/Environments"
        if log_path is not None:
            loaded = False
            timeout = time.time() + timeout
            while time.time() < timeout:
                if occurrence_of_string_in_logs(environments_loaded_string, log_path) >= 1:
                    loaded = True
                    self.log.info("Environments loaded successfully.")
                    break
                self.omni_driver.wait(1)
            assert loaded, f"Environments did not load even after {timeout} seconds. Could not find the target string in logs."   
        self.screenshot("navigated_to_environments")

    
    def select_and_apply_environment(self, right_click=False):
        """Selects environments from window and apply to prim in viewport center
        Returns:
            Material Name: Returns the environment name of applied environment
        """
        environments = self.omni_driver.find_elements(self._all_environments)
        rand_value = random.randrange(0, len(environments))
        environment_label = environments[rand_value].find_element("**/Label[0]").get_text()
        self.omni_driver.find_element(self._environments_slider).send_keys(25)
        self.omni_driver.wait_frames(5)
        if right_click:
            environments[rand_value].right_click()
            self.omni_driver.select_context_menu_option("Set to Stage")
        else:
            environments[rand_value].double_click()
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(200)
    
    def navigate_to_srs_environment(self):
        """Navigates to environments window"""
        srs_environments_window = self.omni_driver.find_element(self._srs_enviroment_system)
        srs_environments_window.bring_to_front()

    def randrange_float(self, start, stop, step):
        return (random.randint(0, int((stop - start) / step)) * step + start)      

    def set_value_in_range(self, value, range1, range2):
        if value < range1:
            settingVal = range1
        elif value > range2:
            settingVal = range2
        else:
            settingVal = value
        return settingVal
    
    def set_and_apply_srs_env(self, index, value):
        self.omni_driver.find_element(self._env_settings_sliders[index]).send_keys(value)
        self.omni_driver.wait_frames(10)
        self.find_and_scroll_element_into_view(self._srs_apply_btn, ScrollAxis.Y, ScrollAmount.CENTER)
        self.find_and_click(self._srs_apply_btn)
        self.omni_driver.wait_frames(10)        
     
    def select_and_apply_all_srs_envs(self):
        # Elevation: increments of 10: -30 -> 60 
        # Cloudiness: increments of 0.25: 0.0 ->  1.25 
        # Azimuth: increments of 1.0: 0.0 -> 360.0 
        # Fog: increments of 0.1: 0.0 -> 1.0 
        _elevation_val = str(self.randrange_float(-30.0, 60.0, 10))
        _cloudiness_val = str(self.randrange_float(0.0, 1.25, 0.25))
        _azimuth_val = str(self.randrange_float(0.0, 360, 1.0))
        _fog_val = str(round(self.randrange_float(0.0, 1.0, 0.1),1))
        _env_settings_values = [_elevation_val,
                                _cloudiness_val,
                                _azimuth_val,
                                _fog_val]
        index = 0
        for index in range(4):
            self.set_and_apply_srs_env(index, _env_settings_values[index])

    def select_and_apply_srs_environment(self, stringVal = "None", value = 0):
        env_settings = ["Elevation", "Cloudiness", "Azimuth", "Fog"]
        if not stringVal == "None" and stringVal in env_settings:
            if stringVal == env_settings[0]:
                setVal = self.set_value_in_range(value, -30, 60)
                valueToApply = str(float(round(setVal/10)*10))
                index = 0
            elif stringVal == env_settings[1]:
                setVal = self.set_value_in_range(value, 0.0, 1.25)
                valueToApply = str(float(round(setVal/0.25)*0.25))
                index = 1
            elif stringVal == env_settings[2]:
                setVal = self.set_value_in_range(value, 0.0, 360)
                valueToApply = str(float(round(setVal)))
                index = 2
            elif stringVal == env_settings[3]:
                setVal = self.set_value_in_range(value, 0.0, 1.0)
                valueToApply = str(float(round(setVal,1)))
                index = 3
            self.set_and_apply_srs_env(index, valueToApply)
        else:
            self.select_and_apply_all_srs_envs()
