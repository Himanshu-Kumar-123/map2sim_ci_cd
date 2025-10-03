# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""View Toolbar class
   This module contains the base methods for Toolbar Window
"""


from ..base_models.base_view_toolbar_model import BaseViewToolbarModel


class ViewToolbarModel(BaseViewToolbarModel):
    """View Toolbar model class for View Toolbar

    Args:
        BaseViewToolbarModel (BaseViewToolbarModel): BaseViewToolbarModel class parent to
        ViewToolbar window class.
    """

    _tool_name = "USD Presenter Toolbar//Frame/**/Placer[0].name=='{}'"

    @property
    def is_displayed(self):
        """Returns whether toolbar is displayed"""
        return self.omni_driver.find_element("USD Presenter Toolbar").is_visible()

    
    def enable_measure_tool(self, window_name="Measure"):
        """Enables Measure Tool Window"""
        measure_tool = self.omni_driver.find_element(self._tool_name.format(window_name))
        if measure_tool.tool_button_is_checked():
            self.log.info("Measure Tool is already enabled")
            return
        measure_tool.click()
        measure = self.wait.element_to_be_located(self.omni_driver, window_name)
        self.wait.visibility_of_element(measure)

    
    def toggle_white_mode(self):
        """
        Enables the White mode of the Viewport
        """
        white_mode_tool = self.omni_driver.find_element(
            self._tool_name.format("white_mode")
        )
        if white_mode_tool.tool_button_is_checked():
            self.log.info("White Mode is already enabled")
            return
        white_mode_tool.click()
        self.log.info("White Mode is clicked")
        self.omni_driver.wait(2)

    
    def enable_tool_from_toolbar(self, window_name):
        """Enables the tool from the vertical toolbar"""
        tool = self.omni_driver.find_element(
            self._tool_name.format(window_name)
        )
        if tool.tool_button_is_checked():
            self.log.info(f"{window_name} is already enabled")
            return
        tool.click()
        self.log.info(f"{window_name} is clicked")
        self.omni_driver.wait(2)
        tool_window = self.wait.element_to_be_located(self.omni_driver, window_name)
        self.wait.visibility_of_element(tool_window)
