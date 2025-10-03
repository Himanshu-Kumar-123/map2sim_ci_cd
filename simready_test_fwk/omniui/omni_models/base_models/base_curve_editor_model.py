# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Curve Editor Model class
   This module contains the base methods for Curve Editor window
"""
from ..base_models.base_model import BaseModel


class BaseCurveEditorModel(BaseModel):
    """Base model class for Assets window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _curve_editor_window = "Curve Editor//Frame/VStack[0]"

    def open(self):
        """Navigates to curve editor window"""
        if "Curve Editor" in self.omni_driver.get_windows()["visible_windows"]:
            self.find_and_click(self._curve_editor_window)
        else:
            self.omni_driver.select_menu_option("Window/Animation/Curve Editor")
            self.find_and_click(self._curve_editor_window)
        self.log_info_with_screenshot("Navigated to curve editor")
