"""Base Variant Editor Model class
   This module contains the base methods for Variant Editor window
"""
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import (
    ElementNotFound,
    PropertyRetrieveFailed,
)
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.waits import Wait
from omniui.utils.enums import ViewportMode
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.common.constants import KeyboardConstants
import os

class BaseVariantEditorModel(BaseModel):
    """Base model class for Variant Editor window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """
    _variant_editor_window = "Variant Editor//Frame/VStack[0]"
    # Locators related to Variants window
    _variant_editor_window_name = "Variant Editor"
    _select_prim_window_name = "Select Prims"
    _menupath = "Tools/Variants/Variant Editor"
    _new_target_prim_icon = "Variant Editor//Frame/**/HStack[1]/ZStack[0]/Button[0]"
    _target_prim_btn = "Select Target Prim//Frame/**/Button[*].text=='__name__'"
    _target_prim_label = "Select Target Prim//Frame/**/Label[*].text=='__name__'"
    _variant_editor_btn = "Variant Editor//Frame/**/Button[*].text=='__name__'"
    _variant_editor_label = "Variant Editor//Frame/**/Label[*].text=='__name__'"
    _select_target_prim_search = "Select Target Prim//Frame/**/StringField[0]"
    _asset_path_search_results = (
        "Select Target Prim//Frame/**/TreeView[1]/**/Label[*].text=='__name__'"
    )
    _select_target_prim_label = "Select Target Prim//Frame/**/Label[*].text=='__name__'"
    _main_treeview = "Select Target Prim//Frame/**/TreeView[0]"
    _variant_tree_view = "Variant Editor//Frame/**/TreeView[0]"
    _select_prim_window_label= "Select Prims//Frame/**/Label[*].text=='__name__'"
    _select_prim_window_btn= "Select Prims//Frame/**/Button[*].text=='__name__'"
    _select_prim_window_search = "Select Prims//Frame/**/StringField[0]"
    _select_properties_search_bar = "Select Properties//Frame/**/StringField[0]"
    _select_properties_window_label = "Select Properties//Frame/**/Label[*].text=='__name__'"
    _select_properties_window_btn = "Select Properties//Frame/**/Button[*].text=='__name__'"
    _variant_minimizer_icon_btn = "Variant Editor//Frame/**/VStack[__index__]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/Image[0"
    _colorwidget_path = "Variant Editor//Frame/**/ColorWidget[0]"
    _variant_transform_rotate = "Variant Editor//Frame/**/ScrollingFrame[0]/**/drag_per_channel_xformOp:rotateXYZ/HStack[__index__]/ZStack[1]/FloatDrag[0]"
    _property_watch_button = "Variant Editor//Frame/**/ScrollingFrame[0]/**/PropertyWatchButton[0]"

    _variant_opinion_btn = "Variant Editor//Frame/**/TreeView[0]/HStack[__index__]/**/PropertyWatchButton[0]"
    _add_property_btn = "Variant Editor//Frame/**/TreeView[0]/HStack[__index__]/**/Button[*].text=='__name__'"
    _target_prim_collapse_btn = "Variant Editor//Frame/**/TreeView[0]/VStack[__index__]/HStack[0]/ZStack[0]/HStack[0]/HStack[0]/VStack[0]/Image[0]"    
    _visibility_choices_menu = "Variant Editor//Frame/**/TreeView[0]/HStack[__index__]/ZStack[0]/HStack[0]/VStack[0]/HStack[0]/ZStack[0]/token_visibility.name == 'choices'"
    _prim_identifier = "Variant Editor//Frame/**/TreeView[0]/**/Label[*].name=='__text__'"
    _material_property_prim = "Variant Editor//Frame/**/TreeView[0]/**/combo_drop_target"
    _material_property_win_search_bar = "MaterialPropertyPopupWindow//Frame/**/StringField[0]"
    _material_property_window_label = "MaterialPropertyPopupWindow//Frame/**/Label[*].text == '__text__'"
    _colorwidget_path = "Variant Editor//Frame/**/ScrollingFrame[0]/**/ColorWidget[0]"

    def get_window_center(self):
        """Get center of variant editor window

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        window = self.omni_driver.find_element(self._variant_editor_window)
        return window.get_widget_center()
    
    def open_variant_editor_window(self):
        """
        Navigates to the Variant Editor window
        Args: None
        Returns: None
        """      
        self.omni_driver.select_menu_option(self._menupath)
        self.wait.window_to_be_visible(self.omni_driver, self._variant_editor_window_name)

    def close_variant_editor_window(self):
        self.omni_driver.close_window(self._variant_editor_window_name)

    def navigate_to_variant_editor(self):
        """
        Navigates to docked variant editor window
        Args: None
        Returns: None
        """   
        self.find_and_click(self._variant_editor_window,refresh=True)   

    def select_new_target_prim(self,stage_layer : str):
        """
        Selects new target Prim icon in Variant editor
        Args:
            stage_layer (str):  Layer name to be selected

        Returns:
            None
        """
        self.find_and_click(self._new_target_prim_icon)
        self.find_and_enter_text(self._select_target_prim_search,stage_layer)
        target_prim = self.find(self._target_prim_label.replace('__name__',stage_layer),True)
        target_prim.click()
        if not target_prim.is_selected():
            initial_pos_x = target_prim.get_size_and_position("screen_position_x")
            initial_pos_y = target_prim.get_size_and_position("screen_position_y")
            self.omni_driver.click_at(initial_pos_x, initial_pos_y + 20)
        self.find_and_click(self._target_prim_btn.replace('__name__','Select'))
     
    def add_prim(self, layer : str):
        """
        Adds Prim layer in a variant
         Args:
            layer (str):  Prim Layer name to be selected
        Returns:
            None
        """
        self.find_and_click(self._variant_editor_btn.replace('__name__','Add Prim'))
        self.find_and_enter_text(self._select_prim_window_search,layer)
        prim = self.find(self._select_prim_window_label.replace('__name__',layer),True)
        prim.click()
        if not prim.is_selected():
            initial_pos_x = prim.get_size_and_position("screen_position_x")
            initial_pos_y = prim.get_size_and_position("screen_position_y")
            self.omni_driver.click_at(initial_pos_x, initial_pos_y + 20)
        select_btn = self.find(self._select_prim_window_btn.replace('__name__','Select'),True)
        select_btn.click()
        while self._select_prim_window_name in self.omni_driver.get_windows()["visible_windows"]:
            initial_pos_x = select_btn.get_size_and_position("screen_position_x")
            initial_pos_y = select_btn.get_size_and_position("screen_position_y")
            self.omni_driver.click_at(initial_pos_x, initial_pos_y + 10)

    def add_property(self,property:str, index:int = 0, apply_to_all_prim :bool = False,search: bool = True):
        """
        Adds property for Prim layer in a variant
         Args:
            property (str):  Property to be selected                                     
            index (int) : 0,2,4....8
        Returns:
            None
        """
        self.find_and_click(self._variant_editor_btn.replace('__name__','Add Property'), True)   
        if search:                                                                                                                           
            self.find_and_enter_text(self._select_properties_search_bar,property)
        self.find_and_click(self._select_properties_window_label.replace('__name__',property))
        if apply_to_all_prim:
            self.find_and_click(self._select_properties_window_btn.replace('__name__','Add To All Prims'))
        else:
            self.find_and_click(self._select_properties_window_btn.replace('__name__','Add'))

    def duplicate_and_rename_variant(self, original_variant:str, new_variant_name:str,rename: bool = True):
        """
        Creates new variant by duplicating existing one and renaming the new variant
         Args:
            original_variant (str):  Existing variant name which needs to be duplicated
            new_variant_name (str) : Name for the new variant
            rename (bool) : Set rename to false just to duplicate variant
        Returns:
            None
        """
        og_variant = self.find(self._variant_editor_label.replace('__name__',original_variant),refresh=True)
        og_variant.right_click()
        self.omni_driver.select_context_menu_option("Duplicate Variant")
        if not rename:
            self.log.info(f"Duplicated {original_variant}")
            return
        variant_1_name = original_variant+ "_1"
        variant_1 = self.find(self._variant_editor_label.replace('__name__',variant_1_name),refresh=True)
        variant_1.right_click()
        self.omni_driver.select_context_menu_option("Rename Variant")
        self.omni_driver.emulate_key_press(KeyboardConstants.backspace)
        self.omni_driver.emulate_char_press(new_variant_name[0:])
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)
    
    def navigate_to_variant(self,variant_name:str):
        """
        Selects existing  variant
         Args:
            variant_name (str):  Name of variant
        Returns:
            None
        """
        element = self.find_and_click(self._variant_editor_label.replace('__name__',variant_name),
                            bring_to_front=True,
                            refresh = True,
                            double_click = False)

    def set_base_color(self,color:str):
        """
        Sets base color property for the selected variant
         Args:
            color (str):  color value in hex code
        Returns:
            None
        """
        colorwidget_element = self.omni_driver.find_element(
            self._colorwidget_path, refresh=True
        )
        colorwidget_element.click()
        self.omni_driver.wait(2)

        for _ in range(7):
            self.omni_driver.emulate_key_press(KeyboardConstants.tab)
            self.omni_driver.wait(2)
    
        self.omni_driver.emulate_char_press(color[1:])
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def scroll_variant_in_view(self, variant_name:str):
        """
        Scrolls down to spot variant
         Args:
            variant_name (str):  Variant name to be visible
        Returns:
            None
        """
        variant_loc = self.find_and_scroll_element_into_view(self._variant_editor_label.replace('__name__',variant_name),ScrollAxis.Y, ScrollAmount.CENTER)
        return variant_loc
        
    def add_new_variant_set(self,variant_set_name:str):
        """
        Adds a new variant set
        Args:
            variant_set_name (str):  Name of variant set
        Returns:
            None
        """
        variant_set_found = False
        loop = 0
        while not variant_set_found and loop < 4 :
            self.find_and_click(self._variant_editor_btn.replace('__name__',"Add New Variant Set"),refresh=True)
            btn = self.find_and_click(self._variant_editor_label.replace('__name__',"Variant_Set"),refresh=True)
            if btn:
                btn.right_click()
                self.omni_driver.select_context_menu_option("Rename Variant Set")
                self.omni_driver.emulate_key_press(KeyboardConstants.backspace)
                self.omni_driver.wait(2)
                text_field_loc = btn.path.replace('Label','StringField')
                text_field_id = self.find(text_field_loc,refresh=True)
                text_field_id.send_keys(variant_set_name)
            self.omni_driver.wait(2)
            loop += 1
            variant = self.find(self._variant_editor_label.replace('__name__',variant_set_name),refresh=True)
            if variant is not None:
                variant_set_found = True
                 
    def add_new_variant(self,variant_name:str):
        """
        Adds a new variant for selected variant set
        Args:
            variant_name (str):  Name of variant 
        Returns:
            None
        """
        variant_set_found = False
        loop = 0
        while not variant_set_found and loop < 4 :
            btn = self.find_and_click(self._variant_editor_label.replace('__name__',"Variant"),refresh=True)
            if btn:
                btn.right_click()
                self.omni_driver.select_context_menu_option("Rename Variant")
                self.omni_driver.emulate_key_press(KeyboardConstants.backspace)
                self.omni_driver.wait(1)
                btn.send_keys(variant_name)
            self.omni_driver.wait(1)
            loop += 1
            variant = self.find(self._variant_editor_label.replace('__name__',variant_name),refresh=True)
            if variant is not None:
                variant_set_found = True
            
    def search_and_select_target_prim(self,path:str):
        """
        Searches and selects target prim in select target prim window
        Args:
            path (str):  path for the layer to be selected seperated by '>'
        Returns:
            None
        """
        self.find_and_click(self._new_target_prim_icon)
        self.expand_treeview(path)
        layers = path.split(">")
        name = layers[-1]
        attempts = 0
        btn = self.find_and_click(self._select_target_prim_label.replace('__name__',name))
        while not btn.is_selected():
            if attempts >= 3:
                break
            self.log.info(f"Attempting to select asset: {name}")
            btn.click()
            self.omni_driver.wait(1)
            attempts += 1
        assert btn.is_selected(), f"Failed to select asset: '{name}'"
        self.find_and_click(self._target_prim_btn.replace('__name__','Select'))

    def expand_treeview(self, tree_path:str):
        """
        Expands the treeview as per the given path separated by '>'.
        Args:
            path (str):  path for the layer to be selected seperated by '>'
        Returns:
            None
        """
        tree_item = tree_path.split(">")
        for item in tree_item:
            item = item.strip()
            self.log.info(f"Expanding {item} on tree view")
            self.toggle_tree_item(item, expand=True)
        self.log.info("Expansion of the treeview is completed")

    def collapse_variant_treeview(self,variant_set_count: int = 0):
        """
        Collapses the variant view.
        Args:
            variant_set_count (int):  No. of how many variant set views need to be collapsed
        Returns:
            None
        """
        element_found = True
        index = 0
        variant_set_collapsed = 0
        while element_found:
            element = self.find(self._variant_minimizer_icon_btn.replace('__index__',str(index)))
            if element:
                if element.image_source(from_style=True).endswith("collapse.svg"):
                    element.click()
                index += 2 
                variant_set_collapsed += 1
                if variant_set_count == variant_set_collapsed:
                    break 
            else:
                element_found = False 

    def toggle_tree_item(self, label:str, expand:bool=True):
        """
        Toggles tree item for Select Target Prim window
        Args:
            label (str):  Tree item
            expand (bool) : To expand the tree item 
        Returns:
            None
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
                self._select_target_prim_label.replace("__name__", name), True
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

    def _get_expand_sign_locator(self, label:str):
        """
        Gets the locator of the expand/collapse button on stage
        Args:
            label (str):  Tree item
        Returns:
            None
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
        hstack_index = (frame_index // 2)
        expand_sign_locator = f"{treeview_path}/HStack[{hstack_index}]/Image[0]"
        self.log.info(f"Expand/collapse sign locator: {expand_sign_locator}")
        return expand_sign_locator
    
    def toggle_prim_collapse_expand_btn(self, action:str , index:int):
        """
        Args:
            action (str): coolapse or expand 
            index (int): Prim index
        """
        btn = self.omni_driver.find_element(self._target_prim_collapse_btn.replace("__index__",str(index)), True)
        if action == "collapse":
            if btn.image_source(from_style=True).endswith("collapse.svg"):
                btn.click()
                btn = self.omni_driver.find_element(self._target_prim_collapse_btn.replace("__index__",str(index)), True)
                assert btn.image_source(from_style=True).endswith("expand.svg"),"Failed to collapse prim section"
        elif action == "expand":
            if btn.image_source(from_style=True).endswith("expand.svg"):
                btn.click()
                btn = self.omni_driver.find_element(self._target_prim_collapse_btn.replace("__index__",str(index)), True)
                assert btn.image_source(from_style=True).endswith("collapse.svg"),"Failed to collapse prim section"
        
    def variant_transform_rotate(self, rotate_value: list, widget_index: int = 1):
        """Adds X, Y and Z rotate values
        :param rotate_value: list containing x, y and z values
        :param widget_index: index of 'Rotate' section in 'Transform' collapsable"""
        if len(rotate_value) != 3:
            assert (
                False
            ), f"Please send X, Y and Z values for Rotation. Received was {rotate_value}"
        for i in range(3):
            self.select_value_for_slider(
                self._variant_transform_rotate.replace("__index__", f"{i}"),
                rotate_value[i],
            )
        self.omni_driver.find_element( self._variant_transform_rotate.replace("__index__", f"{widget_index}"),refresh=True).click()
        self.log_info_with_screenshot("added_rotation_values")

    def toggle_translate_button(self):
        """
        Toggle the rotate XYZ property watch button from L to V 
        """
        self.omni_driver.find_element(self._property_watch_button).click()
        self.omni_driver.wait(1)
        
    def switch_variant_opinion(self, index:int):
        """
        switches property watch button from L to V 
        Args:
        
            index (int): 0,2,4,...even indices for multiple properties
        """
        btn = self.omni_driver.find_element(self._variant_opinion_btn.replace("__index__",str(index)),True)
        btn.click()
        self.omni_driver.wait(1)

    def duplicate_variant(self, original_variant:str):
        """
        Creates new variant by duplicating existing one 
         Args:
            original_variant (str):  Existing variant name which needs to be duplicated
    
        Returns:
            None
        """
        og_variant = self.find(self._variant_editor_label.replace('__name__',original_variant),refresh=True)
        og_variant.right_click()
        self.omni_driver.select_context_menu_option("Duplicate Variant")

    def change_prim_visibility_property(self,option:str,index):  
        """
        changes visibility property of prim
        Args:
            option (str): "invisible/inherited"
            index (_type_): "1,3,5...odd indices in case of multiple prims"
        """
        combobox_btn = self.omni_driver.find_element(self._visibility_choices_menu.replace("__index__",str(index)),True)
        combobox_btn.select_item_from_combo_box(name=option,index=None,stack_combo=False)
        assert combobox_btn.get_combobox_info()["current_value"] == option, "Failed to set desired property : {option}"
        
    def select_material_prim(self,prim:str):
        """
        Selects prim fror property : material:binding

        Args:
            prim (str): prim to be selected
        """
        btn = self.find(self._material_property_prim,refresh=True)
        initial_pos_x = btn.get_size_and_position("screen_position_x")
        initial_pos_y = btn.get_size_and_position("screen_position_y")
        self.omni_driver.click_at(initial_pos_x + 10, initial_pos_y + 10)
        self.find_and_enter_text(self._material_property_win_search_bar,prim)
        prim_label = self.find_and_click(self._material_property_window_label.replace("__text__",prim),refresh=True)
        
        
    def variant_color_picker(self,original_variant: str,color: str):
        """
        For adding color through color picker

        Args:
            original_variant (str): variant name
        """
        og_variant = self.find(self._variant_editor_label.replace('__name__',original_variant),refresh=True)
        og_variant.click()
        self.omni_driver.wait(2)

        colorwidget_element = self.omni_driver.find_element(
            self._colorwidget_path, refresh=True
        )
        colorwidget_element.click()
        self.omni_driver.wait(2)

        for _ in range(7):
            self.omni_driver.emulate_key_press(KeyboardConstants.tab)
            self.omni_driver.wait(2)

        self.omni_driver.emulate_char_press(color[1:])
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.tab)
        og_variant = self.find(self._variant_editor_label.replace('__name__',original_variant),refresh=True)
        og_variant.click()
        self.omni_driver.wait(1)
        self.close_variant_editor_window()
        self.omni_driver.wait(5)
        self.viewport_screenshot("pink_colored_variant_added")
        self.omni_driver.wait(2)

    def validate_prims_in_variant_editor(self, prims:list):
        """
        Validates of list off prim given as input are present in variant editor
        """    
        for prim in prims:
            prim_id = self.find(self._variant_editor_label.replace("__name__",prim),True)
            assert prim_id != None, f"Cannot find prim {prim} in variant editor"
        