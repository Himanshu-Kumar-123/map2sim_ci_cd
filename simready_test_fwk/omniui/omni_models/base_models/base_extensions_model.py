# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Extensions Model class
   This module contains the base methods for Extensions window
"""
import os
import re
import sys

import pyperclip

import pyperclip
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound

if sys.platform == "win32":
    import autoit
import pyautogui
import time

from selenium.webdriver.remote.webdriver import WebDriver


class BaseExtensionsModel(BaseModel):
    """Base model class for Extensions window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Extensions window
    _search_field = "Extensions//Frame/**/StringField[0]"
    _extension_toggle_btn = "Extensions//Frame/**/ToolButton[0].name=='clickable'"
    _extension_search_result_label = 'Extensions//Frame/**/Label[0].text=="__name__"'
    _merge_selected_btn = (
        "Merge Meshes//Frame/VStack[0]/Button[0].text=='Merge Selected'"
    )
    _feature_category_toggle = (
        "Extensions//Frame/**/TreeView[0]/ZStack[0]/HStack[0]/Image[0].name=='expanded'"
    )
    _general_category_toggle = (
        "Extensions//Frame/**/TreeView[0]/ZStack[1]/HStack[0]/Image[0].name=='expanded'"
    )
    _non_toggleable_category_toggle = (
        "Extensions//Frame/**/TreeView[0]/ZStack[2]/HStack[0]/Image[0].name=='expanded'"
    )
    _community_unverifed_category_toggle = (
        "Extensions//Frame/**/TreeView[0]/ZStack[0]/HStack[0]/Image[0].name=='expanded'"
    )
    _extension_tabs = "Extensions//Frame/HStack[0]/ScrollingFrame[0]/HStack[0]/Frame[*]/ZStack[0]/VStack[0]/HStack[1]/VStack[0]/HStack[0]/Button[__index__]"
    _nvidia_tab = "Extensions//Frame/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/VStack[0]/HStack[1]/Button[0]"
    _third_party_tab = "Extensions//Frame/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/VStack[0]/HStack[1]/Button[1]"
    _autoload = "Extensions//Frame/HStack[0]/ScrollingFrame[0]/HStack[0]/Frame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[0]/HStack[1]/HStack[0]/VStack[0]/ToolButton[0]"
    _detail_label = 'Extensions//Frame/**/ScrollingFrame[0]/**/Frame[*]/ZStack[0]/**/HStack[*]/VStack[0]/HStack[*]/Label[*].text=="__detail__"'
    _id_label = 'Extensions//Frame/**/Label[1].name=="Id"'
    _install_btn = "Extensions//Frame/**/Button[0].text=='INSTALL'"
    _remote_install_label = "Extensions//Frame/**/Label[0].text=='REMOTE'"
    _installed_label = "Extensions//Frame/**/Button[0].text=='UP TO DATE'"
    _failure_icon = "Extensions//Frame/**/Image[*].name=='Failed'"
    _doc_link_button = "Extensions//Frame/**/Button[0].name=='OpenDoc'"
    _install_unverified = "Warning//Frame/**/Button[*].text=='Install'"
    _warning_window = "Warning"
    _options = "Extensions//Frame/**/Button[*].name == 'options'"
    _extension_search_path = "Extensions//Frame/**/Label[0].text == '{}'"
    _extension_folder = "Extensions//Frame/HStack[0]/ScrollingFrame[0]/HStack[0]/Frame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[0]/VStack[2]/Button[0]"
    _extension_folder = "Extensions//Frame/HStack[0]/ScrollingFrame[0]/HStack[0]/Frame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[0]/VStack[2]/Button[0]"

    def check_on_autoload_extension(self, autoload: bool = True):
        """Turn on autoload checkbox in extension

        Args:
            autoload (bool, optional): Enabled or disables the autoload functionality. Defaults to True.
        """
        button = self.omni_driver.find_element(self._autoload, refresh=True)
        if autoload:
            if not button.tool_button_is_checked():
                button.click()
            self.screenshot("autoload enabled")
        else:
            if button.tool_button_is_checked():
                button.click()
            self.screenshot("autoload disabled")

    def navigate_to_extensions(self):
        """Navigates to Extensions window"""
        self.omni_driver.select_menu_option("Window/Extensions")
        self.omni_driver.wait(4)

    def _expand_general_category(self):
        """Expands the general category if not open"""
        try:
            self.find_and_click(self._nvidia_tab)
            self.omni_driver.wait(5)
            self.omni_driver.find_element(self._general_category_toggle)
        except ElementNotFound:
            self.find_and_click(self._general_category_toggle.split(".")[0])

    def _expand_featured_category(self):
        """Expands the featured category if not open"""
        try:
            self.find_and_click(self._nvidia_tab)
            self.omni_driver.wait(5)
            self.omni_driver.find_element(self._feature_category_toggle)
        except ElementNotFound:
            self.find_and_click(self._feature_category_toggle.split(".")[0])

    def _expand_non_toggleable_category(self):
        """Expands the non-toggleable category if not open"""
        try:
            self.find_and_click(self._nvidia_tab)
            self.omni_driver.wait(5)
            self.find_and_click(self._non_toggleable_category_toggle)
        except ElementNotFound:
            self.find_and_click(self._non_toggleable_category_toggle.split(".")[0])

    def expand_community_unverified_category(self):
        """Expands community unverified category if not open"""
        try:
            self.find_and_click(self._third_party_tab)
            self.omni_driver.wait(5)
            self.omni_driver.find_element(self._community_unverifed_category_toggle)
        except ElementNotFound:
            self.find_and_click(self._community_unverifed_category_toggle.split(".")[0])

    def expand_all_categories(self):
        """Expands all categories if not open"""
        self._expand_featured_category()
        self._expand_general_category()
        self._expand_non_toggleable_category()

    def _search_extension(self, ext_id: str):
        """Searches for a specific extension

        Args:
            ext_id (str): ID of the extension
        """
        search_bar = self.omni_driver.find_element(self._search_field, refresh=True)
        search_bar.send_keys(ext_id)

    def _select_extension_from_search_result(self, ext_name: str):
        """Clicks on an extension form search result

        Args:
            ext_name (str): Name of extension
        """
        try:
            self.find_and_click(
                self._extension_search_result_label.replace("__name__", ext_name)
            )
        except ElementNotFound:
            self.expand_community_unverified_category()
            self.find_and_click(
                self._extension_search_result_label.replace("__name__", ext_name)
            )

    def _toggle_extension(self):
        """Toggles an extension"""
        button = self.omni_driver.find_element(self._extension_toggle_btn,refresh=True)
        if not button.tool_button_is_checked():
            button.click()

        # TODO: Remove retry steps after click issue is resolved: OM-102905
        retry = 4
        while not button.tool_button_is_checked() and retry > 0:
            button.click()
            self.omni_driver.wait(1)
            retry -= 1

    def _install_extension(self, unverified=False):
        """Toggles an extension

        Args:
            unverified (bool, optional): Is extension community unverified. Defaults to False.
        """
        button = self.omni_driver.find_element(self._install_btn)
        button.click()
        if unverified:
            self._handle_community_unverified_warning()
        self.wait.element_to_be_located(self.omni_driver, self._installed_label)

    def search_and_enable_extension(
        self,
        ext_id: str,
        ext_name: str,
        enable: bool = True,
        install: bool = False,
        unverified=False,
    ):
        """Searches for an extension and enables it

        Args:
            ext_name (str): Extension name
            ext_id (str): Extension ID
            enable (bool) : Toggle to enable or disable extension
        """
        self._search_extension(ext_id)
        self.expand_all_categories()
        self._select_extension_from_search_result(ext_name)

        if install:
            self.install_extension(unverified)

        if enable:
            self.enable_extension(ext_id, ext_name)
            self.omni_driver.wait_frames(5)
            self.omni_driver.wait(2)

    def navigate_to_merge_mesh(self):
        """Navigates to Merge mesh window"""
        self.omni_driver.select_menu_option("Window/Merge Meshes")
        self.omni_driver.wait(2)

    def merge_selected_meshes(self):
        """Merges selected meshes"""
        self.find_and_click(self._merge_selected_btn)

    def check_extension_tabs(self, ext_id: str, ext_name: str):
        """Checks if overview, changelog, dependencies, packages, tests and omnigraph tabs are present in selected extension"""
        self._search_extension(ext_id)
        self.expand_all_categories()
        self._select_extension_from_search_result(ext_name)
        for i in range(6):
            tab = self._extension_tabs.replace("__index__", str(i))
            self.omni_driver.wait(2)
            self.find_and_click(tab)
        self.omni_driver.find_element(self._search_field).send_keys("")

    def close_extension_window(self):
        """Closes extension window"""
        self.omni_driver.close_window("Extensions")

    def enable_extension(self, ext_id: str, ext_name: str):
        """Enables the specified extension

        Args:
            ext_name (str): Extension name
            ext_id (str): Extension ID
        """
        self._toggle_extension()
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait(2)

    def is_extension_enabled(self, ext_id: str, ext_name: str) -> bool:
        """Checks the extension is enabled or not and return boolean

        Args:
            ext_name (str): Extension name
            ext_id (str): Extension ID
        """
        self._search_extension(ext_id)
        self.expand_all_categories()
        self._select_extension_from_search_result(ext_name)
        button = self.omni_driver.find_element(self._extension_toggle_btn)
        return button.tool_button_is_checked()

    def disable_extension(self, ext_id: str, ext_name: str):
        """Disables the specified extension

        Args:
            ext_name (str): Extension name
            ext_id (str): Extension ID
        """
        try:
            self.is_extension_enabled(ext_id=ext_id, ext_name=ext_name)
            button = self.omni_driver.find_element(self._extension_toggle_btn)
            if button.tool_button_is_checked():
                button.click()
        except:
            self.log.info("Extension is not enabled")
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait(2)

    def install_extension(self, unverified=False):
        """Installs the onscreen extension

        Args:
            unverified (bool, optional): Is extension community unverified. Defaults to False.
        """
        self._install_extension(unverified)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait(2)

    def check_detail_labels(self):
        """Checks if version, description, and title are present in selected extension"""
        for detail in ["version", "description", "title"]:
            locator = self._detail_label.replace("__detail__", self.toml_data[detail])
            self.log.info(f"Finding: {locator}")
            self.omni_driver.find_element(locator)

    def check_ext_id(self):
        """Checks if extension ID displayed meets desired format"""
        pattern = re.compile(r"^[^.\s]+\.[^.\s]+")
        ext_id = self.omni_driver.find_element(self._id_label).get_text()
        assert bool(
            pattern.match(ext_id)
        ), "Extension namespace does not conform to format."

    def check_for_failure_icon(self):
        """Validates the presense of the vailure icon, indicating a failure to install/enable"""
        error = False
        try:
            self.omni_driver.find_element(self._failure_icon)
        except ElementNotFound:
            error = True
            self.log.info("No Failure Icon detected.")
        assert error, "Installation/Enabling of application failed."

    def open_doc(self):
        """Opens documentation of the extension. Browser needs to be open."""
        doc_link_btn = self.wait.element_to_be_located(
            self.omni_driver, self._doc_link_button
        )
        doc_link_btn.click()

    def _handle_community_unverified_warning(self):
        """Handles community unverfied warning that comes during installing community unverified extensions"""
        self.find_and_click(self._install_unverified, False)

    def open_documents_shared_location(self):
        """
        Opens the default shared exts location in Documents
        """
        self.navigate_to_extension_settings()
        doc_shared_path = os.path.join(
            os.path.expanduser("~"), "Documents", "Kit", "shared", "exts"
        )
        if sys.platform == "win32":
            doc_shared_path = doc_shared_path.lower().replace("\\", "/")
        extension_path_element = self.omni_driver.find_element(
            self._extension_search_path.format(doc_shared_path), refresh=True
        )
        element_path = extension_path_element.path.replace("/ZStack[0]/Label[0]", "")
        match = re.search(r"\[(\d+)\]$", element_path)
        last_number = int(match.group(1))
        open_btn_locator = element_path.replace(
            f"/TreeView[0]/HStack[{last_number}]",
            f"/TreeView[0]/HStack[{last_number - 1}]/Button[0]",
        )
        self.omni_driver.wait(1)
        self.find_and_click(open_btn_locator, refresh=True)
        self.omni_driver.wait(3)

    def navigate_to_extension_settings(self):
        """
        Navigate to Settings of the Extension Window
        """
        self.find_and_click(self._options, refresh=True)
        self.omni_driver.select_context_menu_option(menupath="Settings", offset_y=2)
        self.omni_driver.wait(2)

    def search_and_enable_third_party_extension(self, ext_id: str, ext_name: str):
        """
        Search and enable third party extensions
        """
        self._search_extension(ext_id=ext_id)
        self.expand_community_unverified_category()
        self.omni_driver.wait(1)
        self.find_and_click(
            self._extension_search_result_label.replace("__name__", ext_name)
        )
        self.omni_driver.wait(2)
        self.enable_extension(ext_id, ext_name)
        self.omni_driver.wait(2)
        button = self.omni_driver.find_element(self._extension_toggle_btn)
        assert button.tool_button_is_checked(), f"{ext_id} is not enabled."

    def get_extension_path(self):
        """retrieves the path of extension"""
        ext_list = self.omni_driver.get_bundled_extension_list()
        path = [ext['path'] for ext in ext_list if 'omni.graph.scriptnode' in ext['id']][0]
        return path
