# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Sequencer class
   This module contains the base methods for Sequencer window
"""


from omni_remote_ui_automator.common.enums import DockPosition
from ..base_models.base_model import BaseModel


class BaseSequencerModel(BaseModel):
    """Base model class for Sequencer window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Sequencer window
    _add_btn = "Sequencer//Frame/**/sequencer_view_content_stack/sequencer_view_tracks_list_frame/**/Button[0]"
    _asset_track = (
        "Sequencer//Frame/**/**/sequencer_tracks_view_frame/sequencer_tracks_view_z_frame/**/track_widget_Asset"
    )
    _window = "Sequencer"
    _sequencer_window = "Sequencer//Frame/**/VStack[0]"

    
    def dock(self, win_name: str, dock_position: DockPosition):
        """Docks sequencer window to specified window

        Args:
            win_name (str): Target window
            dock_position (DockPosition): Docking position
        """
        self.dock_window("Sequencer", win_name, dock_position)

    
    def add_asset_track(self):
        """Add an asset track in Sequencer"""
        self.find_and_click(self._add_btn)
        self.omni_driver.select_context_menu_option("Create Asset Track")
        assert self.wait.element_to_be_located(self.omni_driver, self._asset_track), "Asset track timeline not created"

    
    def get_asset_timeline_center(self):
        """Get the center of timeline for asset track

        Returns:
            float: Returns the computed_width, computed_height, screen_position_x, screen_position_y
        """
        timeline_rectangle = self.omni_driver.find_element(self._asset_track, refresh=True)
        return (
            timeline_rectangle.get_size_and_position("screen_position_x") + 10,
            timeline_rectangle.get_size_and_position("screen_position_y") + 10,
        )

    def enable(self):
        """Enables the sequencer window"""
        self.omni_driver.select_menu_option("Window/Animation/Sequencer")
        assert self.wait.element_to_be_located(self.omni_driver, self._window), "Sequencer window not visible"

    def navigate(self):
        """Navigates to sequencer window"""
        window = self.omni_driver.find_element(self._sequencer_window)
        window.click()
        self.screenshot("navigated_to_sequencer_window")
