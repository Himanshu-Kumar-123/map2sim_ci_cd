# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimProperty Model class
   This module contains the base methods for DriveSimProperty window
"""

from .base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait

class BaseDriveSimPropertyModel(BaseModel):
    """Base model class for DriveSimProperty window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """
    
    def get_asset_cartesian_coordinate(self, _cartesian_x, _cartesian_y, _cartesian_z):
        """Returns the x, y, z cartesian coordinates of an asset"""

        element_id = self.omni_driver.find_element(_cartesian_x)
        Cartesian_x = element_id.get_float_value()

        element_id = self.omni_driver.find_element(_cartesian_y)
        Cartesian_y = element_id.get_float_value()

        element_id = self.omni_driver.find_element(_cartesian_z)
        Cartesian_z = element_id.get_float_value()

        return Cartesian_x, Cartesian_y, Cartesian_z