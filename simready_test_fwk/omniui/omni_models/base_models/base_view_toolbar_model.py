# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base View Toolbar class
   This module contains the base methods for Measure Window
"""


from ..base_models.base_model import BaseModel


class BaseViewToolbarModel(BaseModel):
    """Base View Toolbar model class for View Toolbar

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _tool_name = "View Toolbar//Frame/**/ToolButton[*].name=='{}'"

    def enable_measure_tool(self, window_name="Measure"):
        "Enables Measure Tool Window"
        measure_tool = self.omni_driver.find_element(self._tool_name.format(window_name))
        if measure_tool.tool_button_is_checked():
            self.log.info("Measure Tool is already enabled")
            return
        measure_tool.click()
        measure = self.wait.element_to_be_located(self.omni_driver, window_name)
        self.wait.visibility_of_element(measure)

    def enable_section_tool(self, window_name="Section"):
        "Enables Section Tool Window"
        section_tool = self.omni_driver.find_element(self._tool_name.format(window_name))
        if section_tool.tool_button_is_checked():
            self.log.info("Section Tool is already enabled")
            return
        section_tool.click()
        section = self.wait.element_to_be_located(self.omni_driver, window_name)
        self.wait.visibility_of_element(section)

    @property
    def is_displayed(self):
        """Returns whether toolbar is displayed"""
        return self.omni_driver.find_element("View Toolbar").is_visible()

    def enable_render_settings(self):
        "Enables Renders Settings Window"
        render_settings_tool = self.omni_driver.find_element(self._tool_name.format("Render Settings"))
        if render_settings_tool.tool_button_is_checked():
            return
        render_settings_tool.click()
        self.wait.element_to_be_located(self.omni_driver, "Render Settings")
        measure = self.omni_driver.find_element("Render Settings")
        self.wait.visibility_of_element(measure)
