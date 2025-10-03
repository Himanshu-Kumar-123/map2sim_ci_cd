# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Hotkeys Model class
   This module contains the base methods for Hotkeys window
"""
from ..base_models.base_model import BaseModel


from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis


class BaseHotkeysModel(BaseModel):
    """Base model class for Hotkeys window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Hotkeys window
    _add_global_hotkey_btn = "Hotkeys//Frame/**/Button[0].text=='Add New Global Hotkey'"
    _select_action_dropdown = "Hotkeys//Frame/**/Label[0].text=='Select An Action'"
    _action = "###ACTION_PICKER//Frame/**/Label[*].text=='__action__'"
    _save_hotkey_btn = "Hotkeys//Frame/**/Image[1].name=='save'"
    _window_picker = "###WINDOW_PICKER"
    _window = "###WINDOW_PICKER//Frame/**/Label[*].text=='__window_name__'"
    _add_window_btn = "Hotkeys//Frame/**/Button[0].text=='Add Window'"
    _zstacks = "Hotkeys//Frame/**/HotkeysView[0]/ZStack[*]"
    _add_new_hotkey = "Hotkeys//Frame/**/HotkeysView[0]/**/Button[*]"
    _expand_global_window = "Hotkeys//Frame/**/HotkeysView[0]/HStack[0]/**/Image[0]"
    _action_label = "Hotkeys//Frame/**/Label[0].text=='__action__'"
    _edit_focus_prim_btn = (
        "Hotkeys//Frame/VStack[0]/ScrollingFrame[0]/HotkeysView[0]/ZStack[26]/HStack[0]/HStack[1]/Image[0]"
    )

    _save_focus_prim_hotkey_btn = (
        "Hotkeys//Frame/VStack[0]/ScrollingFrame[0]/HotkeysView[0]/ZStack[26]/HStack[0]/HStack[1]/Image[0]"
    )
    _handle_warning_window = "###Hotkey_WARNING_Restore Defaults//Frame/**/Button[*].text=='Yes'"
    _restore_default_hamburger = "Hotkeys//Frame/VStack[0]/HStack[0]/VStack[0]/ImageWithProvider[0]"

    def _select_action(self, action: str):
        """Selects action to perform

        Args:
            action (str): Action to perform
        """
        self.wait.element_to_be_located(self.omni_driver, self._select_action_dropdown)
        self.find_and_click(self._select_action_dropdown, refresh=True)
        self.omni_driver.emulate_char_press(action)
        self.log.info(f"{action} was entered")
        self.find_and_click(self._action.replace("__action__", action), refresh=True)

    def _enter_hotkey(self, keys: str):
        """Enters the hotkey

        Args:
            keys (str): the key to perform that action
        """
        self.omni_driver.wait(3)
        self.omni_driver.emulate_key_combo_press(keys)
        self.log.info(f"{keys} combo entered")

    def _save_hotkey(self):
        """Saves the hotkey"""
        self.find_and_click(self._save_hotkey_btn, refresh=True)
        self.log.info("Hotkey saved")
        self.screenshot("Hotkey saved")
        self.omni_driver.wait(3)

    def _add_window(self, window_name: str):
        """Adds new window in hotkey window

        Args:
            window_name (str): Name of new window
        """
        self.wait.element_to_be_located(self.omni_driver, self._add_window_btn)
        add_window_btn = self.omni_driver.find_element(self._add_window_btn, True)
        add_window_btn.double_click()
        self.wait.element_to_be_located(self.omni_driver, self._window_picker)
        self.omni_driver.emulate_char_press(window_name)
        self.find_and_click(self._window.replace("__window_name__", window_name))
        self.log.info("New Window added")

    def _click_add_new_window_hotkey(self):
        """Clicks add new window button"""
        add_hotkey_buttons = self.omni_driver.find_elements(self._add_new_hotkey)
        add_button = add_hotkey_buttons[-1]
        add_button.click()
        self.log.info("Clicked add new window hotkey")

    def _scroll_element_to_top(self, label_name: str):
        """Scrolls given label to top

        Args:
            label_name (str): Name of label to be scrolled
        """
        self.find_and_scroll_element_into_view(
            self._action_label.replace("__action__", label_name), ScrollAxis.Y, ScrollAmount.TOP
        )

    def _edit_hotkey(self, action: str, keys: str):
        """Edits existing hotkey

        Args:
            action (str): action whose hotkey needs to be changed
            keys (str): new keys for that action
        """
        self.find_and_click(self._action_label.replace("__action__", action), refresh=True, double_click=True)
        self.find_and_click(self._edit_focus_prim_btn, refresh=True)
        self._enter_hotkey(keys)
        self.find_and_click(self._save_focus_prim_hotkey_btn, refresh=True)

    
    def navigate_to_hotkeys(self):
        """Opens Hotkeys window"""
        self.omni_driver.select_menu_option("Window/Hotkeys")

    
    def add_global_hotkey(self, action: str, keys: str):
        """Adds a global hotkey

        Args:
            action (str): Action that the hotkey shall perform
            keys (str): The key to perform the action
        """
        self.wait.element_to_be_located(self.omni_driver, self._add_global_hotkey_btn)
        self.find_and_click(self._add_global_hotkey_btn, refresh=True, double_click=True)
        self._select_action(action)
        self._enter_hotkey(keys)
        self._save_hotkey()
        self.log.info("Hotkey Saved")
        self.screenshot("hotkey_saved")

    
    def add_new_window_hotkey(self, window_name: str, action: str, keys: str):
        """Adds a new window and makes a new hotkey inside it

        Args:
            window_name (str): Name of new window to be create
            action (str): Action that the hotkey shall perform
            keys (str): the key to perform that action
        """
        self._add_window(window_name)
        self._click_add_new_window_hotkey()
        self._select_action(action)
        self._enter_hotkey(keys)
        self._save_hotkey()
        self.screenshot("New window hotkey added")

    
    def edit_global_hotkey(self, action: str, new_hotkey: str):
        """Edits global hotkey

        Args:
            action (str): Action whose hotkey needs to be edited
            new_hotkey (str): New hotkey
        """
        self.find_and_click(self._expand_global_window)
        self._scroll_element_to_top("Command->Redo")
        self._edit_hotkey(action, new_hotkey)
        self.log.info("Hotkey edited")
        self.screenshot("Hotkey_edited")
        self.omni_driver.wait(3)

    
    def restore_defaults(self):
        """Restores hotkeys to default"""
        self.find_and_click(self._restore_default_hamburger)
        self.omni_driver.select_context_menu_option("Restore Defaults")
        self.wait.element_to_be_located(self.omni_driver, self._handle_warning_window)
        self.find_and_click(self._handle_warning_window)
