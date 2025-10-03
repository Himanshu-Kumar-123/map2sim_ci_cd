# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Stage class
   This module contains the base methods for Stage window
"""

import os
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from pynput.keyboard import Key, Controller
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.constants import KeyboardConstants
from typing import List


class BaseStageModel(BaseModel):
    """Base model class for Stage window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Stage window
    _window_name = "Stage"
    _stage_window = "Stage//Frame/Frame[*]/VStack[0]"
    _light_dropdown = "Stage//Frame/Frame[*]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[5]"
    _light_type = "Stage//Frame/**/Label[*].text=='__light__'"
    _asset_path = "Stage//Frame/**/TreeView[0]/**/Label[*].text=='__name__'"
    _asset_path_search_results = (
        "Stage//Frame/**/TreeView[1]/**/Label[*].text=='__name__'"
    )
    _asset_search_result_labels = "Stage//Frame/**/TreeView[1]/**/Label[*]"
    _stage_label = "Stage//Frame/**/TreeView[0]/HStack[6]/**/Label[0]"
    _stage_search = "Drivesim Scenario Outliner//Frame/VStack[0]/**/ZStack[1]/HStack[0]/Search"
    _stage_sort_order = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[0]"
    _stage_sort_label = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[0]/HStack[0]/HStack[0]/Label[0]"
    _stage_visibility = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[1]/HStack[0]/VStack[0]/Image[0]"
    _stage_type = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[2]/HStack[0]/Label[0]"
    __world_default_prim = (
        "Stage//Frame/**/TreeView[0]/**/Label[*].text=='World (defaultPrim)'"
    )
    _looks_expand = "Stage//Frame/**/TreeView[0]/HStack[1]"
    _all_images = "Stage//Frame/**/TreeView[0]/HStack[*]/Image[0]"
    _expand_environment = (
        "Stage//Frame/**/ScrollingFrame[0]/**/TreeView[0]/**/HStack[1]"
    )
    _main_treeview = "Stage//Frame/**/TreeView[0]"
    _options_btn = "Stage//Frame/**/Button[0].name == 'options'"

    # SRS App locators
    _master_light_switch_label = "Stage//Frame/**/Label[0].text=='master_light_switch'"
    # _open_tree_structure = "Stage//Frame/Frame[0]/**/TreeView[0]/HStack[23]/Spacer[1]"
    _open_tree_structure = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/HStack[10]"
    _luxIntensityRamp_label = "Stage//Frame/**/Label[0].text=='LuxIntensityRamp'"
    _colorRamp_label = "Stage//Frame/**/Label[0].text=='colorRamp'"

    #  TODO - Added this to verify scene is actually loaded
    _stage_tree_view_frame = "Stage//Frame/**/TreeView[0]/Frame[*]"

    _stage_settings_menu = "Stage//Frame/Frame[0]/**/settings_icon"

    #variant related locators
    _variant_selection_combo_box = "Stage//Frame/**/ComboBox[0]"
    _variant_header = "Stage//Frame/Frame[0]/**/Label[0].name=='variant_header'"
    _variant_label = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[3]/HStack[0]/Label[0]"

    #payload related locators
    _payload_header= "Stage//Frame/Frame[0]/**/Label[0].name=='payload_header'"
    _payload_label = "Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/ZStack[4]/HStack[0]/Label[0]"
    
    #material graph
    _material_graph = "Stage//Frame/**/TreeView[1]/**/Label[*].text=='__name__'"

    def navigate_to_stage(self):
        """Navigates to stage window"""
        stage_window = self.omni_driver.find_element(self._stage_window)
        stage_window.click()
        self.screenshot("navigated_to_stage")

    def select_hamburger_menu_option(self, setting: str):
        """
        Selects option from setting menu
        """
        menu_path = setting.split("/")
        menu = self.omni_driver.find_element(self._stage_settings_menu,True)
        menu.click()
        self.omni_driver.wait(2)
        if len(menu_path) > 0:
            self.omni_driver.select_context_menu_option(menu_path[0])
        if len(menu_path) > 1:
            for i in range(1,len(menu_path)): 
                setting_label = "**/Label[*].text=='" + menu_path[i] +"'"
                option = self.omni_driver.find_context_menu_elements(menu_path[i-1],setting_label)
                if option:
                    option[0].click(False)

    def select_light(self, light: str):
        """Selects specific light from stage

        Args:
            light (str): type of light to select
        """
        light_type = self._light_type.replace("__light__", light)
        light = self.omni_driver.find_element(light_type, True)
        light.click()

    def assert_item_exits(self, name: str, search: bool = False):
        """Asserts if a specified item exists in stage

        Args:
            name (str): Asset name
        """
        if search:
            assert self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name)
            ), f"Asset not present in stage Expected: '{name}'"
        else:
            assert self.omni_driver.find_element(
                self._asset_path.replace("__name__", name)
            ), f"Asset not present in stage Expected: '{name}'"
        self.log.info(f"Asset {name} is present in stage")

    def get_stage_label(self):
        element = self.omni_driver.find_element(self._stage_label, refresh=True)
        return element.get_text()

    def select_all_assets(self):
        """Selects all assets in stage"""
        self.find_and_click(self.__world_default_prim)

    def select_asset(self, name: str, search: bool = False):
        """Selects  assets in stage

        Args:
            name (str): Name of asset
            search (bool): True if the asset is to be searched

        Returns:
            OmniElement: Reference of asset item
        """
        if search:
            asset: OmniElement = self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name), True
            )

        else:
            asset: OmniElement = self.omni_driver.find_element(
                self._asset_path.replace("__name__", name), True
            )
        attempts = 0
        while not asset.is_selected():
            if attempts >= 3:
                break
            self.log.info(f"Attempting to select asset: {name}")
            asset.click()
            self.omni_driver.wait(1)
            attempts += 1
        assert asset.is_selected(), f"Failed to select asset: '{name}'"
        return asset

    def search_asset(self, asset_name):
        """Search assets in stage
        Args:
            asset_name (str): Name of asset
        """
        self.find_and_enter_text(self._stage_search, asset_name)
        self.wait.element_to_be_located(
            self.omni_driver,
            locator=self._asset_path_search_results.replace("__name__", asset_name),
        )

    def search_and_select_asset(self, asset_name):
        """Searchs and Selects asset in stage
        Args:
            asset_name (str): Name of asset
        """
        self.search_asset(asset_name)
        self.omni_driver.wait(3)
        return self.select_asset(asset_name, search=True)

    def select_multiple_assets(self, names: []) -> List[OmniElement]:
        """Selects  assets in stage

        Args:
            names list(str): List of Names of asset
        Returns:
            OmniElement: List of Reference of asset item
        """

        assets: List[OmniElement] = []
        keyboard = Controller()
        with keyboard.pressed(Key.ctrl.value):
            for name in names:
                asset = self.omni_driver.find_element(
                    self._asset_path.replace("__name__", name), refresh=True
                )
                asset.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retries = 4
                while not asset.is_selected():
                    if retries == 0:
                        break
                    self.log.info(f"Attempting to select asset: {name}")
                    asset.click()
                    self.omni_driver.wait(1)
                    retries -= 1
                assets.append(asset)
        # TODO: replace above code with following code when key_press API can handle this logic
        # self.omni_driver.key_press(KeyboardConstants.left_control, hold_button=True)
        # for name in names:
        #     asset = self.omni_driver.find_element(self._asset_path.replace("__name__", name), refresh=True)
        #     asset.click()
        #     assets.append(asset)
        # self.omni_driver.key_press(KeyboardConstants.left_control, release_button=True)
        self.log_info_with_screenshot(
            f"Selected {assets} assets.", "selected_multiple_assets"
        )
        return assets

    def select_context_option(self, name: str, menupath: str, search: bool = False):
        """Selects a context option for a specific asset in stage

        Args:
            name (str): Name of asset
            menupath (str): Menu path for navigation
        """
        asset = self.select_asset(name, search=search)
        self.omni_driver.wait(2)
        asset.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(menupath)

    def get_position(self, name: str, search: bool = False):
        """Get centre position of asset

        Args:
            name (str): Name of asset

        Returns:
            _type_: Position of Asset
        """
        if search:
            asset = self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name)
            )
        else:
            asset = self.omni_driver.find_element(
                self._asset_path.replace("__name__", name)
            )
        return asset.get_widget_center()

    def assert_item_not_exits(self, name: str, search: bool = False):
        """Asserts if a specified item does not exists in stage

        Args:
            name (str): Asset name
        """

        try:
            if search:
                self.omni_driver.find_element(
                    self._asset_path_search_results.replace("__name__", name),
                    refresh=True,
                )
            else:
                self.omni_driver.find_element(
                    self._asset_path.replace("__name__", name), refresh=True
                )

            self.log.info(f"Asset {name} is present in stage")
            assert False, f"Asset {name} is present in stage"

        except ElementNotFound:
            self.log.info(f"Asset {name} is not present in stage")
            assert True, f"Asset {name} is not present in stage"

    def assert_material_added(self, name: str, search: bool = False):
        """Assert whether material is added to stage

        Args:
            name (str): Name of material
        """
        looks_folder = self.omni_driver.find_element(self._looks_expand)
        looks_folder.click()
        self.omni_driver.wait_frames(5)
        if search:
            assert self.omni_driver.find_element(
                self._asset_path_search_results.replace("__name__", name)
            ), "Material not added to stage"
        else:
            assert self.omni_driver.find_element(
                self._asset_path.replace("__name__", name)
            ), "Material not added to stage"
        self.screenshot("material_added_to_stage")

    def verify_scene_loaded(self):
        """Verifies whether scene is actuall opened by validating the change in UI for Stage Treeview"""
        frames = self.omni_driver.get_stage()
        if len(frames) > 6:  # 6 is default number of frame widgets on a new stage
            self.log.info("Scene opened and stage loaded.")
        else:
            self.screenshot("scene_load_failed")
            self.log.info("Scene did not open, please verify screenshot")
            assert False, "Scene did not open, please verify screenshot"

    def validate_tile_mesh(self, tile_name: str):
        self.navigate_to_stage()
        self.assert_item_exits("World (defaultPrim)")
        self.search_asset("/World/Geospatial")
        self.search_asset("/World/Geospatial/Map_tiles")
        self.search_asset(f"/World/Geospatial/Map_tiles/{tile_name}")
        self.search_asset(f"/World/Geospatial/Map_tiles/{tile_name}/Looks")

    def rename_asset(self, asset_ref: OmniElement, rename_to: str):
        """Renames asset in Stage

        Args:
        asset_ref(OmniElement): Element Referring to the asset
        rename_to(str): new name
        """
        asset_ref.right_click()
        self.omni_driver.wait(10)
        self.omni_driver.select_context_menu_option("Rename")
        self.omni_driver.wait(5)
        self.omni_driver.emulate_char_press(rename_to)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)
        self.omni_driver.wait(2)

    def expand_environment(self):
        """Expands environment Tree"""
        expand_env_element = self.omni_driver.find_element(self._expand_environment)
        expand_env_element.click()
        self.screenshot("expand_environment_clicked")

    def get_labels_under_tree(self, main_tree_label: str):
        """Get all labels under Tree

        Args:
        main_tree_label(str): Main Label name to get labels under it
        """
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
          
        get_label_elements = main_treeview_elements.find_elements("**/Label[0]")
        all_labels = [
            current_element.get_text()
            for current_element in get_label_elements
            if current_element.is_visible()
        ]

        env_index = all_labels.index(main_tree_label)
        labels_under_env = all_labels[env_index + 2 :][::2]
        return labels_under_env

    def get_subtree_under_label(self, main_tree_label: str):
        """
        Get subtree under labels
        get_labels_under_tree() call returns all tree elements starting from the current label, also returns siblings and child elements of siblings
        This method will give elements under current label only, in sorted format as per UI

        Args:
        main_tree_label(str): Main Label name to get labels under it
        """
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
          
        get_label_elements = main_treeview_elements.find_elements("**/Label[0]")
        all_labels = [
            current_element.get_text()
            for current_element in get_label_elements
            if current_element.is_visible()
        ]

        env_index = all_labels.index(main_tree_label)
        labels_under_env = all_labels[env_index + 2 :][::2]

        all_stage_elems = []
        all_stage_prims = self.omni_driver.get_stage()
        for prim in all_stage_prims:
            prim_path = prim.lstrip("Usd.Prim(<").rstrip(">)")
            all_stage_elems.append(prim_path)

        sub_tree = []
        for lbl in labels_under_env:
            for stg in all_stage_elems:
                if lbl in stg:
                    tokens =  stg.split("/")
                    if tokens[len(tokens)-1] == lbl and tokens[len(tokens)-2] == main_tree_label:  
                        sub_tree.append(lbl)

        return sub_tree

    def toggle_label_visibility(self, label, enable=True):
        """Toggles Visibility of Label

        Args:
        enable(bool): Bool value to enable Visibility of Label
        """
        visibility_element = self._get_visibility_element_of_label(label)
        current_state = not visibility_element.is_selected()
        self.log.info(f"{label} is enabled: {current_state}")
        if (enable and not current_state) or (not enable and current_state):
            self.log.info(f"Switching {label}")
            visibility_element.click()

    def fetch_label_visibility(self, label):
        """Fetches Visibility of Label"""
        visibility_element = self._get_visibility_element_of_label(label)
        current_state = not visibility_element.tool_button_is_checked()
        self.log.info(f"{label} is enabled: {current_state}")
        return current_state

    def _get_visibility_element_of_label(self, label):
        """Generates locator of visibility from label"""
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
        label_element = main_treeview_elements.find_element(
            f"**/Label[0].text=='{label}'"
        )
        label_parent_path = label_element.find_parent_element_path().split("/")[:-2]
        node_num_start = label_parent_path[-2].find("[") + 1
        node_num_end = label_parent_path[-2].find("]")
        label_visibility_node_num = int(label_parent_path[-2][node_num_start:node_num_end]) + 1
        label_visibility_node_name = (
            label_parent_path[-2][:node_num_start]
            + str(label_visibility_node_num)
            + label_parent_path[-2][node_num_end:]
        )
        label_parent_path[-2] = label_visibility_node_name
        visibility_path = "/".join(label_parent_path)
        visibility_parent_element = self.omni_driver.find_element(
            visibility_path, refresh=True
        )
        visibility_child_element: OmniElement = visibility_parent_element.find_element("ToolButton[0]", refresh=True)
        return visibility_child_element

    def fetch_label_type(self, label):
        """Fetches type of object (XForm/Mesh) from Stage using Label

        Args:
        label (str) : Label to find its type in Stage

        Returns:
        Type of object (XForm/Mesh/etc.)"""
        type_element = self._get_type_element_of_label(label)
        label_type = type_element.get_text().strip()
        self.log.info(f"{label} is of Type: {label_type}")
        return label_type

    def _get_type_element_of_label(self, label):
        """Generates locator to fetch type using label

        Args:
        label (str) : Label to find its type in Stage

        Returns:
        Locator where Type is stored for the label"""
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
        label_element = main_treeview_elements.find_element(
            f"**/Label[0].text=='{label}'"
        )
        label_parent_path = label_element.find_parent_element_path().split("/")[:-3]
        node_num_start = label_parent_path[-1].find("[") + 1
        node_num_end = label_parent_path[-1].find("]")
        label_type_node_num = (
            int(label_parent_path[-1][node_num_start:node_num_end]) + 2
        )
        label_type_node_name = (
            label_parent_path[-1][:node_num_start]
            + str(label_type_node_num)
            + label_parent_path[-1][node_num_end:]
        )
        label_parent_path[-1] = label_type_node_name
        label_type_path = "/".join(label_parent_path)
        label_parent_element = self.omni_driver.find_element(
            label_type_path, refresh=True
        )
        label_child_element = label_parent_element.find_element("**/Label[0]")
        return label_child_element

    def fetch_label_selected(self, label):
        """Fetches Selected Property of Label"""
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
        label_element = main_treeview_elements.find_element(
            f"**/Label[0].text=='{label}'"
        )
        current_state = label_element.is_selected()
        self.log.info(f"{label} is selected: {current_state}")
        return current_state

    def select_lux_ramp(self):
        """selects the lux ramp and selects the lights as required"""
        self.omni_driver.wait(3)
        self.find_and_click(self._luxIntensityRamp_label)
        self.omni_driver.wait(3)

    def select_colour_ramp(self):
        """selects the lux ramp and selects the lights as required"""
        self.omni_driver.wait(3)
        self.find_and_click(self._colorRamp_label)
        self.omni_driver.wait(3)

    def create_and_select_master_light_switch_label(self):
        """creates master lights switch from Menu bar"""
        self._create_master_light()
        self.omni_driver.wait_frames(5)
        self.find_and_click(self._master_light_switch_label)
        self.omni_driver.wait(3)

    def _create_master_light(self):
        self.omni_driver.select_menu_option(
            "Create/SRS Light Behavior/Master Light Switch"
        )

    def open_tree_structure(self):
        self.find_and_click(self._open_tree_structure)
        self.omni_driver.wait(2)

    def clear_search_result(self):
        """Clears Search Result text box"""
        search_box = self.omni_driver.find_element(self._stage_search, True)
        self.clear_textbox(search_box)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def get_search_result_assets(self, query: str):
        """Gets the Assets in the Search Result

        Args:
        query(str): Search Query for Assets
        """
        self.find_and_enter_text(self._stage_search, query)
        self.omni_driver.wait(1)
        labels = self.omni_driver.find_elements(self._asset_search_result_labels)
        return labels

    def wait_for_asset_to_be_added(self, asset_name: str):
        """Waits for asset to be added to stage

        Args:
        asset_name(str): Name of asset
        """
        self.wait.element_to_be_located(
            self.omni_driver, locator=self._asset_path.replace("__name__", asset_name)
        )

    def get_center(self):
        """Get center of Stage window

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        stage = self.omni_driver.find_element(self._stage_window)
        return stage.get_widget_center()

    def search_and_delete_asset(self, asset_name: str):
        """Search for a specified item in stage and delete it

        Args:
            name (str): Asset name
        """
        asset = self.search_and_select_asset(asset_name)
        asset.right_click()
        self.omni_driver.wait(5)
        self.omni_driver.select_context_menu_option("Delete")
        self.omni_driver.wait(2)
        self.clear_search_result()
        self.omni_driver.wait(2)
        self.assert_item_not_exits(asset_name)

    def expand_treeview(self, tree_path):
        """
        Expands the treeview as per the given path separated by '>'.
        """
        tree_item = tree_path.split(">")
        for item in tree_item:
            item = item.strip()
            self.log.info(f"Expanding {item} on tree view")
            self.toggle_tree_item(item, expand=True)
        self.log.info("Expansion of the treeview is completed")

    def toggle_tree_item(self, label, expand=True):
        """
        toggles the tree item to expand or collapse
        """
        self.log.info(f"In toggle method to {label} to expand: {expand}")
        self.select_asset(label)
        self.omni_driver.wait(1)
        toggle_done = False
        for _ in range(3):
            expand_sign_locator = self._get_expand_sign_locator(label)
            expand_sign_element = self.omni_driver.find_element(
                expand_sign_locator, refresh=True
            )
            source = expand_sign_element.image_source()
            self.log.info(f"Image source path for {label}: {source}")
            sign = os.path.split(source)[-1].replace(".svg", "")
            current_state = sign == "Minus"
            self.log.info(f"{label} expand state: {current_state}")
            if (expand and not current_state) or (not expand and current_state):
                self.log.info(f"Switching {label}")
                expand_sign_element.click()
                self.omni_driver.wait(2)
            else:
                toggle_done = True
                break
        if not toggle_done:
            raise ValueError("Failed to toggle")

    def _get_expand_sign_locator(self, label):
        """
        Gets the locator of the expand/collapse button on stage
        """
        main_treeview_elements = self.omni_driver.find_element(
            self._main_treeview, refresh=True
        )
        label_element = main_treeview_elements.find_element(
            f"**/Label[0].text=='{label}'", refresh=True
        )
        parent_path = label_element.find_parent_element_path()
        last_occurrence = parent_path.rfind("Frame")
        treeview_path = parent_path[:last_occurrence].rstrip("/")
        first_element = parent_path[last_occurrence:].lstrip("/").split("/")[0]
        node_num_start = first_element.find("[") + 1
        node_num_end = first_element.find("]")
        frame_index = int(first_element[node_num_start:node_num_end])
        hstack_index = frame_index // 3
        expand_sign_locator = f"{treeview_path}/HStack[{hstack_index}]/Image[0]"
        self.log.info(f"Expand/collapse sign locator: {expand_sign_locator}")
        return expand_sign_locator

    def get_asset_icons_list(self, label):
        """
        Gets the list of the icons present before the asset name on stage
        """
        main_treeview_elements = self.omni_driver.find_element(
            self._main_treeview, refresh=True
        )
        label_element = main_treeview_elements.find_element(
            f"**/Label[0].text=='{label}'", refresh=True
        )
        img_locator = "/".join(
            label_element.find_parent_element_path().split("/")[:-1]
            + ["ZStack[0]/Image[*]"]
        )
        image_elements = self.omni_driver.find_elements(img_locator)
        icons = []
        for element in image_elements:
            source = element.image_source()
            self.log.info(f"Image source path for {label}: {source}")
            icons.append(os.path.split(source)[-1].replace(".svg", ""))
        return icons

    def navigate_to_asset_validator_from_stage(self):
        """
        Navigate to asset validator window from the stage window
        Returns: Opened Asset Validator window
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        main_treeview_element = self.omni_driver.find_element(self._main_treeview)
        self.omni_driver.wait(1)
        first_xform_element = main_treeview_element.find_element("**/Label[0].text == 'Xform'")
        first_xform_dimensions = first_xform_element.get_size_and_position("all")
        x_coord = first_xform_dimensions["screen_position_x"] + first_xform_dimensions[
            "computed_width"] + 1
        y_coord = first_xform_dimensions["screen_position_y"] + 1
        self.omni_driver.click_at(x_coord, y_coord, True)
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Validate Stage")
        self.omni_driver.wait(1)

    def click_on_asset_sort(self):
        """
        Click on the Sorting header
        """
        element = self.omni_driver.find_element(self._stage_sort_order, refresh=True)
        #element_name = element.get_text()
        element.click()
    
    def get_sort_label(self):
        """
        Get the current selected sorting order
        """
        element = self.omni_driver.find_element(self._stage_sort_label, refresh=True)
        label = element.get_text()
        return label
    
    def change_sort_order(self, name: str):
        """
        Keep changing sorting order till the requested one is activated
        """
        label = self.get_sort_label()
        while label != name :
            self.click_on_asset_sort()
            self.omni_driver.wait(1)
            label = self.get_sort_label()
   
    def select_variant_from_stage(self,variant_name):
        """
        Selects variant from Stage window
        Args:
        variant_name : variant to be selected
        """

        variant_selector = self.find(self._variant_selection_combo_box, True)
        if variant_selector is not None:
            variant_selector.select_item_from_combo_box(None,variant_name,False)
        self.omni_driver.wait(1)
        property = variant_selector.get_combobox_info()
        assert property["current_value"] == variant_name,"Failed to set property to %s"% property["current_value"]
        
    def validate_prim_variants_from_stage(self, variant_data: dict):
        """Cycles through variant values for various attributes and validates prim become visibility and material mapping.
        
        Args:
            variant_data (dict): a dictionary containing names of variant comboboxes mapped with their values and respective changes
        """
        for variant_name, mapping in variant_data.items():
            values = mapping.keys()
            for value in values:
                self.select_variant_from_stage(variant_name)
                self.omni_driver.wait_for_stage_load(300)
                visible_prims = self.omni_driver.get_visible_prims()
                assert all(
                    prim in visible_prims for prim in mapping[value]
                ), f"Prims of selected variant are not visible. Expected visible: {list(set(mapping[value]) - set(visible_prims))}"
              
            for variant, prim_map in variant_data.items():
                if variant_name != variant and  "visible prims" in prim_map:
                    values1 = prim_map.keys()
                    assert all(
                        prim not in visible_prims for prim in values1
                    ), f"Prims of unselected variant/s should be invisible."
                    
    def validate_material_mapping_from_stage(self, variant_data: dict):
        """validates material mapping from stage 

        Args:
            variant_data (dict): data set to be validated again current material mapping
        """
        for rim_variant_type, material_map in variant_data.items():
            print("Testing Variant Type:", rim_variant_type)
            self.select_variant_from_stage(rim_variant_type)
            self.omni_driver.wait_for_stage_load(300)
            material_mapping = self.omni_driver.get_prim_material_mapping()
            
            for prim in material_map['material map'].keys():
                self.log.info("Testing Variant: " + rim_variant_type)
                assert prim in material_mapping, f"Prim {prim} of selected variant {rim_variant_type} is not visible."
                assert material_mapping[prim] == material_map['material map'][prim], f"Material of prim {prim} is incorrect for variant {rim_variant_type}. Expected: {material_map['material map'][prim]}, Actual: {material_mapping[prim]}"
    
    def get_stage_elements_details(self, name:str):
        """get details of stage elements coordinates

        Args:
            name (string): name of the column in stage
        """
        element = self.omni_driver.find_element(name, refresh=True)
        alignment = element.get_alignment()
        coordinates = element.get_size_and_position("all")
        return alignment, coordinates
    
    def is_column_header_clickable(self, name:str):
        """returns true if the columns header can be clicked/enabled

        Args:
            name (string): name of the column in stage
        """
        element = self.omni_driver.find_element(name, refresh=True)
        element_text_old = element.get_text()
        
        element.click()

        element = self.omni_driver.find_element(name, refresh=True)
        element_text_new = element.get_text()

        is_clicked = False
        if element_text_old != element_text_new:
            is_clicked = True

        return is_clicked
    
    def validate_tree_and_headers_width(self):
        """validates if the total stage width is equal to sum of widths of all visible columns

        Args:
            none
        """
        main_treeview_elements = self.omni_driver.find_element(self._main_treeview)
        tree_width = main_treeview_elements.get_size_and_position("all")["computed_width"]

        headers_width = 0

        column_elem = main_treeview_elements.find_elements("ZStack[*]")
        for header in column_elem:
            headers_width += header.get_size_and_position("all")["computed_width"]
        
        if headers_width == tree_width:
            return True
        else:
            return False

    def add_material_to_first_asset_get_asset_name(self, material:str):
        """add 'material' to the topmost asset in Stage
        Args:
            material(str) : Material to add
        Returns:
            the name of the asset to which 'material' is added
        """
        # Insert an asset in sub tree and return the specific tree

        item = self.omni_driver.find_element("Stage//Frame/Frame[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/TreeView[0]/Frame[3]/ZStack[0]/HStack[0]/HStack[0]/Label[0]")
        item.right_click()
        self.omni_driver.select_context_menu_option(material)
        self.omni_driver.wait(1)

        item_label = item.get_text()
       
        return item_label
        
    def get_column_label(self, column:str):
        """get column label/text from indentifier
        Args:
            column(str) : Column identifier
        Returns:
            the name of the label of the header
        """
        element = self.omni_driver.find_element(column, True)
        return element.get_text()

    def open_material_graph(self, prim:str):
        """open material graph
        Args:
            prim(str) : prim path
        """
        self.search_and_select_asset(prim)

        elem: OmniElement = self.omni_driver.find_element(
                self._material_graph.replace("__name__", prim), True
            )
        elem.right_click()
        self.omni_driver.select_context_menu_option("Open in MDL Material Graph")

    def open_action_graph(self, prim:str):
        """opens action graph by right clicking on the prim stage
        Args:
            prim(str) : prim path
        """
        graph_elem = self.search_and_select_asset(prim)
        graph_elem.right_click()
        self.omni_driver.select_context_menu_option("Open Graph")
        assert "Action Graph" in self.omni_driver.get_windows()["visible_windows"], "Action Graph window was not enabled."