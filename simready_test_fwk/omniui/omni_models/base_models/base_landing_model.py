# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Landing model class
   This module contains the base methods for Landing Model for actions to perform as soon as app opens
"""
import time


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait


class BaseLandingModel(BaseModel):
    """BaseLandingModel class containing common methods"""

    _viewport_progress_bar = "Viewport//Frame/**/ProgressBar[*]"

    
    def wait_for_app_ready(self, timeout: int = 300, polling_freq: int = 1):
        """Waits for the app to be ready by checking if we are able to query any widget

        Args:
            timeout (int, optional):Timeout to wait for app ready. Defaults to 300.
            polling_freq (int, optional): Frequency of API calls. Defaults to 1.
        """
        try:
            Wait(20).element_to_be_located(
                self.omni_driver, self._viewport_progress_bar
            )
            Wait(100).element_to_be_invisible(
                self.omni_driver, self._viewport_progress_bar
            )
        except:
            self.log.info(
                "Progress bar was not caught, waiting for viewport FPS to get stabilized."
            )
        # wait for viewport FPS to stabilize
        target_fps = 40
        end = time.time() + timeout
        while time.time() < end:
            self.log.info(
                f"Wait for viewport FPS to stabilize. Target FPS: {target_fps}"
            )
            frame_info = self.omni_driver.get_viewport_info()["frame_info"]
            fps = frame_info.get("fps")
            if fps is None:
                fps = 0
            if fps >= target_fps:
                self.log.info("Application has loaded and is ready to use.")
                return
            time.sleep(polling_freq)
        assert False, f"App did not load in {timeout} time."
