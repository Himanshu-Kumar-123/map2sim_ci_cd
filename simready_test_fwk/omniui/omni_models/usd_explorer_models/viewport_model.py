# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Viewport Model class
   This module contains the base methods for Omnidriver
"""
from omni_remote_ui_automator.common.constants import RenderEngine
from omni_remote_ui_automator.driver.omnielement import OmniElement

from ..base_models.base_viewport_model import BaseViewportModel


class ViewportModel(BaseViewportModel):
    """Viewport model class for Viewport window

    Args:
        ViewportModel (BaseViewportModel): Viewport class parent to BaseViewportModel
    """

    # Menu Container Widget Path
    _viewport_menu = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[0]"
    _render_realtime = _viewport_menu + "/MenuItemCollection[0]/MenuItem[0]"
    _render_path_trace = _viewport_menu + "/MenuItemCollection[0]/MenuItem[1]"
    _view_menu = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[0]"
    _view_menu_waypoint = "Viewport//Frame/**/Menu[0]/Menu[0]/CategoryMenuCollection[1]/SelectableMenuItem[3]"
    _view_menu_markup = "Viewport//Frame/**/Menu[0]/Menu[0]/CategoryMenuCollection[1]/SelectableMenuItem[4]"
    _camera_menu = "Viewport//Frame/ZStack[0]/**/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]"
    _camera_follow_user = _camera_menu + "/MenuItemCollection[1]"
    _focus_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/**/Menu[0]/MenuItem[1]"
    _navbar_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[0]"
    _show_by_type_menu = "Viewport//Frame/**/Menu[0]/Menu[0]/CategoryMenuCollection[1]"
    _lights_view_menu = "Viewport//Frame/**/Menu[0]/Menu[0]/CategoryMenuCollection[1]/SelectableMenuItem[1]"

    _light_menu = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[2]"
    light_lights_off = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[2]/MenuItemCollection[0]/SelectableMenuItem[0]"
    light_camera_light = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[2]/MenuItemCollection[0]/SelectableMenuItem[1]"
    light_stage_light = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[2]/MenuItemCollection[0]/SelectableMenuItem[2]"
    _light_items = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[2]/MenuItemCollection[0]/SelectableMenuItem[__index__]"

    _navbar_widget = (
        "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[4]/Frame[1]/ZStack[0]/Frame[0]/ZStack[0]/Placer[1]/ZStack[0]"
    )

    def fetch_engine(self, engine: str) -> OmniElement:
        """Returns the engine menu option

        Args:
        engine(str): Engine Name
        """
        option = None
        if engine == RenderEngine.rtx_real_time:
            option = self.omni_driver.find_element(self._render_realtime)
        elif engine == RenderEngine.rtx_interative:
            option = self.omni_driver.find_element(self._render_path_trace)
        else:
            self.log.info("Engine not found")
            raise ValueError(f"{engine} not found in the menu")
        return option

    def select_rendering_engine(self, engine: str):
        """Selects the specified rendering engine

        Args:
            engine (str): Render engine name
        """
        render_dropdown = self.omni_driver.find_element(self._viewport_menu)
        render_dropdown.click()
        engine = self.fetch_engine(engine)
        engine.click(False)
        self.omni_driver.wait(2)
        render_dropdown.click(False)

    def is_renderer_checked(self, engine: str):
        """Returns whether the given renderer is checked in dropdown

        Args:
        engine(str): Engine name
        """
        return self.fetch_engine(engine).tool_button_is_checked()

    def view_menu_toggle_waypoint(self):
        """Toggles Waypoint option in view menu"""
        self._select_view_menu()
        self._select_show_by_type_menu()
        skeleton_view_menu = self.omni_driver.find_element(self._view_menu_waypoint)
        skeleton_view_menu.click(False)

    def get_navbar_position(self):
        """Gets the position info of Navbar widget
        Retuns:
            dict
        """
        elm: OmniElement = self.omni_driver.find_element(self._navbar_widget, True)
        return elm.get_size_and_position("all")

    def is_navbar_visible(self) -> bool:
        """Gets the visibility of the Navbar
        Retuns:
            bool
        """
        try:
            elm: OmniElement = self.omni_driver.find_element(self._navbar_widget, True)
            return elm.is_visible()
        except:
            return False

    def get_viewport_position(self):
        """Gets the position info of Viewport widget
        Retuns:
            dict
        """
        elm: OmniElement = self.omni_driver.find_element(self._viewport_element, True)
        return elm.get_size_and_position("all")

    @property
    def waypoint_icons_enabled(self):
        """Tells whether Waypoint icons are displayed in viewport."""
        elm: OmniElement = self.omni_driver.find_element(self._view_menu_waypoint, True)
        return elm.get_value() == "True"

    @property
    def markup_icons_enabled(self):
        """Tells whether Markup icons are displayed in viewport."""
        elm: OmniElement = self.omni_driver.find_element(self._view_menu_markup, True)
        return elm.get_value() == "True"

    def select_light_by_index(self, index: int = 0):
        """Selectes a light setting from the Lights menu.
        Args:
            index (int): index of light to be selected. Starts from 0
        """
        self.find_and_click(self._light_menu, bring_to_front=False, refresh=True)
        self.find_and_click(
            self._light_items.replace("__index__", str(index)),
            bring_to_front=False,
            refresh=True,
        )

    def select_lights(self, num):
        """Selected light based on its numerical position in dropdown

        Args:
            num (int): position of light in dropdown
        """
        self.find_and_click(self._light_menu, bring_to_front=False, refresh=True)
        light_item = self.find_and_click(
            self._light_items.replace("__index__", str(num)), bring_to_front=False, refresh=True
        )
        self.log.info(f"Lighting mode {light_item.get_name()} is selected")
        self.omni_driver.wait(1)
        self.find_and_click(self._light_menu, bring_to_front=False, refresh=True)
        return light_item.get_name()

    def open_lights_menu(self):
        """Opens the lights menu on top right of viewport."""
        self.find_and_click(self._light_menu)