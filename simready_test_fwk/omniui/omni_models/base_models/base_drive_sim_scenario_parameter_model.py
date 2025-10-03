# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimProperty Model class
   This module contains the base methods for DriveSimProperty window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.common.enums import MeasureMode, ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.waits import Wait

class BaseDriveSimScenarioParamterModel(BaseModel):
    """Base model class for DriveSimProperty window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """
    
    _scenario_parameters_window = "Scenario Parameters//Frame/ScrollingFrame[*]/VStack[*]"
    _scenario_parameters_env_btn = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/Frame[0]/HStack[0]/title.text=='Environment'"
    _scenario_parameters_sun_btn = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[0]/Frame[0]/**/Frame[0]/HStack[0]/title.text=='Sun'"
    _scenario_parameters_weather_btn = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[2]/Frame[0]/**/Frame[0]/HStack[0]/title.text=='Weather'"
    _scenario_parameters_cloud_coverage = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[2]/Frame[0]/**/HStack[0]/HStack[0]/ZStack[0]/float_slider_cloudCoverage"
    _scenario_parameters_sun_azimuth = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[0]/Frame[0]/**/HStack[1]/HStack[0]/ZStack[0]/float_slider_azimuth"
    _scenario_parameters_sun_elevation = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[0]/Frame[0]/**/HStack[2]/HStack[0]/ZStack[0]/float_slider_elevation"
    _scenario_parameters__sun_time_of_day = "Scenario Parameters//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]/**/VStack[0]/CollapsableFrame[0]/Frame[0]/**/VStack[0]/HStack[0]/HStack[0]/VStack[0]/ZStack[0]/Placer[0]/bool_overrideTimeOfDay"
        
    def open_env_tab(self):
        """Opens the environment tab"""
        self.find_and_click(self._scenario_parameters_env_btn, refresh=True)

    def navigate_to_scenario_parameter(self):
        """Navigates to scenario parameter window"""
        stage_window = self.omni_driver.find_element(self._scenario_parameters_window, refresh=True)
        stage_window.click()

    def open_sun_tab(self):
        """Opens the sun tab"""
        self.find_and_click(self._scenario_parameters_sun_btn, refresh=True)

    def open_weather_tab(self):
        """Opens the weather tab"""
        scroll__scenario_parameters_window=self.find_and_scroll_element_into_view(
            self._scenario_parameters_weather_btn,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
        )
        scroll__scenario_parameters_window.click()

    def set_sun_azimuth_postion(self, azimuth_value:str):
        """Sets the sun azimuth

        Args:
            azimuth_value (str): Value to set the azimuth to.
        """
        element = self.find_and_click(self._scenario_parameters_sun_azimuth, refresh=True, double_click=True)
        self.omni_driver.wait(2)
        self.clear_textbox(element)
        element.send_keys(azimuth_value)
        self.omni_driver.wait(2)

    def set_sun_elevation_postion(self, elevation_value:str):
        """Sets the sun elevation

        Args:
            elevation_value (str): Value to set the elevation to.
        """
        element = self.find_and_click(self._scenario_parameters_sun_elevation, refresh=True, double_click=True)
        self.omni_driver.wait(2)
        self.clear_textbox(element)
        element.send_keys(elevation_value)
        self.omni_driver.wait(2)

    def toggle_overrid_time_of_day_checkbox(self, check_on:bool = True):
        """Toggles the override time of day checkbox"""
        self.toggle_checkbox(self._scenario_parameters__sun_time_of_day, check_on)

    def set_cloud_coverage(self):
        """Sets the cloud coverage"""
        self.select_value_for_slider(self._scenario_parameters_cloud_coverage, value=4)

    def change_sun_position(self, azimuth_value:str, elevation_value:str, check_on: bool):
        """Changes the sun position

        Args:
            azimuth_value (str): Value to set the azimuth.
            elevation_value (str): Value to set the elevation.
            check_on (bool): Whether to check the override time of day checkbox.
        """
        self.navigate_to_scenario_parameter()
        self.open_env_tab()
        self.open_sun_tab()
        self.set_sun_azimuth_postion(azimuth_value)
        self.set_sun_elevation_postion(elevation_value)
        self.toggle_overrid_time_of_day_checkbox(check_on)

        self.omni_driver.wait(2)
        self.open_weather_tab()
        self.set_cloud_coverage()

    def change_weather_condition(self):
        """Changes the weather condition"""
        self.navigate_to_scenario_parameter()
        self.open_env_tab()
        self.open_weather_tab()
        self.set_cloud_coverage()
        self.omni_driver.wait(10)
