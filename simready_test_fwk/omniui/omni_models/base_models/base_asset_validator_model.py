"""Base Asset Validator model class
   This module contains the base methods for Asset Validator Model for actions to perform
"""
import re
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from ..base_models.base_model import BaseModel


class BaseAssetValidatorModel(BaseModel):
    """BaseAssetValidator class containing common methods"""

    _asset_validator_window = "Asset Validator"
    # Widget Locators
    _source_combobox = "Asset Validator//Frame/VStack[0]/HStack[0]/ComboBox[0]"
    _browse_uri_btn = "Asset Validator//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/Button[0]"
    _asset_validator_btn = "Asset Validator//Frame/**/Button[*].text == '{}'"
    _validation_section = "Asset Validator//Frame/**/CollapsableFrame[*].title == '{}'"
    _checkbox_label = "**/Label[0].text == '{}'"
    _checkbox = "/CheckBox[0]"
    _btn_path = "**/Button[*].text == '{}'"
    _asset_validator_window_btn = "Asset Validator//Frame/**/Button[*].text == '{}'"
    _result_table = "Asset Validator//Frame/VStack[0]/HStack[1]/VStack[0]/VStack[0]/ScrollingFrame[0]/TreeView[0]"
    _result_table_text = _result_table + """/**/Label[0].text == "{}" """
    _root_triangle = _result_table + "/HStack[0]/Triangle[0]"
    _root_row_checkbox = _result_table + "/VStack[0]/CheckBox[0]"
    _result_rule_name = _result_table + "/Label[*].text == '{}'"
    _save_fixes_checkbox = "Asset Validator//Frame/VStack[0]/HStack[2]/HStack[0]/CheckBox[0]"
    _directory_path_picker = "Select an Asset to Validate//Frame/**/StringField[*].identifier == 'filepicker_directory_path'"
    _search_bar_folder_btn = "Select an Asset to Validate//Frame/VStack[0]/HStack[0]/ZStack[0]/HStack[1]/**/Button[*].text=='__folder__'"
    _file_or_folder_label = "Select an Asset to Validate//Frame/**/None_grid_view/Frame[*]/**/Label[0].text=='__name__'"
    _import_btn = "Select an Asset to Validate//Frame/**/Button[*].text == 'Import'"

    def toggle_check_box(self, configuration: str, checkbox_name: str, check_on: bool = True):
        """
        Toggles the given checkbox in given configuration checker_rule
        Args:
            configuration: Parent configuration for the rule
            checkbox_name: Rule Checker name
            check_on: True if check box needs to turn on else False
        Returns: Turn on/off checkbox
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        section_element = self.omni_driver.find_element(
            self._validation_section.format(configuration),
            refresh=True)
        label_element = section_element.find_element(self._checkbox_label.format(checkbox_name),
                                                     refresh=True)
        checkbox_locator = f"{label_element.find_parent_element_path()}{self._checkbox}"
        self.toggle_checkbox(checkbox_locator, check_on)

    def analyze_usd(self):
        """
        Analyzes the USD file
        Returns: Results of the asset validation analysis
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        self.find_and_click(self._asset_validator_btn.format(" Analyze"))
        self.log.info("Analyze button is clicked.")
        self.omni_driver.wait(2)
        self.wait.element_to_be_located(self.omni_driver, self._root_triangle)
        self.screenshot("usd_file_analyzed")

    def click_button(self, button_name: str):
        """
        Clicks on the given button in Asset Validator window
        Args:
            button_name: Button to be clicked
        Returns: Button clicks on UI
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        self.find_and_click(self._asset_validator_btn.format(button_name))
        self.log.info(f"{button_name} button is clicked.")
        self.omni_driver.wait(2)

    def expand_checker_rule(self, checker_rule: str = "root", expand: bool = True):
        """
        Expands or collapses the specific rule results from the result table
        Args:
            checker_rule: Rule name
            expand: True to expand else False to collapse
        Returns: Expanded or collapsed checker rule in result table
        Raises:
            ElementNotFound: when the element is not found in UI
        """
        if checker_rule == "root":
            self.expand_section(self._root_triangle, expand=expand)
            return
        locator = self._result_rule_name.format(checker_rule)
        label_element = self.omni_driver.find_element(locator, refresh=True)
        element_path = label_element.path
        match = re.search(r'\[(\d+)\]$', element_path)
        last_number = int(match.group(1))
        triangle_locator = element_path.replace(f"/TreeView[0]/Label[{last_number}]",
                                                f"/TreeView[0]/HStack[{last_number + 2}]/Triangle[0]")
        self.expand_section(triangle_locator, expand=expand)

    def click_button_from_category(self, category_name: str, button_name: str):
        """
        Clicks on the button inside the specified category
        Args:
            category_name: Validation category name
            button_name: Button name
        Returns: Clicked on the button inside the specified category
        Raises:
            ElementNotFound if error is not found when it is expected
        """
        category_element = self.omni_driver.find_element(
            self._validation_section.format(category_name),
            refresh=True)
        button_element = category_element.find_element(self._btn_path.format(button_name),
                                                       refresh=True)
        button_element.click()

    def verify_error_warning_info(self, info: str):
        """
        Verifies the error or warning information in the result table
        Args:
            info: Info to be verified.
        Returns: Verification of the error or warning information in the result
        Raises:
            AssertionError : when the assertion fails
        """
        label_elements = self.omni_driver.find_elements(self._result_table_text.format(info))
        assert len(label_elements) > 0, f"No error found with '{info}' details."

    def verify_checker_error_present(self, checker_name: str, present=True):
        """
        Verifies the specific checker error is present in the result table
        Args:
            checker_name: Checker name
            present: True if present else False
        Returns:
        Raises:
            ElementNotFound if error is not found when it is expected
            Exception if error is found when it is not expected
        """
        try:
            label_element = self.omni_driver.find_element(
                self._result_rule_name.format(checker_name), refresh=True)
            if present:
                self.log_info_with_screenshot(f"Error found for {checker_name}",
                                              f"{checker_name}_error")
            else:
                self.log_error_with_screenshot(f"Error found for {checker_name}",
                                               f"{checker_name}_error_found")
                raise Exception(f"Error found for {checker_name}")

        except ElementNotFound as e:
            if present:
                self.log_error_with_screenshot(f"Error not found for {checker_name}",
                                               f"{checker_name}_error_not_found")
                raise e
            else:
                self.log_info_with_screenshot(f"Error not found for {checker_name}",
                                              f"{checker_name}_error_not_found")

    def navigate_to_asset_validator(self):
        """
        Opens the asset validator window
        Returns: Asset validator window opened from the menubar
        Raises:
            Exception: when the menu option is not available
        """
        self.omni_driver.select_menu_option("Window/Utilities/Asset Validator")
        self.omni_driver.wait(2)
        visible_windows = self.omni_driver.get_windows()["visible_windows"]
        self.log.info(f"Visible windows: {visible_windows}")
        return self._asset_validator_window in visible_windows

    def select_source_from_combobox(self, index: int):
        """
        Selects the asset source for validation from the combobox
        Args:
            index: Index for the combobox option, Uri: 0, Stage:1
        Returns: Option selected in the combobox
        Raises:
            ElementNotFound: when element is not found on UI
            ElementNotInteractable: when element could not be interacted during sendkeys action
        """
        self.select_item_from_stack_combo_box(self._source_combobox, index=index)
        self.omni_driver.wait(1)
        self.screenshot(f"selected_{index}_item")

    def select_asset_to_validate(self, path, file):
        """
        Select the asset to validate in asset validation window
        Args:
            path: Asset file path
            file: Asset file name
        Returns: Asset selected in the asset validation window
        Raises:
            ElementNotFound: when element is not found on UI
            ElementNotInteractable: when element could not be interacted during sendkeys action
        """
        self.find_and_click(self._browse_uri_btn)
        search_bar = self.omni_driver.find_element(self._directory_path_picker)
        self.omni_driver.wait(1)
        search_bar.send_keys(path)
        self.omni_driver.wait(5)
        self.wait.element_to_be_located(self.omni_driver,
                                        self._file_or_folder_label.replace("__name__", file))
        self.screenshot(f"navigated_to_{file}_location")
        self.find_and_click(self._file_or_folder_label.replace("__name__", file), refresh=True)
        self.omni_driver.wait(2)
        self.find_and_click(self._import_btn, refresh=True)
        self.omni_driver.wait(1)

    def toggle_checkbox_from_asset_validator(self, checkbox_name: str, check_on: bool = True):
        """
        Toggles the save fixes checkbox on asset validator window
        Returns: Save fixes on or off
        Raises:
            ElementNotFound: when the element is not found in UI
            Exception: when context menu selection fails
        """
        checkbox_dict = {
            "save_fixes": self._save_fixes_checkbox,
            "root_row_checkbox": self._root_row_checkbox
        }
        self.toggle_checkbox(checkbox_dict[checkbox_name], check_on=check_on)
