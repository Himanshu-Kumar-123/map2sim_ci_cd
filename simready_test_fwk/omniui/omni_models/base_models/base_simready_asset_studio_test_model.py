# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Simready Asset Studio Test  Model class
   This module contains the base methods for Simready Asset Studio Test Window
"""
from omniui.omni_models.base_models.base_model import BaseModel


class BaseSimreadyAssetStudioTestModel(BaseModel):
    """Base model class for Test window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _play_sim_label = "SimReady Studio Test Window//Frame/HStack[0]/ZStack[0]/Label[0].text=='Play Sim'"
    _stop_sim_label = "SimReady Studio Test Window//Frame/HStack[0]/ZStack[1]/Label[0].text=='Stop Sim'"

    def wait_and_click_playSim(self):
        """Find and clicks test Play Sim button"""
        _play_sim = self.omni_driver.find_element(self._play_sim_label)
        _play_sim.click()

    def zoom_out_viewport(self):
        "Zooms out so that the current car position is observed on the viewport"
        # self.omni_driver.reset_viewport_camera()
        self.omni_driver.wait(2)
        self.omni_driver.zoom_viewport("Out", start=1.0, end=50.0)
        self.omni_driver.wait(2)

    def wait_and_click_stopSim(self):
        """Find and clicks test Stop Sim button"""
        _stop_sim = self.omni_driver.find_element(self._stop_sim_label)
        _stop_sim.click()
