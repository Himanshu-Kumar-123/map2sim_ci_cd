# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Props Physics Model class
   This module contains the base methods for Physics Window in Props WF
"""
from omniui.omni_models.base_models.base_model import BaseModel


class BasePropsPhysicsModel(BaseModel):
    """Base model class for Physics window in Props WF

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _props_physics_window = "Prop Physics"
    _create_rigid_bodies_btn = "Prop Physics//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/HStack[0]/Button[0].text=='Create rigid body for prop'"
    _start_test_btn = (
        "Prop Physics//Frame/VStack[0]/HStack[0]/Button[0].text=='Start test'"
    )
    _restart_test_btn = (
        "Prop Physics//Frame/VStack[0]/HStack[0]/Button[0].text=='Restart test'"
    )
    _end_test_btn = "Prop Physics//Frame/VStack[0]/HStack[0]/Button[1].text=='End test'"

    def navigate_to_physics_window(self):
        """Navigates to physics window"""
        physics_window = self.omni_driver.find_element(self._props_physics_window)
        physics_window.bring_to_front()

    def create_rigid_bodies(self):
        """Finds and clicks Create rigid body button"""
        self.find_and_click(self._create_rigid_bodies_btn)

    def wait_and_click_start_test(self):
        """Finds and clicks start test btn"""
        self.find_and_click(self._start_test_btn)

    def wait_and_click_restart_test(self):
        """Finds and clicks restart test btn"""
        self.find_and_click(self._restart_test_btn)

    def click_end_test(self):
        """Finds and clicks End test btn"""
        self.find_and_click(self._end_test_btn)
