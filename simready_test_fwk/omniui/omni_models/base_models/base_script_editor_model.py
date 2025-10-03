# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Script Editor Model class
   This module contains the base methods for Script Editor window
"""
from ..base_models.base_model import BaseModel


from omni_remote_ui_automator.common.constants import KeyboardConstants


class BaseScriptEditorModel(BaseModel):
    """Base model class for Script Editor window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _script_editor_window = "Script Editor"
    _directory_path_picker ="Open...//Frame/**/StringField[*].identifier == 'filepicker_directory_path'"
    _search_bar_folder_btn = "Open...//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    _file_or_folder_label = "Open...//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"

    def navigate_to_script_editor(self):
        """Navigates to Script Editor window"""
        self.omni_driver.select_menu_option("Window/Script Editor")
        self.wait.window_to_be_visible(self.omni_driver, self._script_editor_window)

    def hide_script_editor(self):
        """Hide Script Editor window"""
        self.omni_driver.select_menu_option("Window/Script Editor")
        self.wait.window_to_be_invisible(self.omni_driver, self._script_editor_window)

    def enable_replicator_preview(self):
        """Enable Replicator Preview"""
        self.omni_driver.select_menu_option("Replicator/Preview")
        self.omni_driver.wait(2)
    
    def enable_replicator_start(self):
        """Enable Replicator Run"""
        self.omni_driver.select_menu_option("Replicator/Start")
        self.omni_driver.wait(2)

    def enable_replicator_stop(self):
        """Enable Replicator Stop"""
        self.omni_driver.select_menu_option("Replicator/Stop")
        self.omni_driver.wait(2)

    def enable_replicator_pause(self):
        """Enable Replicator Pause"""
        self.omni_driver.select_menu_option("Replicator/Pause")
        self.omni_driver.wait(2)

    def enable_replicator_step(self):
        """Enable Replicator Step"""
        self.omni_driver.select_menu_option("Replicator/Step")
        self.omni_driver.wait(2)

    def enable_replicator_resume(self):
        """Enable Replicator Resume"""
        self.omni_driver.select_menu_option("Replicator/Resume")
        self.omni_driver.wait(2)
        
    def execute_script(self, script: str):
        """Executes a script.
        Args:
            script (str): script to execute
        """
        dimensions = self.omni_driver.get_window_dimensions(self._script_editor_window)
        x_pos = dimensions["position_x"] + dimensions["width"] / 2
        y_pos = dimensions["position_y"] + dimensions["height"] - 100

        self.omni_driver.click_at(x_pos, y_pos)
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.control + "+" + KeyboardConstants.a_key)
        self.omni_driver.emulate_char_press(script)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.control + "+" + KeyboardConstants.enter)

    def execute_python_file(self, path: str, file: str):
        """
        Loads the python file from the given path and executes it fom script editor
        Returns:
        Raises:
            ElementNotFound: when element is not found on UI
            ElementNotInteractable: when element could not be interacted during sendkeys action
        """
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.left_alt + "+" + KeyboardConstants.o_key)
        self.omni_driver.wait(1)
        self.screenshot("open_file_window")
        search_bar = self.omni_driver.find_element(self._directory_path_picker)
        self.omni_driver.wait(1)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)
        self.wait.element_to_be_located(self.omni_driver, self._file_or_folder_label.replace("__name__", file))
        self.screenshot(f"navigated_to_{file}_location")
        python_file = self.omni_driver.find_element(self._file_or_folder_label.replace("__name__", file), refresh=True)
        self.omni_driver.wait(2)
        python_file.double_click()
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.control + "+" + KeyboardConstants.enter)
        self.omni_driver.wait(1)
        self.screenshot("executed_python_file")
    
    
        
