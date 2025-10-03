# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Layer Model class
   This module contains the base methods for Base toolbar window
"""


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound

class BasePreferenceModel(BaseModel):
    """Base model class for Preference window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """
    _root = "Preferences//Frame/HStack[0]"
    _preferences_window = "Preferences"
    _preference_option = "Preferences//Frame/**/TreeView[0]/Label[*].text=='{0}'"
    _preference_menu = "Preferences//Frame/**/preferences_builder_{0}"
    _ui_fps_limit_chkbox = "**/Frame[0]/**/HStack[5]/**/CheckBox[0]"
   
    _ui_fps_limit_floatdrag = "**/Frame[0]/**/HStack[7]/FloatDrag[0]"
    _ui_material_add_custom_path = "**/Frame[0]/preferences_builder_{0}/**/Button[0]"
    _ui_material_save_custom_path = "**/Frame[0]/preferences_builder_{0}/**/Button[0].text=='Save'"
    _ok_button_path = "{0}//Frame/**/Button[0].text=='OK'"
    _preference_combobox = "Preferences//Frame/**/ComboBox[0]"
    _screenshot_path = "Preferences//Frame/**/preferences_builder_Capture Screenshot/**/StringField[0]"
    _capture_only_3D_viewport = "Preferences//Frame/**/preferences_builder_Capture Screenshot/**/CheckBox[0]"
    _multi_gpu_combobox = "Preferences//Frame/**/preferences_builder_Multi-GPU/**/ComboBox[0]"
    _preference_menu_tmp = "Preferences//Frame/VStack[0]/HStack[1]/ScrollingFrame[0]"
    
    def navigate_window(self):
        """Navigate to Preference"""
        self.omni_driver.select_menu_option("Edit/Preferences")
        self.omni_driver.wait(2)
        visible_windows = self.omni_driver.get_windows()["visible_windows"]
        self.log.info(f"Visible windows: {visible_windows}")
        assert self._preferences_window in visible_windows, "Unable to navigate to Preference window"


    def close(self):
        """Closes Preference Window"""
        self.close_window("Preferences")

    def _select_preference_menu_option(self, menu="Stage"):
        """Selects the Menu in Preferences"""
        ele = self.omni_driver.find_element(self._preference_option.format(menu), refresh=True)
        ele.scroll_into_view(axis=ScrollAxis.Y, scroll_amount=ScrollAmount.CENTER)
        x = ele.get_size_and_position("screen_position_x")
        y = ele.get_size_and_position("screen_position_y")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.wait(2)
        ele.double_click()
        self.omni_driver.wait(seconds=2)

    def _select_preference_menu_item(self, item_name="Import"):
        """Selects Preference Menu Item"""
        query = self._preference_menu.format(item_name)
        menu = self.find(query, refresh=True)
        menu.scroll_into_view(axis=ScrollAxis.Y, scroll_amount=ScrollAmount.CENTER)
        self.omni_driver.wait(seconds=2)
        return menu

    def select_stage_import_preference(self, preference=1):
        """
        Selects Preference for drag and drop
        Preference=> 0: Payload 1: Reference
        Default: 1
        """
        self._select_preference_menu_option()
        menu = self._select_preference_menu_item()
        option_box = menu.find_element("/**/ComboBox[*]")
        option_box.select_item_from_combo_box(stack_combo=True, index=preference, name="")
        self.omni_driver.wait(seconds=1)

    
    def get_screenshot_directory(self):
        """Returns Screenshot Directory"""
        self._select_preference_menu_option("Capture Screenshot")
        menu = self._select_preference_menu_item("Capture Screenshot")
        return menu.find_element("**/StringField[*]").get_text()

    
    def toggle_material_distilling(self, enable: bool):
        """Toggles Material Distilling

        Args:
            enable (bool): Whether to enable to disable
        """
        scroll_element = self.omni_driver.find_element(self._preference_option.format("Navigation"))
        x = scroll_element.get_size_and_position("screen_position_x")
        y = scroll_element.get_size_and_position("screen_position_y")
        self.omni_driver.wait(5)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.wait(5)
        self.find_and_scroll_element_into_view(
            self._preference_option.format("Navigation"), axis=ScrollAxis.Y, scroll_amount=ScrollAmount.TOP
        )
        self._select_preference_menu_option("Rendering")
        menu = self._select_preference_menu_item("MDL")
        chkbox = menu.find_element("**/CheckBox[0]")
        if enable:
            if not chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("material_distilling_enabled")
        else:
            if chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("material_distilling_disabled")

    def toggle_fps_limit(self, enable: bool, fps: int = None):
        """Toggles and sets FPS rendering limit

        Args:
            enable (bool): Whether to enable to disable
        """
        self._select_preference_menu_option("Rendering")
        menu = self._select_preference_menu_item("Throttle Rendering")
        chkbox = menu.find_element(self._ui_fps_limit_chkbox)
        if enable:
            if not chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("enabled UI FPS limit")
                if fps:
                    fps_slider = menu.find_element(self._ui_fps_limit_floatdrag)
                    fps_slider.send_keys(fps)
                    self.log_info_with_screenshot(f"Set FPS limit as {fps}")
        else:
            if chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("disabled UI FPS limie")

    def add_material_custom_path(self):
        """
        Opens select file dialog to add Custom Paths in Material Search Path
        """
        self._select_preference_menu_option("Material")
        menu = self._select_preference_menu_item("Material Search Path")
        add_button_locator = menu.find_element(
            self._ui_material_add_custom_path.format("Custom Paths (requires app restart)")
        )
        add_button_locator.scroll_into_view(axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM)
        add_button_locator.double_click()
        self.omni_driver.wait(seconds=2)

    def add_material_custom_path_save(self):
        """
        Save Custom Paths added in Material Search Path
        """
        current_windows = self.omni_driver.get_windows()["visible_windows"]
        menu = self._select_preference_menu_item("Material Search Path")
        save_button_locator = menu.find_element(
            self._ui_material_save_custom_path.format("Custom Paths (requires app restart)")
        )
        save_button_locator.scroll_into_view(axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM)
        save_button_locator.click()
        self.omni_driver.wait(seconds=2)
        new_windows = self.omni_driver.get_windows()["visible_windows"]
        added_window = [window for window in new_windows if window not in current_windows]
        assert len(added_window) == 1, "More than 1 window is added"
        ok_button_locator = self.omni_driver.find_element(self._ok_button_path.format(added_window[0]))
        ok_button_locator.click()
        self.omni_driver.wait(seconds=2)

    
    def update_screenshot_path(self, path):
        """
        Updates the screenshot path
        """
        self.omni_driver.wait(1)
        self.find_and_enter_text(self._screenshot_path, path)
        self.omni_driver.wait(1)

    
    def verify_capture_3d_viewport_checked(self, is_checked=False):
        """
        Verifies the Capture only the 3D viewport checkbox status
        """
        current_status = self.omni_driver.find_element(self._capture_only_3D_viewport).is_checked()
        assert (
            current_status == is_checked
        ), f"Capture Only 3D viewport checkbox is {current_status}, but expected {is_checked}"

    def get_measure_tool_startup_setting(self):
        """Returns the current startup tool setting"""
        self._select_preference_menu_option("Measure")
        menu = self._select_preference_menu_item("Measure Settings")
        combobox_data = menu.find_element("**/ComboBox[*]", True).get_combobox_info()
        return combobox_data["current_value"]

    def set_measure_tool_startup_setting(self, option_name: str):
        """Sets the current startup tool setting

        Args:
        option_name(str): Name of the setting option
        """
        self._select_preference_menu_option("Measure")
        menu = self._select_preference_menu_item("Measure Settings")
        combobox = menu.find_element("**/ComboBox[*]", True)
        combobox.select_item_from_combo_box(None, option_name, False)
        self.omni_driver.wait(1)

    @property
    def get_white_mode_properties(self):
        self._select_preference_menu_option("Rendering")
        menu = self._select_preference_menu_item("White Mode")
        exceptions = menu.find_element("**/HStack[1]/StringField[*]").get_text()
        material = menu.find_element("**/HStack[0]/StringField[*]").get_text()
        return {
            "Exceptions": exceptions,
            "Material": material
        }

    def is_rendering_option_present(self):
        try:
            self.omni_driver.find_element(self._preference_option.format("Rendering"),refresh=True)
            return True
        except ElementNotFound:
            return False
       
    
    def change_multi_gpu_setting(self,index : int):
        """Chnage the rendering gpu setting to auto true or false"""
        self._select_preference_menu_option(menu="Rendering")
        menu = self._select_preference_menu_item("Multi-GPU")
        combobox = menu.find_element("**/ComboBox[*]", True)
        combobox.select_item_from_combo_box(index=index,name=None,stack_combo=False)
        self.omni_driver.wait(1)

    def verify_multi_gpu_setting(self):
        """verifies the gpu rendering gpu setting"""
        
        self._select_preference_menu_option(menu="Rendering")
        menu = self._select_preference_menu_item("Multi-GPU")
        combobox = menu.find_element("**/ComboBox[*]", True)
        value = combobox.get_combobox_info()["current_value"]
        assert value=="False","GPU Rendering value is True"
        self.omni_driver.wait(1)

    def toggle_fabric_scene_delgate(self, enable: bool):
        """Toggles Fabric Scene Delegate

            Args:
            enable (bool): Whether to enable to disable
        """
        self.navigate_window()
        scroll_element = self.omni_driver.find_element(self._preference_menu_tmp,refresh=True)
        x = scroll_element.get_size_and_position("screen_position_x")
        y = scroll_element.get_size_and_position("screen_position_y")
        self.omni_driver.wait(5)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.wait(5)
        self.find_and_scroll_element_into_view(
            self._preference_option.format("Rendering"), axis=ScrollAxis.Y, scroll_amount=ScrollAmount.TOP
        )
        self._select_preference_menu_option("Rendering")
        menu = self._select_preference_menu_item("Fabric Scene Delegate")
        chkbox = menu.find_element("**/CheckBox[0]")
        if enable:
            if not chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("fsd_enabled")
        else:
            if chkbox.is_checked():
                chkbox.click()
                self.log_info_with_screenshot("fsd_disabled")

    def query_rendering_setting(self, setting : str):
        """Queries any setting under Rendering Menu
 
            return True for ON and False for OFF
        """
        self.navigate_window()
        scroll_element = self.omni_driver.find_element(self._preference_menu_tmp,refresh=True)
        x = scroll_element.get_size_and_position("screen_position_x")
        y = scroll_element.get_size_and_position("screen_position_y")
       
        self.find_and_scroll_element_into_view(
            self._preference_option.format("Rendering"), axis=ScrollAxis.Y, scroll_amount=ScrollAmount.CENTER,refresh=True
        )
        self.omni_driver.emulate_mouse_move(x, y) # move cursor to refresh the scroll frame
        self.omni_driver.wait(1)
 
        self._select_preference_menu_option("Rendering")
        menu = self._select_preference_menu_item(setting)
        chkbox = menu.find_element("**/CheckBox[0]")
        return chkbox.is_checked()

