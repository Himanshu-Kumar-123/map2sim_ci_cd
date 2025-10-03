# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""SimReady Studio Mode Bar class
"""


from ..base_models.base_model import BaseModel


class BaseSimreadyStudioModeBarModel(BaseModel):
    """Base model class for SimReady Studio Mode Bar

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for open file modal
    _import_btn = "SimReady Studio ModeBar//Frame/**/Label[0].text=='Import'"
    _vehicles_test_btn = "SimReady Studio ModeBar//Frame/VStack[0]/HStack[0]/VStack[4]/Label[0].text=='Test'"
    _edit_btn = "SimReady Studio ModeBar//Frame/VStack[0]/HStack[0]/VStack[3]/Label[0].text=='Edit'"

    def wait_and_click_import(self):
        """Find and clicks import button"""
        self.wait.element_to_be_located(self.omni_driver, self._import_btn)
        self.find_and_click(self._import_btn)

    def wait_and_click_vehicle_test(self):
        """Find and clicks import button"""
        self.wait.element_to_be_located(self.omni_driver, self._vehicles_test_btn)
        self.find_and_click(self._vehicles_test_btn)
