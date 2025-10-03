# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Measure class
   This module contains the base methods for Measure Window
"""
from omni_remote_ui_automator.common.enums import MeasureMode, ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.driver.omnielement import OmniElement

from ..base_models.base_model import BaseModel

from omniui.framework_lib.softassert import SoftAssert


class BaseMeasureModel(BaseModel):
    """Base Measure model class for Measure Tool

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _measure_mode = "Measure//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/**/ToolButton[{}]"
    _placement_tab = "Measure//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]"
    _selected_measure_dropdown = "Measure//Frame/ScrollingFrame[0]/VStack[0]/VStack[0]/**/ComboBox[0]"
    _display_tab = "Measure//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]"

    # Display Settings
    _setting_displayXYZ = _display_tab + "/**/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]"
    _setting_units = _display_tab + "/**/Frame[0]/VStack[0]/HStack[1]/ComboBox[0]"
    _setting_precision = _display_tab + "/**/Frame[0]/VStack[0]/HStack[2]/ComboBox[0]"
    _setting_label_size = _display_tab + "/**/Frame[0]/VStack[0]/HStack[3]/ComboBox[0]"
    _setting_line_color = _display_tab + "/**/Frame[0]/VStack[0]/HStack[4]/ColorWidget[0]"

    manage_tab = "Measure//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[2]"

    # Placement Tab
    _vertex_mode = _placement_tab + "/**/Label[0].text=='Vertex'"
    _edge_mode = _placement_tab + "/**/Label[0].text=='Edge'"
    _pivot_mode = _placement_tab + "/**/Label[0].text=='Pivot'"
    _midpoint_mode = _placement_tab + "/**/Label[0].text=='Mid Point'"
    _center_mode = _placement_tab + "/**/Label[0].text=='Center'"
    _snap_to_option = _placement_tab + "/**/Label[0].text=='Snap To'"
    _constrain_to_option = _placement_tab + "/**/Label[0].text=='Constrain To'"
    _surface_mode = _placement_tab + "/**/Label[0].text=='Surface'"

    # Manage Tab
    _manage_tab_treeview = manage_tab + "/**/TreeView[0]"
    _list_item_name = _manage_tab_treeview + "/**/Label[*].text == '{}'"
    list_item_delete = _manage_tab_treeview + "/HStack[{}]/ZStack[0]"
    measure_list = _manage_tab_treeview + "/**/ZStack[0]"
    measure_value = _manage_tab_treeview + "/Label[{}]"
    _list_item_dropdown = _manage_tab_treeview + "HStack[{}]/VStack[0]/Triangle[0]"

    _property_name = "Property//Frame/**/StringField[0].name=='prims_name'"

    def _get_checkbox_widget(self, locator: str):
        """Returns Checkbox widget

        Args:
        locator(str): locator of Label
        """
        label = self.omni_driver.find_element(locator, True)
        checkbox = self.omni_driver.find_element(label.find_parent_element_path() + "/RadioButton[0]", True)
        return checkbox

    def _click_snap_mode(self, element: OmniElement):
        """Clicks on the snap selection box"""
        element.click()

    @property
    def constrain_to_combobox(self):
        """Return Constrain to ComboBox"""
        locator = self.omni_driver.find_element(self._constrain_to_option).find_parent_element_path()
        return self.omni_driver.find_element(locator + "/ComboBox[*]")

    @property
    def is_constrain_to_enabled(self):
        """Returns whether constrain_to option is enabled"""
        return self.constrain_to_combobox.is_enabled()

    @property
    def measure_list_len(self):
        """Returns Measurement list length"""
        try:
            return len(self.omni_driver.find_elements(self.measure_list))
        except ElementNotFound:
            return 0

    @property
    def is_surface_checked(self):
        """Returns whether surface option is checked"""
        checkbox = self._get_checkbox_widget(self._surface_mode)
        return checkbox.is_checked()

    @property
    def is_vertex_checked(self):
        """Returns whether vertex option is checked"""
        checkbox = self._get_checkbox_widget(self._vertex_mode)
        return checkbox.is_checked()

    @property
    def is_edge_checked(self):
        """Returns whether edge option is checked"""
        checkbox = self._get_checkbox_widget(self._edge_mode)
        return checkbox.is_checked()

    @property
    def is_midpoint_checked(self):
        """Returns whether midpoint option is checked"""
        checkbox = self._get_checkbox_widget(self._midpoint_mode)
        return checkbox.is_checked()

    @property
    def is_pivot_checked(self):
        """Returns whether pivot option is checked"""
        checkbox = self._get_checkbox_widget(self._pivot_mode)
        return checkbox.is_checked()

    @property
    def is_center_checked(self):
        """Returns whether center option is checked"""
        checkbox = self._get_checkbox_widget(self._center_mode)
        return checkbox.is_checked()

    @property
    def is_vertex_enabled(self):
        """Returns whether vertex option is enabled"""
        checkbox = self._get_checkbox_widget(self._vertex_mode)
        return checkbox.is_enabled()

    @property
    def is_edge_enabled(self):
        """Returns whether edge option is enabled"""
        checkbox = self._get_checkbox_widget(self._edge_mode)
        return checkbox.is_enabled()

    @property
    def is_midpoint_enabled(self):
        """Returns whether midpoint option is enabled"""
        checkbox = self._get_checkbox_widget(self._midpoint_mode)
        return checkbox.is_enabled()

    @property
    def is_pivot_enabled(self):
        """Returns whether pivot option is enabled"""
        checkbox = self._get_checkbox_widget(self._pivot_mode)
        return checkbox.is_enabled()

    @property
    def is_center_enabled(self):
        """Returns whether center option is enabled"""
        checkbox = self._get_checkbox_widget(self._center_mode)
        return checkbox.is_enabled()

    @property
    def is_selected_measure_enabled(self):
        """Returns whether selected measure is enabled"""
        return self.omni_driver.find_element(self._measure_mode.format(MeasureMode.SELECTED_MEASURE.value)).is_enabled()

    @property
    def is_selected_measure_dropdown_enabled(self):
        """Returns whether selected measure dropdown is enabled"""
        return self.omni_driver.find_element(self._selected_measure_dropdown).is_enabled()

    def enable_measure_mode(self, mode: MeasureMode):
        """Enables the given measure mode

        Args:
        mode(MeasureMode): Enum for measure mode
        """
        self.log.info("[MeasureModel] Enabling %s mode", mode.name)
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(mode.value))
        if measure_tool.tool_button_is_checked():
            return
        coords = measure_tool.get_widget_center()
        self.omni_driver.emulate_mouse_move(coords[0], coords[1])
        self.omni_driver.wait(1)
        measure_tool.click()
        tool_option = self.omni_driver.find_element(self._placement_tab)
        self.wait.visibility_of_element(tool_option)

    def disable_measure_mode(self, mode: MeasureMode):
        """Disables the given measure mode

        Args:
        mode(MeasureMode): Enum for measure mode
        """
        self.log.info("[MeasureModel] Disabling %s mode", mode.name)
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(mode.value))
        if not measure_tool.tool_button_is_checked():
            return
        center = measure_tool.get_widget_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        self.omni_driver.wait(1)
        measure_tool.click()
        tool_option = self.omni_driver.find_element(self._placement_tab)
        self.wait.invisibility_of_element(tool_option)

    def verify_ui_layout_initial_state(self):
        """
        Verifies UI layout Initial State

        Verifies:
        1. Initial state of toolbar window
        2. Check visibility of Placement Tab
        3. Check collapsable frame functionality
        """
        assertion = SoftAssert()
        for mode in MeasureMode:
            measure_tool = self.omni_driver.find_element(self._measure_mode.format(mode.value))
            assertion.expect(
                not measure_tool.tool_button_is_checked(),
                f"Measure Mode: {mode.name} is checked by default",
            )
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(MeasureMode.SELECTED_MEASURE.value))
        assertion.expect(
            not measure_tool.is_enabled(),
            f"Measure Mode: {MeasureMode.SELECTED_MEASURE.name} is enabled by default",
        )
        placement_tab = self.omni_driver.find_element(self._placement_tab)
        assertion.expect(not placement_tab.is_visible(), "Placement tab is visible by default")
        display_tab = self.omni_driver.find_element(self._display_tab)
        assertion.expect(display_tab.is_visible(), "Display tab is not enabled by default")
        manage_tab = self.omni_driver.find_element(self.manage_tab)
        assertion.expect(manage_tab.is_visible(), "Manage tab is not enabled by default")
        self.enable_measure_mode(MeasureMode.POINT_TO_POINT)
        assertion.expect(not placement_tab.is_collapsed(), "Placement Tab is collapsed")
        assertion.expect(not display_tab.is_collapsed(), "Display Tab is collapsed")
        assertion.expect(not manage_tab.is_collapsed(), "Manage Tab is collapsed")
        placement_tab.find_element('**/Label[0].text=="Placement"').click()
        display_tab.find_element('**/Label[0].text=="Display"').click()
        manage_tab.find_element('**/Label[0].text=="Manage"').click()
        assertion.expect(placement_tab.is_collapsed(), "Placement Tab is not collapsed")
        assertion.expect(display_tab.is_collapsed(), "Display Tab is not collapsed")
        assertion.expect(manage_tab.is_collapsed(), "Manage Tab is not collapsed")
        assertion.assert_all()

    def change_xyz_display(self, index: int):
        """Changes the XYZ display setting in display tab

        Args:
        index(int): Option index
        """
        self.omni_driver.find_element(self._setting_displayXYZ).select_item_from_combo_box(index, None, False)

    def change_units(self, index: int):
        """Changes the unit setting in display tab

        Args:
        index(int): Option index
        """
        self.omni_driver.find_element(self._setting_units).select_item_from_combo_box(index, None, False)

    def change_precision(self, index: int):
        """Changes the  precision setting in display tab

        Args:
        index(int): Option index
        """
        self.omni_driver.find_element(self._setting_precision).select_item_from_combo_box(index, None, False)

    def change_label_size(self, index: int):
        """Changes the label size setting in display tab

        Args:
        index(int): Option index
        """
        self.omni_driver.find_element(self._setting_label_size).select_item_from_combo_box(index, None, False)

    @property
    def is_xyz_display_enabled(self):
        """Returns whether XYZ display is enabled"""
        return self.omni_driver.find_element(self._setting_displayXYZ).is_enabled()

    @property
    def is_display_tab_enabled(self):
        """Return whether display tab settings are enabled"""
        setting = [
            self.omni_driver.find_element(self._setting_displayXYZ).is_enabled(),
            self.omni_driver.find_element(self._setting_line_color).is_enabled(),
            self.omni_driver.find_element(self._setting_precision).is_enabled(),
            self.omni_driver.find_element(self._setting_label_size).is_enabled(),
            self.omni_driver.find_element(self._setting_units).is_enabled(),
        ]
        self.log.info("Display Tab options enabled: %s", setting)
        return all(setting)

    def enable_vertex_mode(self):
        """Enables vertex option for current measure mode"""
        if self.is_vertex_checked:
            self.log.info("Vertex Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._vertex_mode)
        self._click_snap_mode(checkbox)

    def disable_vertex_mode(self):
        """Disables vertex option for current measure mode"""
        if not self.is_vertex_checked:
            self.log.info("Vertex Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._vertex_mode)
        self._click_snap_mode(checkbox)

    def enable_edge_mode(self):
        """Enables edge option for current measure mode"""
        if self.is_edge_checked:
            self.log.info("Edge Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._edge_mode)
        self._click_snap_mode(checkbox)

    def disable_edge_mode(self):
        """Disables edge option for current measure mode"""
        if not self.is_edge_checked:
            self.log.info("Edge Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._edge_mode)
        self._click_snap_mode(checkbox)

    def enable_midpoint_mode(self):
        """Enables midpoint option for current measure mode"""
        if self.is_midpoint_checked:
            self.log.info("Mid Point Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._midpoint_mode)
        self._click_snap_mode(checkbox)

    def disable_midpoint_mode(self):
        """Disables midpoint option for current measure mode"""
        if not self.is_midpoint_checked:
            self.log.info("Midpoint Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._midpoint_mode)
        self._click_snap_mode(checkbox)

    def enable_pivot_mode(self):
        """Enables pivot option for current measure mode"""
        if self.is_pivot_checked:
            self.log.info("Pivot Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._pivot_mode)
        self._click_snap_mode(checkbox)

    def disable_pivot_mode(self):
        """Disables pivot option for current measure mode"""
        if not self.is_pivot_checked:
            self.log.info("Pivot Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._pivot_mode)
        self._click_snap_mode(checkbox)

    def enable_center_mode(self):
        """Enables center option for current measure mode"""
        if self.is_center_checked:
            self.log.info("Center Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._center_mode)
        self._click_snap_mode(checkbox)

    def disable_center_mode(self):
        """Disables center option for current measure mode"""
        if not self.is_center_checked:
            self.log.info("Center Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._center_mode)
        self._click_snap_mode(checkbox)

    def delete_measurement(self, index: int):
        """Deletes the measurement from the list

        Args:
        index(int): Index of measure to be deleted starting at 1
        """
        self.omni_driver.find_element(self.manage_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.omni_driver.find_element(
            self.list_item_delete.format(3 * (index - 1) + 2)  # HStack calculation with 3 HStack for  each list item
        ).click()

    def add_measure(self, *coordinates: tuple, double_click=False):
        """Makes a measurement at given coordinates

        Args:
        coordinates(list): List of coordinates to plot, format: [(x1,y1), (x2,y2)...]
        """
        x, y = 0, 0
        for coord in coordinates:
            x, y = coord
            self.omni_driver.emulate_mouse_move(x, y)
            self.omni_driver.wait(1)
            self.omni_driver.click_at(x, y)
            self.omni_driver.wait(1)
        self.omni_driver.click_at(x, y, True, True)
        if double_click:
            # Multipoint and Area requires more right click
            self.omni_driver.wait(1)
            self.omni_driver.click_at(x, y, True, True)

    def change_snap_to_setting(self, option: int):
        """Changes Snap To to given option

        Args:
        option(int): option name
        """
        self.omni_driver.find_element(
            self.omni_driver.find_element(self._snap_to_option).find_parent_element_path() + "/ComboBox[0]"
        ).select_item_from_combo_box(option, None, False)

    @property
    def is_placement_options_enabled(self):
        """Returns whether placement options (vertex, edge, etc) are disabled"""
        enabled = all(
            [
                self.is_vertex_enabled,
                self.is_edge_enabled,
                self.is_midpoint_enabled,
                self.is_center_enabled,
                self.is_pivot_enabled,
            ]
        )
        self.log.info("Placement options enabled %s", enabled)
        return enabled

    def get_measure_value(self, index: int):
        """Returns measure value

        Args:
        index(int): Index of the list item starting from 0
        """
        measure = self.wait.element_to_be_located(self.omni_driver, self.measure_value.format(5 + index))
        return measure.get_text()

    def toggle_list_item_dropdown(self, index: int):
        """Toggles the list item dropdown

        Args:
        index(int): Index of list item starting from 0
        """
        self.find_and_click(self._list_item_dropdown.format(3 * index))

    def switch_selected_measure_type(self, option_index: int):
        """Switch the option in the measure dropdown

        Args:
        option_index(int): Name of the option
        """
        combobox = self.omni_driver.find_element(self._selected_measure_dropdown)
        combobox.select_item_from_combo_box(index=option_index, name=None, stack_combo=False)

    def add_selected_measure(self):
        """Clicks on measure button"""
        self.find_and_click(self._measure_mode.format(MeasureMode.SELECTED_MEASURE.value))

    def is_measure_mode_enabled(self, mode: MeasureMode):
        """Returns whether given measure mode is enabled

        Args:
        mode(MeasureMode): Type of Measure mode
        """
        measure_tool = self.omni_driver.find_element(self._measure_mode.format(mode.value))
        return measure_tool.tool_button_is_checked()

    def enable_surface_mode(self):
        """Enables surface option for current measure mode"""
        if self.is_surface_checked:
            self.log.info("surface Mode already enabled")
            return
        self.omni_driver.find_element(self._placement_tab, True).scroll_into_view(
            ScrollAxis.Y.value, ScrollAmount.CENTER.value
        )
        checkbox: OmniElement = self._get_checkbox_widget(self._surface_mode)
        checkbox.click()
        self.omni_driver.wait(2)
        assert self.is_surface_checked, "Failed to enable Surface mode"

    def disable_surface_mode(self):
        """Disables surface option for current measure mode"""
        if not self.is_surface_checked:
            self.log.info("surface Mode already disabled")
            return
        self.omni_driver.find_element(self._placement_tab).scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        checkbox = self._get_checkbox_widget(self._surface_mode)
        self._click_snap_mode(checkbox)

    def get_measurement_name(self):
        """
        Returns name of measurement selected from property window
        """
        return self.omni_driver.find_element(self._property_name).get_text()
