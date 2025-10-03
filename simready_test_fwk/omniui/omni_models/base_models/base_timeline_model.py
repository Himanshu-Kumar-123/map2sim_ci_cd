# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Timeline Model class
   This module contains the base methods for Timeline window
"""
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement



class BaseTimelineModel(BaseModel):
    """Base model class for Timeline toolbar window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Timeline window
    _start_time_code = "Timeline toolbar//Frame/**/Frame[0]/HStack[0]/StringField[0]"
    _end_time_code = "Timeline toolbar//Frame/**/scene_end"

    _timeline_widget = "Viewport//Frame/**/ZStack[*].name=='timeline_minibar_frame'"

    
    def get_start_time_code(self):
        """Gets start time code and returns it

        Returns:
            str: start time code
        """
        start_time_code = self.omni_driver.find_element(self._start_time_code, refresh=True)
        start_time = start_time_code.get_text()
        return start_time

    
    def get_end_time_code(self):
        """Gets end time code and returns it

        Returns:
            str: end time code
        """
        end_time_code = self.omni_driver.find_element(self._end_time_code, refresh=True)
        end_time = end_time_code.get_text()
        return end_time

    def get_timeline_position(self):
        """Gets the position info of timeline widget
        Retuns:
            dict
        """
        elm: OmniElement = self.omni_driver.find_element(self._timeline_widget, True)
        return elm.get_size_and_position("all")
