# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Asset Store Model class
   This module contains the base methods for Assets window
"""
import random
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement

from omniui.framework_lib.softassert import SoftAssert
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from typing import List


class BaseAssetStoreModel(BaseModel):
    """Base model class for Assets Store window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _asset_store_window = "Asset Stores (beta)//Frame/VStack[0]"
    _asset_filter = "Asset Stores (beta)//Frame/**/Button[0].name=='filter'"
    _asset_filter_option = "Filter//Frame/**/RadioButton[*].text=='__name__'"
    _filter_context_menu_sketchfab = "Sketchfab"
    _all_assets = "Asset Stores (beta)//Frame/**/ThumbnailView[0]/Frame[*]"
    _vendor_logo = (
        "Asset Stores (beta)//Frame/**/ThumbnailView[0]/**/ZStack[0]/Image[1]"
    )
    _auth_popup = "Authentication"
    _auth_uname = "Authentication//Frame/**/StringField[0]"
    _auth_pwd = "Authentication//Frame/**/HStack[1]/StringField[0]"
    _auth_remember_me_chkbox = "Authentication//Frame/**/CheckBox[0]"
    _auth_okay_btn = "Authentication//Frame/**/HStack[3]/Button[0]"
    _assets_slider = "Asset Stores (beta)//Frame/**/IntSlider[0]"
    _category_tree_view = "Asset Stores (beta)//Frame/VStack[0]/Frame[0]/HStack[0]/ZStack[0]/VStack[0]/VStack[0]/ScrollingFrame[0]"
    _category_tree_view_toggle_btn = (
        "Asset Stores (beta)//Frame/**/Button[*].name=='navigation'"
    )
    _asset_store_search_field = "Asset Stores (beta)//Frame/**/StringField[0]"
    _active_search_keywords = (
        "Asset Stores (beta)//Frame/VStack[0]/Frame[0]/HStack[0]/ZStack[1]"
        "/VStack[0]/HStack[0]/Frame[0]/HStack[0]/ZStack[0]/HStack[0]/ZStack[0]/HStack[0]/HStack[0]/**/Label[*]"
    )
    _search_field_clear_btn = (
        "Asset Stores (beta)//Frame/VStack[0]/Frame[0]/HStack[0]/ZStack[1]"
        "/VStack[0]/HStack[0]/Frame[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/Button[0]"
    )
    _add_to_my_assets_window = r"###WARNING_Add to My Assets//Frame[0]"
    _asset_category = (
        "Asset Stores (beta)//Frame/**/CategoryView[0]/**/Label[*].text=='__name__'"
    )
    _my_assets_settings_btn = (
        "Asset Stores (beta)//Frame/**/CategoryView[0]/**/Button[*]"
    )
    _my_assets_folders_window = "My Assets Folders"
    _asset_folder_remove_btn = "My Assets Folders//Frame/**/Button[*].name=='remove'"
    _asset_folder_add_btn = "My Assets Folders//Frame/**/Button[*].name=='add'"
    _select_directory_for_my_assets_window = "Select Directory for My Assets"
    _my_assets_all_folders = "My Assets Folders//Frame/**/StringField[*]"

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
        save_path = (
            f"{window}//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
        )
        directory_path = self.wait.element_to_be_located(self.omni_driver, save_path)
        if not is_local_storage:
            path = self._updated_path(path)
        # for i in range(2):
        #     directory_path.click()
        #     self.omni_driver.wait(1)
        #     self.omni_driver.emulate_key_combo_press("ALT+A")
        directory_path.send_keys(path)
        if not skip_file_name:
            new_file_name = (
                f"{window}//Frame/VStack[0]/HStack[2]/ZStack[0]/**/StringField[0]"
            )
            new_file_name = self.omni_driver.find_element(new_file_name)
            new_file_name.double_click()
            new_file_name.send_keys(file_name)
        submit_button = f"{window}//Frame/**/Button[*].text=='{submit_button}'"
        self.omni_driver.find_element(submit_button).click()

    def navigate_to_assets(self):
        """Navigates to asset store window"""
        assets_window = self.omni_driver.find_element(self._asset_store_window)
        assets_window.click()
        self.screenshot("navigated_to_asset_store")

    def apply_filter(self, filter: str):
        """Selects and applies Filter option"""
        filter_btn = self.omni_driver.find_element(self._asset_filter)
        filter_btn.click()
        self.omni_driver.wait(1)

        filter_opt: OmniElement = self.omni_driver.find_element(
            self._asset_filter_option.replace("__name__", filter)
        )
        filter_opt.click()
        self.omni_driver.wait(1)
        filter_btn.click()
        self.omni_driver.wait(1)
        filter_opt: OmniElement = self.omni_driver.find_element(
            self._asset_filter_option.replace("__name__", filter), refresh=True
        )
        assert filter_opt.is_checked(), f"Could not apply '{filter}' filter."

    def perform_asset_store_login(self, uname: str, pwd: str, remember_me: bool = True):
        """Performs the authentication flow for third party asset store

        Args:
            uname (str): Username
            pwd (str): Password
            remember_me (bool, optional): Whether to select remember me or not. Defaults to True.
        """
        self.omni_driver.find_element(self._auth_uname).send_keys(uname)
        self.omni_driver.find_element(self._auth_pwd).send_keys(pwd)
        if remember_me:
            chkbox = self.omni_driver.find_element(self._auth_remember_me_chkbox)
            if not chkbox.is_checked():
                chkbox.click()
        self.screenshot("entered_login_details")
        self.find_and_click(self._auth_okay_btn)

    def perform_asset_store_login_prefilled(self, uname: str, pwd: str):
        """Performs the authentication flow for third party asset store when credentials are prefilled

        Args:
            uname (str): Username
            pwd (str): Password
        """
        username = self.omni_driver.find_element(self._auth_uname).get_text()
        password = self.omni_driver.find_element(self._auth_pwd).get_text()

        assert username == uname, "Actual username doesnot match prefilled username"
        assert password == pwd, "Actual username doesnot match prefilled username"
        assert self.omni_driver.find_element(
            self._auth_remember_me_chkbox
        ).is_checked(), "Remember me checkbox is not checked"
        self.screenshot("prefilled_login_details")
        self.omni_driver.find_element(self._auth_okay_btn)

    def select_random_asset(self):
        """Selects a random asset"""
        self.omni_driver.wait(2)
        assets = self.omni_driver.find_elements(self._all_assets)
        rand_value = random.randrange(0, len(assets))
        self.omni_driver.find_element(self._assets_slider).send_keys(50)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(30)

        for _ in range(5):
            assets[rand_value].double_click()
            try:
                self.omni_driver.find_element(self._auth_popup)
                break
            except ElementNotFound:
                pass

    def handle_add_to_my_assets_warning(self, button_txt: str):
        query_target = (
            self._add_to_my_assets_window + f"/**/Button[*].text=='{button_txt}'"
        )
        btn = self.omni_driver.find_element(query_target)
        btn.click()

    def navigate_to_asset_category(self, category: str):
        """Selects an asset category.
        Args:
            category (str): category to select (case-sensitive)
        """
        query_target = self._asset_category.replace("__name__", category)
        category = self.omni_driver.find_element(query_target)
        category.click()
        self.omni_driver.wait(3)
        assert (
            category.is_selected()
        ), f"Could not select asset store category: {category}"

    def get_asset_count(self):
        try:
            assets = self.omni_driver.find_elements(self._all_assets)
            self.log.info(
                f"{len(assets)} assets are currently visible in the Asset Store window."
            )
            return len(assets)
        except ElementNotFound:
            self.log.info("0 assets are currently visible in the Asset Store window.")
            return 0

    def get_all_assets_names(self):
        """Returns names of all assets currently visible in Asset Store window"""
        assets = self.omni_driver.find_elements(self._all_assets)
        names = [
            asset.find_element("**/VStack[*]/Label[0]").get_text() for asset in assets
        ]
        return names

    def select_asset(self, asset_name: str):
        """Selects assets using its name from currently visible in Asset Store window

        Args:
            asset_name (str) : Name of asset to select it"""
        assets = self.omni_driver.find_elements(self._all_assets)
        names = [
            asset.find_element("**/VStack[*]/Label[0]").get_text() for asset in assets
        ]
        # Get index of asset_name from names
        asset_locator = assets[names.index(asset_name)]
        asset_locator.double_click()

    def get_active_search_keywords(self):
        """Returns the active search keywords"""
        try:
            labels = self.omni_driver.find_elements(self._active_search_keywords)
            return [label.get_text() for label in labels]
        except ElementNotFound:
            return []

    def clear_asset_store_search_field(self):
        try:
            btn = self.omni_driver.find_element(self._search_field_clear_btn)
            btn.click()
            self.log.info("Clicked on clear button")
            self.omni_driver.wait_frames(5)
            self.omni_driver.wait_for_stage_load(30)
        except ElementNotFound:
            self.log.info("Clear button not found")

        try:
            keywords = self.omni_driver.find_elements(self._active_search_keywords)
        except ElementNotFound:
            keywords = []

        assert len(keywords) == 0, "Could not clear keywords from search field."

    def remove_all_asset_folders(self):
        settings_btn = self.omni_driver.find_element(self._my_assets_settings_btn)
        settings_btn.double_click()
        self.wait.element_to_be_located(
            driver=self.omni_driver, locator=self._my_assets_folders_window
        )
        try:
            self.wait.element_to_be_located(
                self.omni_driver, self._asset_folder_remove_btn
            )
            btns = self.omni_driver.find_elements(self._asset_folder_remove_btn)
            for btn in btns[:2]:
                btn.double_click()
            self.log.info("Clicked on all 'remove' buttons")
        except ElementNotFound:
            self.log.info(
                "Could not find 'remove' buttons under 'My Asset Folders' window."
            )

        try:
            open_btn = self.omni_driver.find_element(
                self._asset_folder_remove_btn, refresh=True
            )
        except ElementNotFound:
            open_btn = None

        assert (
            not open_btn
        ), "Could not remove all folder paths from 'My Asset Folders' window."
        self.omni_driver.close_window(self._my_assets_folders_window)

    def get_n_assets(self, n):
        """Returns a list of n assets selected randomly from currently visible assets
            Returned list contains tuples of form (asset: OmniElement, name: str)
        Args:
            n (int): number of assets to fetch
        """
        self.omni_driver.wait(2)
        self.omni_driver.find_element(self._assets_slider).send_keys(50)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(30)
        assets = self.omni_driver.find_elements(self._all_assets)

        if n > len(assets):
            return assets

        random_assets = []
        for _ in range(n):
            # Last asset is named More, so removing it
            rnd = random.randrange(0, len(assets) - 1)
            random_assets.append(
                (
                    assets[rnd],
                    assets[rnd].find_element("**/VStack[*]/Label[0]").get_text(),
                )
            )
            del assets[rnd]
        return random_assets

    def download_n_assets(
        self,
        n: int,
        path: str,
        user: str,
        pwd: str,
        is_local_storage: bool = False,
        ignore_warning_if_not_found: bool = False,
    ):
        """Downloads n random assets from currently visible assets

        Args:
            n (int): number of assets to download
            path (str): destination folder path for downloading assets
            user (str): sketchfab username
            pwd (str): sketchfab password
            is_local_storage (bool): represent download path is of local storage, defaults to False
            ignore_warning_if_not_found (bool): handle warning - Add to my assets, defaults to True

        Returns:
            list of names of downloaded assets
        """
        assets = self.get_n_assets(n)
        names = [asset[1] for asset in assets]
        for index, _ in enumerate(assets):
            assets[index][0].double_click()

            if index == 0:
                self.perform_asset_store_login(user, pwd, remember_me=False)
                self.omni_driver.wait(5)

            self.step_handle_file_explorer(
                path=path,
                file_name="",
                window="Select Directory to Download Asset",
                submit_button="Select",
                skip_file_name=True,
                is_local_storage=is_local_storage,
            )
            if index == 0:
                try:
                    self.wait.element_to_be_located(
                        self.omni_driver, self._add_to_my_assets_window
                    )
                    self.handle_add_to_my_assets_warning(button_txt="Yes")
                except ElementNotFound as element_not_found:
                    if not ignore_warning_if_not_found:
                        raise element_not_found
            self.omni_driver.wait(5)
        self.omni_driver.wait(5)

        return names

    def search_asset(self, query: str):
        """Toggles the tree view

        Args:
            query (str): search query
        """
        search_field = self.omni_driver.find_element(self._asset_store_search_field)
        search_field.send_keys(query)

    def toggle_tree_view(self, visible: bool):
        """Toggles the tree view

        Args:
            visible (bool): visibility flag
        """
        toggle_btn: OmniElement = self.omni_driver.find_element(
            self._category_tree_view_toggle_btn
        )
        tree_view: OmniElement = self.omni_driver.find_element(self._category_tree_view)

        if visible and not tree_view.is_visible():
            toggle_btn.click()
        if not visible and tree_view.is_visible():
            toggle_btn.click()
        self.omni_driver.wait(2)

        assert not (
            visible ^ tree_view.is_visible()
        ), f"Could not toggle {'on' if visible else 'off'} tree view"

    def validate_asset_vendors(self, vendors: List[str]):
        """Validates the vendors of visible assets belong only to list of expected vendors.

        Args:
            vendors (list): list of vendors
        """
        assertion = SoftAssert()

        vendor_logos: List[OmniElement] = self.omni_driver.find_elements(
            self._vendor_logo
        )
        vendors_set = set()

        for vendor_logo in vendor_logos:
            belongs_to_list = False
            for vendor in vendors:
                if vendor.lower() in vendor_logo.image_source() or (
                    vendor.lower() == "my assets"
                    and "folder" in vendor_logo.image_source()
                ):
                    vendors_set.add(vendor)
                    belongs_to_list = True
                    break
            assertion.expect(
                belongs_to_list,
                (
                    "Vendor mentioned in source: "
                    f"{vendor_logo.image_source()} does not belong to "
                    f"list of expected vendors: {vendors}. "
                    "Note: 'My Assets' uses 'folder' icon"
                ),
            )
        for vendor in vendors:
            assertion.expect(
                vendor in vendors_set, f"Could not find assets for filter: {vendor}"
            )
        assertion.assert_all()

    def add_my_assets_folders(self, folder_paths: list):
        """Adds list of folders to My Assets section

        Args:
            folders: list of folders to be added
        """
        settings_btn = self.omni_driver.find_element(self._my_assets_settings_btn)
        settings_btn.click()
        self.omni_driver.wait_for_stage_load()
        self.wait.element_to_be_located(
            driver=self.omni_driver, locator=self._my_assets_folders_window
        )

        for path in folder_paths:
            add_btn: OmniElement = self.omni_driver.find_element(
                self._asset_folder_add_btn, refresh=True
            )
            add_btn.double_click()
            self.omni_driver.wait_for_stage_load()
            self.step_handle_file_explorer(
                path=path,
                file_name=None,
                window=self._select_directory_for_my_assets_window,
                submit_button="Select",
                skip_file_name=True,
            )
            self.omni_driver.wait(10)

        added_folder_elms = self.omni_driver.find_elements(self._my_assets_all_folders)
        added_folders = [elm.get_text() for elm in added_folder_elms]
        assert set(folder_paths) == set(
            added_folders
        ), f"Folders mismatch. List of received folders: {folder_paths}, List of added folders: {added_folders}"

        self.omni_driver.close_window(self._my_assets_folders_window)
        self.omni_driver.wait(3)

    def add_random_asset(self, mode: str, *args):
        """Adds a random asset

         Args:
            position (Float): X and Y position of destination co ordinate

        Returns:
            Asset Name: Returns the name of applied asset
        """
        self.omni_driver.wait(2)
        assets = self.omni_driver.find_elements(self._all_assets)
        rand_value = random.randrange(0, len(assets))
        self.omni_driver.find_element(self._assets_slider).send_keys(50)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(30)

        if mode == "double_click":
            assets[rand_value].double_click()
        elif mode == "drag":
            position = args[0]
            assets[rand_value].drag_and_drop(position[0], position[1])
        else:
            self.log.info(f"{mode} is invalid argument.")
        try:
            self.omni_driver.find_element(self._auth_popup)
        except ElementNotFound:
            pass
