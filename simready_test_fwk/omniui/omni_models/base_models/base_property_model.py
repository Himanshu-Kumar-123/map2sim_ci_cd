# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Property class
   This module contains the base methods for Property window
"""

from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.common.constants import KeyboardConstants


class BasePropertyModel(BaseModel):
    """Base model class for Property window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to property window
    _content_grid_item = "Content//Frame/**/content_browser_treeview_grid_view/**/Label[0].text=='__filename__'"
    _prim_path = "Property//Frame/**/StringField[*].name=='prims_path'"
    _prim_name = "Property//Frame/**/StringField[*].name=='prims_name'"
    _instanceable_chkbox = "Property//Frame/**/HStack[2]/VStack[0]/CheckBox[0]"
    _property_window = "Property//Frame/VStack[0]"
    _all_color_sliders = "Property//Frame/**/drag_per_channel_inputs:color"
    _red_slider = "HStack[0]/**/FloatSlider[0]"
    _green_slider = "HStack[1]/**/FloatSlider[0]"
    _blue_slider = "HStack[2]/**/FloatSlider[0]"
    _applied_material_property_text = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/HStack[0]/VStack[0]/HStack[1]/combo_drop_target"
    _albedo_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Albedo'"
    _normal_map_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Normal'"
    _tagging_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Tagging'"
    _sublayer_name = "Property//Frame/**/CollapsableFrame[0]/**/StringField[0]"
    _world_axis = (
        "Property//Frame/VStack[0]/**/CollapsableFrame[1]/**/HStack[0]/ComboBox[0]"
    )
    _layer_path_widget = "Property//Frame/**/CollapsableFrame[*].title=='Layer Path'"
    _reference_widget = "Property//Frame/**/CollapsableFrame[*].title=='References'"
    _all_references_prim_paths = "**/payref_prim_path"
    _layer_metadata = "Property//Frame/**/CollapsableFrame[*].title=='Layer Metadata'"
    _checkpoint_combobox = "Checkpoint Widget Window//Frame"
    _material_collapse_bar = (
        "Property//Frame/**/ScrollingFrame[0]**/CollapsableFrame[1]"
    )
    _start_time_code_field = (
        "Property//Frame/**/CollapsableFrame[1]/**/HStack[1]/StringField[0]"
    )
    _end_time_code_field = (
        "Property//Frame/**/CollapsableFrame[1]/**/HStack[2]/StringField[0]"
    )
    _offset_btn = "Property//Frame/**/offset_mode_toggle"

    _translate_multimodal = (
        "Property//Frame/**/MultiFloatDragField[0].name=='multivalue'"
    )
    _python_scripting_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='Python Scripting'"
    )
    _remove_python_scripting_btn = "Property//Frame/**/RemovePythonScriptingButton"
    _remove_python_scripting_dialog = "Remove Python Scripting?"
    _confirm_remove_python_scripting_btn = (
        "Remove Python Scripting?//Frame/**/Button[*].text=='Yes'"
    )
    _raw_usd_properties_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='Raw USD Properties'"
    )
    _select_asset_directory_path = "Select Asset...//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _select_asset_button = "Select Asset...//Frame/**/Button[*].text=='Select'"
    _select_asset_grid_item = (
        "Select Asset...//Frame/**/None_grid_view/**/Label[0].text=='__filename__'"
    )
    _warning_window = "Warning"
    _warning_window_yes_btn = "Warning//Frame/**/Button[*].text=='Yes'"
    _warning_window_no_btn = "Warning//Frame/**/Button[*].text=='No'"

    # camera properties
    _camera_collapsable = "Property//Frame/**/CollapsableFrame[*].title=='Camera'"
    # should be used as child for Camera Collapsable
    _clipping_collapsable = "**/CollapsableFrame[*].title=='Clipping'"
    # should be used as child for Clipping Collapsable
    _clipping_range_y = (
        "**/drag_per_channel_clippingRange/HStack[1]/ZStack[1]/FloatDrag[0]"
    )

    # should be used as child for Python Scripting collapsable frame
    _python_scripting_add_asset_btn = (
        f"""**/Button[*].text=="__menu_context_glyph__ Add Asset..." """
    )
    _python_scripting_added_scripts = "**/StringField[*]"
    _script_reorder_grab = """**/HStack[*].identifier=="sdf_asset_array_omni:scripting:scripts[__script_index__].reorder_grab" """

    # should be used as child for Tagging collapsable frame
    _create_new_tag_collapsable = "**/CollapsableFrame[*].title=='Create New Tag'"
    _new_tag_field = "**/StringField[*].name=='new_tag:'"
    _add_tag_btn = "**/Button[*].text=='Add'"
    _namespace_collapsable = "**/CollapsableFrame[*].title=='Tags for __namespace__'"
    _new_tag_field_under_namespace = "**/StringField[*].name=='new_tag:__namespace__'"
    _tag_delete_btn = f"**/Button[*].tooltip=='Remove'"
    _all_tags_fields = "**/StringField[*]"
    _tag_update_button = "**/Button[*].tooltip=='Update'"

    # should be used as child for any collapsable frame
    collapse_bar_child_label = "/**/Label[*].text=='__name__'"

    # To be used as child element with either albedo collapse bar as root or normal collapse bar
    _albedo_and_normal_map = "**/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/Frame[*]/VStack[0]/HStack[0]/HStack[1]/**/StringField[*]"
    _albedo_map_file_icon_btn = "Property//Frame/**/sdf_browse_asset_inputs:diffuse_texture"

    _transform_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='Transform'"
    )
    _transform_pivot_label = "Property//Frame/**/Label[0].text=='Translate:pivot'"
    _add_transform_btn = (
        "Property//Frame/**/Button[*].text=='__menu_context_glyph__ Add Transforms'"
    )
    transform_translate_x = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[0]/HStack[1]/HStack[0]/HStack[0]/**/FloatDrag[0]"
    transform_translate_y = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[0]/HStack[1]/HStack[0]/HStack[1]/**/FloatDrag[0]"
    transform_translate_z = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[0]/HStack[1]/HStack[0]/HStack[2]/**/FloatDrag[0]"
    _tranform_rotate_x = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[__index__]/HStack[1]/HStack[0]/HStack[0]/**/FloatDrag[0]"
    _tranform_rotate_y = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[__index__]/HStack[1]/HStack[0]/HStack[1]/**/FloatDrag[0]"
    _tranform_rotate_z = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[__index__]/HStack[1]/HStack[0]/HStack[2]/**/FloatDrag[0]"
    _transform_scale_x = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[2]/HStack[1]/HStack[0]/HStack[0]/**/FloatDrag[0]"
    _transform_scale_y = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[2]/HStack[1]/HStack[0]/HStack[1]/**/FloatDrag[0]"
    _transform_scale_z = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[2]/HStack[1]/HStack[0]/HStack[2]/**/FloatDrag[0]"
    _linked_transform_scale = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/VStack[0]/HStack[2]/HStack[0]/ZStack[1]/Button[0]"

    _transform_multivalue = "Property//Frame/**/CollapsableFrame[0]/**/MultiFloatDragField[*].name=='multivalue'"

    # color tint locators
    _color_tint_r = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/HStack[1]/**/HStack[0]/ZStack[1]/FloatSlider[0]"
    _color_tint_g = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/HStack[1]/**/HStack[1]/ZStack[1]/FloatSlider[0]"
    _color_tint_b = "Property//Frame/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/HStack[1]/**/HStack[2]/ZStack[1]/FloatSlider[0]"

    _physics_center_of_mass_x = "Property//Frame/**/drag_per_channel_physics:centerOfMass/HStack[0]/**/physprop_physics:centerOfMass"
    _physics_center_of_mass_y = "Property//Frame/**/drag_per_channel_physics:centerOfMass/HStack[1]/**/physprop_physics:centerOfMass"
    _physics_center_of_mass_z = "Property//Frame/**/drag_per_channel_physics:centerOfMass/HStack[2]/**/physprop_physics:centerOfMass"

    _light_collapse_bar = "Property//Frame/**/CollapsableFrame[1].title=='Light'"
    # To be used as child element with _light_collapse_bar
    _light_main_texture = "**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/HStack[1]/ZStack[0]"
    _projector_chkbox = "Property//Frame/**/bool_isProjector"

    # 3D text
    _3d_text_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='Generate3d Text Node'"
    )
    _3d_text_collapse_bar_inputs = (
        "Property//Frame/**/CollapsableFrame[*].title=='Inputs'"
    )
    _3d_text_textbox = "Property//Frame/**/string_inputs:text"
    _3d_text_scale = "Property//Frame/**/float_slider_inputs:scale"
    _3d_text_spacing = "Property//Frame/**/float_slider_inputs:characterSpacing"
    _3d_text_alignment_combobox = "Property//Frame/**/token_inputs:alignment"

    _collapse_frames = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[*]"
    )
    _collapse_frames_all_labels = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/**/Label[*]"
    )
    _search_field = "Property//Frame/VStack[0]/HStack[0]/**/StringField[0]"
    _clear_search = "Property//Frame/VStack[0]/HStack[0]/**/Button[0]"

    # Locators for Node Settings
    _settings_tab = "Property//Frame/**/CollapsableFrame[*].title=='Settings'"
    _add_target_btn = "Property//Frame/**/Button[0].name=='remove'"
    _target_path_field = "Property//Frame/**/StringField[0].name=='models'"
    _add_joints_btn = "Property//Frame/**/Button[0].text=='Add Element'"
    _joints_dropdown_btn = "Property//Frame/**/Button[*].name=='listbox'"
    _search_joint_field = (
        "SearchableComboBoxWindow//Frame/**/StringField[0].name=='search_button'"
    )
    _joint_list_item = "SearchableComboBoxWindow//Frame/**/TreeView[0]/Label[0]"

    # Select Targets Window Locator
    _select_targets_window = "Select Targets"
    _search_target_field = "Select Targets//Frame/**/StringField[0].name=='search'"
    _select_target_btn = "Select Targets//Frame/VStack[0]/VStack[0]/select_button"
    _select_target_asset = "Select Targets//Frame/**/TreeView[0]/**/Label[0].text=='{}'"
    _select_searched_asset = (
        "Select Targets//Frame/**/TreeView[1]/**/Label[*].text=='{}'"
    )
    _selected_targets_label = "Select Targets//Frame/VStack[0]/VStack[0]/Label[0]"

    # Raw USD Properties location
    _pose_label = "Property//Frame/**/Label[*].text=='{}'"

    # Animation Graph Locators
    _animation_graph_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='Animation Graph'"
    )
    _animation_graph_tab = "Property//Frame/**/CollapsableFrame[*].title=='Graph'"

    # Physics Locators
    _physics_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Physics'"
    _physics_collision_enabled = "Property//Frame/**/bool_physics:collisionEnabled"
    _physics_collision_approximation = (
        "Property//Frame/**/Label[*].text=='Approximation'"
    )

    # Physics Locators
    _physics_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Physics'"
    _physics_collision_enabled = "Property//Frame/**/bool_physics:collisionEnabled"
    _physics_collision_approximation = (
        "Property//Frame/**/Label[*].text=='Approximation'"
    )

    # References Locators
    _references_collapse_bar = (
        "Property//Frame/**/CollapsableFrame[*].title=='References'"
    )

    # Payload Locators
    _payloads_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Payloads'"

    # On keyboard Input
    _on_keyboard_input_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='On Keyboard Input Node'"

    # Timer Node
    _timer_node_collapse_bar = "Property//Frame/**/CollapsableFrame[*].title=='Timer Node'"

    # SRS APP locators
    _lux_all_btn = "Property//Frame/**/CollapsableFrame[3]/**/Button[0]"
    _lux_none_btn = "Property//Frame/**/CollapsableFrame[3]/**/Button[1]"
    _lux_Reset_btn = "Property//Frame/**/CollapsableFrame[3]/**/Button[2]"
    _color_all_btn = "Property//Frame/**/CollapsableFrame[3]/**/Button[0]"
    _color_none_btn = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/**/Button[1].text"
    _color_reset_btn = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/**/Button[2].text"
    _create_lux_ramp_btn = "Property//Frame/**/Button[0].text=='Create LUX Ramp'"
    _create_color_ramp_btn = "Property//Frame/**/Button[0].text=='Create Color Ramp'"
    _schematic_schema = (
        "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[4]"
    )
    _class_combobox = "Property//Frame/**/CollapsableFrame[4]/**/ComboBox[0]"
    _apply_btn = "Property//Frame/**/CollapsableFrame[4]/**/Button[1].text=='Apply'"
    _set_rig_btn = "Property//Frame/**/Button[0].text=='Set Rig'"
    _generate_btn = "Property//Frame/**/Button[1].text=='Generate'"
    _select_tagged_window = (
        "Select Tagged Object//Frame/VStack[0]/Button[0].text=='thumb_rig_prop'"
    )

    _all_material_shader_settings = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/CollapsableFrame[*]"

    _albedo_color_sliders = "Property//Frame/**/drag_per_channel_inputs:diffuse_color_constant/HStack[__index__]/**/FloatSlider[0]"

    # Node locators
    _add_attributes_btn = "Property//Frame/**/CollapsableFrame[0]/**/HStack[0]/Button[0]"
    _attr_name = "Create Attribute//Frame/VStack[0]/HStack[0]/StringField[0]"
    _attr_port_search_bar = "Create Attribute//Frame/VStack[0]/HStack[2]/**/HStack[0]/**/StringField[0]"
    _attr_port_type = "Create Attribute//Frame/VStack[0]/HStack[1]/HStack[0]/RadioButton[{}]"
    _attr_type = "Create Attribute//Frame/VStack[0]/HStack[2]/VStack[0]/ScrollingFrame[0]/VStack[0]/Button[*].text=='{}'"
    _attr_add_btn = "Create Attribute//Frame/VStack[0]/HStack[3]/HStack[0]/Button[*]"
    _edit_code_btn = "Property//Frame/**/CollapsableFrame[0]/**/VStack[0]/HStack[1]/HStack[0]/Button[0]"
    _slang_code_editor = "Slang Code Editor//Frame/VStack[0]/ZStack[0]/CodeEditor[1]"
    _slang_save_compile_btn = "Slang Code Editor//Frame/VStack[0]/HStack[1]/Button[1]"
    _node_inputs_collapsable = "Property//Frame/**/CollapsableFrame[*].title=='Inputs'"
    _add_and_remove_attributes_collapsable = "Property//Frame/**/CollapsableFrame[*].title=='Add and Remove Attributes'"
    _create_output_window = "Create Output"
    _create_input_window = "Create Input"
    _attribute_name = "__window__//Frame/**/HStack[0]/StringField[*]"
    _type_search = "__window__//Frame/**/HStack[1]/**/HStack[0]/StringField[*]"
    _type_btn = "__window__//Frame/**/HStack[1]/**/Button[*].text=='{}'"
    _add_attribute_ok_btn = "__window__//Frame/**/Button[*].text=='OK'"
    
    _constant_node_value = "**/drag_per_channel_inputs:value/HStack[{}]/**/FloatDrag[0]"
    _evaluator_type_combobox = "Property//Frame/**/token_evaluator:type"
    _node_parameters_collapsable = "Property//Frame/**/CollapsableFrame[*].title=='Parameters'"
    _keyboard_input_key_in = "Property//Frame/**/token_inputs:keyIn"
    _simulate_on_play = "**/bool_inputs:onlyPlayback"
    _node_input_screen_position = "**/drag_per_channel_inputs:position/HStack[{}]/**/FloatDrag[0]"
    _albedo_tint = "Property//Frame/**/CollapsableFrame[2]/**/drag_per_channel_inputs:diffuse_tint/**/FloatSlider[0]"
    _opacity_toggle = "Property//Frame/**/CollapsableFrame[5]/**/HStack[0]/VStack[0]/ZStack[0]/Placer[0]"
    _base_color_slider = "Property//Frame/**/drag_per_channel_inputs:diffuse_reflection_color/HStack[__index__]/**/FloatSlider[0]"
    # light color locators
    _light_color_sliders = "Property//Frame/**/drag_per_channel_color/HStack[__index__]/**/FloatSlider[0]"
    _light_intensity_slider = "Property//Frame/**/float_slider_intensity"

    # Blend Variants Node
    _variant_set_name_combobox = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/HStack[1]/HStack[0]/ZStack[0]/ComboBox[0]"
    _variant_name_a_combobox = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/HStack[1]/HStack[0]/ZStack[0]/ComboBox[0]"
    _variant_name_b_combobox = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/HStack[1]/HStack[0]/ZStack[0]/ComboBox[0]"
    _set_variant_checkbox = "Property//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/**/CollapsableFrame[0]/**/Placer[0]"

    # On KeyBoard Input node
    _only_simulate_on_play_checkbox = "Property//Frame/**/CollapsableFrame[0]/**/CollapsableFrame[1]/**/bool_inputs:onlyPlayback"
    _key_in_drop_down = "Property//Frame/VStack[0]/ScrollingFrame[0]/**/CollapsableFrame[0]/**/token_inputs:keyIn"
    _duration_fload_slider = "Property//Frame/VStack[0]/ScrollingFrame[0]/**/CollapsableFrame[0]/**/CollapsableFrame[0]/**/float_slider_inputs:duration"

    # Mesh property
    _material_dropdown = "Property//Frame/**/CollapsableFrame[1]/**/Frame[0]/VStack[0]/HStack[0]/VStack[0]/HStack[1]/combo_drop_target"
    
    # Material property
    _property_material_sphere_loc = "Property//Frame/**/preview_drop_target.name == 'material_solo'"

    # Texture property
    _property_texture = "Property//Frame/**/sdf_asset_inputs:texture:file.name=='models'"
    _property_diffuse_texture = "Property//Frame/**/sdf_asset_inputs:diffuse_texture.name=='models'"
    
    
    def handle_select_asset_window(
            self,
            path: str,
            file_name: str,
            is_local_storage=False,
    ):
        """Handles the File Explorer Operation
        Args:
            :param path: path of the folder where the asset is present
            :param file_name: Name of assert file
            :param is_local_storage: whether the path is local storage
        """
        directory_path = self.wait.element_to_be_located(
            self.omni_driver, self._select_asset_directory_path
        )
        self.log.info("Found 'Select Asset...' window")
        self.omni_driver.wait(3)
        if not is_local_storage:
            path = self._updated_path(path)

        directory_path.double_click()
        self.omni_driver.emulate_key_combo_press(
            f"{KeyboardConstants.control}+{KeyboardConstants.a_key}"
        )
        directory_path.send_keys(path)
        self.omni_driver.wait(3)
        file_elm: OmniElement = self.omni_driver.find_element(
            self._select_asset_grid_item.replace("__filename__", file_name)
        )
        file_elm.click()
        self.find_and_click(self._select_asset_button)
        self.wait.element_to_be_invisible(
            self.omni_driver, self._select_asset_directory_path
        )
        self.log.info("Handled 'Select Asset...' window")

    def is_reset_reference_enabled(self, root_widget: OmniElement):
        "Checks if reset button is enabled"
        try:
            query = '/**/HStack[2]/Image[0].source_url.split("/")[-1] == "Changed value.svg"'
            return root_widget.find_element(query, refresh=True)
        except:
            return False

    def current_checkpoint_reference(self, root_widget: OmniElement):
        """Returns current Referenced Checkpoint"""
        current_checkpoint = root_widget.find_element(
            "/**/ZStack[0]/HStack[0]/ZStack[0]/StringField[0]"
        )
        return current_checkpoint.get_text()

    def verify_reference_tooltip(self, root_widget: OmniElement, tooltip_string: str):
        """Return Tooltip String for the Reference"""
        return root_widget.find_element(
            f'/**/ZStack[0]/HStack[0]/ZStack[0]/StringField[0].tooltip == "{tooltip_string}"'
        )

    def navigate_to_property(self):
        """Navigates to property window"""
        property_window = self.omni_driver.find_element(self._property_window)
        property_window.bring_to_front()
        self.screenshot("navigated_to_property")

    def _change_color(self, light_color: str, value: float):
        """Changes specific color

        Args:
            light_color (str): type of color
        """
        all_sliders: OmniElement = self.omni_driver.find_element(
            self._all_color_sliders, True
        )
        color: OmniElement = all_sliders.find_element(light_color, True)
        color.send_keys(str(value))

    def change_light_color(self, red=True, blue=True, green=True):
        """Changes specified color of selected light

        Args:
            red (bool, optional): selects red color. Defaults to True.
            blue (bool, optional): selects blue color. Defaults to True.
            green (bool, optional): selects green color. Defaults to True.
        """
        if red:
            self._change_color(self._red_slider, 0.5)
        if blue:
            self._change_color(self._green_slider, 1.2)
        if green:
            self._change_color(self._blue_slider, 1.5)

    def checkpoint_combobox_change_ref(self, checkpoint: int):
        """Helper Method to Handle Checkpoint Combobox"""
        reference_search = self.omni_driver.find_element(
            self._checkpoint_combobox + "/**/StringField[*]"
        )
        reference_search.click()
        self.omni_driver.emulate_char_press(checkpoint)
        self.omni_driver.wait_frames(15)
        search_result = self.omni_driver.find_element(
            self._checkpoint_combobox + "/**/TreeView[*]/**/HStack[*]"
        )
        search_result.click()
        self.omni_driver.wait_frames(15)

    def get_applied_material_name(self):
        """Gets the applied material to the prim

        Returns:
            String: Name of the applied material
        """
        material_name = self.wait.element_to_be_located(
            self.omni_driver, self._applied_material_property_text
        )
        return material_name.get_text()

    def get_albedo_property_center(self):
        """Scrolls albedo property into view and gets it center

        Returns:
            Tuple: Center position of widget
        """
        albedo = self.find_and_scroll_element_into_view(
            self._albedo_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )

        if albedo.is_collapsed():
            albedo.click()

        albedo_map = albedo.find_element(self._albedo_and_normal_map)
        albedo_map.scroll_into_view(ScrollAxis.Y, ScrollAmount.TOP)
        self.screenshot("albedo_map")
        return albedo_map.get_widget_center()

    def get_normal_property_center(self):
        """Scrolls normal property into view and gets it center

        Returns:
            Tuple: Center position of widget
        """
        normal = self.find_and_scroll_element_into_view(
            self._normal_map_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )

        if normal.is_collapsed():
            normal.click()

        normal_map = normal.find_element(self._albedo_and_normal_map)
        normal_map.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.screenshot("normal_map")
        return normal_map.get_widget_center()

    def add_tag_to_selected_prim(
            self, tag: str, namespace: str, create_new: bool = False
    ):
        """Adds a new tag to given namespace of selected prim
        :param tag: tag which is to be added
        :param namespace: namespace under which the tag is to be added
        :param create_new: whether to create new namespace
        """
        tagging = self.omni_driver.find_element(
            locator=self._tagging_collapse_bar, refresh=True
        )
        property_window: OmniElement = self.omni_driver.find_element(
            self._property_window, True
        )
        window_x, window_y = property_window.get_widget_center()
        self.omni_driver.emulate_mouse_move(window_x, window_y)
        tagging.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.TOP.value)
        if tagging.is_collapsed():
            tagging.click()
            self.omni_driver.wait(2)

        if create_new:
            self.log.info("Add tag to new namespace")
            create_new_tag = self.wait.child_element_to_be_located(
                root_element=tagging, locator=self._create_new_tag_collapsable
            )
            create_new_tag.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.TOP.value)
            if create_new_tag.is_collapsed():
                create_new_tag.click()
                self.omni_driver.wait(2)
            new_tag_field = create_new_tag.find_element(
                locator=self._new_tag_field, refresh=True
            )
            new_tag_field.scroll_into_view(
                ScrollAxis.Y.value, ScrollAmount.CENTER.value
            )

            packed_tag = namespace + "." + tag
            self.omni_driver.wait(2)
            new_tag_field.click()
            self.omni_driver.wait(2)
            new_tag_field.send_keys(packed_tag)

            add_btn = create_new_tag.find_element(locator=self._add_tag_btn)
            add_btn.click()
        else:
            self.log.info("Add tag to existing namespace")
            namespace_tags = self.wait.child_element_to_be_located(
                root_element=tagging,
                locator=self._namespace_collapsable.replace("__namespace__", namespace),
            )
            namespace_tags.scroll_into_view(
                ScrollAxis.Y.value, ScrollAmount.BOTTOM.value
            )
            if namespace_tags.is_collapsed():
                namespace_tags.click()
                self.omni_driver.wait(2)

            new_tag_field = namespace_tags.find_element(
                locator=self._new_tag_field_under_namespace.replace(
                    "__namespace__", namespace
                )
            )
            new_tag_field.scroll_into_view(
                ScrollAxis.Y.value, ScrollAmount.BOTTOM.value
            )
            self.omni_driver.wait(2)
            new_tag_field.click()
            self.omni_driver.wait(2)
            new_tag_field.send_keys(tag)

            add_btn = namespace_tags.find_element(locator=self._add_tag_btn)
            add_btn.click()

        self.log.info(f"Tag: {tag} added under namespace: {namespace}")

    def verify_tag_exists_in_selected_prim(
            self, tag: str, namespace: str, is_expected: bool = True
    ):
        """Verifies the existence of a tag under given namespace of selected prim
        :param tag: tag whose presence is to be verified
        :param namespace: namespace under which the tag should be present
        :param is_expected: whether the presence of tag is expected
        """
        tagging = self.omni_driver.find_element(locator=self._tagging_collapse_bar)

        if tagging.is_collapsed():
            tagging.click()
            self.omni_driver.wait(2)

        try:
            namespace_tags = self.wait.child_element_to_be_located(
                root_element=tagging,
                locator=self._namespace_collapsable.replace("__namespace__", namespace),
            )
        except ElementNotFound:
            self.log.info(f"Tags section not found for namespace: {namespace}")
            assert not is_expected, f"Tags section not found for namespace: {namespace}"
            return

        if namespace_tags.is_collapsed():
            namespace_tags.click()
            self.omni_driver.wait(2)

        tag_string_elms = namespace_tags.find_elements(
            locator="**/Label[*].name=='label'"
        )
        tags = [tag.get_text() for tag in tag_string_elms]

        tag_found = False
        for t in tags:
            if t == tag:
                self.log.info(f"Tag: {tag} found under namespace: {namespace}")
                tag_found = True

        if is_expected:
            assert tag_found, f"Tag: {tag} not found under namespace: {namespace}"
        else:
            assert not tag_found, f"Tag: {tag} found under namespace: {namespace}"

    def delete_tag_from_selected_prim(self, tag: str, namespace: str):
        """Deletes tag present under given namespace of selected prim
        :param tag: tag which is to be deleted
        :param namespace: namespace under which this tag belongs
        """
        packed_tag = namespace + "." + tag
        tagging = self.omni_driver.find_element(
            locator=self._tagging_collapse_bar, refresh=True
        )
        if tagging.is_collapsed():
            tagging.click()
            self.omni_driver.wait(2)

        namespace_tags = self.wait.child_element_to_be_located(
            root_element=tagging,
            locator=self._namespace_collapsable.replace("__namespace__", namespace),
        )

        if namespace_tags.is_collapsed():
            namespace_tags.click()
            self.omni_driver.wait(2)

        self.log.info(f"Attempt to click on the Delete button for tag {packed_tag}")
        all_tag_delete_btns = namespace_tags.find_elements(locator=self._tag_delete_btn)
        tag_string_elms = namespace_tags.find_elements(
            locator="**/Label[*].name=='label'"
        )
        tags = [tag.get_text() for tag in tag_string_elms]
        self.log.info(f"Remove len: {len(all_tag_delete_btns)}")
        for i in range(len(all_tag_delete_btns)):
            if tags[i] == tag:
                all_tag_delete_btns[i].scroll_into_view(
                    ScrollAxis.Y.value, ScrollAmount.CENTER.value
                )
                all_tag_delete_btns[i].click()
                break

    def edit_tag(self, tag: str, namespace: str, new_tag: str, revert: bool = False):
        """Edits a given tag belonging to given namespace
        :param tag: tag that is to be edited
        :param namespace: namespace of tag
        :param new_tag: new name for the tag
        :param revert: flag to revert the change after typing new tag
        """
        packed_tag = namespace + "." + tag
        new_packed_tag = namespace + "." + new_tag
        tagging = self.omni_driver.find_element(
            locator=self._tagging_collapse_bar, refresh=True
        )
        tagging.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.TOP.value)
        if tagging.is_collapsed():
            tagging.click()
            self.omni_driver.wait(2)

        namespace_tags = self.wait.child_element_to_be_located(
            root_element=tagging,
            locator=self._namespace_collapsable.replace("__namespace__", namespace),
        )

        self.log.info(f"Found tags for namespace {namespace}")

        if namespace_tags.is_collapsed():
            namespace_tags.click()
            self.omni_driver.wait(2)

        all_tags_fields = namespace_tags.find_elements(self._all_tags_fields)
        target_field: OmniElement = None
        for tag_field in all_tags_fields:
            if tag_field.get_text() == packed_tag:
                target_field = tag_field
                break

        if target_field:
            target_field.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.CENTER.value)
            target_field.click()
            self.omni_driver.wait(1)
            self.omni_driver.emulate_key_combo_press(
                f"{KeyboardConstants.control}+{KeyboardConstants.a_key}"
            )
            target_field.send_keys(new_packed_tag)
            if revert:
                self.log.info("Attempt to click Revert button.")
                tag_revert_btn = namespace_tags.find_element(
                    locator=self._tag_delete_btn.replace("__name__", packed_tag),
                    refresh=True,
                )
                tag_revert_btn.click()
            else:
                self.log.info("Attempt to click Update button")
                all_tag_update_btns = namespace_tags.find_elements(
                    locator=self._tag_update_button
                )
                tag_update_btn: OmniElement = None
                for btn in all_tag_update_btns:
                    if btn.is_visible():
                        tag_update_btn = btn
                        break

                if tag_update_btn:
                    tag_update_btn.click()
                    self.omni_driver.wait(2)
                    if tag_update_btn.is_visible():
                        assert (
                            False
                        ), "Failed to update tag. Update button is still visible."
                else:
                    assert False, "Failed to update tag. Update button is not visible."
        else:
            assert False, f"Tag {tag} was not found under namespace {namespace}"

    def get_sublayer_name(self):
        """Fetches name of clicked sublayer and returns its name

        Returns:
            str: Name of sublayer
        """
        self.navigate_to_property()
        sublayer_name = self.omni_driver.find_element(
            self._sublayer_name, refresh=True
        ).get_text()
        sublayer_name = sublayer_name.split("/")[-1]
        return sublayer_name

    def step_change_layer_checkpoint(self, checkpoint: int):
        """Changes the checkpoint of given sublayer"""
        layer_path = self.omni_driver.find_element(self._layer_path_widget)
        reference_dropdown = layer_path.find_element(
            "/**/HStack[1]/ZStack[0]/HStack[0]/ZStack[0]"
        )
        reference_dropdown.click()
        self.checkpoint_combobox_change_ref(checkpoint=checkpoint)
        return layer_path

    def step_reference_widget_change_checkpoint(self, checkpoint: int = 1, reset=False):
        """Changes Checkpoint reference in Reference Widget"""
        ref_widget = self.find_and_scroll_element_into_view(
            locator=self._reference_widget,
            axis=ScrollAxis.Y,
            scroll_amount=ScrollAmount.CENTER,
        )
        if reset:
            reset_btn = self.is_reset_reference_enabled(ref_widget)
            if reset_btn:
                reset_btn.click()
            else:
                raise Exception("Reset Reference button is not available")
            self.omni_driver.wait_for_stage_load(timeout=100)
            return ref_widget
        ref_widget.find_element(
            "/**/ZStack[0]/HStack[0]/ZStack[0]", refresh=True
        ).click()
        self.checkpoint_combobox_change_ref(checkpoint=checkpoint)
        # Note: Bypassing the script bug by cicking elsewhere
        self.navigate_to_property()
        self.omni_driver.wait(2)
        return ref_widget

    def get_material_drop_center(self):
        """Scrolls material property into view and gets it center

        Returns:
            Tuple: Center position of widget
        """
        material_name = self.omni_driver.find_element(
            self._applied_material_property_text, refresh=True
        )
        # return material_name.get_text()

        material = self.find_and_scroll_element_into_view(
            self._material_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )

        if material.is_collapsed():
            material.click()

        material_name = self.omni_driver.find_element(
            self._applied_material_property_text, refresh=True
        )
        return material_name.get_widget_center()

    def update_layer_metadata(self, data: dict):
        """Updates Layer Metadata of a selected layer

        Args:
            data: A dictionary containing key-value pairs for properties like 'worldAxis',
            'startTimeCode', 'endTimeCode', etc.
        """
        layer_metadata: OmniElement = self.find_and_scroll_element_into_view(
            self._layer_metadata, ScrollAxis.Y, ScrollAmount.TOP
        )
        if layer_metadata.is_collapsed():
            layer_metadata.click()
            self.omni_driver.wait(2)

        if "worldAxis" in data:
            axis_combo_box: OmniElement = layer_metadata.find_element(
                locator="**/ComboBox[*]"
            )
            axis_combo_box.select_item_from_combo_box(
                index=None, name=data["worldAxis"], stack_combo=False
            )

    def change_start_time_code(self, start_time: float):
        """Changes start time code in layer property

        Args:
            start_time (float): New start time code
        """
        start_time_code = self.omni_driver.find_element(
            self._start_time_code_field, refresh=True
        )
        self.omni_driver.wait(2)
        start_time_code.send_keys(start_time)
        self.omni_driver.wait(2)

    def change_end_time_code(self, end_time: float):
        """Changes end time code in layer property

        Args:
            end_time (float): New end time code
        """
        end_time_code = self.omni_driver.find_element(
            self._end_time_code_field, refresh=True
        )
        self.omni_driver.wait(2)
        end_time_code.send_keys(end_time)
        self.omni_driver.wait(2)

    def _open_transform_settings(self):
        """Opens the 'Transform' collapse bar"""
        transform_collapse_bar = self.find_and_scroll_element_into_view(
            self._transform_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if transform_collapse_bar.is_collapsed():
            transform_collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'Transform' settings.")
            self.omni_driver.wait(2)

    def verify_pivot_translate_exists(self):
        try:
            self._open_transform_settings()
            self.log.info("navigated_to_transform_property")
            self.omni_driver.find_element(self._transform_pivot_label, True)
            self.log.info("Pivot Translate option does exists")
            return True
        except:  # TODO Need to fix scroll into view
            self.log.info("Pivot Translate option does  not exists")
            return False

    def _add_transform_if_not_present(self):
        """If for the selected prim, transform properties are not present by default,
        this method will click on the 'Add Transform' button"""
        self._open_transform_settings()
        try:
            add_transform_btn: OmniElement = self.omni_driver.find_element(
                self._add_transform_btn.replace(
                    "__menu_context_glyph__", self.get_glyph_code("menu_context.svg")
                ),
                refresh=True,
            )
            center = add_transform_btn.get_widget_center()
            self.omni_driver.emulate_mouse_move(center[0], center[1])
            add_transform_btn.double_click()
            self.log.info(
                "Transform was not present for selected prim. Clicked on 'Add Transform' button"
            )
            self.wait.element_to_be_located(
                self.omni_driver, self.transform_translate_x
            )
        except ElementNotFound:
            pass 

    def transform_translate(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z translate values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        self._add_transform_if_not_present()
        if x is not None:
            self.select_value_for_slider(self.transform_translate_x, x)
        if y is not None:
            self.select_value_for_slider(self.transform_translate_y, y)
        if z is not None:
            self.select_value_for_slider(self.transform_translate_z, z)
        self.log_info_with_screenshot(
            "All translate values set.", "translate_values_set"
        )

    def transform_rotate(self, rotate_value: list, widget_index: int = 1):
        """Adds X, Y and Z rotate values
        :param rotate_value: list containing x, y and z values
        :param widget_index: index of 'Rotate' section in 'Transform' collapsable"""
        if len(rotate_value) != 3:
            assert (
                False
            ), f"Please send X, Y and Z values for Rotation. Received was {rotate_value}"
        self._open_transform_settings()
        self.select_value_for_slider(
            self._tranform_rotate_x.replace("__index__", f"{widget_index}"),
            rotate_value[0],
        )
        self.select_value_for_slider(
            self._tranform_rotate_y.replace("__index__", f"{widget_index}"),
            rotate_value[1],
        )
        self.select_value_for_slider(
            self._tranform_rotate_z.replace("__index__", f"{widget_index}"),
            rotate_value[2],
        )
        self.log_info_with_screenshot("added_rotation_values")

    def transform_scale(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z scale values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        self._add_transform_if_not_present()
        if x:
            self.select_value_for_slider(self._transform_scale_x, x)
        if y:
            self.select_value_for_slider(self._transform_scale_y, y)
        if z:
            self.select_value_for_slider(self._transform_scale_z, z)
        self.log_info_with_screenshot(
            "All translate values set.", "translate_values_set"
        )

    def verify_python_scripting_is_present(self):
        """Verifies whether python scripting is present for selected prim"""
        try:
            self.omni_driver.find_element(
                self._python_scripting_collapse_bar, refresh=True
            )
            self.log.info(
                "'Python Scripting' component found in Property window for selected prim."
            )
        except ElementNotFound:
            self.log.info(
                "Could not find 'Python Scripting' component in the Property window for selected prim."
            )
            raise

        usd_properties: OmniElement = self.find_and_scroll_element_into_view(
            self._raw_usd_properties_collapse_bar,
            ScrollAxis.Y,
            ScrollAmount.TOP,
            refresh=True,
        )
        attempts = 0
        while usd_properties.is_collapsed():
            if attempts >= 3:
                break
            self.log.info("USD Properties is collapsed. Attempting to expand it")
            usd_properties.click()
            attempts += 1
        self.omni_driver.wait(2)

        try:
            usd_properties.find_element(
                self.collapse_bar_child_label.replace(
                    "__name__", "omni:scripting:scripts"
                ),
                refresh=True,
            )
            self.log.info(
                "'omni:scripting:scripts' label found in the Raw USD properties component window for selected prim."
            )
        except ElementNotFound:
            self.log.info(
                "Could not find 'omni:scripting:scripts' label in the "
                "Raw USD properties component window for selected prim."
            )
            raise

    def remove_python_scripting(self):
        """Removes python scripting from the property window"""
        remove_btn: OmniElement = self.find_and_scroll_element_into_view(
            self._remove_python_scripting_btn,
            ScrollAxis.Y,
            ScrollAmount.TOP,
            refresh=True,
        )
        self.log.info("Found and scrolled to 'Remove Python Scripting Button'")
        remove_btn.click()

        self.log.info(
            "Attempt to locate 'Remove Python Scripting Dialog' and confirm it."
        )
        self.wait.element_to_be_located(
            self.omni_driver, self._remove_python_scripting_dialog
        )
        self.omni_driver.find_element(
            self._confirm_remove_python_scripting_btn, refresh=True
        ).click()
        self.omni_driver.wait(2)

        try:
            self.verify_python_scripting_is_present()
            assert False, "Could not remove python scripting for selected prim"
        except ElementNotFound:
            self.log.info("Successfully removed python scripting for selected prim")

    def add_python_script_to_selected_prim(
            self, file_name: str, folder_path: str, by_drag_and_drop: bool = False
    ):
        """Adds python script to selected prim
        Args:
            :param file_name: Name of script file
            :param folder_path: path of the folder where the script is present
            :param by_drag_and_drop: flag for drag and drop action
        """
        python_scripting: OmniElement = self.find_and_scroll_element_into_view(
            self._python_scripting_collapse_bar,
            ScrollAxis.Y,
            ScrollAmount.TOP,
            refresh=True,
        )
        if python_scripting.is_collapsed():
            self.log.info("Python Scripting is collapsed. Attempting to expand it")
            python_scripting.click()
            self.omni_driver.wait(2)

        add_asset_btn: OmniElement = python_scripting.find_element(
            self._python_scripting_add_asset_btn.replace(
                "__menu_context_glyph__", self.get_glyph_code("menu_context.svg")
            ),
            refresh=True,
        )
        if by_drag_and_drop:
            self.log.info("Add script by drag and drop")
            file: OmniElement = self.omni_driver.find_element(
                self._content_grid_item.replace("__filename__", file_name), refresh=True
            )
            x_from, y_from = file.get_widget_center()
            y_from = y_from - 20
            x_to, y_to = add_asset_btn.get_widget_center()
            self.omni_driver.drag_from_and_drop_to(x_from, y_from, x_to, y_to)
        else:
            self.log.info("Add script by clicking on 'Add Script' button")
            add_asset_btn.double_click()
            self.handle_select_asset_window(path=folder_path, file_name=file_name)

        self.omni_driver.wait(5)
        script_added = False
        fields = python_scripting.find_elements(self._python_scripting_added_scripts)
        self.log.info("Fetched all added scripts of selected prim")
        for field in fields:
            if file_name in field.get_text():
                script_added = True
                break

        assert (
            script_added
        ), "Could not find added script in Python Scripting collapsable frame."

    def handle_python_scripting_warning_window(self, click_no: bool = False):
        """Handles the warning window that pops up when a USD file containing
        python scripts in opened
        Args:
            :param click_no: click on No button when this flag is True
        """
        window = self.wait.element_to_be_located(self.omni_driver, self._warning_window)
        self.log.info("Found 'Warning' window")
        if click_no:
            self.omni_driver.find_element(self._warning_window_no_btn).click()
            self.log.info("Clicked No")
        else:
            self.omni_driver.find_element(self._warning_window_yes_btn).click()
            self.log.info("Clicked Yes")
        self.wait.invisibility_of_element(window)

    def scripting_drag_top_script_to_bottom(self):
        """Drags the topmost script to bottom of the list in Python Scripting Component
        for the selected prim"""
        python_scripting: OmniElement = self.find_and_scroll_element_into_view(
            self._python_scripting_collapse_bar,
            ScrollAxis.Y,
            ScrollAmount.TOP,
            refresh=True,
        )
        if python_scripting.is_collapsed():
            self.log.info("Python Scripting is collapsed. Attempting to expand it")
            python_scripting.click()
            self.omni_driver.wait(2)

        fields = python_scripting.find_elements(self._python_scripting_added_scripts)
        fields.append(fields.pop(0))
        required_script_seq = [x.get_text() for x in fields]
        self.log.info("Fetched all scripts")

        no_of_scripts = len(fields)
        if no_of_scripts <= 1:
            self.log.info(
                "Only one script is added. Cannot perform drag_top_script_to_bottom action."
            )
            return

        top_script: OmniElement = python_scripting.find_element(
            self._script_reorder_grab.replace("__script_index__", str(0)), refresh=True
        )
        bottom_script: OmniElement = python_scripting.find_element(
            self._script_reorder_grab.replace(
                "__script_index__", str(no_of_scripts - 1)
            ),
            refresh=True,
        )

        # drag top script to bottom
        x_from, y_from = top_script.get_widget_center()
        x_to = bottom_script.get_size_and_position("screen_position_x")
        y_to = bottom_script.get_size_and_position(
            "screen_position_y"
        ) + bottom_script.get_size_and_position("computed_height")
        self.omni_driver.drag_from_and_drop_to(x_from, y_from, x_to, y_to)
        self.omni_driver.wait(3)

        # fetch new sequence
        new_fields = python_scripting.find_elements(
            self._python_scripting_added_scripts
        )
        new_script_seq = [x.get_text() for x in new_fields]

        assert required_script_seq == new_script_seq, (
            "Order of scripts does not match. "
            "Top script should appear at bottom and sequence of other scripts should be unchanged."
        )

    def get_center(self):
        """Get center of property

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        property_win = self.omni_driver.find_element(self._property_window)
        return property_win.get_widget_center()

    def get_texture_file_center(self):
        """Scrolls texture file property into view and gets it center

        Returns:
            Tuple: Center position of widget
        """
        widget = self.find_and_scroll_element_into_view(
            self._light_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )

        if widget.is_collapsed():
            widget.click()

        texture = widget.find_element(self._light_main_texture)
        self.log_info_with_screenshot("texture_file")
        return texture.get_widget_center()

    def toggle_projector_light(self, enable: bool):
        """Toggles projector light"""
        chkbx = self.find_and_scroll_element_into_view(
            self._projector_chkbox, ScrollAxis.Y, ScrollAmount.CENTER
        )
        if enable:
            if not chkbx.is_checked():
                chkbx.click()
                self.log_info_with_screenshot("enabled_projector_light")
        else:
            if chkbx.is_checked():
                chkbx.click()
                self.log_info_with_screenshot("disabled_projector_light")

    def edit_far_clipping_range(self, value):
        """Edits the far clipping range (Y value) for selected camera"""
        camera_collapsable: OmniElement = self.omni_driver.find_element(
            self._camera_collapsable
        )
        if camera_collapsable.is_collapsed():
            camera_collapsable.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
            camera_collapsable.click()
            self.omni_driver.wait(2)
            assert (
                not camera_collapsable.is_collapsed()
            ), "Could not expand 'Camera' Collapsable"
            self.log.info("Expanded 'Camera' collapsable")

        clipping_collapsable: OmniElement = camera_collapsable.find_element(
            self._clipping_collapsable, True
        )
        clipping_collapsable.scroll_into_view(ScrollAxis.Y, ScrollAmount.TOP)
        if clipping_collapsable.is_collapsed():
            clipping_collapsable.click()
            self.omni_driver.wait(2)
            assert (
                not clipping_collapsable.is_collapsed()
            ), "Could not expand 'Clipping' Collapsable"
            self.log.info("Expanded 'Clipping' collapsable")

        far_clipping_field: OmniElement = clipping_collapsable.find_element(
            self._clipping_range_y, True
        )
        far_clipping_field.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)

        # need to hover on property window because it does not update otherwise
        property_window: OmniElement = self.omni_driver.find_element(
            self._property_window, True
        )
        window_x, window_y = property_window.get_widget_center()
        self.omni_driver.emulate_mouse_move(window_x, window_y)
        self.omni_driver.wait(3)
        far_clipping_field.send_keys(value)
        self.log_info_with_screenshot(
            f"Sent value {value} to far clipping field (Y)", "set_far_clipping_value"
        )

    def _open_3d_text_input_settings(self):
        """Opens Input collapse bar under 'Generate3d Text Node' collapse bar"""
        collapse_bar = self.find_and_scroll_element_into_view(
            self._3d_text_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        if collapse_bar.is_collapsed():
            collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'Generate3d Text Node' settings.")
            self.omni_driver.wait(2)

        inputs_collapse_bar = self.find_and_scroll_element_into_view(
            self._3d_text_collapse_bar_inputs, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        if inputs_collapse_bar.is_collapsed():
            inputs_collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'Inputs' settings.")
            self.omni_driver.wait(2)

    def change_3d_text_text(self, text: str):
        """Sets text for 3d Text
        :param text: text which is to be set
        """
        self._open_3d_text_input_settings()
        textbox: OmniElement = self.omni_driver.find_element(
            self._3d_text_textbox, True
        )
        textbox.send_keys(text)
        self.log.info("Changed text of 3d text")

    def change_3d_text_alignment(self, alignment: str):
        """Sets alignment for 3d Text
        :param alignment: alignment to set. Can be left, center or right
        """
        self._open_3d_text_input_settings()
        alignment_combobox: OmniElement = self.omni_driver.find_element(
            self._3d_text_alignment_combobox, True
        )
        if alignment.lower() == "left":
            alignment_combobox.select_item_from_combo_box(
                index=0, name="", stack_combo=True
            )
        if alignment.lower() == "center":
            alignment_combobox.select_item_from_combo_box(
                index=1, name="", stack_combo=True
            )
        if alignment.lower() == "left":
            alignment_combobox.select_item_from_combo_box(
                index=2, name="", stack_combo=True
            )
        self.log.info("Changed 3d text alignment.")

    def change_3d_text_character_spacing(self, value: float):
        """Sets character spacing for 3D text
        :param value: spacing value
        """
        self._open_3d_text_input_settings()
        spacing_field = self.omni_driver.find_element(self._3d_text_spacing, True)
        spacing_field.send_keys(value)
        self.log.info("Changed 3d text character spacing")

    def change_3d_text_scale(self, value: float):
        """Sets scale for 3D text
        :param value: scale value
        """
        self._open_3d_text_input_settings()
        scale_field = self.omni_driver.find_element(self._3d_text_scale, True)
        scale_field.send_keys(value)
        self.log.info("Changed 3d text scale")

    def check_collapse_frames_filter(self, label_text, label_count):
        """
        Checks if only appropriate collapse frames are visible after filtering
        """
        count = 0
        frames = self.omni_driver.find_elements(self._collapse_frames)
        for i in frames:
            if i.is_visible():
                assert self._assert_label_exists(
                    i, label_text
                ), f"Label {label_text} doesn't exist in visible frame"
                count += 1
            else:
                assert not self._assert_label_exists(
                    i, label_text
                ), f"Label {label_text} exists in inivisible frame"
        assert (
                count == label_count
        ), f"expected label count {label_count} doesn't match original count {count}"

    def _assert_label_exists(self, root_widget, label_text):
        try:
            root_widget.find_element(f"/**/Label[0].text=='{label_text}'")
            return True
        except ElementNotFound:
            return False

    def verify_keyword_count_in_search_results(self, keyword: str, expected_count: int):
        """Checks if the keyword has appeared given number of times in search results
        Args:
            keyword (str): keyword to search
            expected_count (int): number of times keyword is expected
        """
        all_labels = self.omni_driver.find_elements(self._collapse_frames_all_labels)
        count = 0
        for label in all_labels:
            if label.is_visible():
                count += label.get_text().lower().count(keyword.lower())

        assert (
                count == expected_count
        ), f"Expected {expected_count} occurrences of '{keyword}' in the search results. Found {count}"

    def verify_n_assets_selected(self, n: int):
        """Checks if given number of assets are selected.
        Args:
            n (int): number of selected assets
        """
        field: OmniElement = self.omni_driver.find_element(self._prim_name)
        assert (
                f"{n} models selected" in field.get_text()
        ), "Could not verify number of selected assets from prim names field."

    def assert_visible_frames_count(self, visible_frame_count):
        """Counts the number of visible collapsable frames"""
        count = 0
        frames = self.omni_driver.find_elements(self._collapse_frames)
        for i in frames:
            if i.is_visible():
                count += 1
        assert (
                visible_frame_count == count
        ), f"expected visible frame count {visible_frame_count} doesn't match original count {count}"

    def get_visible_frames_count(self):
        """Returns the count of visible frames"""
        count = 0
        frames = self.omni_driver.find_elements(self._collapse_frames)
        for i in frames:
            if i.is_visible():
                count += 1

        self.log.info(f"Visible frames count: {count}")
        return count

    def search_filter(self, text):
        """
        Searches for text in property window search bar
        """
        self.omni_driver.wait(2)
        search_field = self.omni_driver.find_element(self._search_field)
        self.omni_driver.wait(2)
        search_field.send_keys("")
        self.omni_driver.wait(1)
        
        search_field.send_keys(text)

        elem = self.omni_driver.find_element(self._search_field)
        self.omni_driver.wait(2)
        
        # Observed flakiness, the text box does not get clear and new text is appended
        if elem.get_value() != text:
            elem.send_keys(text)

        self.log.info(f"Searched for '{text}' in Property window")

    def clear_search_filter(self):
        """
        Clears search filter
        """
        self.omni_driver.wait(2)
        self.find_and_click(self._clear_search, refresh=True)
        self.omni_driver.wait(2)
        assert (
                self.omni_driver.find_element(self._search_field).get_text() == ""
        ), "Search field not cleared"

    def get_rotate_coordinates(self, widget_index: int = 1):
        """Returns list of rotate values

        Args:
            widget_index (int, optional): position of Rotate stack in Vstack . Defaults to 1.
        """
        rotate_values = []
        rotate_values.append(
            float(
                self.omni_driver.find_element(
                    self._tranform_rotate_x.replace("__index__", f"{widget_index}"),
                    refresh=True,
                ).get_value()
            )
        )
        rotate_values.append(
            float(
                self.omni_driver.find_element(
                    self._tranform_rotate_y.replace("__index__", f"{widget_index}"),
                    refresh=True,
                ).get_value()
            )
        )
        rotate_values.append(
            float(
                self.omni_driver.find_element(
                    self._tranform_rotate_z.replace("__index__", f"{widget_index}"),
                    refresh=True,
                ).get_value()
            )
        )
        return rotate_values

    def invisibility_of_widgets_after_search(self):
        try:
            self.omni_driver.find_element(self._prim_path, refresh=True)
            assert False, "Prim Path widget should be invisible in search results."
        except ElementNotFound:
            pass
        try:
            self.omni_driver.find_element(self._instanceable_chkbox, refresh=True)
            assert (
                False
            ), "Instanceable Checkbox widget should be invisible in search results."
        except ElementNotFound:
            pass

    def toggle_linked_transformation_scale(self):
        """Toggles linked transformation scale"""
        self.omni_driver.wait(2)
        self.find_and_click(self._linked_transform_scale)

    def get_scale_coordinates(self):
        """Returns list of scale values"""
        scale_values = []
        scale_values.append(
            float(
                self.omni_driver.find_element(
                    self._transform_scale_x,
                    refresh=True,
                ).get_value()
            )
        )
        scale_values.append(
            float(
                self.omni_driver.find_element(
                    self._transform_scale_y,
                    refresh=True,
                ).get_value()
            )
        )
        scale_values.append(
            float(
                self.omni_driver.find_element(
                    self._transform_scale_z,
                    refresh=True,
                ).get_value()
            )
        )
        return scale_values

    def get_translate_coordinates(self):
        """Returns list of translate values"""
        translate_values = []
        translate_values.append(
            float(
                self.omni_driver.find_element(
                    self.transform_translate_x,
                    refresh=True,
                ).get_value()
            )
        )
        translate_values.append(
            float(
                self.omni_driver.find_element(
                    self.transform_translate_y,
                    refresh=True,
                ).get_value()
            )
        )
        translate_values.append(
            float(
                self.omni_driver.find_element(
                    self.transform_translate_z,
                    refresh=True,
                ).get_value()
            )
        )
        return translate_values

    def _open_node_settings(self):
        """Opens the 'Settings' collapse bar"""
        settings_collapse_bar = self.omni_driver.find_element(self._settings_tab, True)
        if settings_collapse_bar.is_collapsed():
            settings_collapse_bar.click()
            self.log.info("Clicked to expand 'Settings' tab.")
            self.omni_driver.wait(2)

    def add_animation_source(self, target: str):
        """Adds the given target in animation source

        Args:
        target(str): Target name
        """
        settings_tab = self.omni_driver.find_element(self._settings_tab, True)
        settings_tab.find_element("**/Button[0]").double_click()
        self.search_and_select_target(target)
        path = self.omni_driver.find_element(self._target_path_field, True).get_text()
        if target not in path:
            raise ValueError(f"Failed to add target '{target}' in Animation Source")

    def settings_add_joints(self, joint: str):
        """Adds the given joint in the node property > settings

        Args:
        joint(str): joint name
        """
        self.find_and_click(self._add_joints_btn, refresh=True)
        self.wait.element_to_be_located(self.omni_driver, self._joints_dropdown_btn)
        self.find_and_click(self._joints_dropdown_btn, refresh=True)
        self.wait.element_to_be_located(self.omni_driver, self._search_joint_field)
        self.find_and_enter_text(self._search_joint_field, joint)
        joint_name = self.omni_driver.find_element(self._joint_list_item, True)
        if joint not in joint_name.get_text():
            raise ValueError(f"Failed to find joint '{joint}' in the list")
        joint_name.click(False)
        settings_tab = self.omni_driver.find_element(self._settings_tab, True)
        fields = settings_tab.find_elements("**/StringField[0]")
        for field in fields:
            if field.get_text() == joint:
                return
        raise ValueError(f"Failed to add joint '{joint}' to the property > settings")

    def search_and_select_target(self, target: str):
        """Selects the given target in Select Targets Window

        Args:
        target(str): target name
        """
        self.wait.element_to_be_located(self.omni_driver, self._select_target_btn)
        self.omni_driver.wait(1)
        self.find_and_enter_text(self._search_target_field, target)
        self.omni_driver.wait(1)
        self.find_and_click(self._select_searched_asset.format(target), refresh=True)
        # if not asset.tool_button_is_checked():
        #     asset.click()
        self.omni_driver.wait(1)
        selection_status = self.omni_driver.find_element(
            self._selected_targets_label, True
        ).get_text()
        if target not in selection_status:
            raise ValueError(f"Failed to select {target} in the target list")
        self.find_and_click(self._select_target_btn, refresh=True)
        self.omni_driver.wait(1)

    def _open_raw_usd_properties(self):
        """Opens Raw USD Properties Tab"""
        usd_properties = self.omni_driver.find_element(
            self._raw_usd_properties_collapse_bar, True
        )
        if usd_properties.is_collapsed():
            usd_properties.click()
            self.log.info("Clicked to expand 'Raw USD Properties' tab.")
            self.omni_driver.wait(2)
        assert not usd_properties.is_collapsed(), "Failed to open Raw USD Properties tab"

    def connect_input_pose(self, connect_from: str, pose_name: str):
        """Connects input pose of a node

        Args:
        connect_from(str): Name of the node to connect from
        pose_name(str): Name of input pose
        """
        self._open_raw_usd_properties()
        pose_label = self.omni_driver.find_element(
            self._pose_label.format(pose_name), True
        )
        pose_add_btn = "/".join(
            pose_label.find_parent_element_path().split("/")[:-1] + ["**/Button[0]"]
        )
        self.find_and_click(pose_add_btn, double_click=True)
        self.search_and_select_target(connect_from)
        self.verify_target_settings(self._raw_usd_properties_collapse_bar, connect_from)

    def verify_target_settings(self, collapse_bar: str, target: str):
        """Verifies whether target is added to the setting

        Args:
        collapse_bar(str): Collapse  Bar locator
        target(str): target name
        """
        collapse_bar_tab = self.omni_driver.find_element(collapse_bar, True)
        model_fields = collapse_bar_tab.find_elements(
            "**/StringField[*].name=='models'"
        )
        for model in model_fields:
            if target in model.get_text():
                return
        raise ValueError(f"Failed to add target '{target}' to the setting")

    def add_animation_graph_target(self, target: str):
        """Adds the given target to the Animation Graph Property"""
        collapse_bar = self.omni_driver.find_element(
            self._animation_graph_collapse_bar, True
        )
        if collapse_bar.is_collapsed():
            collapse_bar.click()
            self.log.info("Clicked to expand 'Animation Graph' tab.")
            self.omni_driver.wait(2)
        graph_tab = self.omni_driver.find_element(self._animation_graph_tab, True)
        if graph_tab.is_collapsed():
            graph_tab.click()
            self.log.info("Clicked to expand 'Graph' tab.")
            self.omni_driver.wait(2)

        pose_label = graph_tab.find_element("**/Label[*].text=='Animation Graph'", True)
        pose_add_btn = "/".join(
            pose_label.find_parent_element_path().split("/")[:-1] + ["**/Button[0]"]
        )
        self.find_and_click(pose_add_btn, double_click=True)
        self.search_and_select_target(target)
        self.verify_target_settings(self._animation_graph_tab, target)

    def navigate_to_schematic_schema(self):
        """Navigates to schematic schema"""
        schematic_schema = self.find_and_scroll_element_into_view(
            self._schematic_schema, ScrollAxis.Y, ScrollAmount.TOP
        )

        if schematic_schema.is_collapsed():
            schematic_schema.click()
            self.omni_driver.wait(2)

    def select_class(self, category: int):
        """Selects class from dropdown

        Args:
            category (int): Index of class
        """
        self.select_item_by_index_from_combo_box(self._class_combobox, category)

    def click_apply(self):
        """Clicks on apply button"""
        self.find_and_click(self._apply_btn)

    def select_set_rig(self):
        """Select Rig btn"""
        rig_btn = self.find_and_scroll_element_into_view(
            self._set_rig_btn, ScrollAxis.Y, ScrollAmount.TOP
        )
        rig_btn.click()

    def select_a_rig_file(self):
        """Select thumbnail Rig"""
        self.find_and_click(self._select_tagged_window)

    def generate_thumbnail(self):
        "Find and click generate button"
        self.find_and_click(self._generate_btn)

    def click_lux_all_btn(self):
        """select all lights"""
        lux_all = self.find_and_scroll_element_into_view(
            self._lux_all_btn, ScrollAxis.Y, ScrollAmount.TOP
        )
        lux_all.click()
        # self.find_and_click(self._lux_All_btn)
        """compare the screenshots"""
        # self.screenshot("vehicles_lights_lux_all.png")

    def click_colour_all_btn(self):
        """select all lights"""
        _color_all = self.find_and_scroll_element_into_view(
            self._color_all_btn, ScrollAxis.Y, ScrollAmount.CENTER
        )
        _color_all.click()
        # self.find_and_click(self._color_All_btn)
        # self.screenshot("vehicles_lights_colour_all.png")

    def create_lux_and_colour_switches(self):
        """Creates the lux and color switches"""

        self.find_and_click(self._create_lux_ramp_btn)
        self.find_and_click(self._create_color_ramp_btn)

    def reference_to_prim_path_exists(self, prim_path: str):
        """Checks whether the given prim path exists in the reference list
        Args:
            prim_path(str): prim path to verify
        """
        try:
            collapse_bar: OmniElement = self.omni_driver.find_element(
                self._reference_widget, True
            )
        except ElementNotFound:
            return False
        if collapse_bar.is_collapsed():
            collapse_bar.click()
            self.log.info("Clicked to expand 'References' tab.")
            self.omni_driver.wait(2)

        path_elms = collapse_bar.find_elements(self._all_references_prim_paths)
        reference_exists = False
        for elm in path_elms:
            if prim_path == elm.get_text():
                return True
        return False

    def get_prim_path(self):
        """Returns prim path"""
        return self.omni_driver.find_element(self._prim_path, True).get_text()

    def is_physics_collision_visible(self):
        """Checks if physics collision is visible in the property window"""
        try:
            _physics = self.omni_driver.find_element(
                self._physics_collision_enabled, refresh=True
            )
            self.log.info("Physics collision is visible in the property window")
            return _physics.is_visible()
        except ElementNotFound:
            self.log.info("Physics collision is not visible in the property window")
            return False

    def _expand_physics_settings(self):
        """Opens the 'Physics' collapse bar"""
        physics_collapse_bar = self.find_and_scroll_element_into_view(
            self._physics_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if physics_collapse_bar.is_collapsed():
            physics_collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'Physics' settings.")
            self.omni_driver.wait(2)

    def physics_collision_enabled(self):
        """Get Physics collision is enabled or not"""
        self._expand_physics_settings()
        collision_enabled = self.omni_driver.find_element(
            self._physics_collision_enabled
        ).is_checked()
        self.log.info(f"Physics Collision Enabled: {collision_enabled}")
        return collision_enabled

    def physics_collision_approximation(self):
        """Get Physics collision approximation"""
        self._expand_physics_settings()
        _approximation = self.omni_driver.find_element(
            self._physics_collision_approximation
        )
        _parent_approximation = "/".join(
            _approximation.find_parent_element_path().split("/")[:-1]
        )
        _combobox_value = self.omni_driver.find_element(
            _parent_approximation + "/**/ComboBox[0]"
        )
        approximation_value = _combobox_value.get_combobox_info()["current_value"]
        self.log.info(f"Physics Collision Approximation: {approximation_value}")
        return approximation_value

    def transform_physics_center_of_mass(
            self, x: float = None, y: float = None, z: float = None
    ):
        """
        Sets the center of mass values

        Args:
            x (float, optional): x value. Defaults to None.
            y (float, optional): y value. Defaults to None.
            z (float, optional): z value. Defaults to None.
        """
        if x is not None:
            # Double click on X field to enable editing
            x_element = self.find_and_scroll_element_into_view(
                self._physics_center_of_mass_x,
                axis=ScrollAxis.Y,
                scroll_amount=ScrollAmount.TOP,
            )
            x_element.double_click()
            self.clear_textbox(x_element)
            self.select_value_for_slider(self._physics_center_of_mass_x, x)
        if y is not None:
            # Double click on Y field to enable editing
            y_element = self.omni_driver.find_element(self._physics_center_of_mass_y)
            y_element.double_click()
            self.clear_textbox(y_element)
            self.select_value_for_slider(self._physics_center_of_mass_y, y)
        if z is not None:
            # Double click on Z field to enable editing
            z_element = self.omni_driver.find_element(self._physics_center_of_mass_z)
            z_element.double_click()
            self.clear_textbox(z_element)
            self.select_value_for_slider(self._physics_center_of_mass_z, z)
        self.log_info_with_screenshot(
            "All Physics Center of Mass values set.", "physics_center_of_mass_set"
        )

    def transform_color_tint(self, r: float = None, g: float = None, b: float = None):
        """Adds RGB values for selected prim
        :param r: r value
        :param g: y value
        :param b: b value
        """
        if r:
            self.select_value_for_slider(self._color_tint_r, r)
        if g:
            self.select_value_for_slider(self._color_tint_g, g)
        if b:
            self.select_value_for_slider(self._color_tint_b, b)
        self.log_info_with_screenshot("All rgb values set.", "rgb_values_set")

    def verify_color_tint_values(
            self, r: float = None, g: float = None, b: float = None
    ):
        """verifies color tint RGB values to incoming value"""
        rgb_values = []
        rgb_values.append(
            round(
                float(
                    self.omni_driver.find_element(
                        self._color_tint_r,
                        refresh=True,
                    ).get_value()
                ),
                3,
            )
        )
        rgb_values.append(
            round(
                float(
                    self.omni_driver.find_element(
                        self._color_tint_g,
                        refresh=True,
                    ).get_value()
                ),
                3,
            )
        )
        rgb_values.append(
            round(
                float(
                    self.omni_driver.find_element(
                        self._color_tint_b,
                        refresh=True,
                    ).get_value()
                ),
                3,
            )
        )

        assert (
                rgb_values[0] == r and rgb_values[1] == g and rgb_values[2] == b
        ), "RGB value are not matching"

        self.log_info_with_screenshot("All rgb values set.", "rgb_values_set")

    def get_material_and_shader_settings(self):
        """Returns all material and shader settings"""
        all_collapsable_frames = self.omni_driver.find_elements(
            self._all_material_shader_settings
        )
        settings = []
        for collapsable_frame in all_collapsable_frames:
            label = collapsable_frame.find_element("**/Label[0]").get_text()
            settings.append(label)
        return settings

    def change_albedo_colour(self):
        """Changes albedo colour of asset with omni pbr material"""
        self.search_filter("Albedo Color")
        self.screenshot("before_color_change")
        for i in range(3):
            self.select_value_for_slider(
                self._albedo_color_sliders.replace("__index__", str(i))
            )
        self.screenshot("after_color_change")
        self.clear_search_filter()

    def get_albedo_colour(self):
        """fetches albedo colour of asset with omni pbr material"""
        self.search_filter("Albedo Color")
        rgb_combo = []
        for i in range(3):
            element = self.find(self._albedo_color_sliders.replace("__index__", str(i)), refresh=True)
            rgb = element.get_value()
            rgb_combo.append(rgb)
        return rgb_combo

    def get_base_color(self):
        """fetches base colour of asset """
        self.search_filter("Base Color")
        rgb_combo = []
        for i in range(3):
            element = self.find(self._base_color_slider.replace("__index__", str(i)), refresh=True)
            rgb = element.get_value()
            rgb_combo.append(rgb)
        return rgb_combo

    def get_light_color(self):
        """fetches light colour of asset """
        self.search_filter("Color")
        rgb_combo = []
        for i in range(3):
            element = self.find(self._light_color_sliders.replace("__index__", str(i)), refresh=True)
            rgb = element.get_value()
            rgb_combo.append(rgb)
        return rgb_combo

    def get_light_intensity(self):
        """fetches light intensity of asset """
        self.search_filter("Intensity")
        element = self.find(self._light_intensity_slider, refresh=True)
        intensity = element.get_value()
        return intensity

    def _expand_references_settings(self):
        """Opens the 'References' collapse bar"""
        references_collapse_bar = self.find_and_scroll_element_into_view(
            self._references_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if references_collapse_bar.is_collapsed():
            references_collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'References' settings.")
            self.omni_driver.wait(2)

    def get_references_asset_path(self):
        """Get Asset Path from References"""
        self._expand_references_settings()
        references_collapse_bar = self.omni_driver.find_element(
            self._references_collapse_bar
        )
        return self._get_asset_path_text(references_collapse_bar)

    def _get_asset_path_text(self, collapse_bar: OmniElement):
        """
        Gets the assets path for the references or payloads
        """
        asset_path_label = collapse_bar.find_element("**/Label[*].text=='Asset Path'")
        asset_parent_path = "/".join(
            asset_path_label.find_parent_element_path().split("/")[:-1]
        )
        asset_path_element = self.omni_driver.find_element(
            f"{asset_parent_path}/**/StringField[0]"
        )
        asset_path_text = asset_path_element.get_text()
        return asset_path_text

    def _expand_payloads_settings(self):
        """
        Opens the 'Payloads' collapse bar
        """
        payloads_collapse_bar = self.find_and_scroll_element_into_view(
            self._payloads_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if payloads_collapse_bar.is_collapsed():
            payloads_collapse_bar.click()
            self.omni_driver.log("Clicked to expand 'Payloads' settings.")
            self.omni_driver.wait(2)

    def get_payloads_asset_path(self):
        """
        Gets the asset path of the payload
        """
        self._expand_payloads_settings()
        payloads_collapse_bar = self.omni_driver.find_element(
            self._payloads_collapse_bar
        )
        return self._get_asset_path_text(payloads_collapse_bar)

    def get_multivalue_transform_value(self):
        """Gets the values from multivalue transform field (like a matrix)"""
        elm: OmniElement = self.omni_driver.find_element(
            self._transform_multivalue, refresh=True
        )
        return elm.get_multifloatdragfield_values()

    def get_layer_world_axis(self):
        """Gets the world axis of selected layer"""
        elm: OmniElement = self.omni_driver.find_element(self._world_axis, refresh=True)
        return elm.get_combobox_info()["current_value"]

    @property
    def get_instanceable_checkbox_status(self):
        instanceable_chkbox_element = self.omni_driver.find_element(
            self._instanceable_chkbox, refresh=True
        )
        status = instanceable_chkbox_element.is_checked()
        return status

    def add_attribute_to_node(self, name: str, port_type: int, type: str):
        """
        adds attribute to node
        Args:
            name(Str): name of the attribute
            port_type(int): input:0, output:1, state:2
            type(str): attribute type
        """
        self.find_and_click(self._add_attributes_btn, bring_to_front=False)
        attribute_name = self.omni_driver.find_element(self._attr_name)
        attribute_port_type = self.omni_driver.find_element(self._attr_port_type.format(port_type))
        attribute_port_search = self.omni_driver.find_element(self._attr_port_search_bar)

        attribute_name.send_keys(name)
        attribute_port_type.click()
        attribute_port_search.send_keys(type)
        self.find_and_click(self._attr_type.format(type))
        self.find_and_click(self._attr_add_btn, refresh=True)
        self.omni_driver.close_window("Create Attribute")

    def edit_slang_node(self, code: str):
        """
        edits slang code
        Args: code: code to be edited

        """
        self.find_and_click(self._edit_code_btn, bring_to_front=False)
        editor = self.omni_driver.find_element(self._slang_code_editor)
        editor.double_click()
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.control + "+" + 'A')
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.backspace)
        editor.send_keys(code)
        self.find_and_click(self._slang_save_compile_btn)
        self.close_window('Slang Code Editor')

    def _open_inputs_tab(self):
        """Opens the Inputs Tab of selected Action Graph node"""
        inputs: OmniElement = self.omni_driver.find_element(self._node_inputs_collapsable, True)
        if inputs.is_collapsed():
            inputs.click()
            self.log.info("Clicked to expand 'Inputs' tab.")
            self.omni_driver.wait(2)
        assert not inputs.is_collapsed(), "Failed to open Inputs tab"
        return inputs
    
    def _open_add_and_remove_attributes_tab(self):
        """Opens the Add and Remove Attributes Tab of selected MessageBus Event nodes"""
        collapsable: OmniElement = self.omni_driver.find_element(self._add_and_remove_attributes_collapsable, True)
        if collapsable.is_collapsed():
            collapsable.click()
            self.log.info("Clicked to expand 'Inputs' tab.")
            self.omni_driver.wait(2)
        assert not collapsable.is_collapsed(), "Failed to open Inputs tab"
        return collapsable

    def select_node_input_attribute_name(self, value: str):
        """Selects specified value from the Attribute Name combobox
        under Inputs section for a graph node

        Args:
            value (str): value to be selected
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()
        combo: OmniElement = inputs_collapsable.find_element("**/ComboBox[*]", True)

        self.select_item_by_name_from_combo_box(combo.path, value)

    def node_input_add_target_prim(self, name: str, search: bool = False,double_click: bool = False):
        """Adds specified prim as target in the Inputs section
        for selected graph node

        Args:
            name (str): name of the prim
            search (bool): whether to search and select
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()
        add_btn: OmniElement = inputs_collapsable.find_element(
            "**/Button[*]", refresh=True
        )
        center = add_btn.get_widget_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        if double_click:
            add_btn.double_click()
        else:
            add_btn.click()

        self.wait.window_to_be_visible(self.omni_driver, self._select_targets_window)

        if search:
            self.search_and_select_target(name)
        else:
            self.find_and_click(self._select_target_asset.format(name), refresh=True)
            self.find_and_click(self._select_target_btn, refresh=True)

    def node_input_set_variant(self, set_name: str = None, variant_name: str = None, set_variant: bool = None):
        """Sets the info for 'Set Variant Selection' Node

        Args:
            set_name (str): variant set name
            variant_name (str): variant name
            set_variant (bool): whether to check the Set Variant checkbox
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()

        if set_name is not None:
            set_elm: OmniElement = inputs_collapsable.find_element(
                "**/HStack[1]/**/ComboBox[0]", refresh=True
            )
            set_elm.select_item_from_combo_box(index=None, name=set_name, stack_combo=False)
        if variant_name is not None:
            variant_elm: OmniElement = inputs_collapsable.find_element(
                "**/HStack[2]/**/ComboBox[0]", refresh=True
            )
            variant_elm.select_item_from_combo_box(index=None, name=variant_name, stack_combo=False)
        if set_variant is not None:
            checkbox: OmniElement = inputs_collapsable.find_element(
                "**/CheckBox[0]", refresh=True
            )
            if set_variant and not checkbox.is_checked():
                self.find_and_click(checkbox.path, refresh=True)
            elif not set_variant and checkbox.is_checked():
                self.find_and_click(checkbox.path, refresh=True)
        self.log_info_with_screenshot("Variant details filled.", "node_input_variant_details_filled")

    def node_input_simulate_on_play(self, enable: bool):
        """Clicks on the 'Only Simulate on Play' checkbox

        Args:
            enable (bool): Expected state of the checkbox
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()
        checkbox: OmniElement = inputs_collapsable.find_element(self._simulate_on_play, refresh=True)

        if enable and not checkbox.is_checked():
            self.find_and_click(checkbox.path, refresh=True)
        elif not enable and checkbox.is_checked():
            self.find_and_click(checkbox.path, refresh=True)
        self.log_info_with_screenshot("simulate_on_play")

    def node_input_screen_position(self, x: float = None, y: float = None):
        """Sets the Screen Position in Input of 'Draw Screen Space Text Node'

        Args:
            x (float, optional): x value. Defaults to None.
            y (float, optional): y value. Defaults to None.
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()

        if x is not None:
            field: OmniElement = inputs_collapsable.find_element(
                self._node_input_screen_position.format(0), refresh=True
            )
            field.double_click()
            self.omni_driver.emulate_key_combo_press(f"{KeyboardConstants.control}+{KeyboardConstants.a_key}")
            self.omni_driver.emulate_char_press(x)
        if y is not None:
            field: OmniElement = inputs_collapsable.find_element(
                self._node_input_screen_position.format(1), refresh=True
            )
            field.double_click()
            self.omni_driver.emulate_key_combo_press(f"{KeyboardConstants.control}+{KeyboardConstants.a_key}")
            self.omni_driver.emulate_char_press(y)
        self.log_info_with_screenshot("screen_position_set")
    
    def node_input_event_name(self, name: str):
        """Sends text to Event Name text box of On MessageBus Event node

        Args:
            name (str): Name of event
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()
        text_box: OmniElement = inputs_collapsable.find_element(
            "**/token_inputs:eventName", refresh=True
        )
        text_box.send_keys(name)
        self.log_info_with_screenshot("event_name")
    
    def node_input_value(self, value: str):
        """Sends text to Value text box of Constant node

        Args:
            value (str): Value to be sent
        """
        inputs_collapsable: OmniElement = self._open_inputs_tab()
        text_box: OmniElement = inputs_collapsable.find_element(
            "**/HStack[0]/**/StringField[*]", refresh=True
        )
        text_box.send_keys(value)
        self.log_info_with_screenshot("value_sent")
    
    def add_message_bus_event_output_attribute(self, name: str, type: str):
        """Adds the output attribute for On MessageBus Event node

        Args:
            name (str): Name of the attribute
            type (str): Type of the attribute
        """
        collapsable: OmniElement = self._open_add_and_remove_attributes_tab()
        add_btn: OmniElement = collapsable.find_element(
            "**/Button[*].text=='Add +'", refresh=True
        )
        add_btn.click()
        self.wait.window_to_be_visible(self.omni_driver, self._create_output_window)
        att_name: OmniElement = self.omni_driver.find_element(
            self._attribute_name.replace("__window__", self._create_output_window), 
            refresh=True
        )
        type_search: OmniElement = self.omni_driver.find_element(
            self._type_search.replace("__window__", self._create_output_window), 
            refresh=True
        )
        
        att_name.send_keys(name)
        self.omni_driver.wait(1)
        type_search.send_keys(type)
        self.omni_driver.wait(1)
        type_btn = self.wait.element_to_be_located(self.omni_driver, self._type_btn.format(type).replace("__window__", self._create_output_window))
        type_btn.click()

        self.find_and_click(
            self._add_attribute_ok_btn.replace("__window__", self._create_output_window), 
            refresh=True
        )
        self.wait.window_to_be_invisible(self.omni_driver, self._create_output_window)
    
    def add_message_bus_event_input_attribute(self, name: str, type: str):
        """Adds the input attribute for Send MessageBus Event node

        Args:
            name (str): Name of the attribute
            type (str): Type of the attribute
        """
        collapsable: OmniElement = self._open_add_and_remove_attributes_tab()
        add_btn: OmniElement = collapsable.find_element(
            "**/Button[*].text=='Add +'", refresh=True
        )
        add_btn.click()
        self.wait.window_to_be_visible(self.omni_driver, self._create_input_window)
        att_name: OmniElement = self.omni_driver.find_element(
            self._attribute_name.replace("__window__", self._create_input_window), 
            refresh=True
        )
        type_search: OmniElement = self.omni_driver.find_element(
            self._type_search.replace("__window__", self._create_input_window), 
            refresh=True
        )
        
        att_name.send_keys(name)
        self.omni_driver.wait(1)
        type_search.send_keys(type)
        self.omni_driver.wait(1)
        type_btn = self.wait.element_to_be_located(
            self.omni_driver, 
            self._type_btn.format(type).replace("__window__", self._create_input_window)
        )
        type_btn.click()

        self.find_and_click(
            self._add_attribute_ok_btn.replace("__window__", self._create_input_window), 
            refresh=True
        )
        self.wait.window_to_be_invisible(self.omni_driver, self._create_input_window)

    def edit_constant_node_value(self, x: float, y: float, z: float):
        """Edits the 3d value of Constant nodes

        Args:
            x (float): x value
            y (float): y value
            z (float): z value
        """
        inputs_collapsable: OmniElement = self.omni_driver.find_element(self._node_inputs_collapsable, True)
        x_elm: OmniElement = inputs_collapsable.find_element(self._constant_node_value.format(0), True)
        y_elm: OmniElement = inputs_collapsable.find_element(self._constant_node_value.format(1), True)
        z_elm: OmniElement = inputs_collapsable.find_element(self._constant_node_value.format(2), True)

        x_elm.send_keys(x)
        y_elm.send_keys(y)
        z_elm.send_keys(z)
        self.log.info(f"Edited Constant node value to new values: {x}, {y}, {z}")

    def set_graph_evaluator_type(self, type: str):
        """Selects the evaluator:type in Raw USD Properties for selected ActionGraph

        Args:
            type (str): type of evaluator to select
        """
        self._open_raw_usd_properties()
        self.select_item_by_name_from_combo_box(self._evaluator_type_combobox, type)

    def _open_parameters_tab(self):
        """Opens the Parameters Tab of selected Action Graph node"""
        parameters: OmniElement = self.omni_driver.find_element(self._node_parameters_collapsable, True)
        if parameters.is_collapsed():
            parameters.click()
            self.log.info("Clicked to expand 'Parameters' tab.")
            self.omni_driver.wait(2)
        assert not parameters.is_collapsed(), "Failed to open Parameters tab"

    def select_keyboard_input_node_key_in(self, key: str):
        self._open_parameters_tab()
        self.select_item_by_name_from_combo_box(self._keyboard_input_key_in, key)

    def select_file_for_albedo_map(self, folder_path: str, file_name: str):
        """selects the file for albedo map
        Args:
            folder_path (str): folder path where file is stored
            file_name (stre): File name
        """
        open_file_icon = self.omni_driver.find_element(self._albedo_map_file_icon_btn)
        open_file_icon.double_click()
        self.omni_driver.wait(1)
        self.handle_select_asset_window(path=folder_path, file_name=file_name)
        self.omni_driver.wait(2)

    def set_timer_node_duration(self, duration: str):
        """Sets the duration for action graph timer node
        Args:
            duration (str): duration
        """
        timer_node_collapse_bar = self.find_and_scroll_element_into_view(
            self._timer_node_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )
        self.select_value_for_slider(self._duration_fload_slider, duration)
        self.log.info(f"Successfully set the duration to: {duration}")

    def node_input_add_blend_variants_details(self, prim_name: str = None, variable_set_name: str = None,
                                              variable_name_a: str = None, varibale_name_b: str = None,
                                              set_variant_check_box_toggel: bool = True):
        """Sets the duration for action graph timer node
        Args:
           prim_name: (str) = Prima name that need to addd in target prim
           variable_set_name: (str) = Variable set name,
           variable_name_a: (str) = Variable name a,
           varibale_name_b: (str) = Variable name b,
           set_variant_check_box_toggel: (bool) = Toggles the set variant checkbox
        """
        if prim_name is not None:
            self.node_input_add_target_prim("SM_Bag_A05_01 (defaultPrim)")

        if variable_set_name is not None:
            combobox = self.omni_driver.find_element(self._variant_set_name_combobox)
            combobox.select_item_from_combo_box(name=variable_set_name, index=None, stack_combo=False)

        if variable_name_a is not None:
            combobox = self.omni_driver.find_element(self._variant_name_a_combobox)
            combobox.select_item_from_combo_box(name=variable_name_a, index=None, stack_combo=False)

        if varibale_name_b is not None:
            combobox = self.omni_driver.find_element(self._variant_name_b_combobox)
            combobox.select_item_from_combo_box(name=varibale_name_b, index=None, stack_combo=False)

        if set_variant_check_box_toggel:
            check_box = self.omni_driver.find_element(self._set_variant_checkbox, refresh=True)
            check_box.double_click()

    def set_albedo_tint(self, x_coord: int = 0, y_coord: int = 0):
        """Sets the albedo tint
        Args:
           x_coord: (int) = x coord to click
           y_coord: (int) = y coord to click
        """
        albedo_tint = self.omni_driver.find_element(self._albedo_tint)
        center = albedo_tint.get_widget_center()
        x, y = center[0] + x_coord, center[1] + y_coord
        self.omni_driver.click_at(x, y, double=True)

    def enable_opacity_toggle(self):
        """ enables opacity for """
        opacity_toggle = self.omni_driver.find_element(self._opacity_toggle)
        property_window: OmniElement = self.omni_driver.find_element(
            self._property_window, True
        )
        window_x, window_y = property_window.get_widget_center()
        self.omni_driver.emulate_mouse_move(window_x, window_y)
        opacity_toggle.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.CENTER.value)
        opacity_toggle.double_click()

    def add_material_to_mesh(self, x_coord: int = 0, y_coord: int = 0):
        """ adds material to selected mesh
        Args:
           x_coord: (int) = x coord to click
           y_coord: (int) = y coord to click
        """
        material_dropdown = self.omni_driver.find_element(self._material_dropdown)
        center = material_dropdown.get_widget_center()
        self.omni_driver.click_at(center[0], center[1])
        x, y = center[0] + x_coord, center[1] + y_coord
        self.omni_driver.click_at(x, y, double=True)
        
    def apply_material_on_selected_model(self):
        """
        Clicks on sphere material for selected layer in stage
        """
        self.find_and_click(locator=self._property_material_sphere_loc,refresh=True)
    
    def get_texture_details_from_property(self, texture:str):
        """ Get texture file/details of the active/clicked prim from property window
        Args:
            None
        Returns:
            Texture field value (could be empty or filename)
      """
        texture_details = ""
        try:
            elem_texture = self.omni_driver.find_element(texture, refresh=True)
            texture_details = elem_texture.get_value()
        except ElementNotFound:
            self.log.info("Texture Element not found for this prim ")
            pass
                
        self.log.info(f"Texture Details : {texture_details}")
        return texture_details
    
