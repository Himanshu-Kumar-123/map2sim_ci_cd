# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Scene Optimizer model class
   This module contains the base methods for Scene Optimizer Model for actions to perform
"""
import os

from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.waits import Wait
from ..base_models.base_model import BaseModel


class BaseSceneOptimizerModel(BaseModel):
    """BaseSceneOptimizer class containing common methods"""

    _scene_optimizer_window = "Scene Optimizer"
    # Widget Locators
    _operations_tab = "Scene Optimizer//Frame/**/Label[*].text == 'Operations'"
    _report_tab = "Scene Optimizer//Frame/**/Label[*].text == 'Report {}'"
    _load_preset_btn = "Scene Optimizer//Frame/**/Label[*].text == 'Load Preset'"
    _save_preset_btn = "Scene Optimizer//Frame/**/Label[*].text == 'Save Preset'"
    _execute_all_btn = "Scene Optimizer//Frame/**/Label[*].text == 'Execute All'"
    _clear_all_processes_btn = "Scene Optimizer//Frame/**/Label[*].text == 'Clear All Processes'"
    _add_scene_optimizer_process_btn = "Scene Optimizer//Frame/**/Label[*].text == 'Add Scene Optimizer Process'"
    _merge_static_meshes = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Merge Static Meshes'"
    _compute_pivot = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Compute Pivot'"
    _optimize_skeleton_roots = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Optimize Skeleton Roots'"
    _find_coinciding_meshes = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Find Coinciding Meshes'"
    _de_duplicate_geometry = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'De-duplicate Geometry'"
    _process_point_clouds = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Process Point Clouds'"
    _compute_extents = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Compute Extents'"
    _optimize_materials = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Optimize Materials'"
    _prune_leaf_xforms = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Prune Leaf Xforms'"
    _split_meshes = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Split Meshes'"
    _generate_projection_uvs = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Generate Projection UVs'"
    _python_script = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Python Script'"
    _configure = "Scene Optimizer//Frame/**/CollapsableFrame[*].title == 'Configure'"
    _close_section = "Scene Optimizer//Frame/ScrollingFrame[0]/Frame[0]/VStack[0]/ZStack[1]/Frame[0]/VStack[0]/ScrollingFrame[0]/VStack[0]/ZStack[0]/ZStack[0]/HStack[0]/VStack[1]/Button[0]"
    _sections = "Scene Optimizer//Frame/ScrollingFrame[0]/Frame[0]/VStack[0]/ZStack[1]/Frame[0]/VStack[0]/ScrollingFrame[0]/VStack[0]/ZStack[*]"
    _execute_process_btn = "Scene Optimizer//Frame/**/Button[0].text == '{}'"
    _process_section = _sections + "/ZStack[0]/CollapsableFrame[0].title == '{}'"
    _triangle = "**/Triangle[0].alignment == '{}'"

    _add_btn = "/**/PrimPathsArgumentWidget[0]/HStack[0]/ZStack[0]/Button[0]"
    _add_textfield = "/**/PrimPathsArgumentWidget[0]/HStack[0]/TextField[0]/StringField[0]"
    _add_edit_btn = "/**/PrimPathsArgumentWidget[0]/HStack[0]/Button[0]"
    _checkbox_label = "**/BoolArgumentWidget[*]/Label[0].text == '{}'"
    _checkbox = "/HStack[0]/CheckBox[0]"
    _combobox_label = "**/EnumArgumentWidget[*]/Label[0].text == '{}'"
    _combobox = "/HStack[0]/ComboBox[0]"

    # Merge Static Meshes
    _output_name = "**/PrimPathArgumentWidget[0]/HStack[0]/TextField[0]/StringField[0]"
    _execute_merge_static_meshes = "**/Button[*].text == 'Execute - Merge Static Meshes'"

    # De-duplicate Geometry
    _tolerance = "**/PrimPathArgumentWidget[0]/HStack[0]/TextField[0]/StringField[0]"
    _execute_deduplicate_geometry = "**/Button[*].text == 'Execute - De-duplicate Geometry'"

    # Generate Projection UVs
    _scale_factor = "**/PrimPathArgumentWidget[0]/HStack[0]/TextField[0]/StringField[0]"

    # Python Script
    _python_code = "/**/CodeArgumentWidget[0]/HStack[0]/StringField[0]"

    # Confirm Clear
    _ok_btn = "Confirm Clear//Frame/**/Button[*].text == 'Ok'"
    _cancel_btn = "Confirm Clear//Frame/**/Button[*].text == 'Cancel'"

    def select_configure(self):
        """
        Selects the Configure option form the Add Scene Optimizer Process menulist
        """
        self.find_and_click(self._add_scene_optimizer_process_btn)
        self.omni_driver.select_context_menu_option("Configure")
        configure_section: OmniElement = self.omni_driver.find_element(self._configure)
        self.wait.visibility_of_element(configure_section)
        return configure_section

    def load_preset(self, preset_name: str):
        """
        Loads the existing presets in Scene Optimizer
        Args:
            preset_name: Preset that to be loaded
        """
        self.find_and_click(self._load_preset_btn)
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(preset_name)
        self.omni_driver.wait(2)

    def navigate_to_scene_optimizer(self):
        """Opens Scene Optimizer window"""
        self.omni_driver.select_menu_option("Window/Utilities/Scene Optimizer")
        self.omni_driver.wait(2)
        visible_windows = self.omni_driver.get_windows()["visible_windows"]
        self.log.info(f"Visible windows: {visible_windows}")
        return self._scene_optimizer_window in visible_windows

    def clear_all_processes(self):
        """Clears all the scene optimizer processes"""
        self.find_and_click(self._clear_all_processes_btn)
        self.omni_driver.wait(2)
        self.find_and_click(self._ok_btn)
        self.omni_driver.wait(2)
        self.screenshot("clear_all_processes")
        self.wait.element_to_be_invisible(self.omni_driver, self._close_section)

    def execute_all_processes(self, report_number=1, timeout=120):
        """Executes all the selected optimization processes"""
        self.find_and_click(self._execute_all_btn)
        self.log.info("Execute All Processes button is clicked.")
        self.omni_driver.wait(2)
        wait = Wait(timeout)
        wait.element_to_be_located(self.omni_driver, self._report_tab.format(report_number))
        self.screenshot("report_generated")

    def verify_listed_processes(self, processes, position: bool = False, index: int = 0):
        """Verifies the list of processes loaded in Scene Optimizer"""
        all_processes = self.omni_driver.find_elements(self._sections)
        try:
            if position:
                process_ele = all_processes[index].find_element(
                    f"ZStack[0]/CollapsableFrame[0].title == '{processes}'")
                self.log.info(f"Found {process_ele} process element at {index} index position")
                self.screenshot("listed_process_in_so")
                return True
            process_names = processes.split(',')
            for i in range(len(all_processes)):
                self.log.info(f"Searching {process_names[i].strip()}")
                process_ele = all_processes[i].find_element(f"ZStack[0]/CollapsableFrame[0].title == '{process_names[i].strip()}'")
                self.log.info(f"Found {process_ele} process element")
            self.screenshot("listed_process_in_so")
            return True
        except ElementNotFound:
            return False

    def add_scene_optimizer_process(self, process_name):
        """
        Loads the Scene Optimizer Process from the list
        Args:
            process_name: Scene Optimizer process name
        """
        self.find_and_click(self._add_scene_optimizer_process_btn)
        self.omni_driver.select_context_menu_option(process_name)
        self.omni_driver.wait(2)

    def enter_python_code(self, python_code):
        """
        Enter the python code
        Args:
            python_code: python script that needs to be run
        """
        key = "ZStack[0]/CollapsableFrame[0].title == 'Python Script'"
        self.omni_driver.wait(3)
        item, index = self.get_child_element(self._sections, key)
        _process_section = self._sections.replace("ZStack[*]", f"ZStack[{index}]")
        python_code_edit = _process_section + self._python_code
        self.find_and_enter_text(python_code_edit, python_code)

    def click_add_btn(self, process_name):
        """
        Clicks on the Add button to add the selected xform/prim
        Args:
            process_name: Scene Optimizer process name in which add button is clicked
        """
        key = f"ZStack[0]/CollapsableFrame[0].title == '{process_name}'"
        item, index = self.get_child_element(self._sections, key)
        _process_section = self._sections.replace("ZStack[*]", f"ZStack[{index}]")
        add_btn = _process_section + self._add_btn
        self.find_and_click(add_btn)

    def fetch_report_data(self, data, operation, prim_type=None, column=None, category=None):
        prim_type_value = []

        # Count dictionaries with same operation name
        operation_count = sum(1 for report in data for entry in report if entry.get("Operation") == operation)

        # Iterate through the reports to find the count
        for entry in data[0]:
            if entry.get("Operation") == operation and entry.get("Entries"):
                if category:
                    prim_type_value = [item["Message"] for item in entry["Entries"] if item["Category"] == category]
                    break
                elif prim_type:
                    prim_type_entry = next((e for e in entry["Entries"] if e.get("Prim Type") == prim_type), None)
                    if prim_type_entry:
                        prim_type_value.append(prim_type_entry.get(column, 0))
                        if len(prim_type_value) == operation_count:
                            break
        return prim_type_value

    def get_selected_meshes(self, process_name):
        key = f"ZStack[0]/CollapsableFrame[0].title == '{process_name}'"
        item, index = self.get_child_element(self._sections, key)
        _process_section = self._sections.replace("ZStack[*]", f"ZStack[{index}]")
        selected_mesh= _process_section + self._add_textfield
        return self.omni_driver.find_element(selected_mesh, refresh=True).get_text()

    def toggle_check_box(self, process_name: str, checkbox_name: str, check_on: bool = True):
        """
        toggles the given checkbox in given process name
        """
        section_element = self.omni_driver.find_element(self._process_section.format(process_name),
                                                        refresh=True)
        label_element = section_element.find_element(self._checkbox_label.format(checkbox_name),
                                                     refresh=True)
        checkbox_locator = f"{label_element.find_parent_element_path()}{self._checkbox}"
        self.toggle_checkbox(checkbox_locator, check_on)

    def select_from_combobox(self, process_name: str, combobox_name: str, option: str):
        """
        Selects the options from the combobox for any given process
        """
        section_element = self.omni_driver.find_element(self._process_section.format(process_name),
                                                        refresh=True)
        label_element = section_element.find_element(self._combobox_label.format(combobox_name), refresh=True)
        combobox_locator = f"{label_element.find_parent_element_path()}{self._combobox}"
        self.select_item_from_stack_combo_box(combobox_locator, name=option)
