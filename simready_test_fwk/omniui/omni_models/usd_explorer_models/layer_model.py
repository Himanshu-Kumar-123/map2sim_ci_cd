# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Layer Model class
   This module contains the methods for Measure Window
"""
from omni_remote_ui_automator.common.enums import MeasureMode
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


from ..base_models.base_layer_model import BaseLayerModel
from omniui.framework_lib.softassert import SoftAssert


class LayerModel(BaseLayerModel):
    """Layer model class for Measure Tool

    Args:
        LayerModel (BaseLayerModel): BaseLayerModel class is base class for measure window
    """
    _window = "Layer"

    def navigate_to_window(self):
        """Navigates to Layer window"""
        if self._window not in self.omni_driver.get_windows()["visible_windows"]:
            self.omni_driver.select_menu_option("Window/Layer")
        window = self.wait.element_to_be_located(self.omni_driver, self._root)

        window.click()
    

