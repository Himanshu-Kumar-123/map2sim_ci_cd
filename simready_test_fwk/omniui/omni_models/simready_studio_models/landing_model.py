# Copyright (c) 202, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Landing model class
   This module contains the methods for Landing Model for actions to perform as soon as app opens
"""


from omniui.omni_models.base_models.base_model import BaseModel


class LandingModel(BaseModel):
    """LandingModel class containing common methods"""

    _import_btn = "SimReady Studio ModeBar//Frame/**/Label[0].text=='Import'"

    def wait_for_app_ready(self, timeout: int = 300, polling_freq: int = 1):
        """Waits for the app to be rady by checking if we are able to query any widget

        Args:
            timeout (int, optional):Timeout to wait for app ready. Defaults to 300.
            polling_freq (int, optional): Frequency of API calls. Defaults to 1.
        """
        self.wait.timeout = timeout
        self.wait.polling_interval = polling_freq
        self.wait.element_to_be_located(self.omni_driver, self._import_btn)
    
