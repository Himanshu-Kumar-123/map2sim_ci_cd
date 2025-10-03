# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Sim Ready Studio Open class
"""

from ..base_models.base_model import BaseModel


class BaseSimreadyStudioOpenWindowModel(BaseModel):
    """Base model class for Sim Ready Studio Open window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _recent_asset_btn = (
         #"SimReady Studio Open Window//Frame/ZStack[0]/Frame[0]/ZStack[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/TreeView[0]/VStack[0]/HStack[0]/VStack[1]/Label[0]=='vehicle_2016'"
        "SimReady Studio Open Window//Frame/**/ScrollingFrame[0]/**/Label[0]"
    )
    #_recent_asset_image = "SimReady Studio Open Window//Frame/ZStack[0]/Frame[0]/ZStack[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/TreeView[0]/VStack[0]/HStack[0]/VStack[0]/ImageWithProvider[0]"

    def select_recent_asset(self):
        """Find and selects recent asset"""
        recent_button = self.wait.element_to_be_located(self.omni_driver,self._recent_asset_btn)
        recent_button.click()