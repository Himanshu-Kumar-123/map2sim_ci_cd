# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base DriveSimScenarioAction Model class
   This module contains the base methods for DriveSimScenarioAction window
"""
from .base_model import BaseModel


class BaseDriveSimScenarioActionModel(BaseModel):
    """Base model class for DriveSimScenarioAction window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _add_action_to_entity_btn = "Drivesim Scenario Action Window//Frame/**/Button[0].text == 'Add Action to Entity'"
    _action_list_search_field = "Action(s) list//Frame/VStack[0]/Frame[0]/HStack[0]/ZStack[1]/StringField[0]"
    _action_list_search_result = "Action(s) list//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/Label[*].text == '{}'"
    _create_action_btn = "Action(s) list//Frame/**/Button[0].text=='Create selected action(s)'"

    def add_action_btn(self):
        """Clicks on Add action button"""
        self.find_and_click(self._add_action_to_entity_btn, refresh=True)

    def search_action_element(self, element: str):
        """Enter the element name in search field

        Args:
            element (str): element name
        """
        self.find_and_enter_text(self._action_list_search_field, element)

    def search_and_add_action_to_entity(self, entity: str):
        """Searched and action to the entity

        Args:
            entity (str): entity name
        """
        self.add_action_btn()
        self.omni_driver.wait(1)

        self.search_action_element(entity)
        self.omni_driver.wait(1)

        self.find_and_click(self._action_list_search_result.format(entity))
        self.omni_driver.wait(1)

        self.find_and_click(self._create_action_btn)
