# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Content Model class
   This module contains the base methods for Base toolbar window
"""
import pyperclip


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.driver.exceptions import ElementNotFound, PropertyRetrieveFailed
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.waits import Wait
import time


class BaseContentModel(BaseModel):
    """Base model class for Content window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for content window
    _content_root_window = "Content"
    _directory_path_picker = "Content//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _directory_explorer_window = "Content//Frame/**/content_browser_treeview_grid_view"
    _directory_structure_window = "Content//Frame/**/content_browser_treeview_folder_view"
    _checkpoints_list = (
        "Content//Frame/VStack[0]/HStack[1]/**/CollapsableFrame[1]/**/VStack[1]/ZStack[0]/TreeView[0]/ZStack[*]"
    )
    _checkpoints_indices = "Content//Frame/**/CollapsableFrame[1]/**/TreeView[0]/ZStack[*]/**/HStack[0]/Label[0]"
    _separator_2 = "Content//Frame/VStack[0]/HStack[1]/ZStack[0]/Placer[0]/Rectangle[0]"
    _checkpoints_description = "Content//Frame/**/CollapsableFrame[1]/**/TreeView[0]/ZStack[*]/**/HStack[0]/Label[1]"
    _content_grid_item = "Content//Frame/**/content_browser_treeview_grid_view/**/Label[0].text=='__filename__'"
    _import_btn = "Import Options//Frame/VStack[0]/HStack[1]/Button[0].text=='Import'"
    _file_image_provider = "Content//Frame/**/content_browser_treeview_grid_view/__frame__/**/ImageWithProvider[0]"
    _options_btn = "Content//Frame/VStack[0]/HStack[0]/HStack[0]/VStack[0]/Button[0]"
    _content_view = "Content//Frame/VStack[0]/HStack[1]/ZStack[0]/HStack[0]/HStack[0]/ZStack[1]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/Button[0]"
    _tags_column = "Content//Frame/**/ScrollingFrame[1]/content_browser_treeview/Label[0]"
    _tags = "Content//Frame/**/ScrollingFrame[1]/content_browser_treeview/Frame[*]/Label[0]"
    _search_bar_folder_btn = (
        "Content//Frame/VStack[0]/HStack[0]/HStack[0]/ZStack[0]/HStack[1]" + "/**/Button[*].text=='__folder__'"
    )

    # New Connection locators
    _add_new_connection = "Content//Frame/**/Label[*].text=='Add New Connection ...'"
    _content_window = "Content//Frame/VStack[0]"
    _new_connection_server_name_txtbox = "Add Nucleus connection//Frame/**/StringField[0]"
    _new_connection_server_ok_btn = "Add Nucleus connection//Frame/**/Button[*].text=='Ok'"
    _new_connection_server_cancel_btn = "Add Nucleus connection//Frame/**/Button[*].text=='Cancel'"
    _server_added = "Content//Frame/**/Label[*].text=='__server__'"
    _folder_label = "Content//Frame/**/Label[*].text=='__name__'"
    _content_slider = "Content//Frame/**/IntSlider[0]"
    _content_item_label = "Content//Frame/**/content_browser_treeview_grid_view/**/Label[0].text=='__name__'"
    _content_item_label_all = "Content//Frame/**/content_browser_treeview_grid_view/**/Label[*]"

    # New USD dialog
    _new_usd_textbox = "New USD//Frame/**/StringField[0]"
    _new_usd_create_btn = "New USD//Frame/**/Button[0]"

    # Create bookmark dialog
    _create_bookmark_textbox = "Add Bookmark//Frame/**/StringField[0]"
    _create_bookmark_ok_btn = "Add Bookmark//Frame/**/Button[0]"

    _bookmark_lable = "Content//Frame/**/content_browser_treeview_folder_view/HStack[3]/Label[0].text=='__label__'"
    _content_browser_label = "Content//Frame/**/content_browser_treeview_grid_view/**/Label[0].text=='__name__'"
    _content_browser_tree_view_label = (
        "Content//Frame/**/content_browser_treeview_folder_view/**/Label[0].text=='__name__'"
    )

    # New Folder dialog
    _new_folder_textbox = "Create folder//Frame/**/StringField[0]"
    _new_folder_ok_btn = "Create folder//Frame/**/Button[0]"

    # drag_drop
    _parent_frames = "Content//Frame/**/content_browser_treeview_grid_view/Frame[*]"

    # Collection Options
    _select_collection_folder = "Collection Options//Frame/**/Button[*].name=='folder'"
    _start_collect = "Collection Options//Frame/**/Button[*].text=='Start'"
    _usd_only_chkbox = "Collection Options//Frame/**/HStack[0]/CheckBox[0]"
    _material_only_chkbox = "Collection Options//Frame/**/HStack[1]/CheckBox[0]"
    _flat_collection_chkbox = "Collection Options//Frame/**/HStack[2]/CheckBox[0]"
    _flat_collection_texture_combobox = "Collection Options//Frame/**/ComboBox[0]"
    _collecting_window = "Collecting"
    _search_field = "Content//Frame/VStack[0]/HStack[0]/HStack[0]/HStack[0]/Frame[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/HStack[0]/StringField[0]"
    _search_label = "Content//Frame/VStack[0]/HStack[0]/HStack[0]/HStack[0]/Frame[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/HStack[0]/ZStack[0]/HStack[0]/Label[0]"
    _search_x_button = "Content//Frame/VStack[0]/HStack[0]/HStack[0]/HStack[0]/Frame[0]/ZStack[0]/HStack[0]/VStack[2]/HStack[0]/VStack[0]/Button[0]"

    # Move overwrite dialog
    _move_window = "MOVE//Frame/**/VStack[0]"
    _move_confirm_btn = "MOVE//Frame/**/Button[0].text=='Confirm'"

    # Opening a Read Only File
    _open_original_file = "Opening a Read Only File//Frame/VStack[0]/VStack[0]/HStack[1]/Button[0]"

    _please_wait_window = "Please Wait"

    # save this stage dialog window
    _save_this_stage_dialog_window = f"""__exclamation_glyph__"""
    _save_this_stage_dialog_save_btn = f"""__exclamation_glyph__//Frame/**/Button[*].text=="Save" """
    _save_this_stage_dialog_dont_save_btn = f"""__exclamation_glyph__//Frame/**/Button[*].text=="Don't Save" """
    _save_this_stage_dialog_cancel_btn = f"""__exclamation_glyph__//Frame/**/Button[*].text=="Cancel" """

    _directory_path_buttons = "Content//Frame/VStack[0]/HStack[0]/HStack[0]/ZStack[0]/HStack[1]/VStack[0]/HStack[0]/ZStack[0]/ZStack[0]/HStack[1]/ScrollingFrame[0]/ZStack[0]/VStack[0]/HStack[0]/Frame[0]/HStack[0]/Button[*]"

    _converting_window = "Converting..."

    _script_node_warning = "Warning"
    _script_node_warning_btn = "Warning//Frame/**/Button[*].text=='{}'"

    _login_required = "Login Required"
    _login_required_cancel_btn = "Login Required//Frame/**/Button[*].text=='Cancel'"

    # content list view locators
    # _content_item_label = "Content//Frame/**/content_browser_treeview/HStack[*]/Label[0].text=='__name__'"
    # _content_item_label_all = "Content//Frame/**/content_browser_treeview/HStack[*]/Label[*]"
    # _content_browser_label = "Content//Frame/**/content_browser_treeview_folder_view/HStack[*]/Label[0].text=='__name__'"
    # _parent_frames = "Content//Frame/**/content_browser_treeview/HStack[*]"

    def handle_save_this_stage_pop_up(self, response: str):
        try:
            window: OmniElement = self.wait.element_to_be_located(
                self.omni_driver,
                self._save_this_stage_dialog_window.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
            )
            self.wait.visibility_of_element(window)
        except (ElementNotFound, PropertyRetrieveFailed):
            self.log.info("'Save this stage' pop up did not appear")
            return
        self.log.info("Found 'Save this stage' pop up")
        if response.lower() == "save":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_save_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Save'")
        elif response.lower() == "don't save":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_dont_save_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Don't Save'")
        if response.lower() == "cancel":
            self.omni_driver.find_element(
                self._save_this_stage_dialog_cancel_btn.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")
                ),
                refresh=True,
            ).click()
            self.log.info("Clicked 'Cancel'")
        self.wait.invisibility_of_element(window)
        self.log.info("'Save this stage' pop up handled")

    def ae_create_new_folder(self, folder_name: str):
        """Adds a new folder in Current Directory"""
        explorer = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(menupath="New Folder")
        textbox = self.omni_driver.find_element(self._new_folder_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(folder_name)
        self.find_and_click(self._new_folder_ok_btn)

    def rename_file_or_folder(self, path: str, file_or_folder: str, folder_name: str):
        """Renames a  file or folder"""
        target = self.step_verify_file_exists(path=path, file_or_folder=file_or_folder)
        if not target:
            self.log.warning("[BaseContentModel] Failed to find %s in %s", file_or_folder, path)
            return
        target.right_click()
        self.omni_driver.select_context_menu_option("Rename")
        self.omni_driver.emulate_key_press(button=KeyboardConstants.tab)
        self.omni_driver.emulate_char_press(folder_name)
        self.omni_driver.emulate_key_press(button=KeyboardConstants.enter)

    def _do_path_exists(self, directory_path: str, is_local_storage: bool = False):
        """Verifies if path exists"""
        if is_local_storage:
            path = directory_path
        else:
            path = self._updated_path(directory_path)
        search_bar: OmniElement = self.omni_driver.find_element(self._directory_path_picker)
        search_bar.click(bring_to_front=True)
        self.omni_driver.wait(3)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)
        folders = path.replace("omniverse://", "").split("/")
        try:
            for folder in folders:
                self.omni_driver.find_element(self._search_bar_folder_btn.replace("__folder__", folder))
            return True
        except:
            return False

    def find_directory(self, name="Omniverse"):
        """Returns the Directory Folder"""
        query_directory = f"/**/Label[0].text=='{name}'"
        return self.omni_driver.find_element(locator=self._directory_structure_window + query_directory)

    def _upload_file(self, file: str, source: str, is_local_storage: bool = False):
        """Uploads  a file in given folder"""
        explorer = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.select_context_menu_option(menupath="Upload Files and Folders")
        self.step_handle_file_explorer(file_name=file, path=source, is_local_storage=is_local_storage)

    def add_folder_path(self, omniverse_folder: str):
        """Adds the folder in given directory"""
        if self._do_path_exists(omniverse_folder):
            self.log.info("[BaseContentModel] Folder path %s already exists", omniverse_folder)
            self.screenshot("path_exists")
            return
        self.log.info("[BaseContentModel] Adding folder path %s", omniverse_folder)
        self.omni_driver.create_folder(omniverse_folder)

    def step_upload_files(self, destination: str, server_folder: str, files: list, is_local_storage: bool = False):
        """Uploads a file to given location"""
        self.add_folder_path(destination)
        # upload
        for file in files:
            self.log.info('Upload file: "%s" in "%s" from "%s"', file, destination, server_folder)
            self._upload_file(file=file, source=server_folder, is_local_storage=is_local_storage)

    def step_verify_file_exists(self, path: str, file_or_folder: str):
        "Verifies the file/folder exists in given Path"
        if not self._do_path_exists(directory_path=path):
            self.log.error("%s path does not exists", path)
            return False
        query_target = self._parent_frames + f"/**/Label[0].text=='{file_or_folder}'"
        try:
            target = self.omni_driver.find_element(locator=query_target, refresh=True)
            return target
        except:
            return False

    def step_handle_file_explorer(
        self,
        path: str,
        file_name: str,
        window="Select File or Folder",
        submit_button="Open",
        is_local_storage=False,
        skip_file_name=False,
    ):
        """Handes the File Explorer Operation"""
        save_path = f"{window}//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
        directory_path = self.omni_driver.find_element(save_path)
        if not is_local_storage:
            path = self._updated_path(path)
        directory_path.send_keys("")
        directory_path.send_keys(path)
        if not skip_file_name:
            new_file_name = f"{window}//Frame/VStack[0]/HStack[2]/ZStack[0]/**/StringField[0]"
            new_file_name = self.omni_driver.find_element(new_file_name)
            new_file_name.double_click()
            self.omni_driver.emulate_char_press(file_name)
        submit_button = f"{window}//Frame/**/Button[*].text=='{submit_button}'"
        self.omni_driver.find_element(submit_button, True).click()

    def delete_a_file_or_folder(self, path: str, file_or_folder: str):
        """Deletes a  file or folder"""
        target = self.step_verify_file_exists(path=path, file_or_folder=file_or_folder)
        if not target:
            self.log.warning("[BaseContentModel] Failed to find %s in %s", file_or_folder, path)
            return
        target.right_click()
        self.omni_driver.select_context_menu_option("Delete")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(button=KeyboardConstants.enter)
        assert not self.step_verify_file_exists(
            path=path, file_or_folder=file_or_folder
        ), f"Failed to perform Delete on {file_or_folder} in {path}"

    def copy_paste_a_dir(self, source: str, file_or_folder: str, destination: str):
        """Copy and Paste an item at given destination"""
        self.add_folder_path(destination)
        target = self.step_verify_file_exists(path=source, file_or_folder=file_or_folder)
        target.right_click()
        self.omni_driver.select_context_menu_option("Copy")
        assert self._do_path_exists(directory_path=destination), "Destination folder Not Found"
        explorer = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.select_context_menu_option("Paste", offset_y=1)
        self.omni_driver.wait(2)

    def select_file(self, directory_path: str, file: str):
        """
        Navigates to the directory and selects the file

        :param directory_path: path where the file can be found
        :param file: file to be selected
        """
        self._do_path_exists(directory_path=directory_path)
        file_context = self.step_verify_file_exists(directory_path, file)
        file_context.click()

    def switch_content_view(self):
        """switch content view from grid view to list view"""
        content_view = self.omni_driver.find_element(self._content_view)
        content_view.click()

    def switch_grid_view(self):
        """switch grid view by resizing to 1"""
        self.navigate_to_content_window()
        self.omni_driver.find_element(self._content_slider).send_keys(1)

    def is_tags_column_visible(self):
        """Returns True if tags column is visible, False otherwise"""
        tags_column = self.omni_driver.find_element(self._tags_column)
        column_val = tags_column.get_text()
        return True if "Tags" in column_val else False

    def search(self, attr):
        """Performs search operation"""
        search_bar = self.omni_driver.find_element(self._search_field)
        search_bar.click(bring_to_front=True)
        self.omni_driver.wait(3)
        search_bar.send_keys(attr)
        self.omni_driver.wait(5)

    def found_in_search_result(self, attr, val):
        """verifies if the value is found in result ot not
        :param attr: folder/file/tag
        :param val: value to search for
        :return Bool
        """
        if attr == "folder":
            res = self.omni_driver.find_element(self._folder_label.replace("__name__", val))

        if attr == "tag":
            tags_list = [tag.get_text() for tag in self.omni_driver.find_elements(self._tags)]
            match_found = [match for match in tags_list if val in match]
            res = len(match_found) > 0
        return True if res else False

    def open_file_with_path(self, directory_path: str, file: str):
        """
        Navigates to the directory and Opens the file in viewport

        :param directory_path: path where the file can be found
        :param file: file to be selected
        """
        self._do_path_exists(directory_path=directory_path)
        file_context = self.step_verify_file_exists(directory_path, file)
        file_context.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(timeout=200)

    def get_checkpoint_indices(self):
        """

        :return: indices_order : list
        """
        checkpoints_indices = self.omni_driver.find_elements(self._checkpoints_indices)
        indices_order = [int(_.get_text()[1:-1]) for _ in checkpoints_indices]
        return indices_order

    def perform_checkpoint_actions(self, checkpoint, menu_option):
        """
        performs action on checkpoint from context menu

        :param checkpoint: checkpoint on which action to be performed
        :param menu_option: option to select from context menu
        """
        checkpoint.right_click()
        self.omni_driver.select_context_menu_option(menu_option)
        if menu_option == "Open":
            self.omni_driver.wait(2)
            self.omni_driver.wait_for_stage_load()
        return

    def expand_vertical_separator(self, locator: str, expand_by_val: int, expand_to: str):
        """
        expands the vertical separator in context menu
        :param locator: separator locator
        :param expand_by_val: val with which separator has to expand
        :param expand_to: left/right
        :return: initial_pos_x, expanded_pos_x
        """

        element = self.omni_driver.find_element(locator)
        initial_pos_x = element.get_size_and_position("screen_position_x")
        initial_pos_y = element.get_size_and_position("screen_position_y")
        expand_pos_x = initial_pos_x - expand_by_val if expand_to == "left" else initial_pos_x + expand_by_val
        element.drag_and_drop(expand_pos_x, initial_pos_y)
        expanded_pos_x = element.get_size_and_position("screen_position_x")
        return initial_pos_x, expanded_pos_x

    def _click_add_connection(self):
        """Clicks on add new connection option"""
        self.find_and_click(self._add_new_connection)

    def _enter_new_connection_server(self, server_name: str):
        """Enter the connection details for the serer

        Args:
            server_name (str): Server name
        """
        self.omni_driver.find_element(self._new_connection_server_name_txtbox).send_keys(server_name)
        self.screenshot("Entered_Server_details")
        ok_btn = self.omni_driver.find_element(self._new_connection_server_ok_btn, refresh=True)
        ok_btn.click()

    def add_new_connection(self, server_name: str, resize: bool = False):
        "Adds new connection"
        self.find_directory().click()
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        self._click_add_connection()
        self._enter_new_connection_server(server_name)

    def navigate_to_content_window(self):
        """Navigates to content window"""
        property_window = self.omni_driver.find_element(self._content_window)
        property_window.click()
        self.screenshot("navigated_to_content_window")

    def verify_server_added(self, server: str):
        """Verifies if server has been successfully added or not

        Args:
            server (str): server name
        """
        server_label = self._server_added.replace("__server__", server)
        self.wait.element_to_be_located(self.omni_driver, server_label)

    def navigate_to_path(self, directory: str, folder_to_search: str = None):
        """Navigates to a specified path in nucleus server

        Args:
            directory (str): Path for navigation
            folder_to_search(str) : Folder to search after navigating to check successfull navigation
        """
        searchbar = self.omni_driver.find_element(self._directory_path_picker)
        searchbar.send_keys(directory)
        if folder_to_search:
            self.wait.element_to_be_located(self.omni_driver, self._folder_label.replace("__name__", folder_to_search))
        self.omni_driver.wait(5)

    def open_file(self, directory: str):
        """Opens a specified file from content browser

        Args:
            directory (str): Directory of folder/file to locate
        """
        path = directory.split("/")
        if len(path) == 1:
            file = self.omni_driver.find_element(self._folder_label.replace("__name__", path[0]))
            file.double_click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(self._folder_label.replace("__name__", item))
                self.omni_driver.wait(1)

        self.omni_driver.wait(5)
        self.omni_driver.wait_for_stage_load()

    def get_checkpoint_description(self, ind):
        """
        returns checkpoint description at following index
        :param ind: starts from 0

        """
        checkpoints_description = self.omni_driver.find_elements(self._checkpoints_description)
        return checkpoints_description[ind].get_text()

    def open_usd_file(
        self,
        file_name: str,
        folder_path: str,
        is_local_storage: bool = False,
        isreadonly: bool = False,
        handle_dont_save: bool = False,
        handle_please_wait: bool = False,
        timeout: int = 200,
        ignore_please_wait_exception=False,
        ignore_timeout_exception: bool = False
    ):
        """
        Opens the usd file from Content browser window
        Args:
            file_name: File name to be opened
            folder_path: Path of the folder in which file resides
            is_local_storage: File is saved on local storage or server storage
            isreadonly: File is read only or not
            handle_dont_save: Don't Save window to be handled or not
            handle_please_wait: Please wait window to be handled or not
            timeout: Timeout for Window appearance/disappearance
            ignore_please_wait_exception: Please Wait window exception to be ignored or not

        Returns:
            Files opened in Viewport

        Raises:
            ElementNotFound: If element could not be located.
        """
        if not file_name.endswith((".usd", ".usdc", ".usda", ".live")):
            self.log.error("[BaseContentModel] Provide file name with '.usd', '.usda', '.usdc' or '.live' extension.")
            return

        retry = 3
        while retry:
            if self._do_path_exists(directory_path=folder_path, is_local_storage=is_local_storage):
                break
            retry -= 1
        if retry == 0:
            self.log.error("%s path does not exists", folder_path)
            return False
        query_target = self._parent_frames + f"/**/Label[0].text=='{file_name}'"

        target: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
        target.double_click()

        self.omni_driver.wait(2)

        if isreadonly:
            original_file = self.wait.element_to_be_located(self.omni_driver, self._open_original_file)
            original_file.click()
        if handle_dont_save:
            self.handle_save_this_stage_pop_up("don't save")
        if handle_please_wait:
            try:
                wait = Wait(timeout)
                wait.element_to_be_located(self.omni_driver, self._please_wait_window)
                wait.window_to_be_invisible(self.omni_driver, self._please_wait_window)
            except ElementNotFound as e:
                if ignore_please_wait_exception:
                    self.log.info("Ignored 'Please Wait' window appearance.")
                else:
                    self.log.info("'Please Wait' window could not be located.")
                    raise e
        self.omni_driver.wait(2)
        try:
            self.omni_driver.wait_for_stage_load(timeout=timeout)
        except:
            if ignore_timeout_exception:
                self.log.info("Timeout while loading scene. Ignore exception and continue.")
            else:
                raise
        self.screenshot(f"opened_scene_{file_name}")

    def save_with_options(self, with_comment: bool = False, description: str = ""):
        self.omni_driver.emulate_key_combo_press("CTRL+ALT+S")
        if with_comment:
            try:
                query_target = r"Select Files to Save##file.py//Frame/**/StringField[*]"
                checkpoint_desc_elm: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
                if checkpoint_desc_elm:
                    height = checkpoint_desc_elm.get_size_and_position("computed_height")
                    if height > 0:
                        checkpoint_desc_elm.send_keys(description)
                    else:
                        self.log.info("Comment box not found in the save menu.")
            except:
                pass

        try:
            query_target = r"Select Files to Save##file.py//Frame/**/" r"Button[*].text=='Save Selected'"
            save_btn: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
            save_btn.click(bring_to_front=True)
            self.log.info("File saved successfully.")
        except:
            self.log.info("Could not close 'Select Files to Save' window")

    def verify_checkpoint_description_exists(self, description, file_name, folder_path):
        if not self._do_path_exists(directory_path=folder_path):
            self.log.error("%s path does not exists", folder_path)
            return False
        query_target = self._parent_frames + f"/**/Label[0].text=='{file_name}'"

        target: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
        target.click()
        self.omni_driver.wait(2)

        checkpoints_descriptions = self.omni_driver.find_elements(self._checkpoints_description)

        description_exists = False
        for desc in checkpoints_descriptions:
            if desc.get_text() == description:
                self.log.info(f"Description: {description} exists for file: {file_name}")
                description_exists = True
                break

        assert description_exists, f"Description: {description} does not exist for file: {file_name}"

    def download_file(self, file_name: str, file_path: str, destination_path, resize: bool = True):
        """Downloads given file

        Args:
            file_name (str): Name of file to be downloaded
            file_path (str): Path of filr
            destination_path (_type_): Download destination of file
            resize (bool, optional): Reduces size of thumbnails. Defaults to True.

        Returns:
            _type_: _description_
        """
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        path_exists = False
        for i in range(2):
            try:
                path_exists = self._do_path_exists(directory_path=file_path)
            except:
                pass
        if not path_exists:
            self.log.error("%s path does not exists", file_path)
            return False

        target: OmniElement = self.omni_driver.find_element(
            locator=self._content_browser_label.replace("__name__", file_name), refresh=True
        )
        target.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Download")
        self.omni_driver.wait(2)

        self.step_handle_file_explorer(
            path=destination_path,
            file_name=file_name,
            window="Download Files",
            submit_button="Save",
            is_local_storage=True,
        )

    def is_save_enabled(self):
        self.omni_driver.emulate_key_combo_press("CTRL+ALT+S")
        self.omni_driver.wait(3)
        save_menu_visible = False
        try:
            query_target = r"Select Files to Save##file.py//Frame/VStack[0]"
            save_menu: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
            save_menu_visible = True
            self.log.info("Save menu opened.")
        except:
            pass

        assert not save_menu_visible, "Save menu should not pop up since there is no change in current file."

    def delete_content(self, content_path: str, content_name: str, resize: bool = True):
        """Deletes given content from the system

        Args:
            content_path (str): Directory path of content to be deleted
            content_name (str): Name of content to be deleted
        """
        directory_path = self.omni_driver.find_element(self._directory_path_picker)
        directory_path.send_keys(content_path)
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        self.omni_driver.wait(5)
        content_item = self.omni_driver.find_element(
            self._content_item_label.replace("__name__", content_name), refresh=True
        )
        self.omni_driver.wait(5)
        content_item.right_click()
        self.omni_driver.select_context_menu_option("Delete")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

    def convert_to_usd_and_open(self, filename: str, drag_to_position):
        """Converts other file format to USD and drags it to viewport to open it

        Args:
            filename (str): Name of the file to open
            drag_to_position (Tuple[float,float]): Co-ordiantes of destination to drag and drop
        """
        try:
            self.omni_driver.wait(5)
            file = self.omni_driver.find_element(self._content_grid_item.replace("__filename__", filename))
            file.right_click()
            self.omni_driver.select_context_menu_option("Convert to USD")
            self.find_and_click(self._import_btn)
            self.wait.timeout = 240
            self.wait.polling_interval = 2
            converting_window = self.wait.element_to_be_located(self.omni_driver, self._converting_window)
            self.wait.invisibility_of_element(converting_window)
            self.wait.timeout = 60
            self.wait.polling_interval = 0.5
            converted_folder = self.omni_driver.find_element(
                self._content_grid_item.replace("__filename__", filename.split(".")[0]), refresh=True
            )
            converted_folder.double_click()
            self.omni_driver.wait(5)
            converted_file_label = self.omni_driver.find_element(
                self._content_grid_item.replace("__filename__", filename.split(".")[0] + ".usd"), refresh=True
            )
            assert converted_file_label, "Converted usd file missing"
            try:
                converted_file = self.omni_driver.find_element(
                    self._file_image_provider.replace("__frame__", "Frame[1]"),
                    refresh=True,
                )
            except ElementNotFound:
                converted_file = self.omni_driver.find_element(
                    self._file_image_provider.replace("__frame__", "Frame[0]"),
                    refresh=True,
                )
            converted_file.drag_and_drop(drag_to_position[0], drag_to_position[1])
            self.omni_driver.wait(10)
            self.omni_driver.wait_for_stage_load()
            self.viewport_screenshot("opened_converted_usd")

        except ElementNotFound:
            self.log.error(f"File with name {filename} is not present")
            self.viewport_screenshot(f"{filename}_not_present")

    def unhide_thumbnail_folders(self):
        """Unhides the thumbnail folder"""
        options_btn: OmniElement = self.omni_driver.find_element(locator=self._options_btn, refresh=True)
        options_btn.click(bring_to_front=True)
        self.omni_driver.wait(3)

        query_target = r"Options//Frame/VStack[0]/ZStack[0]/VStack[0]/HStack[1]/CheckBox[0]"
        checkbox: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)

        if checkbox.is_checked():
            checkbox.click()
            self.log.info("Clicked on 'Hide Thumbnails Folders' checkbox")
            self.omni_driver.wait(2)

    def verify_item_visible(self, name: str, extension: str = ""):
        """Verifies if the item is visible in content window tree view

        Args:
            name (str): name of item to search
        """
        self.omni_driver.wait(2)
        self.find_and_click(self._content_item_label.replace("__name__", name + extension), refresh=True)
        self.log.info(f"Successful in finding {name} in content window.")

    def add_usd_to_tree_view(self, folder: str, file_name: str):
        """Adds a USD to folder from tree view using context menu

        Args:
            folder (str): Name of folder
            file_name (str): Name of USD
        """
        folder_element = self.omni_driver.find_element(
            self._content_browser_tree_view_label.replace("__name__", folder)
        )
        folder_element.right_click()
        self.omni_driver.select_context_menu_option("New USD File")
        textbox = self.omni_driver.find_element(self._new_usd_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(file_name)
        self.find_and_click(self._new_usd_create_btn)

    def add_bookmark(self, folder: str, bookmark_name: str):
        """Add a bookmark for a specific folder

        Args:
            folder (str): Name of folder
            bookmark_name (str): Name of bookmark
        """
        folder_element = self.omni_driver.find_element(self._content_browser_label.replace("__name__", folder))
        folder_element.right_click()
        self.omni_driver.select_context_menu_option("Add Bookmark")
        textbox = self.omni_driver.find_element(self._create_bookmark_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(bookmark_name)
        self.find_and_click(self._create_bookmark_ok_btn)

    def verify_bookmark_added(self, bookmark_name: str):
        """Verifies whether bookmark was added or not

        Args:
            bookmark_name (str): Name of bookmark
        """
        self.omni_driver.find_element(self._bookmark_lable.replace("__label__", bookmark_name))
        self.wait.element_to_be_located(self.omni_driver, self._bookmark_lable.replace("__label__", bookmark_name))

    def open_bookmark(self, bookmark_name: str):
        """Opens added bookmark

        Args:
            bookmark_name (str): Name of bookmark
        """
        self.find_and_click(self._bookmark_lable.replace("__label__", bookmark_name))

    def delete_file(self, name: str, extension: str = ""):
        """Deletes the item in content window tree view

        Args:
            name (str): name of item to search
            extension (str, optional): Extension of file if present. Defaults to "".
        """
        item = self.omni_driver.find_element(
            self._content_item_label.replace("__name__", name + extension), refresh=True
        )
        item.right_click()
        self.omni_driver.select_context_menu_option("Delete")
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.enter)

        try:
            self.omni_driver.find_element(self._content_item_label.replace("__name__", name + extension), refresh=True)
            self.screenshot("file/folder not deleted")
            self.log.info(f"Un-Successful in deleting file/folder {name + extension} in content window.")
            assert False, "File/Folder was not deleted"
        except ElementNotFound:
            self.screenshot("File_Folder_deleted")
            self.log.info(f"Successful in deleting file/folder {name + extension} in content window.")
            assert True

    def delete_bookmark(self, bookmark_name: str):
        """Deletes the added bookmark

        Args:
            bookmark_name (str): Name of the bookmark
        """
        bookmark = self.omni_driver.find_element(self._bookmark_lable.replace("__label__", bookmark_name))
        bookmark.right_click()
        self.omni_driver.select_context_menu_option("Delete")
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.enter)
        try:
            self.omni_driver.find_element(self._bookmark_lable.replace("__label__", bookmark_name), refresh=True)
            self.screenshot("bookmark not deleted")
            self.log.info(f"Un-Successful in deleting bookmark {bookmark_name} in content window.")
            assert False, "Bookmark was not deleted"
        except ElementNotFound:
            self.screenshot("bookmark_deleted")
            self.log.info(f"Successful in deleting bookmark {bookmark_name} in content window.")
            assert True

    def create_folder_context_menu_folder_view(self, target_folder: str, folder_name: str):
        """Creates a folder using context menu in folder view (left section of content window)

        Args:
            target_folder (str): Name of parent folder
            folder_name (str): Name of new folder
        """
        folder_element = self.omni_driver.find_element(
            self._content_browser_tree_view_label.replace("__name__", target_folder)
        )
        folder_element.right_click()
        self.omni_driver.select_context_menu_option("New Folder")
        textbox = self.omni_driver.find_element(self._new_folder_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(folder_name)
        self.find_and_click(self._new_folder_ok_btn)

    def create_folder_context_menu_explorer_view(self, folder_name: str):
        """Creates a folder using context menu in explorer view (Right section of content window)

        Args:
            folder_name (str): Name of new folder
        """
        explorer: OmniElement = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("New Folder")
        textbox = self.omni_driver.find_element(self._new_folder_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(folder_name)
        self.find_and_click(self._new_folder_ok_btn)

    def select_folder(self, folder_name: str):
        """Selects a folder from folder view (left section of content window)

        Args:
            folder_name (str): Name of folder to select
        """
        folder_element = self.omni_driver.find_element(
            self._content_browser_tree_view_label.replace("__name__", folder_name)
        )
        folder_element.click()
        self.omni_driver.wait(2)

    def open_folder(self, folder_name: str):
        """Opens a folder by double clicking on it

        Args:
            folder_name (str): Name of folder to open
        """
        folder_element = self.omni_driver.find_element(self._content_item_label.replace("__name__", folder_name))
        folder_element.double_click()

    def add_usd_to_folder_view(self, folder: str, file_name: str):
        """Adds a USD to folder from folder view using context menu (Wight section of content window)

        Args:
            folder (str): Name of folder
            file_name (str): Name of USD
        """
        folder_element = self.wait.element_to_be_located(
            self.omni_driver, self._content_item_label.replace("__name__", folder)
        )
        folder_element.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("New USD File")
        textbox = self.omni_driver.find_element(self._new_usd_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(file_name)
        self.find_and_click(self._new_usd_create_btn)

    def add_usd_to_explorer_view(self, file_name: str):
        """Adds a USD to folder from folder view using context menu (Right section of content window)

        Args:
            file_name (str): Name of USD
        """

        explorer: OmniElement = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("New USD File")
        textbox = self.omni_driver.find_element(self._new_usd_textbox)
        self.clear_textbox(textbox)
        self.omni_driver.emulate_char_press(file_name)
        self.find_and_click(self._new_usd_create_btn)

    def drag_drop(self, file_name: str, drag_to_position, timeout: int = 60):
        """Drags and drops file with given name to the given position

        Args:
            file_name (str): Name of file
            drag_to_position (_type_): x and y co-ordinates of destination position
        """
        key = f"**/Label[0].text=='{file_name}'"
        self.omni_driver.wait(3)
        _, index = self.get_child_element(self._parent_frames, key)
        frame_locator = self._parent_frames.replace("Frame[*]", f"Frame[{index}]")
        try:
            content_item = self.omni_driver.find_element(frame_locator + "/**/Image[0]", refresh=True)
        except Exception:
            content_item = self.omni_driver.find_element(frame_locator + "/**/ImageWithProvider[0]", refresh=True)
        widget_center = content_item.get_widget_center()
        content_item.click()
        self.omni_driver.wait(1)
        self.omni_driver.drag_from_and_drop_to(
            widget_center[0], widget_center[1], drag_to_position[0], drag_to_position[1]
        )
        self.omni_driver.wait(10)
        self.omni_driver.wait_for_stage_load(timeout=timeout)

    def copy(self, content_name: str, resize: bool = True):
        """Copies given content

        Args:
            content_name (str): name of content to be copied
            resize (bool, optional): resize thumbnails. Defaults to True.
        """
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        key = f"**/Label[0].text=='{content_name}'"
        item, index = self.get_child_element(self._parent_frames, key)
        frame_locator = self._parent_frames.replace("Frame[*]", f"Frame[{index}]")
        self.omni_driver.wait(3)
        self.omni_driver.find_element(frame_locator).right_click()
        self.omni_driver.select_context_menu_option("Copy")

    def paste(self, dest_folder_path: str, dest_folder_name: str, copied_content_name: str, resize: bool = True):
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        self.omni_driver.find_element(self._directory_path_picker).send_keys(dest_folder_path)
        dest_folder = self.omni_driver.find_element(self._content_item_label.replace("__name__", dest_folder_name))
        self.omni_driver.wait(3)
        dest_folder.right_click()
        self.omni_driver.select_context_menu_option("Paste")
        self.omni_driver.wait(3)
        self.omni_driver.find_element(self._directory_path_picker).send_keys(dest_folder_path + dest_folder_name)
        key = f"**/Label[0].text=='{copied_content_name}'"
        self.omni_driver.wait(3)
        item, index = self.get_child_element(self._parent_frames, key)
        frame_locator = self._parent_frames.replace("Frame[*]", f"Frame[{index}]")
        self.omni_driver.wait(3)
        try:
            self.omni_driver.find_element(frame_locator)
            self.screenshot("pasted_successfully")
            self.log.info(f"{copied_content_name} pasted successfully")
        except ElementNotFound:
            self.log.info(f"{copied_content_name} not pasted successfully")

    def add_collection_path_details(self, collection_path: str, collection_name: str):
        select_folder_btn: OmniElement = self.omni_driver.find_element(locator=self._select_collection_folder)
        assert select_folder_btn, "'Select Folder' button not found"
        select_folder_btn.click()
        self.omni_driver.wait(2)
        self.step_handle_file_explorer(
            path=collection_path,
            file_name=collection_name,
            window="Select Collect Destination",
            submit_button="Select",
        )

    def collect_asset(self, path: str, file: str, collection_path: str, collection_name: str, mode="", timeout=120):
        if not self.step_verify_file_exists(path=path, file_or_folder=file):
            assert False, f"File: {file} does not exist under path: {path}"

        query_target = self._parent_frames + f"/**/Label[0].text=='{file}'"
        file: OmniElement = self.omni_driver.find_element(locator=query_target, refresh=True)
        file.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Collect Asset")
        self.omni_driver.wait(2)

        # add collection path
        self.add_collection_path_details(collection_path, collection_name)
        self.omni_driver.wait(2)

        # select mode
        flat_check_box: OmniElement = self.omni_driver.find_element(locator=self._flat_collection_chkbox)
        usd_check_box: OmniElement = self.omni_driver.find_element(locator=self._usd_only_chkbox)
        material_check_box: OmniElement = self.omni_driver.find_element(locator=self._material_only_chkbox)
        if mode.lower() == "":
            if flat_check_box.is_checked():
                flat_check_box.click()
            if usd_check_box.is_checked():
                usd_check_box.click()
            if material_check_box.is_checked():
                material_check_box.click()
        if mode.lower() == "usd":
            if flat_check_box.is_checked():
                flat_check_box.click()
            if not usd_check_box.is_checked():
                usd_check_box.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retry = 4
                while not usd_check_box.is_checked() and retry > 0:
                    usd_check_box.click()
                    self.omni_driver.wait(1)
                    retry -= 1
                assert usd_check_box.is_checked(), "Failed to choose 'USD Only' mode"
            if material_check_box.is_checked():
                material_check_box.click()
            self.log.info("Checked 'USD Only' checkbox and unchecked others")
        if mode.lower() == "material":
            if flat_check_box.is_checked():
                flat_check_box.click()
            if usd_check_box.is_checked():
                usd_check_box.click()
            if not material_check_box.is_checked():
                material_check_box.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retry = 4
                while not material_check_box.is_checked() and retry > 0:
                    material_check_box.click()
                    self.omni_driver.wait(1)
                    retry -= 1
                assert material_check_box.is_checked(), "Failed to choose 'Material Only' mode"
            self.log.info("Checked 'Material Only' checkbox and unchecked others")
        if mode.lower() == "flat":
            if not flat_check_box.is_checked():
                flat_check_box.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retry = 4
                while not flat_check_box.is_checked() and retry > 0:
                    flat_check_box.click()
                    self.omni_driver.wait(1)
                    retry -= 1
                assert flat_check_box.is_checked(), "Failed to choose 'Flat Collection' mode"
            if usd_check_box.is_checked():
                usd_check_box.click()
            if material_check_box.is_checked():
                material_check_box.click()
            self.log.info("Checked 'Flat Collection' checkbox and unchecked others")
            self.select_item_by_index_from_combo_box(self._flat_collection_texture_combobox, index=0)

        # start collection of assets
        start_btn: OmniElement = self.omni_driver.find_element(locator=self._start_collect, refresh=True)
        start_btn.click()

        timeout = time.time() + timeout
        collecting_window = None
        collection_started = False
        while time.time() < timeout:
            try:
                collecting_window: OmniElement = self.omni_driver.find_element(
                    locator=self._collecting_window, refresh=True
                )
            except ElementNotFound:
                pass
            if collecting_window and not collection_started:
                collection_started = True
            if collection_started:
                if collecting_window.is_visible() is False:
                    break
        assert collection_started, f"Collecting Window never found."
        assert collecting_window.is_visible() is False, f"Collection was not completed in the time provided."
        self.log.info(f"Collection of assets completed.")

    def collection_verification(self, base_dir: str, collection_name: str, files: dict):
        for file, rel_path in files.items():
            target = None
            for i in range(2):
                path = base_dir + "/" + collection_name + rel_path
                target = self.step_verify_file_exists(path=path, file_or_folder=file)
                if target:
                    break
            assert target, f"Could not find file: {file} under collection in path: {path}"

    def get_item_count_in_folder(self, folder_path: str, is_local_storage=False):
        self._do_path_exists(directory_path=folder_path, is_local_storage=is_local_storage)
        try:
            items = self.omni_driver.find_elements(self._content_item_label_all)
            self.log.info(f"{len(items)} items found under path: {folder_path}")
            return len(items)
        except ElementNotFound:
            self.log.info(f"0 items found under path: {folder_path}")
            return 0

    def copy_url_link(self, content_name: str, resize: bool = True):
        """Copies folder or files url location

        Args:
            content_name (str): name of file or folder including extension
            resize (bool, optional): Shrinks down thumbnail size. Defaults to True.
        """
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        content_item = self.omni_driver.find_element(self._content_item_label.replace("__name__", content_name))
        self.omni_driver.wait(2)
        content_item.right_click()
        self.omni_driver.select_context_menu_option("Copy URL Link")
        self.omni_driver.wait(2)

    def verify_copy_url_link(self, content_name):
        """Verifies if correct URL is copied

        Args:
            content_name (_type_): name of content whose URL is copied
        """
        url = pyperclip.paste()
        content = url.split("/")[-1]
        directory = url[: url.rfind(content)]
        self.step_verify_file_exists(directory, content)

    def get_folder_center(self, folder_name: str):
        """Gets the center coordinates of folder

        Args:
            folder_name (str): Name of destination folder

        Returns:
            Tuple: Center coordinates of targeted folder
        """
        folder = self.omni_driver.find_element(self._content_item_label.replace("__name__", folder_name))
        folder_center = list(folder.get_widget_center())
        folder_center[1] = folder_center[1] - 50  # Adding a offset to account for folder image
        return tuple(folder_center)

    def handle_move_overwrite_dialog(self, confirm: bool = True):
        """Handles moves confirm window

        Args:
            confirm (bool, optional): Whether to confirm the dialog. Defaults to True.
        """

        window = self.omni_driver.find_element(self._move_window)
        if window:
            if confirm:
                self.find_and_click(self._move_confirm_btn)

    def delete_stale_test_file(self, path: str, content_name: str, resize=True):
        """Delete stale files if any from the path provided

        Args:
            path (str): path location of folder/file to be deleted
            content_name (str): name of content to be deleted
            resize (bool, optional): Resizes thumbnails in content window. Defaults to True.
        """
        self.navigate_to_content_window()
        if resize:
            self.omni_driver.find_element(self._content_slider).send_keys(1)
        self.navigate_to_path(path)
        try:
            content_item = self.omni_driver.find_element(
                self._content_item_label.replace("__name__", content_name), refresh=True
            )
            self.omni_driver.wait(5)
            content_item.right_click()
            self.omni_driver.select_context_menu_option("Delete")
            self.omni_driver.wait(2)
            self.omni_driver.emulate_key_press(KeyboardConstants.enter)
            self.log.info("Directory was cleaned")
        except ElementNotFound:
            self.log.info("Directory is Clean")

    def enter_path_and_navigate(self, path: str, assert_file_or_folder: str):
        """Enters path and navigates to it

        Args:
            path (str): Destination path
            assert_file_or_folder (str): To check file/folder present in path for successful navigation
        """
        self.find_and_enter_text(self._directory_path_picker, path)
        self.wait.element_to_be_located(
            self.omni_driver, self._content_item_label.replace("__name__", assert_file_or_folder)
        )

    def open_file_folder(
            self,
            directory: str,
            stage_load_timeout: int = 240,
            isreadonly: bool = False,
            wait_timeout: int = 120
            ):
        """Opens a specified file from content browser

        Args:
            directory (str): Directory of folder/file to locate
            stage_load_timeout (int, optional): Timeout for stage to finish loading. Defaults to 60.
        """
        path = directory.split("/")
        if len(path) == 1:
            file = self.omni_driver.find_element(self._content_item_label.replace("__name__", path[0]))
            file.double_click()
        if len(path) > 1:
            for item in path:
                self.find_and_click(self._content_item_label.replace("__name__", item))
                self.omni_driver.wait(1)
        if isreadonly:
            original_file = self.wait.element_to_be_located(self.omni_driver, self._open_original_file)
            original_file.click()

        self.omni_driver.wait(5)
        wait = Wait(wait_timeout)
        wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)
        self.omni_driver.wait_for_stage_load(stage_load_timeout)

    def open_folder_location(self, folder_path: str, is_local_storage: bool = False):
        """
        Opens folder location in content window
        :param folder_path: path of the folder
        :param is_local_storage: whether it is local storage
        :return: True if folder is opened else False
        """
        if not self._do_path_exists(directory_path=folder_path, is_local_storage=is_local_storage):
            self.log.error("%s path does not exists", folder_path)
            return False
        return True

    def create_new_python_script(self, script_name: str, script_type: str):
        """
        Creates new python script in content window
        :param script_name: new name for the script
        :param script_type: type of script: BehaviorScript or Empty
        """
        explorer: OmniElement = self.omni_driver.find_element(self._directory_explorer_window)
        explorer.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(menupath=f"New Python Script ({script_type})")
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.escape)
        self.omni_driver.wait(1)
        explorer.right_click()
        self.omni_driver.select_context_menu_option(menupath=f"New Python Script ({script_type})")
        self.omni_driver.wait(2)

        self.log.info("Typing script name")
        self.omni_driver.emulate_char_press(script_name)
        self.log.info("Press Enter key")
        self.omni_driver.emulate_key_press(KeyboardConstants.enter)

        # verify whether new script is visible in content browser
        query_target = self._parent_frames + f"/**/Label[0].text=='{script_name}.py'"
        try:
            self.wait.element_to_be_located(self.omni_driver, query_target)
            self.log.info(f"New python script created: {script_name}.py")
        except ElementNotFound:
            self.log.info(f"Failed to create new python script: {script_name}.py")

    def get_current_directory_path(self):
        """Retrieves path of current directory

        Returns:
            str: path of current directory
        """
        path_buttons = self.omni_driver.find_elements(self._directory_path_buttons)
        last_button = path_buttons[-1]
        return last_button.get_name()

    def edit_file(self, file_path: str, file_name: str):
        """Edits a file from content window

        Args:
            file_path (str): Path of the file
            file_name (str): Name of the file
        """
        self.navigate_to_path(file_path)
        content_file = self.wait.element_to_be_located(
            self.omni_driver, self._content_grid_item.replace("__filename__", file_name)
        )
        content_file.right_click()
        self.omni_driver.select_context_menu_option("Edit...")

    def edit_python_script(self, file_path: str, file_name: str):
        """Edits a python script from content window

        Args:
            file_path (str): Path of the file
            file_name (str): Name of the file
        """
        self.navigate_to_path(file_path)
        content_file = self.wait.element_to_be_located(
            self.omni_driver, self._content_grid_item.replace("__filename__", file_name)
        )
        content_file.right_click()
        self.omni_driver.select_context_menu_option("Edit Python Script")

    def get_latest_file_checkpoint(self, file_path: str, file_name: str):
        """Selects file and returns latest checkpoint number

        Args:
            file_name (str): name of file
            file_path (str): path of file
        """
        self.select_file(file_path, file_name)
        self.omni_driver.wait(5)
        return self.get_checkpoint_indices()[0]

    def get_checkpoint_count(self, file_path: str, file_name: str):
        """Selects file and returns number of checkpoints

        Args:
            file_name (str): name of file
            file_path (str): path of file
        """
        self.select_file(file_path, file_name)
        self.omni_driver.wait(5)
        checkpoints_indices = self.omni_driver.find_elements(self._checkpoints_indices)
        return len(checkpoints_indices)

    def expand_folder(self, folder: str, check_sub_folder: str = None):
        """Expands a folder in the tree view
        Args:
            folder (str): category to expand
            check_sub_folder (str): presence of sub category to be checked
        """
        label: OmniElement = self.omni_driver.find_element(
            self._content_browser_tree_view_label.replace("__name__", folder), True
        )
        label.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.omni_driver.wait(1)
        y = label.get_widget_center()[1]
        x = label.get_size_and_position("screen_position_x")

        # TODO: remove the retries after click issue gets resolved (OM-102905)
        retry = 4
        while retry:
            try:
                self.omni_driver.click_at(x - 35, y)
                self.omni_driver.wait(1)
                self.omni_driver.find_element(
                    self._content_browser_tree_view_label.replace("__name__", check_sub_folder), True
                )
                break
            except ElementNotFound:
                retry -= 1
        if retry == 0:
            self.log.info(f"Could not expand {folder} folder in 4 tries.")

    def tree_view_folder_exists(self, folder: str):
        try:
            self.omni_driver.find_element(self._content_browser_tree_view_label.replace("__name__", folder), True)
            return True
        except ElementNotFound:
            return False

    def resize_window(self, width: float, height: float):
        """Resizes the Content Window
        Args:
            width (float): new width
            height (height): new height
        """
        window: OmniElement = self.omni_driver.find_element(self._content_root_window, True)
        window.resize_window(width, height)
        self.log.info(f"Resized Content Window to new dimensions: {width} x {height}")

    def select_validate_usd(self, path: str, file: str):
        """
        Selects the validate USD option from the context menu
        Args:
            path: USD file path
            file: USD file name
        Returns: Selection of the validate USD option from the context menu
        Raises:
            ElementNotFound: when the element is not found in UI
            Exception: when context menu selection fails
        """
        self.select_context_menu_option(path, file, option="Validate USD")

    def select_context_menu_option(self, path, file, option):
        """
        Selects the given option from the context menu
        Args:
            path: USD file path
            file: USD file name
            option: Context menu option to be selected
        Returns: Selection of the given option from the context menu
        Raises:
            ElementNotFound: when the element is not found in UI
            Exception: when context menu selection fails
        """
        target = self.step_verify_file_exists(path=path, file_or_folder=file)
        if not target:
            self.log.warning("[BaseContentModel] Failed to find %s in %s", file, path)
            return
        target.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(option)
        self.omni_driver.wait(2)

    def handle_scriptnode_warning(self, choice: str = "Yes"):
        """Handles the Warning window which appears because of ScriptNode

        Args:
            choice (str, optional): Choice to pick: Yes or No. Defaults to "Yes".
        """
        self.wait.window_to_be_visible(self.omni_driver, self._script_node_warning)
        self.find_and_click(self._script_node_warning_btn.format(choice), refresh=True)
        self.wait.window_to_be_invisible(self.omni_driver, self._script_node_warning)

    def cancel_login_required(self):
        """
        Cancels the login to server prompt
        """
        attempt = 0
        self.omni_driver.wait(10)
        try:
            while attempt < 3:
                cancel_btn = self.omni_driver.find_element(self._login_required_cancel_btn, refresh=True)
                self.omni_driver.wait(1)
                cancel_btn.click()
                self.omni_driver.wait(2)
                attempt += 1
                self.omni_driver.wait(5)
        except ElementNotFound:
            pass