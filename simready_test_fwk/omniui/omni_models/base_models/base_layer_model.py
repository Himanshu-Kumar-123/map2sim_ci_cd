# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Layer class
   This module contains the base methods for Layer window
"""

from ..base_models.base_content_model import BaseContentModel
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omniui.utils.omni_models import OmniModel
from omniui.utils.utility_functions import get_window_model


class BaseLayerModel(BaseModel):
    """Base model class for Layer window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Common locators
    _layer_insert_btn = "Layer//Frame/**/Button[*].name=='layerinsert'"
    _root = "Layer//Frame/VStack[0]"
    _layer = "Layer//Frame/VStack[0]/**/Label[*].text=='__name__'"
    _insert_subLayer_button = "Layer//Frame/**/ScrollingFrame[1]/HStack[0]/Button[0]"
    _create_sublayer = "Layer//Frame/**/ScrollingFrame[1]/HStack[0]/Button[1]"
    _create_sublayer_input_name = (
        "Create Sublayer//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"
    )
    _layer_prim = "Layer//Frame/**/TreeView[0]/**/Label[*].text=='{}'"
    _create_sublayer_save = "Create Sublayer//Frame/VStack[0]/HStack[2]/Button[0]"
    _transfer_root_layer_false = "Transfer Content//Frame/**/Button[1]"
    _transfer_root_layer_true = "Transfer Content//Frame/**/Button[0]"
    _created_sublayer_label = "Layer//Frame/**/layer_widget/**/Label[0].text=='__name__'"
    _mute_layer_toggles = "Layer//Frame/**/TreeView[0]/**/layer_widget/local_mute"
    _save_path = "Create Sublayer//Frame/**/ScrollingFrame[0]/**/filepicker_directory_path"
    _load_path = "Insert Sublayer//Frame/**/ScrollingFrame[0]/**/filepicker_directory_path"
    _insert_subLayer_input_name = (
        "Insert Sublayer//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"
    )
    _sublayer_save_btn = "Layer//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/ZStack[{}]/**/ToolButton[0]"
    _insert_subLayer_open_button = "Insert Sublayer//Frame/VStack[0]/HStack[2]/Button[0]"
    _layer_label = "Layer//Frame/**/Label[*].text=='__label__'"
    _save_layer_as_path = "Save Layer As//Frame/**/ScrollingFrame[0]/**/filepicker_directory_path"
    _save_layer_as_input_name = "Save Layer As//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"
    _save_layer_as_save = "Save Layer As//Frame/VStack[0]/HStack[2]/Button[0]"
    _expand_locator = "Layer//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/ZStack[*]"

    # live session
    _live_status = "Content//Frame/**/Label[*].text=='.live'"
    _root_layer_live_btn = "Layer//Frame/**/ToolButton[*].name=='live_update'"
    _join_session_radio_btn = "Live Session//Frame/**/RadioButton[*].name=='join_session_radio_button'"
    _create_session_radio_btn = "Live Session//Frame/**/RadioButton[*].name=='create_session_radio_button'"
    _session_name_stringfield = "Live Session//Frame/**/StringField[*].name=='new_session_name_field'"
    _create_session_btn = "Live Session//Frame/**/Button[*].text=='CREATE'"
    _sessions_combobox = "Live Session//Frame/**/ComboBox[*]"
    _join_btn = "Live Session//Frame/**/Button[*].text=='JOIN'"

    # merge dialog
    _merge_confirm_btn = "{}//Frame/**/Button[*].name=='confirm_button'"

    # options
    _options_btn = "Layer//Frame/**/Button[*].name=='options'"

    # Overwrite
    _overwrite_ok_button = r"__exclamation_glyph__ Overwrite//Frame/VStack[0]/HStack[1]/Button[0]"

    def navigate_to_window(self):
        """Navigate to Layer Window"""
        window = self.omni_driver.find_element(self._root)
        window.click()
        self.screenshot("navigate_to_layer")
        self.omni_driver.wait(1)

    def insert_layer_into_current_scene(self, file_name: str, folder_path: str):
        """Inserts Layer into the Current Stage"""
        layer_insert: OmniElement = self.omni_driver.find_element(self._layer_insert_btn)
        layer_insert.click(bring_to_front=True)
        self.omni_driver.wait(2)
        content_model: BaseContentModel = get_window_model(self.omni_driver,
                                                           OmniModel.content_model, app="Create")
        content_model.step_handle_file_explorer(
            path=folder_path, file_name=file_name, window="Insert Sublayer", submit_button="Open"
        )
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(10)

    def save_changes(self):
        """Save current changes"""
        query = "Layer//Frame/**/HStack[1]/VStack[0]/ZStack[0]/ToolButton[0]"
        save_button = self.omni_driver.find_element(query)
        save_button.click()
        self.omni_driver.wait(seconds=3)

    def create_sublayer(self, sublayer_name: str, save_path: str,
                        transfer_root_layer: bool = False, overwrite: bool = False):
        """Creates new sublayer with a given sublayer name

        Args:
            sublayer_name (str): Name of sublayer to be created
            transfer_root_layer (bool, optional): Transfer root layer to new layer. Defaults to False.
            overwrite (bool, optional): Overwrites the existing layer. Defaults to False.
        """
        self.omni_driver.wait(2)
        self.find_and_click(self._create_sublayer)
        self.omni_driver.wait(3)
        save_path_input = self.omni_driver.find_element(self._save_path)
        save_path_input.send_keys(save_path)
        create_sublayer_input = self.omni_driver.find_element(self._create_sublayer_input_name)
        create_sublayer_input.double_click()
        self.omni_driver.emulate_char_press(sublayer_name)
        self.omni_driver.wait(2)
        self.find_and_click(self._create_sublayer_save, refresh=True)
        if overwrite:
            try:
                btn = self.wait.element_to_be_located(self.omni_driver,
                                                      self._overwrite_ok_button.replace(
                                                          "__exclamation_glyph__",
                                                          self.get_glyph_code("exclamation.svg")))
                btn.click()
                self.log.info("Overwritten existing file.")
            except ElementNotFound:
                self.log.info("File was not present, saved it for first time.")
        if "Transfer Content" in self.omni_driver.get_windows()["visible_windows"]:
            try:
                if transfer_root_layer:
                    self.find_and_click(self._transfer_root_layer_true)
                else:
                    self.find_and_click(self._transfer_root_layer_false)
            except ElementNotFound:
                self.log.info("Tranfer content to ROOT layer pop up not found.")
                self.screenshot("no_transfer_content")
        self.omni_driver.wait(2)
        sublayer = self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", sublayer_name))
        self.omni_driver.wait(1)
        sublayer.click()
        self.omni_driver.wait(2)
        sublayer.click()
        self.omni_driver.wait(2)

    def delete_sublayer(self, sublayer_name: str):
        """Deleted given sublayer

        Args:
            sublayer_name (str): Name of sublayer to be deleted
        """
        self.omni_driver.wait(2)
        sublayer = self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", sublayer_name), refresh=True
        )
        sublayer.right_click()
        self.omni_driver.select_context_menu_option("Remove Layer")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def make_sublayer_authorising(self, sublayer_name: str):
        """Makes the given sublayer an authorising sublayer

        Args:
            sublayer_name (str): Name of sublayer to make authorising.
        """
        self.omni_driver.wait(2)
        sublayer = self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", sublayer_name), refresh=True
        )
        # TODO: use context menu and remove double click when related bug is resolved: OVSWQA-2067
        # sublayer.right_click()
        # self.omni_driver.select_context_menu_option("Set Authoring Layer")
        sublayer.double_click()

    def toggle_mute_layer(self, sublayer_index: int):
        """Mute given sublayer

        Args:
            sublayer_name (str): Name of sublayer to be muted
        """
        self.omni_driver.wait(2)
        all_sublayer_mute_toggles = self.omni_driver.find_elements(self._mute_layer_toggles)
        all_sublayer_mute_toggles[sublayer_index].click()

    def save_sublayer_changes(self, sublayer_name: str, Authoring: bool = False):
        """Saved changes of given sublayer

        Args:
            sublayer_name (str): Name of sublayer
        """
        self.omni_driver.wait(2)
        if Authoring:
            sublayer_name += " (Authoring Layer)"
        self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", sublayer_name)).right_click()
        self.omni_driver.select_context_menu_option("Save")

    def insert_sublayer(self, sublayer_name: str, load_path: str, checkpoint=1):
        """Inserts existing sublayer

        Args:
            sublayer_name (str): Name of sublayer to be merged
            load_path (str): Directory path of folder where the sublayer is present
        """
        self.omni_driver.wait(2)
        insert_btn = self.omni_driver.find_element(self._insert_subLayer_button, refresh=True)
        insert_btn.double_click()
        load_path_input = self.omni_driver.find_element(self._load_path)
        load_path_input.send_keys(load_path)
        insert_sublayer_input = self.omni_driver.find_element(self._insert_subLayer_input_name)
        if checkpoint != 1:
            sublayer_name += f"%3F%26{checkpoint}"
        insert_sublayer_input.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(sublayer_name)
        self.omni_driver.wait(2)
        self.find_and_click(self._insert_subLayer_open_button)

    def merge_sublayer(self, sublayer_name: str):
        """Merges sublayers

        Args:
            sublayer_name (str): Name of sublayer to be merged
        """
        self.omni_driver.wait(2)
        self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", sublayer_name)).right_click()
        self.omni_driver.select_context_menu_option("Merge Down One")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def is_sublayer_readonly(self, index_level: int):
        """Verifys Sublayer is readonly"""
        query = (
                f"Layer//Frame/**/TreeView[0]/ZStack[{index_level}]/"
                + 'VStack[*]/layer_widget/**/Image[0].name=="layer_read_only_lock"'
        )
        try:
            self.omni_driver.find_element(query)
            self.log.info("[BaseLayerModel] Layer has lock icon")
            for i in range(index_level, index_level + 5):
                try:
                    query = (
                            "Layer//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/"
                            + f'ZStack[{i}]/VStack[1]/layer_widget/ToolButton[0].name=="dirty_readonly"'
                    )
                    self.omni_driver.find_element(query)
                    return True
                except:
                    pass
            self.log.error("[BaseLayerModel] Layer does not have read only icon")
        except:
            self.log.error("[BaseLayerModel] Layer does not have lock icon")
            return False
        return False

    def flatten_sublayer(self):
        """Flattens sublayers"""
        self.omni_driver.wait(2)
        self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", "Root Layer")).right_click()
        self.omni_driver.select_context_menu_option("Flatten Sublayers")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def get_position(self, name: str, authoring=False):
        """Get centre position of layer

        Args:
            name (str): Name of layer
            authoring(bool): If the layer is Authoring layer
        Returns:
            _type_: Position of layer
        """
        if authoring:
            name += " (Authoring Layer)"
        layer = self.omni_driver.find_element(self._layer_label.replace("__label__", name),
                                              refresh=True)
        return layer.get_widget_center()

    def assert_item_exits(self, name: str):
        """Asserts if a specified item exists in stage

        Args:
            name (str): Asset name
        """
        assert self.omni_driver.find_element(
            self._layer_label.replace("__label__", name)
        ), f"Layer not present in Layer window Expected: '{name}'"
        self.log.info(f"Layer {name} is present in layer window")

    def save_a_copy(self, sublayer_name: str, save_path: str, authoring=False):
        """Saves a copy of the sublayer

        Args:
            sublayer_name (str): name of sublayer to make a copy
            authoring (bool, optional): Authoring status of sublayer. Defaults to False.
        """
        self.omni_driver.wait(2)
        if authoring:
            new_sublayer_name = sublayer_name + " (Authoring Layer)"
        self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", new_sublayer_name)).right_click()
        self.omni_driver.select_context_menu_option("Save a Copy")
        save_as_path_input = self.omni_driver.find_element(self._save_layer_as_path)
        self.omni_driver.wait(2)
        save_as_path_input.send_keys(save_path)
        save_as_input_name = self.omni_driver.find_element(self._save_layer_as_input_name)
        save_as_input_name.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press("copy_" + sublayer_name)
        self.omni_driver.wait(2)
        self.find_and_click(self._save_layer_as_save)

    def expand_item(self, name: str, authoring=False):
        if authoring:
            name += " (Authoring Layer)"
        key = f"**/Label[0].text=='{name}'"
        item, index = self.get_child_element(self._expand_locator, key)
        expand_locator = self._expand_locator.replace("*", str(index - 1))
        expand = self.omni_driver.find_element(expand_locator + "/**/Image[0]")
        expand.click()

    def select_layer(self, layer: str, is_authoring_layer: False):
        if is_authoring_layer:
            layer += " (Authoring Layer)"

        layer_elm: OmniElement = self.omni_driver.find_element(
            self._layer.replace("__name__", layer))
        layer_elm.click()

    def create_live_session(self, session_name="demo"):
        """Creates a new live session

        Args:
            session_name (str): Name of session. Defaults to "demo".
        """
        live_session_tool_btn: OmniElement = self.omni_driver.find_element(
            self._root_layer_live_btn, refresh=True)
        live_session_tool_btn.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Create Session")

        create_session_radiobtn = self.wait.element_to_be_located(self.omni_driver,
                                                                  self._create_session_radio_btn)
        if not create_session_radiobtn.is_checked():
            create_session_radiobtn.click()
        self.find_and_click(self._session_name_stringfield)
        self.omni_driver.emulate_char_press(session_name)
        self.find_and_click(self._create_session_btn)

        self.wait.element_to_be_enabled(live_session_tool_btn)
        self.wait.element_to_be_located(self.omni_driver, self._live_status)

    def join_live_session(self, session_name="demo"):
        """Joins an existing live session

        Args:
            session_name (str, optional): Name of session. Defaults to "demo".
        """
        live_session_tool_btn: OmniElement = self.omni_driver.find_element(
            self._root_layer_live_btn, refresh=True)
        live_session_tool_btn.right_click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Join Session")

        join_radiobtn = self.wait.element_to_be_located(self.omni_driver,
                                                        self._join_session_radio_btn)
        if not join_radiobtn.is_checked():
            join_radiobtn.click()
        self.omni_driver.wait(2)
        sessions = self.omni_driver.find_element(self._sessions_combobox)
        sessions.select_item_from_combo_box(index=None, name=session_name, stack_combo=False)
        self.omni_driver.wait(2)
        self.find_and_click(self._join_btn)

        self.wait.element_to_be_enabled(live_session_tool_btn)
        self.wait.element_to_be_located(self.omni_driver, self._live_status)

    def get_center(self):
        """Get center of layers

        Returns:
            Tuple: Tuple containing x and y coordinates
        """
        layer = self.omni_driver.find_element(self._root)
        return layer.get_widget_center()

    def move_prim_to_sublayer(self, prim: OmniElement, sublayer_name: str, handle=False):
        """Moves a asset to the given sublayer

        Args:
        prim_name(OmniElement): OmniElement ref to the prim
        sublayer_name(str): name of sublayer to move to
        handle(str): flag to handle merge dialog
        """
        sublayer = self.omni_driver.find_element(self._layer_prim.format(sublayer_name), True)
        x = sublayer.get_size_and_position("screen_position_x")
        y = sublayer.get_size_and_position("screen_position_y") + 10
        prim.drag_and_drop(x, y)
        self.omni_driver.wait(1)
        if handle:
            self.confirm_merge_dialog()

    def confirm_merge_dialog(self):
        """Confirm Merge dialog on moving delta prim"""
        windows = self.omni_driver.get_windows()["visible_windows"]
        window_name = None
        for win in windows:
            if "Merge Prim Spec" in win:
                window_name = win
                break
        assert window_name, "Failed to find window name 'Merge Prim Spec'"
        self.find_and_click(self._merge_confirm_btn.format(window_name))
        self.omni_driver.wait_for_stage_load()

    def select_a_prim(self, prim_name: str):
        """Selects a prim in the layer window

        Args:
        prim_name(str): name of prim in TreeView
        """
        prim = self.omni_driver.find_element(self._layer_prim.format(prim_name), refresh=True)
        prim.scroll_into_view(ScrollAxis.Y.value, ScrollAmount.BOTTOM.value)
        prim.double_click()

    def find_delta_prim(self, prim_name: str):
        """Finds the delta prim in the Layer window

        Args:
        prim_name(str): Name of the prim
        """
        h_stacks = self.omni_driver.find_elements(
            "Layer//Frame/**/TreeView[0]/**/Label[*].text == '{}'".format(prim_name)
        )
        self.log.info(f"hstacks: {h_stacks}")
        for stack in h_stacks:
            try:
                locator = "/".join(stack.find_parent_element_path().split("/")[:-1])
                self.log.info(f"Locator: {locator}")
                self.omni_driver.find_element(
                    locator + "/VStack[0]/ZStack[0]/VStack[0]/HStack[0]/Image[0]")
                return self.omni_driver.find_element(locator + f"/**/Label[0].text=='{prim_name}'")
            except ElementNotFound:
                pass

    def is_sublayer_dirty(self, sublayer_name: str):
        """Verifies if the sublayer has unsaved changes

        Args:
        sublayer_name: name of the sublayer
        """
        child_locator = "Layer//Frame/VStack[0]/ScrollingFrame[0]/TreeView[0]/ZStack[*]"
        key = f"**/Label[0].text=='{sublayer_name}'"
        _, index = self.get_child_element(child_locator, key)
        save_button = self.omni_driver.find_element(self._sublayer_save_btn.format(index + 2), True)
        return save_button.tool_button_is_checked()

    def find_a_prim(self, prim_name: str):
        """Returns non - delta prim instance

        Args:
        prim_name(str): Name of the prim
        """
        h_stacks = self.omni_driver.find_elements(self._layer_prim.format(prim_name))
        self.log.info(f"hstacks: {h_stacks}")
        for stack in h_stacks:
            locator = "/".join(stack.find_parent_element_path().split("/")[:-1])
            try:
                self.log.info(f"Locator: {locator}")
                self.omni_driver.find_element(
                    locator + "/VStack[0]/ZStack[0]/VStack[0]/HStack[0]/Image[0]")
            except ElementNotFound:
                return self.omni_driver.find_element(locator + f"/**/Label[0].text=='{prim_name}'")

    def show_session_layer(self, state: bool = True):
        try:
            session_layer = self.omni_driver.find_element(self._layer_prim.format("Session Layer"),
                                                          True)
            if state == True:
                return session_layer
        except ElementNotFound:
            pass

        self.find_and_click(self._options_btn, refresh=True)
        self.omni_driver.select_context_menu_option("Show Session Layer")

        session_layer = self.omni_driver.find_element(self._layer_prim.format("Session Layer"),
                                                      True)
        return session_layer

    def validate_layer(self, layer_name: str, validation_type: str):
        """
        Selects the asset validation for the given layer
        Args:
            layer_name: Layer name that needs to be validated
            validation_type: Asset Validation type
        Returns:
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        layer_name_element = self.omni_driver.find_element(
            self._created_sublayer_label.replace("__name__", layer_name), refresh=True)
        layer_name_element.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(validation_type)
        self.omni_driver.wait(2)
