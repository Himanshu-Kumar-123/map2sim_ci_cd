# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Viewport class
   This module contains the base methods for Viewport window
"""
import os
import re
from typing import Dict
from omni_remote_ui_automator.common.enums import (
    Mesh,
    Shape,
    CameraFlyControl,
    ScrollAmount,
    ScrollAxis,
)
from omniui.framework_lib.softassert import SoftAssert
from ..base_models.base_model import BaseModel
import time
import math
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omniui.framework_lib.image_comparison_helper import ImageComparisonHelper


class BaseViewportModel(BaseModel):
    """Base model class for Viewport window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to viewport window
    _viewport_window = "Viewport"
    _viewport_element = "Viewport//Frame/ZStack[0]"
    _render_type = "Viewport//Frame/**/SingleRenderMenuItem[*].text=='__render_engine_name__'"
    _render_type = "Viewport//Frame/**/SingleRenderMenuItem[*].text=='__render_engine_name__'"
    _render_menu_dropdown = "Viewport//Frame/**/Menu[0]/Menu[1]"
    _viewport_hamburger = (
        "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[3]/Frame[*]/ZStack[0]/ZStack[0]/Frame[*]/Menu[0]/Menu[0]"
    )
    _viewport_menu = "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[3]/Frame[*]/ZStack[0]/ZStack[0]/Frame[*]/Menu[0]/Menu[0]/SettingsRendererMenuItem[0]"
    _view_menu = "Viewport//Frame/**/Menu[0]/Menu[2]"
    _render_resolution_menu = "Viewport//Frame/**/ResolutionCollectionMenu[0]"
    _resolution_menu_item = "Viewport//Frame/**/MenuItem[*].text=='__resolution_name__'"
    _custom_resolution_item = "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[4]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[0]/SettingsRendererMenuItem[0]/MenuItem[0]"

    _view_resolution_menu = "Viewport//Frame/ZStack[0]/**/Frame[0]/Menu[0]/ZStack[0]"
    _custom_resolution_alias = (
        "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[36]/StringField[0]"
    )
    _custom_resolution_height = (
        "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[40]/IntField[0]"
    )
    _custom_resolution_alias = (
        "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[36]/StringField[0]"
    )
    _custom_resolution_height = (
        "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[40]/IntField[0]"
    )
    _custom_resolution_width = "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[38]/IntField[0]"
    _custom_resolution_add_btn = "Preferences//Frame/**/preferences_builder_Resolution Settings/**/HStack[41]/Button[0]"
    _custom_resolution_chkboxs = "Preferences//Frame/**/preferences_builder_Resolution Settings/**/CheckBox[0]"
    _preferences_resolution = "Preferences//Frame/VStack[0]/HStack[0]/ScrollingFrame[0]/TreeView[0]/Label[9]"
    _preferences_sort = "Preferences//Frame/**/ComboBox[*]"
    _preference_resolution_label = (
        "Preferences//Frame/**/preferences_builder_Resolution"
        " Settings/Frame[0]/**/resolution_treeview/HStack[*]/StringField[0]"
    )
    _view_menu_sub_menu_items = "Viewport//Frame/**/SelectableMenuItem[*].text=='__item_name__'"
    _preference_resolution_label = (
        "Preferences//Frame/**/preferences_builder_Resolution"
        " Settings/Frame[0]/**/resolution_treeview/HStack[*]/StringField[0]"
    )
    _view_menu_sub_menu_items = "Viewport//Frame/**/SelectableMenuItem[*].text=='__item_name__'"
    _show_by_type_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]"
    _camera_view_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/SelectableMenuItem[0]"
    _skeleton_view_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/SelectableMenuItem[2]"
    _lights_view_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/SelectableMenuItem[1]"
    _mesh_view_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/SelectableMenuItem[5]"
    _viewport = "Viewport"
    _save_selected_btn = "Select Files to Save##file.py//Frame/**/Button[*].text=='Save Selected'"
    _view_menu_waypoint = "Viewport//Frame/**/Menu[0]/Menu[2]/SelectableMenuItem[3]"
    _collider_all_menu = (
        "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/Menu[0]/Menu[0]/SelectableMenuItem[2]"
    )
    _physics_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/Menu[0]"
    _colliders_menu = "Viewport//Frame/**/Menu[0]/Menu[2]/CategoryMenuCollection[1]/Menu[0]/Menu[0]"
    _viewport_tooltip = "Viewport//Frame/**/ZStack[4]/Frame[3]/ZStack[0]/Placer[0]/**/Label[0]"

    # Bottom toolbar in Viewport for apps like View, FE
    _open_btn = "Viewport//Frame/**/Button[0].name=='open'"
    _save_btn = "Viewport//Frame/**/Button[0].name=='save'"
    _share_btn = "Viewport//Frame/**/Button[0].name=='share'"
    _dolly_btn = "Viewport//Frame/**/Button[0].name=='dolly'"
    _pan_btn = "Viewport//Frame/**/Button[0].name=='pan'"
    _orbit_btn = "Viewport//Frame/**/Button[0].name=='orbit'"
    _look_btn = "Viewport//Frame/**/Button[0].name=='look'"
    _frame_btn = "Viewport//Frame/**/Button[0].name=='frame'"
    _teleport_btn = "Viewport//Frame/**/Button[*].name=='teleport'"
    _section_btn = "Viewport//Frame/**/Button[0].name=='section'"
    _waypoint_prev_btn = 'Viewport//Frame/**/Button[0].name=="wpre"'
    _waypoint_play_btn = 'Viewport//Frame/**/Button[0].name=="wpla"'
    _waypoint_next_btn = 'Viewport//Frame/**/Button[0].name=="wnex"'
    _markup_prev_btn = 'Viewport//Frame/**/Button[0].name=="mprevi"'
    _markup_next_btn = 'Viewport//Frame/**/Button[0].name=="mnext"'
    _markup_approve_btn = 'Viewport//Frame/**/Button[0].name=="mappro"'
    _markup_cancel_btn = 'Viewport//Frame/**/Button[0].name=="mrejec"'
    _markup_cancel_btn = 'Viewport//Frame/**/Button[0].name=="mrejec"'
    _turntable_btn = 'Viewport//Frame/**/Button[0].name=="turntable"'
    _capture_btn = 'Viewport//Frame/**/Button[0].name=="Screenshot"'
    _screenshot_btn = 'Viewport//Frame/**/Button[0].name=="Screenshot"'
    _options_btn = 'Viewport//Frame/**/Button[0].name=="options"'
    _import_btn = 'Viewport//Frame/**/Button[0].name=="import"'
    _measure_btn = "Viewport//Frame/**/Button[0].name=='measure'"
    _section_btn = "Viewport//Frame/**/Button[0].name=='section'"
    _focus_btn = "Viewport//Frame/**/ZStack[5]/Frame[1]/**/Menu[0]/MenuItem[0]"
    _view_focus_btn = "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[7]/Frame[1]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/Menu[0]/MenuItem[1]"
    _resolution_label = "Viewport//Frame/**/menubar_resolution_label"
    _timeline_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[1]"
    _navigation_bar_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[0]"

    _waypoint_add_btn = 'Viewport//Frame/**/Button[0].name=="waypoint"'
    _waypoint_add_pin_btn = 'Viewport//Frame/**/Button[0].name=="Waypoint"'
    _markup_btn = 'Viewport//Frame/**/Button[*].name=="markup"'
    # Camera menu options -
    _camera_menu = "Viewport//Frame/ZStack[0]/**/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[3]"
    _camera_follow_user = _camera_menu + "/MenuItemCollection[1]"
    _camera_collection = _camera_menu + "/MenuItemCollection[0]"
    _camera_follow_user = _camera_menu + "/MenuItemCollection[1]"
    _camera_list = _camera_collection + "/SingleCameraMenuItem[{}]"
    _camera_options_expand = "Viewport//Frame/**/ExpandMenuItem[0]"
    _camera_options_lens = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[0]"
    _camera_options_zoom = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[1] "
    _view_camera_options_zoom = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[2] "
    _camera_options_focal_distance = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[4] "
    _camera_options_sample_focal_distance = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[5] "
    _camera_options_camera_f_stop = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[7] "
    _view_camera_options_zoom = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[2] "
    _camera_options_focal_distance = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[4] "
    _camera_options_sample_focal_distance = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[5] "
    _camera_options_camera_f_stop = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[7] "
    _camera_options_ae = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[9] "
    _camera_options_ae_slider = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[10] "
    _camera_options_ae_slider = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[10] "
    _camera_options_iso = "Viewport//Frame/**/ZStack[0]/HStack[0]/Menu[0]/MenuItem[11] "
    _camera_types = "Viewport//Frame/**/Menu[0]/Menu[3]/SingleCameraMenuItem[*]"
    _camera_speed = "Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[8]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[3]/MenuItem[0]"

    # Viewport Settings
    _settings = "Viewport//Frame/**/Menu[0]/Menu[0]"
    _navigation_settings = "Viewport//Frame/**/Menu[0]/Menu[0]/Menu[0]"
    _interia_mode = "Viewport//Frame/**/Menu[0]/Menu[0]/Menu[0]/MenuItem[6]"
    _nav_height = "Viewport//Frame/**/ImageWithProvider[0].name=='{}'"
    _navbar_btn = "Viewport//Frame/**/ZStack[5]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[0]"

    # Perspective menu
    _perspective_menu = "Viewport//Frame/**/Menu[0]/Menu[3]"
    _perspective_camera_item = "Viewport//Frame/**/Menu[0]/Menu[3]/SingleCameraMenuItem[0]"

    # View Camera menu
    _view_camera_types = "Viewport//Frame/**/Menu[0]/Menu[1]/SingleCameraMenuItem[*]"
    _view_perspective_camera = "Viewport//Frame/**/Menu[0]/Menu[1]/SingleCameraMenuItem[0]"
    _view_top_camera = "Viewport//Frame/**/Menu[0]/Menu[1]/SingleCameraMenuItem[1]"
    _view_front_camera = "Viewport//Frame/**/Menu[0]/Menu[1]/SingleCameraMenuItem[2]"
    _view_right_camera = "Viewport//Frame/**/Menu[0]/Menu[1]/SingleCameraMenuItem[3]"
    _view_cameras = "Viewport//Frame/**/Menu[0]/Menu[1]/MenuItemCollection[0]"

    # Debug view rendering mode
    _debug_view = "Viewport//Frame/**/RadioMenuCollection[*].text=='Debug View'"
    _debug_rendering_mode = "Viewport//Frame/**/MenuItem[*].text=='__name__'"

    # Lights
    _light_menu = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[4]"
    _light_items = "Viewport//Frame/**/Frame[0]/Menu[0]/Menu[4]/MenuItemCollection[0]/SelectableMenuItem[__num__]"

    # Nav Bar Tooltip locators
    _navbar_tooltip = "Viewport//Frame/**/Rectangle[*].name=='tooltip'"
    _navbar_tooltip_text = "Viewport//Frame/**/Placer[2]/**/Label[*]"
    _navbar_tool_tip_image = "Viewport//Frame/**/Placer[2]/**/Image[*]"

    # Timeline bar
    play_button = "Viewport//Frame/**/Stack[1]/**/HStack[0]/ToolButton[0]"
    _play_int_slider = "Viewport//Frame/**/IntSlider[0].name=='timeline'"

    # Toolbar
    _arrow_btn = "USD Presenter Toolbar//Frame/HStack[0]/VStack[0]/ZStack[0]/Placer[4]"
    _sun_study_btn = "USD Presenter Toolbar//Frame/HStack[0]/VStack[0]/ZStack[0]/Placer[9]/ZStack[0]"
    _location_btn = "USD Presenter Toolbar//Frame/HStack[0]/VStack[0]/ZStack[0]/Placer[10]/ZStack[0]"
    _playlist_btn = "USD Presenter Toolbar//Frame/HStack[0]/VStack[0]/ZStack[0]/Placer[8]/ZStack[0]"

    # Sun study Location
    _location_dropdown = "Sun Study Location//Frame/VStack[0]/HStack[0]/CityComboBox[0]"
    _latitude = "Sun Study Location//Frame/VStack[0]/HStack[1]/FloatDrag[0]"
    _longitude = "Sun Study Location//Frame/VStack[0]/HStack[2]/FloatDrag[0]"
    _north_orientation = "Sun Study Location//Frame/VStack[0]/HStack[3]/FloatDrag[0]"
    _close_btn = "Sun Study Location//Frame/VStack[0]/HStack[5]/HStack[0]/Button[0]"

    # Sun Study
    _date_time = "Sun Study//Frame/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/ZStack[0]/Placer[1]/Label[0]"
    _play_btn = "Sun Study//Frame/VStack[0]/VStack[0]/ZStack[0]/HStack[1]/PlayButton[0]"
    _circle_slider = "Sun Study//Frame/VStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ZStack[0]/Placer[2]/Circle[0]"

    # Sun study date & time
    _apply_btn = "Sun Study Date & Time//Frame/VStack[0]/HStack[1]/HStack[0]/Button[0]"
    _month = "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[0]/ZStack[0]/Placer[0]/ComboBox[0]"
    _year = "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[0]/ZStack[0]/Placer[2]/ComboBox[0]"
    _date = "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[0]/ZStack[2]/Placer[*]/Button[0].text=='_date_'"
    _meridian_arrow = (
        "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/Placer[9]/ZStack[0]/Placer[1]/Triangle[0]"
    )
    _minute_up = (
        "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/Placer[7]/ZStack[0]/Placer[0]/Triangle[0]"
    )
    _minute_down = (
        "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/Placer[7]/ZStack[0]/Placer[1]/Triangle[0]"
    )
    _hour_up = (
        "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/Placer[2]/ZStack[0]/Placer[0]/Triangle[0]"
    )
    _hour_down = (
        "Sun Study Date & Time//Frame/VStack[0]/HStack[0]/VStack[1]/ZStack[0]/Placer[2]/ZStack[0]/Placer[1]/Triangle[0]"
    )

    # Playlist
    _time_per_item = (
        "Playlist//Frame/VStack[0]/HStack[3]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/ZStack[0]/FloatField[0]"
    )
    _transition_type = "Playlist//Frame/VStack[0]/HStack[3]/VStack[0]/HStack[1]/ZStack[0]"
    _cut_transition = "{}//Frame/VStack[0]/ZStack[0]/Button[0]"
    _smooth_transition = "{}//Frame/VStack[0]/ZStack[1]/Button[0]"
    _transition_time = (
        "Playlist//Frame/VStack[0]/HStack[3]/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/ZStack[0]/FloatField[0]"
    )
    _playlist_play_btn = "Playlist//Frame/VStack[0]/HStack[2]/ZStack[1]"
    _playlist_dropdown = "Playlist//Frame/VStack[0]/HStack[0]/ZStack[0]/VStack[0]/HStack[0]"
    _playlist_dropdown_options = "{}//Frame/VStack[0]/**/Label[0]"
    _playlist_settings = "Playlist//Frame/VStack[0]/HStack[0]/ZStack[1]"
    _new_playlist = "{}//Frame/**/StringField[0]"
    _new_playlist_ok_btn = "{}//Frame/VStack[0]/HStack[1]/Button[0]"
    _rename_playlist = "{}//Frame/**/StringField[0]"
    _rename_playlist_ok_btn = "{}//Frame/VStack[0]/HStack[1]/Button[0]"
    _warning_no_btn = "Warning//Frame/**/Button[1]"

    # Windows
    _measure_window = "Measure"
    _section_window = "Section"

    #bind materials
    _bind_material_search_drop_down_btn ="Bind material to __name__###context_menu_bind//Frame/**/combo_open_button"
    _material_pop_window_string_field = "MaterialPropertyPopupWindow//Frame/**/StringField[0]"
    _searched_material_label = "MaterialPropertyPopupWindow//Frame/**/ScrollingFrame[0]/**/Label[0].text=='__name__'"
    _bind_material_combo_box = "Bind material to __name__###context_menu_bind//Frame/**/ComboBox[0]"
    _bind_material_ok_btn = "Bind material to __name__###context_menu_bind//Frame/**/assign_material_ok_button"

    # Configurator Buttons
    _configurator_button = "Viewport//Frame/**/ButtonProxy[*].text == '{}'"
    _generic_label = "Viewport//Frame/**/Label[*].text=='{}'"

    def __init__(self, omni_driver, **kwargs):
        super().__init__(omni_driver)
        self.image_comparison: ImageComparisonHelper = kwargs.get("image_comparison", None)
        self.golden_image_dir = kwargs.get("golden_image_dir", "")

    def generate_reference_data(self, test_data, labels=None, locators=None):
        """
        Generates the reference data for the configurator scenes
        Args:
            test_data: Test data that contains the variant and options
            labels: Labels to locate the element
            locators: Locators to locate the element
        """
        data = dict()
        for variant_name, key in test_data.items():
            data[variant_name] = dict()
            self.click_configurator_button(variant_name, labels=labels, locators=locators)
            old_visible = self.omni_driver.get_visible_prims()
            old_material_map = self.omni_driver.get_prim_material_mapping()
            for detail_name, validation_type in key.items():
                curr_dict = dict()
                self.click_configurator_button(detail_name, variant_name, labels, locators)
                self.omni_driver.wait_for_stage_load(300)

                current_visible = self.omni_driver.get_visible_prims()
                current_material_map = self.omni_driver.get_prim_material_mapping()

                new_visible = list(set(current_visible) - set(old_visible))
                new_material_map = self._material_map_difference(old_material_map,
                                                                 current_material_map)

                if len(new_visible):
                    curr_dict["visible prims"] = new_visible
                if len(new_material_map.keys()):
                    curr_dict["material map"] = new_material_map

                data[variant_name][detail_name] = curr_dict
                old_visible = current_visible
                old_material_map = current_material_map

        self.log.info(f"Generated reference data: {data}")

    def _material_map_difference(self, old_material_map: dict, current_material_map: dict):
        """Generates a dictionary of materials which are present in current map but not in old map.

        Args:
            old_material_map (dict): old material mapping dictionary
            current_material_map (dict): current material mapping dictionary
        Returns:
            dict: a dictionary containing difference between two material maps
        """
        diff = dict()
        for key, value in current_material_map.items():
            if key not in old_material_map or old_material_map[key] != value:
                diff[key] = value
        return diff

    def click_configurator_button(self, button_name, variant=None, labels=None, locators=None):
        """
        Clicks on the button in the configurator mode
        Args:
            button_name: Button name from the configurator mode
            variant: Variants in the configurator
            labels: Labels to locate the element
            locators: Locators to locate the element
        """
        if labels:
            if button_name in labels['variants']:
                ele = self.find_and_scroll_element_into_view(
                    f"{labels['_ragnarok_base_locator']}{labels['_ragnarok_variant_locator'].format(labels['variants'].index(button_name))}",
                    ScrollAxis.Y,
                    ScrollAmount.CENTER,
                    refresh=True)
            else:
                ele = self.find_and_scroll_element_into_view(
                    f"{labels['_ragnarok_base_locator']}{labels['_ragnarok_variant_option_locator'].format(labels['variants'].index(variant), labels[variant].index(button_name))}",
                    ScrollAxis.Y,
                    ScrollAmount.CENTER,
                    refresh=True)
            ele.click()

        elif locators:
            ele = self.find_and_scroll_element_into_view(
                f"{locators['_base_config_locator']}{locators[button_name]}",
                ScrollAxis.Y,
                ScrollAmount.CENTER,
                refresh=True)
            ele.click()
        else:
            self.find_and_click(self._configurator_button.format(button_name), refresh=True)
        self.log.info(f"Clicked {button_name} in Configurator mode")
        self.screenshot(f"{button_name}_clicked")
        self.omni_driver.wait(2)

    def validate_configurator_options(self, test_data: dict, labels=None, locators=None):
        """
        Cycles through variant values for various attributes and validates prim become visibility and material mapping.
        Args:
            test_data: Dictionary that contains names of variants and data associated with the variant
            labels: Labels to locate the element
            locators: Locators to locate the element
        """
        for variant_name, mapping in test_data.items():
            values = mapping.keys()
            if labels or locators:
                self.click_configurator_button(variant_name, labels=labels, locators=locators)
            for detail_name, validation_type in mapping.items():
                self.click_configurator_button(detail_name, variant_name, labels, locators)
                self.omni_driver.wait_for_stage_load(300)

                if "material_map" in validation_type:
                    all_material_mapping = self.omni_driver.get_prim_material_mapping()

                    for prim, materials in validation_type["material_map"].items():
                        if set(all_material_mapping[prim]) != set(materials):
                            assert False, f"Material mapping is not as per expectation. Found: {dict.fromkeys(validation_type['material map'])}"

                if "visible_prims" in validation_type:
                    visible_prims = self.omni_driver.get_visible_prims()
                    assert all(
                        prim in visible_prims for prim in validation_type["visible_prims"]
                    ), f"Prims of selected variant are not visible. Expected visible: {list(set(validation_type['visible_prims']) - set(visible_prims))}"

                    # check that prims related to other variant values are not visible
                    for value_2 in values:
                        if value_2 != detail_name and "visible_prims" in mapping[value_2]:
                            assert all(
                                prim not in visible_prims for prim in
                                mapping[value_2]["visible_prims"]
                            ), f"Prims of unselected variant/s should be invisible. Found: {list(set(mapping[value_2]['visible_prims']) - set(visible_prims))}"

    def select_rendering_engine(self, engine):
        """Selects the specified rendering engine

        Args:
            engine (str): Render engine name
        """
        render_dropdown = self.omni_driver.find_element(self._render_menu_dropdown)
        # TODO: remove the mouse move step when click issue gets resolved (OM-102905)
        x, y = render_dropdown.get_widget_center()
        self.omni_driver.emulate_mouse_move(x, y)
        render_dropdown.click()
        self.omni_driver.wait(2)
        render_engine = self._render_type.replace("__render_engine_name__", engine)
        engine = self.omni_driver.find_element(render_engine)
        engine.click(False)
        self.omni_driver.wait(2)
        render_dropdown.click(False)

    def viewport_video_capture(self, name, duration, fps, file_format="mp4"):
        """Capture video of the viewport

        Args:
            name (str): Name of the file
            duration (_type_): Duration of video
            fps (_type_): FPS of video
            file_format (str, optional): Format of video. Defaults to "mp4".
        """
        path = os.path.join(self.ss_dir, f"{name}.{file_format}")
        self.omni_driver.viewport_video_capture(path, duration, fps)

    def zoom(
        self,
        direction,
        start=1,
        end=500,
        screenshot_prefix: str = "",
        img_validate: bool = False,
    ):
        """Zoom in and out operation on viewport

        Args:
            direction (str): Direction of zoom i.e. In or Out
            start (int, optional): Start position. Defaults to 1.
            end (int, optional): End position. Defaults to 500.
            screenshot_prefix (str, optional): Prefix to be added to filename as unique identifier.
                                               Defaults to None.
            img_validate (bool, optional): Image validation will be performed if this flag is true.
        """
        self.omni_driver.reset_viewport_camera()
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}before_zoom_{direction}")
        self.omni_driver.zoom_viewport(direction, start, end)
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}after_zoom_{direction}")

        if img_validate:
            self.image_comparison.ssim(
                os.path.join(
                    self.golden_image_dir,
                    f"{screenshot_prefix}after_zoom_{direction}.png",
                ),
                f"{screenshot_prefix}after_zoom_{direction}.png",
            )

    def rotate(
        self,
        x_coordinate=100,
        y_coordinate=-10,
        screenshot_prefix: str = "",
        img_validate: bool = False,
    ):
        """Performs rotate operation on viewport

        Args:
             x_coordinate (int, optional): X axis position. Defaults to 100.
            y_coordinate (int, optional): Y axis position. Defaults to -10.
            screenshot_prefix (str, optional): Prefix to be added to filename as unique identifier.
                                               Defaults to None.
            img_validate (bool, optional): Image validation will be performed if this flag is true.
        """
        self.omni_driver.reset_viewport_camera()
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}before_rotate")
        self.omni_driver.rotate_viewport(x_coordinate, y_coordinate)
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}after_rotate")

        if img_validate:
            self.image_comparison.ssim(
                os.path.join(self.golden_image_dir, f"{screenshot_prefix}after_rotate.png"),
                f"{screenshot_prefix}after_rotate.png",
            )

    def pan(
        self,
        x_coordinate=-100,
        y_coordinate=0,
        screenshot_prefix: str = "",
        reset_camera: bool = True,
        img_validate: bool = False,
    ):
        """Performs pan operation on viewport

        Args:
            x_coordinate (int, optional): X axis position. Defaults to -100.
            y_coordinate (int, optional): Y axis position. Defaults to 0.
            screenshot_prefix (str, optional): Prefix to be added to filename as unique identifier.
                                               Defaults to None.
            reset_camera (bool, optional): Flag to reset camera. Defaults to True.
            img_validate (bool, optional): Image validation will be performed if this flag is true.
        """
        if reset_camera:
            self.omni_driver.reset_viewport_camera()
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}before_pan")
        self.omni_driver.pan_viewport(x_coordinate, y_coordinate)
        self.omni_driver.wait(2)
        self.viewport_screenshot(f"{screenshot_prefix}after_pan")

        if img_validate:
            self.image_comparison.ssim(
                os.path.join(self.golden_image_dir, f"{screenshot_prefix}after_pan.png"),
                f"{screenshot_prefix}after_pan.png",
            )

    def perform_zoom_pan_and_rotate(self, name: str = None, img_validate: bool = False):
        """Performs zoom in,zoom out, pan and rotate operation in same sequence.

        Args:
            name (str, optional): Prefix to be added to filename as unique identifier.
                                  Defaults to None. Defaults to None.
            img_validate (bool, optional): Image validation will be performed if this flag is true.
        """
        self.zoom("In", screenshot_prefix=name, img_validate=img_validate)
        self.zoom("Out", screenshot_prefix=name, img_validate=img_validate)
        self.pan(screenshot_prefix=name, img_validate=img_validate)
        self.rotate(screenshot_prefix=name, img_validate=img_validate)

    def get_center(self):
        """Get center of viewport

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        viewport = self.omni_driver.find_element(self._viewport_element)
        return viewport.get_widget_center()

    def create_prim(self, prim: Mesh or Shape = Mesh.CONE, delay_after_right_click: int = None, coordinates: tuple = None):
        """Creates a prim in the viewport.

        Args:
            prim (MeshorShape, optional): Mesh type to be created. Defaults to Mesh.CONE.
            delay_after_right_click (int, optional): Duration to wait after the right click. Defaults to None.
            coordinates (tuple, optional): Coordinates to right click. If none, right click goes to viewport center. Defaults to None.
        """
        viewport = self.omni_driver.find_element(self._viewport_element, refresh=True)
        self.omni_driver.wait(1)
        if coordinates:
            self.omni_driver.click_at(x=coordinates[0], y=coordinates[1], right=True)
        else:
            viewport.right_click()
        self.omni_driver.wait(1)
        if delay_after_right_click:
            self.omni_driver.wait(delay_after_right_click)

        if prim in Mesh:
            self.omni_driver.wait(1)
            self.omni_driver.select_context_menu_option(f"Create/Mesh/{prim.value}", offset_x=5, offset_y=5)
        elif prim in Shape:
            self.omni_driver.wait(1)
            self.omni_driver.select_context_menu_option(f"Create/Shape/{prim.value}", offset_x=5, offset_y=5)

    def create_material(self, material: str):
        """Creates a material at center of viewport"""
        viewport = self.omni_driver.find_element(self._viewport_element)
        viewport.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option(f"Create/Material/{material}", offset_x=5, offset_y=5)

    def create_camera(self, delay_after_right_click: int = None):
        """Creates a camera at center of viewport"""
        viewport = self.omni_driver.find_element(self._viewport_element)
        viewport.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option(f"Create/Camera", offset_x=5, offset_y=5)

    def _select_view_menu(self):
        """Clicks on view menu (eye icon)"""
        view_menu = self.omni_driver.find_element(self._view_menu)
        view_menu.click(False)

    def _select_show_by_type_menu(self):
        """Clicks on show by type menu"""
        show_by_type_menu = self.omni_driver.find_element(self._show_by_type_menu)
        show_by_type_menu.click(False)

    def _select_camera_view_menu(self):
        """Clicks on camera view menu"""
        camera_view_menu = self.omni_driver.find_element(self._camera_view_menu)
        camera_view_menu.click(False)

    def toggle_camera_view(self, enable: bool = True):
        """Toggles Camera view menu option

        Args:
            enable (bool, optional): Set to turn ON/OFF Camera View. Defaults to True.
        """
        self._select_view_menu()
        self._select_show_by_type_menu()
        element = self.omni_driver.find_element(self._camera_view_menu)
        previous_state = element.is_selected()
        self.screenshot("previous_camera_view")
        self.log.info("Camera View is enabled: %s", previous_state)
        if (enable and not previous_state) or (not enable and previous_state):
            self.log.info("Switching Camera View")
            self._select_camera_view_menu()
            self.screenshot("current_camera_view")
            element = self.omni_driver.find_element(self._camera_view_menu)
            assert enable == element.is_selected(), "Failed to toggle Camera View"
        self._select_view_menu()

    def _select_skeleton_view_menu(self):
        """Clicks on skeleton view menu"""
        skeleton_view_menu = self.omni_driver.find_element(self._skeleton_view_menu)
        skeleton_view_menu.click(False)

    def toggle_skeleton_view(self, toggle: bool = True):
        """Toggles skeleton view menu option

        Args:
            toggle (bool, optional): Toggle to turn ON/OFF skeleton view. Defaults to True.
        """
        self._select_view_menu()
        self._select_show_by_type_menu()
        if toggle:
            if not self.omni_driver.find_element(self._skeleton_view_menu).is_selected():
                self._select_skeleton_view_menu()
        self.screenshot("Skeleton_options_enabled")
        self._select_view_menu()

    def change_resolution(self, resolution: str):
        """Sets the resolution of viewport

        Args:
            resolution (str): Resolution string
        """
        self.omni_driver.set_viewport_resolution(resolution=resolution)

    def _open_viewport_menu(self):
        self.omni_driver.find_element(self._viewport_hamburger, True).click(bring_to_front=False)
        self.log_info_with_screenshot("Opened 'Viewport Hamburger Menu'", "viewport_hamburger_menu")
        self.omni_driver.find_element(self._viewport_menu, True).click(bring_to_front=False)
        self.log_info_with_screenshot("Opened 'Viewport' submenu", "viewport_submenu")

    def select_resolution_from_ui(self, resolution_name):
        self._open_viewport_menu()
        self.omni_driver.find_element(self._render_resolution_menu, True).click(bring_to_front=False)
        self.log_info_with_screenshot("Opened 'Render Resolution' submenu", "render_resolution_submenu")

        self.omni_driver.find_element(self._resolution_menu_item.replace("__resolution_name__", resolution_name), True).click(
            bring_to_front=False
        )
        self.omni_driver.wait_for_stage_load()
        self.omni_driver.click_at(0, 0) # close the resolution menu by clicking somewhere
        self.log_info_with_screenshot(f"Selected resolution: {resolution_name}", f"selected_{resolution_name}")

    def undock_viewport(self):
        """Undocks Viewport"""
        self.omni_driver.find_element(self._viewport_element).bring_to_front(undock=True)

    def check_viewport_memory_leak(self):
        vram_usage = []
        height = float(self.omni_driver.find_element(self._viewport_element).get_size_and_position("computed_height"))
        width = float(self.omni_driver.find_element(self._viewport_element).get_size_and_position("computed_width"))
        for i in range(10):
            if i % 2 == 0:
                height += 100
                width += 100
            else:
                height -= 100
                width -= 100
            self.omni_driver.wait(3)
            self.omni_driver.find_element(self._viewport).resize_window(width, height)
            self.omni_driver.wait(3)
            vram = self.omni_driver.get_viewport_info()["frame_info"]["vram_info"][0]["usage"]
            vram_usage.append(vram)
        flag = False
        i = 1
        while i < len(vram_usage):
            if vram_usage[i] < vram_usage[i - 1]:
                flag = True
            i += 1
        assert flag == True, "Memory leak present"

    def wait_for_frame_progression(self, timeout: int = 240):
        """Waits for 512 progressions in case of Path tracing and IRAY.

        Raises:
            RuntimeError: If frames dont get loaded within timeout

        """
        engine = self.omni_driver.get_viewport_info()["frame_info"]["render_mode"]
        end = time.time() + timeout

        if engine == "RaytracedLighting":
            while time.time() < end:
                try:
                    progression = self.omni_driver.get_viewport_info()["frame_info"]["progression"]
                    assert progression == 1, "There is some issue with rendering, please check."
                    frame_number = self.omni_driver.get_viewport_info()["frame_info"]["frame_number"]
                    break
                except:
                    time.sleep(2)
            while time.time() < end:
                updated_frame_number = self.omni_driver.get_viewport_info()["frame_info"]["frame_number"]
                if updated_frame_number > frame_number:
                    break
                time.sleep(2)
        elif engine == "HdStormRendererPlugin":
            while time.time() < end:
                try:
                    progression = self.omni_driver.get_viewport_info()["frame_info"]["progression"]
                    assert progression == 0, "There is some issue with rendering, please check."
                    frame_number = self.omni_driver.get_viewport_info()["frame_info"]["frame_number"]
                    break
                except:
                    time.sleep(2)
            while time.time() < end:
                updated_frame_number = self.omni_driver.get_viewport_info()["frame_info"]["frame_number"]
                if updated_frame_number > frame_number:
                    break
                time.sleep(2)
        elif engine == "iray":
            while time.time() < end:
                try:
                    updated_progression = self.omni_driver.get_viewport_info()["frame_info"]["progression"]
                    if updated_progression == 512:
                        break

                except:
                    time.sleep(2)
        elif engine == "PathTracing":
            while time.time() < end:
                try:
                    updated_progression = self.omni_driver.get_viewport_info()["frame_info"]["progression"]
                    if updated_progression == 512:
                        break
                    time.sleep(2)
                except:
                    time.sleep(2)
        if time.time() > end:
            self.log.error(f"Rendering was not finished within {timeout} seconds.")
            raise RuntimeError(f"Rendering was not finished within {timeout} seconds.")

    def open(self):
        """Clicks on Open Button"""
        self.find_and_click(self._open_btn)

    def import_btn(self):
        """Clicks on Import Button"""
        self.find_and_click(self._import_btn)

    def enable_dolly(self):
        """Enables dolly"""
        self.find_and_click(self._dolly_btn)

    def enable_pan(self):
        """Enables pan"""
        self.find_and_click(self._pan_btn)

    def enable_orbit(self):
        """Enables orbit"""
        self.find_and_click(self._orbit_btn)

    def enable_look(self):
        """Enables look"""
        self.find_and_click(self._look_btn)

    def toggle_dolly(self, enable=True):
        """Toggles Dolly Mode

        Args:
        enable(bool): Bool value to enable Dolly Mode
        """
        element = self.omni_driver.find_element(self._dolly_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_dolly_mode")
        self.log.info("dolly Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching dolly mode")
            element.click()
        self.screenshot("current_dolly_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle dolly mode"

    def toggle_pan(self, enable=True):
        """Toggles pan Mode

        Args:
        enable(bool): Bool value to enable pan Mode
        """
        element = self.omni_driver.find_element(self._pan_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_pan_mode")
        self.log.info("Pan Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching pan mode")
            element.click()
        self.screenshot("current_pan_mode")
        self.omni_driver.wait(5)
        self.log.info(element.tool_button_is_checked())
        assert enable == element.tool_button_is_checked(), "Failed to toggle pan mode"

    def toggle_orbit(self, enable=True):
        """Toggles Orbit Mode

        Args:
        enable(bool): Bool value to enable orbit Mode"""
        element = self.omni_driver.find_element(self._orbit_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_orbit_mode")
        self.log.info("orbit Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching orbit mode")
            element.click()
        self.screenshot("current_orbit_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle orbit mode"

    def toggle_look(self, enable=True):
        """Toggles look Mode

        Args:
        enable(bool): Bool value to enable look Mode
        """
        element = self.omni_driver.find_element(self._look_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_Look_mode")
        self.log.info("Look Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching Look mode")
            element.click()
        self.screenshot("current_Look_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle Look mode"

    def enable_frame(self):
        """Enables frame"""
        self.find_and_click(self._frame_btn)

    def enable_teleport(self):
        """Enables teleport"""
        self.find_and_click(self._teleport_btn)

    def toggle_teleport(self, enable=True):
        """Toggles Teleport Mode

        Args:
        enable(bool): Bool value to enable teleport Mode"""
        element = self.omni_driver.find_element(self._teleport_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_teleport_mode")
        self.log.info("teleport Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching teleport mode")
            element.click()
        self.screenshot("current_teleport_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle teleport mode"

    def toggle_focus_mode(self):
        """Toggles Focus Mode in Viewport"""
        self.find_and_click(self._focus_btn, refresh=True)

    def toggle_focus_in_view(self):
        """Toggles Focus Mode in Viewport"""
        self.find_and_click(self._view_focus_btn, refresh=True)

    def navigator_bar_capture_screenshot(self):
        """Left Clicks Capture in Navigator Bar"""
        self.find_and_click(self._capture_btn)

    def open_preference_window(self):
        """Left clicks Options in Navigator Bar"""
        self.find_and_click(self._options_btn)
        self.omni_driver.wait(1)

    def next_waypoint(self):
        """Changes to next waypoint"""
        self.find_and_click(self._waypoint_next_btn)

    def select_preference_viewport_resolution(self):
        """Left clicks on Viewport resolution in preference window"""
        self.find_and_click(self._preferences_resolution)
        self.omni_driver.wait(1)

    def sort_resolution(self, index: int):
        """Sorts resolution by type
        sort_by: Width:0, Height:1, Alphabetical ascending:2, Alphabetical descending:3
        """
        self.omni_driver.find_element(self._preferences_sort).select_item_from_combo_box(index)
        resolutions = self.omni_driver.find_elements(self._preference_resolution_label)
        res = [resolution.get_text() for resolution in resolutions]
        return res

    def close_preference_window(self):
        self.omni_driver.close_window("Preferences")

    def open_screenshots_location(self, offset_y=0):
        """Opens Screenshot Location by right-clicking Capture in Navigator Bar"""
        capture = self.omni_driver.find_element(self._capture_btn)
        capture.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("View Screenshots", offset_y=offset_y)
        self.omni_driver.wait(2)

    def expand_camera_options(self, expand: bool):
        """Expand camera options

        Args:
            expand (bool): If true expand, otherwise collapse.
        """
        camera_expand = self.omni_driver.find_element(self._camera_options_expand, refresh=True)

        try:
            focal_dist = self.omni_driver.find_element(self._camera_options_focal_distance, refresh=True)
        except:
            focal_dist = None

        if expand:
            if not focal_dist:
                camera_expand.click()
                self.log.info("Camera options expanded.")
            else:
                self.log.info("Camera options is already expanded.")
            self.screenshot("expanded_camera_options")

        else:
            if focal_dist:
                camera_expand.click()
                self.log.info("Camera options collapsed.")
            else:
                self.log.info("Camera options is already collapsed.")
            self.screenshot("collapsed_camera_options")

    def find_and_assert_all_camera_options(self):
        """Searches and asserts all the camera options are visible on screen"""
        self.log.info("Validating if all camera options are visible on screen.")
        soft_assert = SoftAssert()
        camera_lens = self.omni_driver.find_element(self._camera_options_lens)
        zoom = self.omni_driver.find_element(self._camera_options_zoom)
        focal_dist = self.omni_driver.find_element(self._camera_options_focal_distance)
        sample_focal_dist = self.omni_driver.find_element(self._camera_options_sample_focal_distance)
        f_stop = self.omni_driver.find_element(self._camera_options_camera_f_stop)
        ae = self.omni_driver.find_element(self._camera_options_ae)
        iso = self.omni_driver.find_element(self._camera_options_iso)

        soft_assert.expect(camera_lens.is_visible(), "Camera Lens option is not visible")
        soft_assert.expect(zoom.is_visible(), "Camera Zoom option is not visible")
        soft_assert.expect(focal_dist.is_visible(), "Camera Focal Distance option is not visible")
        soft_assert.expect(
            sample_focal_dist.is_visible(),
            "Camera Sample Focal Distance option is not visible",
        )
        soft_assert.expect(f_stop.is_visible(), "Camera Lens F-Stop is not visible")
        soft_assert.expect(ae.is_visible(), "Camera Lens AE is not visible")
        soft_assert.expect(iso.is_visible(), "Camera Lens ISO is not visible")
        self.screenshot("camera_options")
        soft_assert.assert_all()
        self.log.info("All camera options are visible on screen.")

    def camera_change_focus(self, distance: int):
        """Changes camera focus

        Args:
            distance (int): Focal Distance to set
        """
        focal_dist = self.omni_driver.find_element(self._camera_options_focal_distance)
        focal_dist.send_keys(distance)
        self.log.info(f"Changed focal distance to {distance}")
        self.screenshot(f"changed_focal_distance_to_{distance}")
        self.omni_driver.wait(2)

    def click_camera_options_sample_focal_distance(self):
        """Clicks on camera view menu"""
        sample_focal_dist = self.omni_driver.find_element(self._camera_options_sample_focal_distance)
        sample_focal_dist.click(False)

    def tear_off_menu(
        self,
        element: OmniElement,
        initial_offset_x: float = 0,
        initial_offset_y: float = 0,
        final_offset_x: float = 0,
        final_offset_y: float = 0,
        tolerance: float = 1,
    ):
        """Performs tear off operation for a menu
        Args:
            element (OmniElement): item of the menu which will be used to calculate
            relative position of the tear off bar
            initial_offset_x (float): horizontal offset from the center of the element
            initial_offset_y (float): vertical offset from the center of the element
            final_offset_x (float): horizontal offset from center of viewport
            final_offset_y (float): vertical offset from center of  viewport
            tolerance (float): maximum difference allowed between displacement of menu and
            displacement of element
        """
        viewport_center = self.get_center()
        x_initial = element.get_size_and_position("screen_position_x")
        y_initial = element.get_size_and_position("screen_position_y")
        x_pos = (
            element.get_size_and_position("screen_position_x")
            + element.get_size_and_position("computed_width") / 2
            + initial_offset_x
        )
        y_pos = element.get_size_and_position("screen_position_y") + initial_offset_y
        x_final = viewport_center[0] + final_offset_x
        y_final = viewport_center[1] + final_offset_y
        self.log.info("Performing drag and drop operation")
        self.omni_driver.drag_from_and_drop_to(x_pos, y_pos, x_final, y_final)
        self.log.info(f"Dragged from ({x_pos}, {y_pos}) to ({x_final}, {y_final})")

        elm_displacement_x = abs(element.get_size_and_position("screen_position_x") - x_initial)
        elm_displacement_y = abs(element.get_size_and_position("screen_position_y") - y_initial)
        menu_displacement_x = abs(x_final - x_pos)
        menu_displacement_y = abs(y_final - y_pos)

        self.log.info(
            f"Displacement of Menu: ({menu_displacement_x}, {menu_displacement_y})"
            f"\nDisplacement of element: ({elm_displacement_x}, {elm_displacement_y})"
        )

        # when the menu is displaced, all the items in it go under same displacement.
        success = math.isclose(elm_displacement_x, menu_displacement_x, rel_tol=tolerance) and math.isclose(
            elm_displacement_y, menu_displacement_y, rel_tol=tolerance
        )

        if success:
            self.log.info(
                "[Tear Off Menu] SUCCESS: Both the Menu and element have "
                f"similar displacements within given tolerance range: {tolerance}."
            )
        else:
            self.log.info(
                "[Tear Off Menu] FAIL: The displacements of the Menu and element are not "
                f"similar within the tolerance: {tolerance}"
            )
        return success

    def fullscreen(self, assert_width: bool = False, assert_height: bool = True):
        viewport_old = self.omni_driver.find_element(self._viewport_element)
        old_width = viewport_old.get_size_and_position("computed_width")
        old_height = viewport_old.get_size_and_position("computed_height")
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.f11)
        viewport_old = self.omni_driver.find_element(self._viewport_element, refresh=True)
        if assert_height:
            new_height = viewport_old.get_size_and_position("computed_height")
            assert old_height < new_height, "Viewport height did not change"
        if assert_width:
            new_width = viewport_old.get_size_and_position("computed_width")
            assert old_width < new_width, "Viewport width did not change"
        self.log.info("Viewport size changed to fullscreen")

    def camera_move(
        self,
        direction: CameraFlyControl,
        duration: int,
        hold: bool = False,
        release: bool = False,
        fast: bool = False,
        slow: bool = False,
    ):
        """Moves the camera

        Args:
            direction (CameraFlyControl): Direction to move camera in like Left, Right, Forward and Backward
            duration (int): Duration of how much to moce
            hold (bool, optional): Whether to hold the button. Defaults to False.
            release (bool, optional): Whether to release the button. Defaults to False.
            fast (bool, optional): Fast fly. Defaults to False.
            slow (bool, optional): Slow fly. Defaults to False.
        """
        center = self.get_center()
        self.omni_driver.click_at_and_hold(center[0], center[1], right_click=True, hold_click=True)
        self.log.info("Pressed and hold right click")
        if direction.name in ("FORWARD", "BACKWARD", "LEFT", "RIGHT"):
            if fast:
                self.log.info("Motion: Fast")
                self.omni_driver.key_press(
                    combo=KeyboardConstants.left_shift,
                    duration_to_hold=duration,
                    hold_button=True,
                    release_button=release,
                )
                self.log.info("Left Shift pressed")
                self.omni_driver.key_press(
                    combo=direction.value,
                    duration_to_hold=duration,
                    hold_button=hold,
                    release_button=release,
                )
                self.log.info(f"{direction.value} pressed")
                self.omni_driver.key_press(
                    combo=KeyboardConstants.left_shift,
                    duration_to_hold=duration,
                    hold_button=False,
                    release_button=True,
                )
                self.log.info("Left Shift released")
            elif slow:
                self.log.info("Motion: Slow")
                self.omni_driver.key_press(
                    combo=KeyboardConstants.left_control,
                    duration_to_hold=duration,
                    hold_button=True,
                    release_button=release,
                )
                self.log.info("Left Ctrl pressed")
                self.omni_driver.key_press(
                    combo=direction.value,
                    duration_to_hold=duration,
                    hold_button=hold,
                    release_button=release,
                )
                self.log.info(f"{direction.value} pressed")
                self.omni_driver.key_press(
                    combo=KeyboardConstants.left_control,
                    duration_to_hold=duration,
                    hold_button=False,
                    release_button=True,
                )
                self.log.info("Left Shift released")
            else:
                self.log.info("Motion: Normal")
                self.omni_driver.key_press(
                    combo=direction.value,
                    duration_to_hold=duration,
                    hold_button=hold,
                    release_button=release,
                )
                self.log.info(f"{direction.value} pressed")
        else:
            self.log.error(f"Provided input direction - {direction.name} is not valid.")
            assert False, f"Provided input direction - {direction.name} is not valid."
        self.omni_driver.click_at_and_hold(center[0], center[1], right_click=True, release_click=True)
        self.log.info("Released right click")

    def camera_turn(self, x: float, y: float):
        """Turns the camera into Left and Right

        Args:
            x (float): Value to move in X
            y (float): Value to move in Y
        """
        center = self.get_center()
        self.omni_driver.click_at_and_hold(center[0], center[1] - 50, right_click=True, hold_click=True)
        self.log.info("Pressed and hold right click")
        self.omni_driver.emulate_mouse_move(x, y)
        self.log.info(f"Dragged mouse from {center[0]},{center[1] - 50} to {x},{y}")
        self.omni_driver.click_at_and_hold(center[0], center[1] - 50, right_click=True, release_click=True)
        self.log.info("Released right click")

    def capture_live_video(self, name, duration):
        """Initializes viewport video capture in child thread

        Args:
            name (_type_): Name of video
            duration (_type_): Duration of video

        Returns:
            _type_: _description_
        """
        import threading

        self.log.info("Starting video capture in another thread.")
        thread = threading.Thread(target=self.viewport_video_capture, args=(name, duration, 24))
        self.log.info("Started video capture in another thread.")
        thread.start()
        return thread

    def _navigate_to_viewport_settings(self):
        """Navigates to viewport settings"""
        self.find_and_click(self._settings, bring_to_front=False)
        self.log.info("Navigated to viewport settings")

    def _navigate_to_viewport_navigation_settings(self):
        """Navigates to viewport navigation settings"""
        self.find_and_click(self._navigation_settings, bring_to_front=False)
        self.log.info("Navigated to viewport navigation settings")

    def toggle_inertia(self, enable: bool = False):
        """Enables Inertia mode

        Args:
            enable (bool, optional): Whether to enable or disable inertia. Defaults to False.
        """
        self._navigate_to_viewport_settings()
        self._navigate_to_viewport_navigation_settings()
        inertia = self.omni_driver.find_element(self._interia_mode)
        inertia_center = inertia.get_widget_center()

        if enable:
            self.omni_driver.wait(2)
            self.omni_driver.click_at(inertia_center[0] + 40, inertia_center[1], double=True)
            self.log.info("Toggled inertia ON")
        else:
            self.log.info("Toggled inertia OFF")
        self.screenshot("toggled_viewport_inertia_setting")

    def drag_viewport_element(self, x_pos: float, y_pos: float):
        """Performs Drag operation on Viewport Window

        Arguments:
        x_pos(float): X-coordinate to drag mouse to
        y_pos(float): Y-coordinate to drag mouse to
        """
        viewport_window = self.omni_driver.find_element(self._viewport_element)
        viewport_window.drag_and_drop(x_pos, y_pos)

    def add_waypoint(self):
        """Adds Waypoint from Waypoint Tool in Nav Bar"""
        self.find_and_click(self._waypoint_add_btn)
        self.omni_driver.wait(1)

    def switch_to_perspective(self):
        """Switches to camera perspective"""
        self.find_and_click(self._perspective_menu)
        self.find_and_click(self._perspective_camera_item, False)
        self.log_info_with_screenshot("switched to camera perspective")
        self.find_and_click(self._perspective_menu, False)

    def switch_to_camera(self, index: int):
        """Switches to Camera with given name

        Args:
        index(int): index of camera starting from 1
        """
        self.find_and_click(self._camera_menu)
        self.find_and_click(self._camera_collection, False)
        self.log_info_with_screenshot("switched to camera collection")
        self.find_and_click(self._camera_list.format(index - 1), False)

    def click_camera_lock(self, index: int, ss_suffix: str = ""):
        """Clicks on the Lock button for camera at given index

        Args:
            index (int): index of camera starting from 1
            ss_suffix (str): suffix for screenshot
        """
        self.find_and_click(self._camera_menu)
        self.find_and_click(self._camera_collection, False)
        camera_item: OmniElement = self.omni_driver.find_element(self._camera_list.format(index - 1))
        x = (
            camera_item.get_size_and_position("screen_position_x")
            + camera_item.get_size_and_position("computed_width")
            - 10
        )
        y = camera_item.get_widget_center()[1]
        self.omni_driver.click_at(x, y)
        self.log_info_with_screenshot(f"Clicked on Lock icon for camera {index}.", f"camera_{index}_{ss_suffix}")

    def open_perspective_camera_properties(self):
        """Opens properties section for perspective camera"""
        self.switch_to_perspective()
        self.find_and_click(self._camera_menu)
        perspective_widget: OmniElement = self.omni_driver.find_element(self._perspective_camera_item)
        center_x, center_y = perspective_widget.get_widget_center()
        width = perspective_widget.get_size_and_position("computed_width")
        self.omni_driver.click_at(center_x + width / 2 - 15, center_y)
        self.log.info("Clicked on camera properties icon.")

    def select_debug_view_rendering_mode(self, renderer: str):
        """Changes rendering mode in debug view

        Args:
            renderer (str): name of renderer
        """
        render_dropdown = self.omni_driver.find_element(self._render_menu_dropdown, True)
        render_dropdown.click()
        self.find_and_click(self._debug_view, False, True)
        renderer_menu = self.find_and_scroll_element_into_view(
            self._debug_rendering_mode.replace("__name__", renderer),
            ScrollAxis.Y,
            ScrollAmount.TOP,
            refresh=True,
        )
        renderer_menu.click(False)
        self.omni_driver.wait(5)
        assert renderer_menu.tool_button_is_checked() == True, "Appropriate renderering mode isn't selected"
        self.log.info(f"Rendering mode changed to {renderer}")

    def save_usd(self):
        """Save the current USD"""
        self.find_and_click(self._save_btn)
        try:
            self.find_and_click(self._save_selected_btn)
            self.log.info("File saved successfully.")
        except ElementNotFound:
            self.log.info("Could not close 'Select Files to Save' window")

    def click_open_btn(self):
        """Clicks on Open Button"""
        self.find_and_click(self._open_btn)

    def focus_on_selected_asset(self):
        self.omni_driver.emulate_key_press(KeyboardConstants.f_key)
        self.omni_driver.wait_for_stage_load()

    def open_previous_waypoint(self):
        """Navigate to Previous Waypoint"""
        self.omni_driver.find_element(self._waypoint_prev_btn, True).click()
        self.omni_driver.wait_for_stage_load()

    def toggle_playlist_mode(self):
        """Play/Pause Waypoint Playlist"""
        self.omni_driver.find_element(self._waypoint_play_btn, True).click()
        self.omni_driver.wait_for_stage_load()

    def open_next_waypoint(self):
        """Navigate to Next Waypoint"""
        self.omni_driver.find_element(self._waypoint_next_btn, True).click()
        self.omni_driver.wait_for_stage_load()

    @property
    def waypoint_navigation_enabled(self):
        """Returns whether waypoint navigation is enabled"""
        waypoint_tool = [
            self.omni_driver.find_element(self._waypoint_next_btn, True),
            self.omni_driver.find_element(self._waypoint_prev_btn, True),
            self.omni_driver.find_element(self._waypoint_play_btn, True),
        ]
        is_enabled = all([x.is_checked() for x in waypoint_tool])
        self.log.info("[Nav Bar] Waypoint Navigation is checked: %s", is_enabled)
        return is_enabled

    @property
    def current_renderer(self):
        """Returns current renderer of viewport"""
        return self.omni_driver.get_viewport_info()["frame_info"]["render_mode"]

    def nav_bar_options(self) -> Dict[str, OmniElement]:
        """Searches all the nav bar options visible on screen
        None if option is not"""

        elements = {
            "open_btn": self._open_btn,
            "share_btn": self._share_btn,
            "save_btn": self._save_btn,
            "import_btn": self._import_btn,
            "dolly_btn": self._dolly_btn,
            "pan_btn": self._pan_btn,
            "orbit_btn": self._orbit_btn,
            "look_btn": self._look_btn,
            "frame_btn": self._frame_btn,
            "teleport_btn": self._teleport_btn,
            "waypoint_prev_btn": self._waypoint_prev_btn,
            "waypoint_play_btn": self._waypoint_play_btn,
            "waypoint_next_btn": self._waypoint_next_btn,
            "turntable_btn": self._turntable_btn,
            "capture_btn": self._capture_btn,
            "screenshot_btn": self._screenshot_btn,
            "options_btn": self._options_btn,
            "waypoint_btn": self._waypoint_add_btn,
            "markup_btn": self._markup_btn,
            "markup_prev_btn": self._markup_prev_btn,
            "markup_next_btn": self._markup_next_btn,
            "markup_approve_btn": self._markup_approve_btn,
            "markup_cancel_btn": self._markup_cancel_btn,
        }

        options = {}

        for element, element_val in elements.items():
            try:
                val = self.omni_driver.find_element(element_val, True)
            except Exception as exc:
                self.log.info(f"Element not found: {element} with locator {element_val}")
                val = None
            options[element] = val

        return options

    def select_lights(self, num):
        """Selected light based on its numerical position in dropdown

        Args:
            num (int): position of light in dropdown
        """
        self.find_and_click(self._light_menu)
        light_item = self.find_and_click(self._light_items.replace("__num__", str(num)), bring_to_front=False)
        self.log.info(f"Lighting mode {light_item.get_name()} is selected")
        return light_item.get_name()

    def view_menu_toggle_waypoint(self):
        """Toggles Waypoint option in view menu"""
        self._select_view_menu()
        skeleton_view_menu = self.omni_driver.find_element(self._view_menu_waypoint)
        skeleton_view_menu.click(False)

    def find_camera_menu(self):
        """Finds the camera menu on screen"""
        camera_menu = self.omni_driver.find_element(self._camera_menu)
        return camera_menu

    def switch_resolution_in_view(self, res: str):
        """Switches resolution in view"""
        self.omni_driver.wait(3)
        self.find_and_click(self._view_resolution_menu)
        self.omni_driver.wait(3)
        self.omni_driver.select_context_menu_option(res)
        self.omni_driver.wait(3)
        self.log_info_with_screenshot(f"Selected resolution: {res}")

    def open_resolution_settings(self):
        """Opens resolution settings in view"""
        self.find_and_click(self._view_resolution_menu)
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Settings")
        self.log_info_with_screenshot("Resolution settings opened")

    def add_custom_resolution(self, res_name="4k", height="3000", width="4000"):
        """Adds a custom resolution with specified name, height, width"""
        self.find_and_enter_text(self._custom_resolution_alias, res_name)
        width_el = self.find_and_scroll_element_into_view(
            self._custom_resolution_width, ScrollAxis.X, ScrollAmount.CENTER
        )
        width_el.send_keys(width)
        height_el = self.find_and_scroll_element_into_view(
            self._custom_resolution_height, ScrollAxis.X, ScrollAmount.CENTER
        )
        height_el.send_keys(height)
        add_el = self.find_and_scroll_element_into_view(
            self._custom_resolution_add_btn, ScrollAxis.X, ScrollAmount.CENTER
        )
        add_el.click()
        self.omni_driver.wait(1)
        self.log_info_with_screenshot(f"Custom resolution: {res_name} is added")
        self.omni_driver.close_window("Preferences")

    def mark_resolutions_active(self, active: bool = True):
        """marks resolution inactive"""
        self.open_resolution_settings()
        elements = self.omni_driver.find_elements(self._custom_resolution_chkboxs)
        for el in elements:
            if active and el.is_checked() is False:
                el.click()
            elif not active and el.is_checked():
                el.click()

    def create_light(self, light="Disk Light"):
        """Creates a light at center of viewport"""
        viewport = self.omni_driver.find_element(self._viewport_element, True)
        viewport.right_click()
        self.omni_driver.select_context_menu_option(f"Create/Light/{light}", offset_x=5, offset_y=5)
        self.omni_driver.wait_for_stage_load()

    def open_close_res_menu(self):
        """Opens and closes resolution menu"""
        self.omni_driver.wait(2)
        self.find_and_click(self._resolution_label, False)
        self.omni_driver.wait(2)
        self.find_and_click(self._resolution_label, False)

    def get_viewport_resolution(self):
        """Gets viewport resolution

        Returns:
            List[int]: Return list with x & y components of resolution
        """
        resolution = self.omni_driver.get_viewport_info()["frame_info"]["resolution"]
        return resolution

    def click_share_btn(self):
        """Clicks on Share Button"""
        self.find_and_click(self._share_btn)

    def switch_to_view_camera_option(self, index: int, collections: bool = False):
        """Switches to Camera with given name

        Args:
        index(int): index of camera starting from 0
        Perspective: 0, Top:1, Front:2, Right:3
        CloseUp:0 , LongUSD Presenter:1 with collections = True

        """
        self.find_and_click(self._camera_menu)
        self.log_info_with_screenshot("Opened view camera menu")
        if collections:
            self.find_and_click(self._camera_collection, False)
            self.log_info_with_screenshot("switched to camera collection")
            self.find_and_click(self._camera_list.format(index), False)
        else:
            self.find_and_click(self._camera_types.format(index))
        self.omni_driver.wait(2)

    def _select_mesh_view_menu(self):
        """Clicks on mesh view menu"""
        mesh_view_menu = self.omni_driver.find_element(self._mesh_view_menu)
        mesh_view_menu.click(False)

    def toggle_mesh_view_menu_view(self, toggle: bool = True):
        """Toggles mesh_view_menu view menu option

        Args:
            toggle (bool, optional): Toggle to turn ON/OFF mesh_view_menu view. Defaults to True.
        """
        self._select_view_menu()
        self._select_show_by_type_menu()
        if toggle:
            if not self.omni_driver.find_element(self._mesh_view_menu).is_selected():
                self._select_mesh_view_menu()
        else:
            if self.omni_driver.find_element(self._mesh_view_menu).is_selected():
                self._select_mesh_view_menu()
        self.screenshot("mesh_options_enabled")
        self._select_view_menu()

    def reduce_camera_sensitivity(self):
        center = self.get_center()
        self.omni_driver.click_at_and_hold(center[0], center[1], right_click=True, hold_click=True)
        self.omni_driver.emulate_mouse_move(center[0] + 50, center[1] - 50)
        self.omni_driver.wait(3)
        for i in range(20):
            self.omni_driver.emulate_mouse_scroll("out", 500, 500)
            self.omni_driver.wait(1)
        self.omni_driver.emulate_mouse_move(center[0] - 50, center[1] + 50)
        self.omni_driver.click_at_and_hold(center[0], center[1], right_click=True, release_click=True)

    def follow_user(self, y):
        self.find_and_click(self._camera_menu)
        follow_user_submenu = self.find_and_click(self._camera_follow_user, False)
        center = follow_user_submenu.get_widget_center()
        self.omni_driver.click_at(center[0] + 100, center[1] + y)
        self.find_and_click(self._camera_menu)

    def create_waypoint_by_pin(self):
        self.find_and_click(self._waypoint_add_pin_btn)

    def open_waypoint_manager_by_pin(self):
        pin = self.omni_driver.find_element(self._waypoint_add_pin_btn)
        pin.right_click()

    def zoom_out(self):
        "Zooms out so that the current car position is observed on the viewport"
        # self.omni_driver.reset_viewport_camera()
        self.omni_driver.wait(2)
        self.omni_driver.zoom_viewport("Out", start=1, end=50)
        self.omni_driver.wait(2)

    def create_xform(self):
        """
        Creates a Xform
        """
        viewport = self.omni_driver.find_element(self._viewport_element)
        viewport.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Create/Xform", offset_x=5, offset_y=5)

    def is_nav_bar_tooltip_visible(self):
        """Returns whether navbar tooltip is visible"""
        try:
            self.omni_driver.find_element(self._navbar_tooltip, True)
            return True
        except ElementNotFound:
            return False

    def get_tooltip_text(self):
        """Returns tooltip text"""
        return self.omni_driver.find_element(self._navbar_tooltip_text, True).get_text()

    def get_tooltip_images(self):
        """Return Image elements of tooltip"""
        return self.omni_driver.find_elements(self._navbar_tool_tip_image)

    def toggle_tooltips_visibility(self):
        """Toggle tooltips visibility"""
        options = self.omni_driver.find_element(self._options_btn, True)
        options.right_click()
        self.omni_driver.select_context_menu_option("Toggle Tooltips")

    def _select_colliders_all_menu(self):
        """Clicks on All option from Colliders menu"""
        collider_all_menu = self.omni_driver.find_element(self._collider_all_menu)
        collider_all_menu.click(False)

    def _select_physics_menu(self):
        """Clicks on Physics menu"""
        physics_menu = self.omni_driver.find_element(self._physics_menu)
        physics_menu.click(False)

    def _select_colliders_menu(self):
        """Clicks on Colliders menu"""
        colliders_menu = self.omni_driver.find_element(self._colliders_menu)
        colliders_menu.click(False)

    def toggle_all_in_colliders(self, toggle: bool = True):
        """Toggles All option under Colliders

        Args:
            toggle (bool, optional): Toggle to turn ON/OFF All in colliders. Defaults to True.
        """
        self._select_view_menu()
        self._select_show_by_type_menu()
        self._select_physics_menu()
        self._select_colliders_menu()
        if toggle:
            if not self.omni_driver.find_element(self._collider_all_menu).is_selected():
                self._select_colliders_all_menu()
        self.screenshot("Collider_enabled")
        self._select_view_menu()

    def _select_lights_view_menu(self):
        """Clicks on skeleton view menu"""
        skeleton_view_menu = self.omni_driver.find_element(self._lights_view_menu)
        skeleton_view_menu.click(False)

    def toggle_view_menu_lights(self, enable=True):
        """Toggle Lights visibility in viewport

        Returns: whether lights menu is enabled or disabled
        """
        self._select_view_menu()
        self._select_show_by_type_menu()
        current_state = self.omni_driver.find_element(self._lights_view_menu).is_checked()
        if enable != current_state:
            self.log.info("Toggling lights menu option")
            self._select_lights_view_menu()
            self.screenshot("lights_menu_toggled")
            self._select_view_menu()
            current_state = self.omni_driver.find_element(self._lights_view_menu).is_checked()
        else:
            self.log.error("Menu Option is already set")
        return current_state

    def play_animation(self):
        """Method to click on play button"""
        play = self.omni_driver.find_element(self.play_button, True)
        x = play.get_size_and_position("screen_position_x")
        y = play.get_size_and_position("screen_position_y")
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.wait(2)
        play.click()

    def is_animation_playing(self):
        """Returns whether animation is playing"""
        play_btn = self.omni_driver.find_element(self.play_button, True)
        return play_btn.is_enabled() and play_btn.tool_button_is_checked()

    def get_play_timestamp(self):
        """Returns the timestamp of animation played"""
        return self.omni_driver.find_element(self._play_int_slider, True).get_int_value()

    def is_arrow_enabled(self):
        """True if arrow button is enabled, False otherwise"""
        arrow = self.omni_driver.find_element(self.play_button, True)
        return arrow.is_enabled()

    def slide(self, element, val):
        el = self.omni_driver.find_element(element, True)
        center = el.get_widget_center()
        el.drag_and_drop(val, center[1])
        self.omni_driver.wait(2)

    def change_camera_speed(self, speed: str):
        """Modifies the camera speed
        speed: slow/average/fast
        """
        speed_type = {"slow": 125, "average": 160, "fast": 210}
        self.find_and_click(self._camera_menu)
        self.slide(self._camera_speed, speed_type[speed])
        # camera_speed = self.omni_driver.find_element(self._camera_speed, True)
        # center = camera_speed.get_widget_center()
        # camera_speed.drag_and_drop(type[speed], center[1])
        # self.omni_driver.wait(2)

    def select_lens(self, lens: str):
        camera_lens = self.omni_driver.find_element(self._camera_options_lens)
        camera_lens.click()
        camera_lens.select_item_from_combo_box_delegate(None, lens)

    def zoom_camera(self, val: int):
        zoom_cam = self.omni_driver.find_element(self._view_camera_options_zoom)
        zoom_cam.send_keys(val)
        self.omni_driver.wait(2)

    def enable_ae(self):
        ae = self.omni_driver.find_element(self._camera_options_ae, True)
        self.omni_driver.wait(1)
        center = ae.get_widget_center()
        self.log.info("Center:", center[0], center[1])
        self.omni_driver.click_at(center[0] + 6, center[1])
        self.omni_driver.wait(1)

    def change_camera_ae(self, val: int):
        self.slide(self._camera_options_ae_slider, val)
        self.omni_driver.wait(2)

    def change_camera_fstop(self, val: int):
        """Changes camera fstop"""
        fstop = self.omni_driver.find_element(self._camera_options_camera_f_stop)
        self.clear_textbox(fstop)
        fstop.send_keys(val)
        self.omni_driver.wait(2)
        self.log.info(f"Changed fstop to {val}")

    def change_camera_iso(self, val: int):
        """Changes camera iso"""
        iso = self.omni_driver.find_element(self._camera_options_iso)
        self.clear_textbox(iso)
        iso.send_keys(val)
        self.log.info(f"Changed iso to {val}")

    def set_context_menu_option(self, context_menu_option):
        """Set context_menu_option of selected item"""
        viewport = self.omni_driver.find_element(self._viewport_element)
        viewport.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option(context_menu_option)

    def is_nav_height_locked(self):
        """Returns whether nav height is locked/unlocked"""
        try:
            return self.omni_driver.find_element(self._nav_height.format("Locked"), True)
        except ElementNotFound:
            return False

    def open_sun_study_location(self):
        """Left clicks Location icon in Tool Bar"""
        self.find_and_click(self._location_btn)
        self.omni_driver.wait(1)

    # check line 1500
    def change_location(self, name=""):
        """selects value from location dropdown"""
        location_dropdown = self.omni_driver.find_element(self._location_dropdown)
        location_dropdown.select_item_from_combo_box(name=name)
        self.omni_driver.wait(1)

    def get_location_coordinates(self):
        """Retrieves location coordinates"""
        longitude = self.omni_driver.find_element(self._longitude, True).get_float_value()
        latitude = self.omni_driver.find_element(self._latitude, True).get_float_value()
        north_orientation = self.omni_driver.find_element(self._north_orientation, True).get_float_value()

        return longitude, latitude, north_orientation

    def get_location(self):
        """Retrieves current location from location modal"""
        location_dropdown = self.omni_driver.find_element(self._location_dropdown)
        return location_dropdown.get_combobox_info()["current_value"]

    def close_sun_study_location(self):
        """Left clicks Close Button in Location modal"""
        self.find_and_click(self._close_btn)
        self.omni_driver.wait(1)

    def open_sun_study(self):
        """Left clicks Sun icon in Tool Bar"""
        self.find_and_click(self._sun_study_btn)
        self.omni_driver.wait(1)

    @staticmethod
    def set_toggle_arrow(current, desired, up_el, down_el):
        """sets the value with toggle arrow
        :param current: current value of attribute
        :param desired: value to be set
        :param up_el: toggle up arrow element
        :param down_el: toggle down arrow element
        """
        flag = True
        while flag:
            if current < desired:
                up_el.click()
                current += 1
            else:
                down_el.click()
                current -= 1
            if current == desired:
                flag = False

    def set_date_time(
        self,
        date: str = None,
        month: int = None,
        year: int = None,
        hour: int = None,
        minute: int = None,
        meridian: str = None,
    ):
        """sets date time in sun study datetime modal
        param: date: takes value from 1 to 31 in str format
        param: month: indexing starts from 0, 0-11
        param: year: indexing starts from 0, value in dropdown starts from 2000
        param: meridian: 'AM' or 'PM'
        """
        curr_date_time = self.get_sun_study_date_time()
        match = re.search(r"(\d{2}):(\d{2}) ([APM]{2})", curr_date_time)
        curr_hour, curr_min, curr_meridian = (
            int(match.group(1)),
            int(match.group(2)),
            match.group(3),
        )

        self.find_and_click(self._date_time)
        self.omni_driver.wait(1)

        if date:
            self.find_and_click(self._date.replace("_date_", date), bring_to_front=False)
        if month:
            self.omni_driver.find_element(self._month).select_item_from_combo_box(month, None, False)
        if year:
            self.omni_driver.find_element(self._year).select_item_from_combo_box(year, None, False)

        if hour and curr_hour != hour:
            arrow_up = self.omni_driver.find_element(self._hour_up)
            arrow_down = self.omni_driver.find_element(self._hour_down)
            self.set_toggle_arrow(curr_hour, hour, arrow_up, arrow_down)

        if minute and curr_min != minute:
            arrow_up = self.omni_driver.find_element(self._minute_up)
            arrow_down = self.omni_driver.find_element(self._minute_down)
            self.set_toggle_arrow(curr_min, minute, arrow_up, arrow_down)

        if meridian and curr_meridian != meridian:
            self.find_and_click(self._meridian_arrow)

        self.find_and_click(self._apply_btn)
        self.omni_driver.wait(5)

    def set_time_using_slider(self, x_pos: int = None):
        """sets time in sun study using slider
        for eg: 6am: x_pos = 546
                4pm: x_pos = 875
                6pm: x_pos = 940
        """
        self.slide(self._circle_slider, x_pos)

    def get_sun_study_date_time(self):
        date_time = self.omni_driver.find_element(self._date_time)
        return date_time.get_text()

    def close_sun_study(self):
        self.omni_driver.close_window("Sun Study")

    def open_playlist(self):
        """Left clicks playlist icon in Tool Bar"""
        self.find_and_click(self._playlist_btn)
        self.omni_driver.wait(1)

    def set_transition_time(self, time: int):
        """sets transition time(in secs) in playlist"""
        transition_time = self.omni_driver.find_element(self._transition_time)
        transition_time.send_keys(time)

    def set_time_per_item(self, time: int):
        """sets time per item (in secs) in playlist"""
        time_per_item = self.omni_driver.find_element(self._time_per_item)
        time_per_item.send_keys(time)

    def get_custom_window(self, substr: str):
        """Retrieves custom window based on substring"""
        windows = self.omni_driver.get_windows()["visible_windows"]
        window = [window for window in windows if substr in window][0]
        return window

    def set_transition_type(self, type: str):
        """sets transition type in playlist
        :param type:str Cut/Smooth
        """
        self.find_and_click(self._transition_type)
        window = self.get_custom_window("CustomWidgetMenu")
        if window and type.lower() == "cut":
            self.find_and_click(self._cut_transition.format(window))
        elif window and type.lower() == "smooth":
            self.find_and_click(self._smooth_transition.format(window))

    def play(self):
        """plays the camera in playlist"""
        self.find_and_click(self._playlist_play_btn)

    def select_visible_viewport(self):
        """Get center of viewport

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        viewport = self.omni_driver.find_element(self._viewport_element)
        viewport_hamburger = self.omni_driver.find_element(self._viewport_hamburger)
        offset = (
            viewport_hamburger.get_size_and_position("screen_position_y")
            + viewport_hamburger.get_size_and_position("computed_height")
            + 1
        )
        start_pos_x = viewport.get_size_and_position("screen_position_x") + offset
        start_pos_y = viewport.get_size_and_position("screen_position_y") + offset
        end_pos_x = start_pos_x + viewport.get_size_and_position("computed_width") - offset
        end_pos_y = start_pos_y + viewport.get_size_and_position("computed_height") - offset
        self.omni_driver.click_at_and_hold(start_pos_x, start_pos_y, hold_click=True)
        self.omni_driver.emulate_mouse_move(end_pos_x, end_pos_y)
        self.omni_driver.wait(1)
        self.omni_driver.click_at(end_pos_x, end_pos_y)

    def get_viewport_tooltip(self):
        """Get viewport tooltip"""
        return self.omni_driver.find_element(self._viewport_tooltip, True)

    def toggle_turntable(self, enable=True):
        """Toggles turntable tool

        Args:
        enable(bool): Bool value to enable turntable tool"""
        element = self.omni_driver.find_element(self._turntable_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_turntable_tool_mode")
        self.log.info("Turntable is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching turntable tool")
            element.click()
        self.screenshot("current_turntable_tool_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle turntable tool mode"

    def select_playlist(self, index: int):
        """Selects playlist from available list of playlist

        :params: index: starts from 0
        """
        self.find_and_click(self._playlist_dropdown)
        window = self.get_custom_window("CustomWidgetMenu")
        playlists = self.omni_driver.find_elements(self._playlist_dropdown_options.format(window))
        playlists[index].click()

    def get_available_playlists(self):
        """Retrieves available list of playlist

        Returns: list
        """
        self.find_and_click(self._playlist_dropdown)
        window = self.get_custom_window("CustomWidgetMenu")
        playlists = self.omni_driver.find_elements(self._playlist_dropdown_options.format(window))
        return [playlist.get_text() for playlist in playlists]

    def create_new_playlist(self, playlist_name: str):
        """Creates a new playlist

        :param: playlist_name: name of the playlist
        """
        self.find_and_click(self._playlist_settings)
        self.omni_driver.select_context_menu_option("Create New Playlist")
        window = self.get_custom_window("DIALOG")
        textbox = self.omni_driver.find_element(self._new_playlist.format(window))
        textbox.send_keys(playlist_name)
        self.find_and_click(self._new_playlist_ok_btn.format(window))

    def rename_playlist(self, playlist: int = None, name: str = None):
        """Renames selected playlist

        :param: playlist: index of playlist to be renamed/ by default current playlist
                name: name of the playlist
        """
        if playlist:
            self.select_playlist(playlist)
            self.omni_driver.wait(1)
        self.find_and_click(self._playlist_settings)
        self.omni_driver.select_context_menu_option("Rename Playlist")
        window = self.get_custom_window("DIALOG")
        textbox = self.omni_driver.find_element(self._rename_playlist.format(window))
        textbox.send_keys(name)
        self.find_and_click(self._rename_playlist_ok_btn.format(window))

    def duplicate_playlist(self, playlist: int = None, name: str = None):
        """Duplicates selected playlist

        :param: playlist: index of playlist to be duplicated/ by default current playlist
                name: name of the playlist
        """
        if playlist:
            self.select_playlist(playlist)
            self.omni_driver.wait(1)
        self.find_and_click(self._playlist_settings)
        self.omni_driver.select_context_menu_option("Duplicate Playlist")
        window = self.get_custom_window("DIALOG")
        if name:
            textbox = self.omni_driver.find_element(self._new_playlist.format(window))
            textbox.send_keys(name)
        self.find_and_click(self._new_playlist_ok_btn.format(window))

    def delete_playlist(self, playlist: int = None):
        """Deletes selected playlist
        :param: playlist: index of playlist to be deleted/ by default current playlist
        """
        if playlist:
            self.select_playlist(playlist)
            self.omni_driver.wait(1)
        self.find_and_click(self._playlist_settings)
        self.omni_driver.select_context_menu_option("Delete Current Playlist")

    def toggle_measure_tool(self, enable=True):
        """Toggles Teleport Mode

        Args:
        enable(bool): Bool value to enable teleport Mode"""
        element = self.omni_driver.find_element(self._measure_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_teleport_mode")
        self.log.info("teleport Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching teleport mode")
            element.click()
        self.screenshot("current_teleport_mode")
        assert enable == element.tool_button_is_checked(), "Failed to toggle teleport mode"

    def is_measure_tool_visible(self) -> bool:
        """Gets the visibility of the measure window
        Retuns:
            bool
        """
        return self._measure_window in self.omni_driver.get_windows()["visible_windows"]

    def is_section_tool_visible(self) -> bool:
        """Gets the visibility of the section window
        Retuns:
            bool
        """
        return self._section_window in self.omni_driver.get_windows()["visible_windows"]

    def get_screenshot_preferences(self, offset_y=0):
        """Returns Screenshot Directory"""
        capture = self.omni_driver.find_element(self._capture_btn)
        capture.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Screenshot Settings", offset_y=offset_y)
        self.omni_driver.wait(2)

    def toggle_navbar_visibility_mode(self):
        """Toggles NavBar Visibility Mode in Viewport"""
        self.find_and_click(self._navbar_btn, refresh=True)

    def toggle_section_tool(self, enable=True):
        """Toggles Section Tool

        Args:
        enable(bool): Bool value to enable section tool"""
        element = self.omni_driver.find_element(self._section_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("before_toggling_section_tool")
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching Section Tool")
            element.click()
        self.screenshot("after_toggling_section_tool")
        assert enable == element.tool_button_is_checked(), "Failed to toggle section tool"

    def toggle_timeline_bar(self, enable=True):
        """Toggles Timeline Mode

        Args:
        enable(bool): Bool value to enable timeline Mode"""
        element = self.omni_driver.find_element(self._timeline_btn, refresh=True)
        current_state = element.tool_button_is_checked()
        self.screenshot("previous_timeline_mode")
        self.log.info("Timeline Mode is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching timeline mode")
            element.click()
        self.screenshot("current_timeline_mode")
        # assert enable == element.tool_button_is_checked(), "Failed to toggle timeline bar"

    def is_timeline_visible(self) -> bool:
        """Gets timeline minibar visibility

        Returns:
            bool
        """
        try:
            element = self.omni_driver.find_element(self._timeline_btn, refresh=True)
            return element.tool_button_is_checked()
        except:
            return False

    def viewport_menu_bar_status(self):
        """Return true or false According to viewport menu bar visibility"""
        if not self.omni_driver.find_element(self._viewport_menu, True):
            return False

        return True

    def is_teleport_tool_active(self):
        """Returns whether teleport tool is active"""
        return self.omni_driver.find_element(self._teleport_btn, refresh=True).tool_button_is_checked()

    def is_orbit_tool_active(self):
        """Returns whether orbit tool is active"""
        return self.omni_driver.find_element(self._orbit_btn, refresh=True).tool_button_is_checked()

    def cancel_warning(self):
            """ Cancels the warning dialog """
            self.find_and_click(self._warning_no_btn)

    def bind_material_to_viewport_asset(self,asset_name: str,drop_down_index: int,material_name:str):
        """Assigns material to viewport asset

        Args:
            asset_name (str): viewport asset
            drop_down_index (int): value to be assigned Stronger/Weaker (0/1) than Descendants
            material_name (str): material name that needs to be assigned
        """

        asset_coords =  self.omni_driver.get_prim_screen_coordinates(f"/World/{asset_name}")
        self.log.info(f"Prim coordinates {asset_coords}")
        self.omni_driver.wait(2)
        self.omni_driver.click_at(asset_coords["x"],asset_coords["y"], right=True)
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Assign Material", offset_x=5, offset_y=5)
        self.find_and_click(self._bind_material_search_drop_down_btn.replace("__name__", asset_name),refresh=True)
        self.omni_driver.wait(2)

        self.find_and_enter_text(self._material_pop_window_string_field, material_name)
        material = self.wait.element_to_be_located(
            self.omni_driver,
            self._searched_material_label.replace("__name__", material_name),
        )
        material.click()
        combo_box: OmniElement = self.omni_driver.find_element(self._bind_material_combo_box.replace("__name__", asset_name))
        combo_box.select_item_from_combo_box(index=drop_down_index, name="", stack_combo=True)
        ok_btn = self.omni_driver.find_element(self._bind_material_ok_btn.replace("__name__", asset_name))
        self.omni_driver.wait(2)
        ok_btn.click()
        self.omni_driver.screenshot(f"added_material_to_{asset_name}")

    def is_text_present_in_viewport(self, text: str) -> bool:
        """Returns whether the text is present in the Viewport Window

        Args:
            text (str): text to search

        Returns:
            bool: True if text is present, else False
        """
        try:
            self.omni_driver.find_element(self._generic_label.format(text), refresh=True)
            self.log_info_with_screenshot(f"Text '{text}' is present in viewport.", "text_in_viewport")
            return True
        except ElementNotFound:
            self.log_info_with_screenshot(f"Text '{text}' is not present in viewport.", "text_in_viewport")
            return False
