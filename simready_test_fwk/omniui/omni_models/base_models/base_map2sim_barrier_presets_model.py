# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Map2simBarrierPresets Model class
   This module contains the base methods for Map2simBarrierPresets window
"""

import time
from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait

class BaseMap2simBarrierPresetsModel(BaseModel):
    """Base model class for Map2simBarrierPresets window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Terrain Selection Elements
    _terrain_selection_combo = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/HStack[1]/ComboBox[0]"
    )

    _load_terrain_button = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/**/HStack[0]/Button[0]"
    )

    # Barrier Type Selection
    _barrier_type_combo = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[1]/CollapsableFrame[0]/**/HStack[1]/ComboBox[0]"
    )

    _fence_preset_combo = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[1]/CollapsableFrame[1]/**/HStack[1]/ComboBox[0]"
    )

    # Configuration Options  
    _elevation_adaptation_checkbox = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[2]/CollapsableFrame[0]/**/HStack[0]/CheckBox[0]"
    )

    _fence_height_slider = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[2]/CollapsableFrame[0]/**/HStack[1]/FloatSlider[0]"
    )

    _spacing_interval_field = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[2]/CollapsableFrame[0]/**/HStack[2]/FloatField[0]"
    )

    # Action Buttons
    _apply_barrier_presets_button = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[3]/HStack[0]/Button[0]"
    )

    _preview_button = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[3]/HStack[1]/Button[1]"
    )

    _reset_button = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[3]/HStack[2]/Button[2]"
    )

    # Status and Progress
    _generation_progress_bar = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[4]/ProgressBar[0]"
    )

    _status_label = (
        "Barrier Presets//Frame/ScrollingFrame[0]/VStack[4]/Label[0]"
    )

    def select_terrain_type(self, terrain_name):
        """Selects terrain type by name from dropdown

        Args:
            terrain_name (str): Name of the terrain to select
        """
        self.select_item_by_name_from_combo_box(self._terrain_selection_combo, terrain_name)

    def load_terrain(self):
        """Clicks on Load Terrain button"""
        self.find_and_click(self._load_terrain_button, refresh=True)

    def select_barrier_type(self, barrier_type):
        """Selects barrier type from dropdown

        Args:
            barrier_type (str): Type of barrier to select (e.g., 'Fence', 'Wall', 'Guardrail')
        """
        self.select_item_by_name_from_combo_box(self._barrier_type_combo, barrier_type)

    def select_fence_preset(self, preset_name):
        """Selects fence preset from dropdown

        Args:
            preset_name (str): Name of the fence preset to select
        """
        self.select_item_by_name_from_combo_box(self._fence_preset_combo, preset_name)

    def enable_elevation_adaptation(self, enable=True):
        """Enables or disables elevation adaptation checkbox

        Args:
            enable (bool): True to enable, False to disable
        """
        self.toggle_checkbox(self._elevation_adaptation_checkbox, enable)

    def set_fence_height(self, height_value):
        """Sets fence height using slider

        Args:
            height_value (float): Height value for the fence
        """
        self.set_slider_value(self._fence_height_slider, height_value)

    def set_spacing_interval(self, interval_value):
        """Sets spacing interval between fence posts

        Args:
            interval_value (float): Spacing interval value
        """
        element = self.omni_driver.find_element(self._spacing_interval_field)
        element.click()
        self.omni_driver.wait(1)
        element.send_keys(str(interval_value))

    def apply_barrier_presets(self):
        """Clicks on Apply Barrier Presets button"""
        self.find_and_click(self._apply_barrier_presets_button, refresh=True)

    def preview_barriers(self):
        """Clicks on Preview button to preview barriers before applying"""
        self.find_and_click(self._preview_button, refresh=True)

    def reset_configuration(self):
        """Clicks on Reset button to reset all configurations"""
        self.find_and_click(self._reset_button, refresh=True)

    def wait_for_generation_complete(self, timeout=120):
        """Waits for barrier generation to complete

        Args:
            timeout (int): Maximum time to wait in seconds
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                status_element = self.omni_driver.find_element(self._status_label)
                status_text = status_element.get_text()
                
                if "Complete" in status_text or "Finished" in status_text:
                    self.log.info("Barrier generation completed successfully")
                    return True
                elif "Error" in status_text or "Failed" in status_text:
                    self.log.error(f"Barrier generation failed: {status_text}")
                    return False
                    
                self.omni_driver.wait(2)
            except:
                self.omni_driver.wait(2)
                continue
                
        self.log.error(f"Barrier generation did not complete within {timeout} seconds")
        return False

    def get_generation_progress(self):
        """Gets current generation progress percentage

        Returns:
            float: Progress percentage (0-100)
        """
        try:
            progress_element = self.omni_driver.find_element(self._generation_progress_bar)
            # This would depend on how the progress bar exposes its value
            # You may need to adjust based on actual implementation
            progress_value = progress_element.get_property("value")
            return float(progress_value) if progress_value else 0.0
        except:
            return 0.0

    def get_status_text(self):
        """Gets current status text

        Returns:
            str: Current status message
        """
        try:
            status_element = self.omni_driver.find_element(self._status_label)
            return status_element.get_text()
        except:
            return "Status unavailable"

    def configure_fence_for_elevation_testing(self):
        """Configures fence settings specifically for elevation testing"""
        # Select appropriate terrain with elevation variation
        self.select_terrain_type("Terrain with Elevation")
        self.omni_driver.wait(2)
        
        # Load the terrain
        self.load_terrain()
        self.omni_driver.wait(5)
        
        # Select fence as barrier type
        self.select_barrier_type("Fence")
        self.omni_driver.wait(2)
        
        # Select standard fence preset
        self.select_fence_preset("Standard Fence")
        self.omni_driver.wait(2)
        
        # Enable elevation adaptation
        self.enable_elevation_adaptation(True)
        self.omni_driver.wait(1)
        
        # Set appropriate fence height
        self.set_fence_height(2.0)  # 2 meter height
        self.omni_driver.wait(1)
        
        # Set reasonable spacing
        self.set_spacing_interval(3.0)  # 3 meter intervals
        self.omni_driver.wait(1)
        
        self.log.info("Configured fence settings for elevation testing") 