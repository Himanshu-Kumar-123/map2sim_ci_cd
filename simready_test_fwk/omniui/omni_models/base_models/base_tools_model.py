# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Tools Model class
   This module contains the base methods for Tools window
"""
from ..base_models.base_model import BaseModel



class BaseToolsModel(BaseModel):
    """Base model class for Tools window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to tools windows

    # Pivot Tool
    _pivot_tools_menupath = "Tools/Pivot"
    _add_pivot_btn = "Pivot Tool//Frame/**/Button[*].name=='AddPivot'"
    _remove_pivot_btn = "Pivot Tool//Frame/**/Button[*].name=='RemovePivot'"
    _pivot_x = "Pivot Tool//Frame/**/HStack[0]/FloatField[0]"
    _pivot_y = "Pivot Tool//Frame/**/HStack[1]/FloatField[0]"
    _pivot_z = "Pivot Tool//Frame/**/HStack[2]/FloatField[0]"

    # Array Tool
    _array_tool_manupath = "Tools/Array"
    _array_reset_btn = "Array Tool//Frame/**/Button[0].text=='Reset All'"
    _array_preview_btn = "Array Tool//Frame/VStack[0]/VStack[0]/HStack[0]/VStack[1]/Button[0]"

    
    def open_pivot_tools(self):
        """Opens pivot tools window"""
        self.omni_driver.select_menu_option(self._pivot_tools_menupath)
        self.log_info_with_screenshot("opened_pivot_tools")

    
    def add_pivot(self):
        "Adds pivot to prim"
        add_btn = self.find_and_click(self._add_pivot_btn)
        assert not add_btn.is_enabled(), "Clicking on add pivot did not disable the button"
        self.log_info_with_screenshot("clicked_on_add_pivot")

    
    def remove_pivot(self):
        "Removes pivot to prim"
        remove_btn = self.find_and_click(self._remove_pivot_btn)
        assert not remove_btn.is_enabled(), "Clicking on remove pivot did not disable the button"
        self.log_info_with_screenshot("clicked_on_remove_pivot")

    
    def add_pivot_value(self, pivot_value: list):
        "Adds X, Y and Z pivot values"
        if len(pivot_value) != 3:
            assert False, f"Please send X, Y and Z values for Pivot. Received was {pivot_value}"
        self.select_value_for_slider(self._pivot_x, pivot_value[0])
        self.select_value_for_slider(self._pivot_y, pivot_value[1])
        self.select_value_for_slider(self._pivot_z, pivot_value[2])
        self.log_info_with_screenshot("added_pivot_values")
