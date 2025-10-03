# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Sim Ready Studio Edit class
"""

from .base_model import BaseModel


class BaseSimreadyStudioEditModel(BaseModel):
    """Base model class for Sim Ready Studio Edit window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _props_physics_btn = "SimReady Studio Edit Window//Frame/ZStack[0]/VStack[0]/HStack[1]/HStack[0]/ZStack[2]/Label[0].text=='Physics'"
    _props_labels_btn = "SimReady Studio Edit Window//Frame/**/Label[0].text=='Labels'"
    _tags_and_thumbnails_tab = "SimReady Studio Edit Window//Frame/ZStack[0]/VStack[0]/HStack[1]/HStack[1]/ZStack[1]/Label[0]"
    _stage_lighting_checkbox = "SimReady Studio Edit Window//Frame/ZStack[0]/VStack[0]/HStack[1]/HStack[2]/VStack[0]/HStack[0]/CheckBox[0]"

    def wait_and_click_labels_btn(self):
        """Find and clicks labels button"""
        self.wait.element_to_be_located(self.omni_driver, self._props_labels_btn)
        self.find_and_click(self._props_labels_btn)

    def wait_and_click_physics_btn(self):
        """Find and clicks physics button"""
        self.wait.element_to_be_located(self.omni_driver, self._props_physics_btn)
        self.find_and_click(self._props_physics_btn)

    def select_tags_and_thumbnail_tab(self):
        self.find_and_click(self._tags_and_thumbnails_tab)

    def disable_stage_lighting(self):
        "disables the stage lighting, if enabled; so that the light updates can be observed easily"
        stage_lighting = self.omni_driver.find_element(self._stage_lighting_checkbox)
        if stage_lighting.is_enabled():
            self.find_and_click(self._stage_lighting_checkbox)
        stage_lighting = self.omni_driver.find_element(self._stage_lighting_checkbox,refresh=True)
        assert stage_lighting.is_checked() == False, "Stage lighting is not disabled"