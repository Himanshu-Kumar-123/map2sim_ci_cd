# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Section class
   This module contains the base methods for Section Tool Window
"""
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from ..base_models.base_model import BaseModel
from omniui.utils.enums import SectionOption


class BaseSectionModel(BaseModel):
    """Base Section model class for Section Tool

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _all_sections = "Section//Frame/ScrollingFrame[0]/HStack[0]/VStack[0]/HStack[0]/ComboBox[0]"
    _section_dropdown = "Section//Frame/HStack[0]/VStack[0]/HStack[0]/ZStack[0]/VStack[0]/HStack[0]"
    _dropdown_button = _section_dropdown + "/**/Triangle[0]"
    _add_section = "Section//Frame/**/Button[*].name=='add'"
    _save_section = "Section//Frame/**/Button[*].name=='save_dirty'"
    _section_option = "Section//Frame/**/Button[*].name=='option'"

    # Options Tab
    _collapsable_tab = "Section//Frame/**/SimpleCollapsableFrame[*].title == '{}'"
    _section_manipulator = "Section//Frame/**/Label[0].text=='Display Section Manipulator'"
    _section_slice = "Section//Frame/**/Label[0].text=='Display Section Slice'"
    _section_light = "Section//Frame/**/Label[0].text=='Section Light'"
    _cut_direction = "Section//Frame/**//rtx/sectionPlane/cutDirection"

    # Quick move tab
    _align_to = "Section//Frame/**/Button[*].text=='__axis__'"

    # Review tab
    _previous_button = "Section//Frame/**/Button[0].name=='preview'"
    _next_button = "Section//Frame/**/Button[0].name=='next'"

    def enable_section_tool(self):
        if "Section" not in self.omni_driver.get_windows()["visible_windows"]:
            self.omni_driver.select_menu_option("Tools/Section")
            self.log_info_with_screenshot("Opened section tool")
        else:
            self.log_info_with_screenshot("Section tool already visible")

    def _get_checkbox_widget(self, locator: str):
        """Returns Checkbox widget

        Args:
        locator(str): locator of Label
        """
        label = self.omni_driver.find_element(locator)
        checkbox = self.omni_driver.find_element(label.find_parent_element_path() + "/**/CheckBox[0]", True)
        return checkbox

    @property
    def section_slice_enabled(self):
        """Returns whether display is enabled"""
        return self._get_checkbox_widget(self._section_slice).is_checked()

    @property
    def section_manipulator_enabled(self):
        """Returns whether display is enabled"""
        return self._get_checkbox_widget(self._section_manipulator).is_checked()

    @property
    def section_light_enabled(self):
        """Returns whether section light is enabled"""
        return self._get_checkbox_widget(self._section_light).is_checked()

    @property
    def current_section(self):
        """Returns Current Section Name"""
        label = self.omni_driver.find_element(self._section_dropdown + "/**/Label[0]")
        return label.get_text()

    def add_section(self):
        """Adds new section"""
        self.find_and_click(self._add_section)

    def save_section(self):
        """Saves current section"""
        self.find_and_click(self._save_section)

    def select_section_option(self, option: SectionOption):
        """Open Section Options"""
        self.find_and_click(self._section_option)
        self.omni_driver.select_context_menu_option(option.value)

    def enable_section_slice(self):
        """Enables Display Section Option"""
        if self.section_slice_enabled:
            self.log.info("Section slice is already enabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_slice)
            checkbox.click()
        assert self.section_light_enabled is True, "Section slice was not enabled"
        self.screenshot("Enabled section slice")

    def disable_section_slice(self):
        """Disables Display Section Option"""
        if not self.section_slice_enabled:
            self.log.info("Section slice is already disabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_slice)
            checkbox.click()
        assert self.section_slice_enabled is False, "Section slice was not disabled"
        self.screenshot("Disabled section slice")

    def enable_section_light(self):
        """Enables Section Light Option"""
        if self.section_light_enabled:
            self.log.info("Section Light is already enabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_light)
            checkbox.click()
            # TODO: remove the retries after click issue gets resolved (OM-102905)
            retry = 4
            while not self.section_light_enabled:
                if retry == 0:
                    break
                checkbox.click()
                self.omni_driver.wait(1)
                retry -= 1
        assert self.section_light_enabled is True, "Section light was not enabled"
        self.screenshot("Enabled section light")

    def disable_section_light(self):
        """Disables Section Light Option"""
        if not self.section_light_enabled:
            self.log.info("Section Light is already disabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_light)
            checkbox.click()
            # TODO: remove the retries after click issue gets resolved (OM-102905)
            retry = 4
            while self.section_light_enabled:
                if retry == 0:
                    break
                checkbox.click()
                self.omni_driver.wait(1)
                retry -= 1
        assert self.section_light_enabled is False, "Section light was not disabled"
        self.screenshot("Disabled section light")

    def change_cut_direction(self, index: int):
        """Change Section Cut direction

        Args:
        index(int): Index of the ComboBox Option
        """
        options_tab = self.omni_driver.find_element(self._collapsable_tab.format("Options"))
        combo_box = options_tab.find_element("**/ComboBox[0]")
        combo_box.select_item_from_combo_box(index, None, True)
        self.omni_driver.wait(2)
        self.screenshot(f"Changed section cut direction to index {index}")

    def enable_section_manipulator(self):
        """Enables Section Manipulator Option"""
        if self.section_manipulator_enabled:
            self.log.info("Section Manipulator is already enabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_manipulator)
            checkbox.click()
            # TODO: remove the retries after click issue gets resolved (OM-102905)
            retry = 4
            while not self.section_manipulator_enabled:
                if retry == 0:
                    break
                checkbox.click()
                self.omni_driver.wait(1)
                retry -= 1
        assert self.section_manipulator_enabled is True, "Section manipulator was not enabled"
        self.screenshot("Enabled section manipulator")

    def disable_section_manipulator(self):
        """Enables Section Manipulator Option"""
        if not self.section_manipulator_enabled:
            self.log.info("Section Manipulator is already disabled")
        else:
            checkbox = self._get_checkbox_widget(self._section_manipulator)
            checkbox.click()
            # TODO: remove the retries after click issue gets resolved (OM-102905)
            retry = 4
            while self.section_manipulator_enabled:
                if retry == 0:
                    break
                checkbox.click()
                self.omni_driver.wait(1)
                retry -= 1
        assert self.section_manipulator_enabled is False, "Section manipulator was not disabled"
        self.screenshot("Disabled section manipulator")

    def get_sections_count(self):
        """Returns total no of sections

        Returns:
            int: total no of sections
        """
        all_sections = self.omni_driver.find_element(self._all_sections)
        return len(all_sections.get_combobox_info()["all_options"])

    def get_current_section_name(self):
        """Returns current section name

        Returns:
            str: current section name
        """
        all_sections = self.omni_driver.find_element(self._all_sections)
        return all_sections.get_combobox_info()["current_value"]

    def get_current_section_index(self):
        """Returns current section index

        Returns:
            int: returns current section index
        """
        all_sections = self.omni_driver.find_element(self._all_sections)
        return all_sections.get_combobox_info()["current_index"]

    def align_section_to(self, axis: str):
        """Aligns section to X, Y or Z

        Args:
            axis (str): axis e.g. X/Y/Z
        """
        self.find_and_click(self._align_to.replace("__axis__", axis.upper()))
        self.omni_driver.wait(2)

    def next_section(self):
        """Navigates to next section"""
        self.find_and_scroll_element_into_view(
            self._collapsable_tab.format("Review"), ScrollAxis.Y, ScrollAmount.TOP, True
        )
        initial_index = self.get_current_section_index()
        self.find_and_click(self._next_button)
        self.omni_driver.wait(2)
        final_index = self.get_current_section_index()
        self.screenshot(f"next navigation from section {initial_index} to {final_index}")

    def prev_section(self):
        """Navigates to previous section"""
        self.find_and_scroll_element_into_view(
            self._collapsable_tab.format("Review"), ScrollAxis.Y, ScrollAmount.TOP, True
        )
        initial_index = self.get_current_section_index()
        self.find_and_click(self._previous_button)
        self.omni_driver.wait(2)
        final_index = self.get_current_section_index()
        self.screenshot(f"prev navigation from section {initial_index} to {final_index}")

    def select_section(self, index: int):
        """Selects the section of given index

        Args:
            index (int): index of section to be selected
        """
        all_sections = self.omni_driver.find_element(self._all_sections)
        all_sections.select_item_from_combo_box(index, None, True)
        self.omni_driver.wait(2)
        actual_index = all_sections.get_combobox_info()["current_index"]
        assert actual_index == index, f"Expected index {index} doesn't match actual index {actual_index}"
        self.screenshot(f"Changed section cut direction to index {index}")
