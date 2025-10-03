# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Avatar Studio Model class
   This module contains the base methods for Avatar Studio window
"""
import os
from typing import Union
import pyperclip
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omniui.omni_models.avatar_configurator_models.select_file_or_directory_model import *
from omniui.utils.utility_functions import get_downloads_folder_path
from ...utils.app_enums.avatar_configurator import *
from ..base_models.base_model import BaseModel


class AvatarStudioModel(BaseModel):
    """Model class for Avatar Studio window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _window_name = "Avatar Studio"
    _loading_text = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/ZStack[0]/VStack[0]/Label[0]"
    )
    _avatar_filter_field = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/**/PropertyTreeWidget[0]/HStack[0]/**/StringField[0]"
    )
    _avatar_property_text = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/**/PropertyTreeWidget[0]/**/Label[*].text=='{}'"
    )
    _avatar_all_properties = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/**/PropertyTreeWidget[0]/ScrollingFrame[0]/TreeView[0]/*"
    )
    _properties_button = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/**/VisibilityTogglerToolbarWidget[0]/ToolButtonWidget[0]/**/Label[0].text=='Properties'"
    )
    _app_button = (
        _window_name
        + "//Frame/**/AvatarConfiguratorViewWidget[0]/**/ToolButtonWidget[*]/**/Label[0].text=='{}'"
    )

    _image_enabled = "Switch_On.svg"
    _image_disabled = "Switch_Off.svg"

    temp_download_path = os.path.join(
        get_downloads_folder_path(), "temp_avatar_configurator_files"
    )

    _combobox_types = Union[
        AvatarModels,
        SceneModels,
        SceneMoods,
        OutfitModels,
        GlassesModels,
        HeadgearModels,
        EyeColors,
        SkinColors,
    ]
    _colourbox_types = Union[
        ScenePrimaryColors,
        SceneSecondaryColors,
        SceneTertiaryColors,
        OutfitPrimaryColors,
        OutfitSecondaryColors,
        GlassesColors,
        HeadgearColors,
        HairColors,
    ]
    _filepicker_types = Union[
        BackgroundImages,
        OutFitLogo,
    ]
    _all_types = Union[_combobox_types, _colourbox_types, _filepicker_types]

    def wait_for_window_to_load(self) -> None:
        """Waits for a window to load and loading text to become invisible.

        Args:
            None

        Raises:
            TimeoutException: If the window does not load within the timeout period.
        """
        self.wait.timeout = 5 * 60
        self.wait.element_to_be_located(self.omni_driver, self._loading_text)
        _loading_text_parent = self._loading_text[: self._loading_text.rfind("/")]
        _parent_element = self.omni_driver.find_element(_loading_text_parent)
        self.wait.invisibility_of_element(_parent_element)
        self.log.info(
            f"{self._window_name} - LoadingText is located and is not visible"
        )
        self.omni_driver.wait(5)

    def _get_frame_path_from_label(self, label_name: str) -> str:
        """Method to calculate Frame Path using Label"""
        label_element = self.omni_driver.find_element(
            self._avatar_property_text.format(label_name), refresh=True
        )
        zstack_parent_path = "/".join(
            label_element.find_parent_element_path().split("/")[:-1]
        )

        all_property_list = self.omni_driver.find_elements(self._avatar_all_properties)
        zstack_index = frame_path = None
        for index, current_property in enumerate(all_property_list):
            property_path = current_property.path
            index_of_bracket = property_path.rfind("[")
            if zstack_index is None and property_path == zstack_parent_path:
                zstack_index = index
            elif (
                zstack_index is not None
                and property_path[index_of_bracket - 5 : index_of_bracket] == "Frame"
            ):
                frame_path = property_path
                break
        if frame_path is None:
            raise ValueError(f"Failed to find Frame for Property - {label_name}")
        return frame_path

    def _select_combobox_value(
        self,
        enum_data: _combobox_types,
    ):
        """Method to select combobox value"""
        label_name = enum_data.UI_LABEL.value
        new_value = enum_data.value
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        combobox_path = f"{frame_path}/**/ComboBox[0]"

        combobox_element = self.omni_driver.find_element(combobox_path, refresh=True)
        combobox_info = combobox_element.get_combobox_info()
        self.log.info(combobox_info)
        self.select_item_from_stack_combo_box(combobox_path, name=new_value)

    def _fetch_combobox_value(
        self,
        enum_data: _combobox_types,
    ):
        """Method to fetch combobox value"""
        label_name = enum_data.UI_LABEL.value
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        combobox_path = f"{frame_path}/**/ComboBox[0]"

        combobox_element = self.omni_driver.find_element(combobox_path, refresh=True)
        combobox_info = combobox_element.get_combobox_info()
        self.log.info(combobox_info)
        current_value = combobox_info["current_value"]
        return current_value

    def _select_color_picker_value(
        self,
        enum_data: _colourbox_types,
    ):
        """Method to select color picker value"""
        label_name = enum_data.UI_LABEL.value
        new_value = enum_data.value
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        colorwidget_path = f"{frame_path}/**/ColorWidget[0]"
        colorwidget_element = self.omni_driver.find_element(
            colorwidget_path, refresh=True
        )
        colorwidget_element.click()
        self.omni_driver.wait(2)

        for _ in range(7):
            self.omni_driver.emulate_key_press(KeyboardConstants.tab)
            self.omni_driver.wait(2)

        self.omni_driver.emulate_char_press(new_value[1:])
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_press(KeyboardConstants.tab)

        self.omni_driver.find_element(self._properties_button).click()

    def _fetch_color_picker_value(
        self,
        enum_data: _colourbox_types,
    ):
        """Method to fetch color picker value"""
        label_name = enum_data.UI_LABEL.value
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        colorwidget_path = f"{frame_path}/**/ColorWidget[0]"
        colorwidget_element = self.omni_driver.find_element(
            colorwidget_path, refresh=True
        )
        colorwidget_element.click()
        self.omni_driver.wait(2)

        for _ in range(7):
            self.omni_driver.emulate_key_press(KeyboardConstants.tab)
            self.omni_driver.wait(2)

        self.omni_driver.emulate_key_combo_press(
            KeyboardConstants.control + "+" + KeyboardConstants.c_key
        )
        self.omni_driver.wait(2)
        current_value = pyperclip.paste()

        self.omni_driver.find_element(self._properties_button).click()

        return current_value

    def _get_toggle_path_from_label(self, label_name: str) -> str:
        """Method to calculate Toggle Button Path of File Picker using Label"""
        label_element = self.omni_driver.find_element(
            self._avatar_property_text.format(label_name), refresh=True
        )
        zstack_parent_path = label_element.find_parent_element_path().split("/")[:-1]

        zstack_last_parent_name = zstack_parent_path[-1]
        node_num_start = zstack_last_parent_name.find("[") + 1
        node_num_end = zstack_last_parent_name.find("]")
        toggle_button_num = (
            int(zstack_last_parent_name[node_num_start:node_num_end]) + 1
        )
        toggle_button_path = (
            zstack_last_parent_name[:node_num_start]
            + str(toggle_button_num)
            + zstack_last_parent_name[node_num_end:]
        )
        zstack_parent_path[-1] = toggle_button_path
        toggle_path = "/".join(zstack_parent_path)

        return toggle_path

    def filepicker_button_state(
        self,
        enum_data: _filepicker_types,
        new_value: bool = None,
    ) -> bool:
        """Gets or sets the state of a filepicker button.

        Args:
            enum_data: An object containing UI label information.
            new_value: The new state to set. Optional.

        Returns:
            The current state of the button.

        Raises:
            ValueError: If the image source value is unexpected.
        """
        label_name = enum_data.UI_LABEL.value
        toggle_path = self._get_toggle_path_from_label(label_name=label_name)
        image_path = f"{toggle_path}/**/Image[0]"

        image_element = self.omni_driver.find_element(image_path, refresh=True)
        image_src = os.path.split(image_element.image_source())[-1]
        if image_src not in [self._image_enabled, self._image_disabled]:
            raise ValueError(f"Unexpected Image Source Value: {image_src}")

        current_state = image_src == self._image_enabled
        if new_value is None:
            self.log.info(f"Fetch {label_name} State: {str(current_state)}")
            return current_state
        elif current_state ^ new_value:
            self.log.info(f"Updating {label_name} to State: {str(new_value)}")
            image_element.click()
            self.omni_driver.wait(2)
            return new_value
        else:
            self.log.info(f"{label_name} already in State: {str(new_value)}")
            return current_state

    def is_filepicker_select_button_visible(
        self,
        enum_data: _filepicker_types,
    ) -> bool:
        """Determines if the file picker select button is visible.

        Args:
            enum_data: An object containing UI_LABEL with the label name.

        Returns:
            True if the select button is visible, False otherwise.
        """
        label_name = enum_data.UI_LABEL.value
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        select_button_path = f"{frame_path}/**/Button[0]"
        try:
            self.omni_driver.find_element(select_button_path, refresh=True)
            return True
        except ElementNotFound:
            return False

    def _select_filepicker(
        self,
        enum_data: _filepicker_types,
    ):
        """Method to set file picker value"""
        label_name = enum_data.UI_LABEL.value
        new_value = enum_data.value
        local_path = self.download_file(new_value)
        self.filepicker_button_state(enum_data=enum_data, new_value=True)
        frame_path = self._get_frame_path_from_label(label_name=label_name)
        select_button_path = f"{frame_path}/**/Button[0]"
        select_button_element = self.omni_driver.find_element(
            select_button_path, refresh=True
        )
        select_button_element.click()
        self.omni_driver.wait(2)

        file_full_path = local_path
        path_sep = os.sep if os.sep in file_full_path else "/"
        file_path = file_full_path[: file_full_path.rfind(path_sep)]
        file_name = file_full_path[file_full_path.rfind(path_sep) + 1 :]
        file_or_directory_model = SelectFileOrDirectoryModel(self.omni_driver)
        if file_or_directory_model.is_window_visible():
            file_or_directory_model.enter_path_and_navigate(file_path, file_name)
            file_or_directory_model.open_file_folder(file_name)
            file_or_directory_model.click_ok_button()
            if file_or_directory_model.is_window_visible():
                raise Exception(
                    "Select File or Directory Window is still open after clicking Ok Button"
                )
        else:
            raise Exception("Select File or Directory Window is not found")

    def _fetch_filepicker(
        self,
        enum_data: _filepicker_types,
    ):
        """Method to fetch file picker value"""
        current_state = self.filepicker_button_state(enum_data)
        if current_state:
            label_name = enum_data.UI_LABEL.value
            frame_path = self._get_frame_path_from_label(label_name=label_name)
            stringfield_path = f"{frame_path}/**/StringField[0]"
            stringfield_element = self.omni_driver.find_element(
                stringfield_path, refresh=True
            )
            return stringfield_element.get_value()
        return None

    def download_file(self, usd_path: str) -> str:
        """Downloads a file from a specified path from Nucleus.

        Args:
            usd_path: The path of the file to download.

        Returns:
            str: The local path of the downloaded file.

        Raises:
            Exception: If the download fails.
        """
        path_sep = os.sep if os.sep in usd_path else "/"
        usd_folder_path = usd_path[: usd_path.rfind(path_sep)]
        copy_result = self.omni_driver.download(
            usd_folder_path, self.temp_download_path, "OVERWRITE"
        )
        if not copy_result == "Result.OK":
            raise Exception("Failed to download Files from Nucleus")
        file_name = usd_path[usd_path.rfind(path_sep) + 1 :]
        return os.path.join(self.temp_download_path, file_name)

    def set_avatar_property(self, enum_data: _all_types) -> None:
        """Sets the property of the avatar.

        Args:
            enum_data: The new property value, which can be a combobox, color picker, or file picker value.

        Raises:
            None.
        """
        if isinstance(enum_data, self._combobox_types):
            self._select_combobox_value(enum_data)
        elif isinstance(enum_data, self._colourbox_types):
            self._select_color_picker_value(enum_data)
        elif isinstance(enum_data, self._filepicker_types):
            self._select_filepicker(enum_data)
        self.omni_driver.wait(5)
        _str_value = self.get_str_repr(enum_data)
        self.log_info_with_screenshot(_str_value + ".png")

    def fetch_avatar_property(self, enum_data: _all_types) -> str:
        """Fetches the property of the avatar.

        Args:
            enum_data: An enumeration data of combobox, colourbox, or filepicker types.

        Returns:
            The fetched value of the given enum data.

        Logs:
            Info: Fetched value.

        Raises:
            None.
        """
        if issubclass(enum_data, self._combobox_types):
            fetched_value = self._fetch_combobox_value(enum_data)
            self.log.info(f"Fetched Value - {fetched_value}")
            return fetched_value
        if issubclass(enum_data, self._colourbox_types):
            fetched_value = self._fetch_color_picker_value(enum_data)
            self.log.info(f"Fetched Value - {fetched_value}")
            return fetched_value
        if issubclass(enum_data, self._filepicker_types):
            fetched_value = self._fetch_filepicker(enum_data)
            self.log.info(f"Fetched Value - {fetched_value}")
            return fetched_value
        return None

    def click_button(self, button: Buttons):
        """Clicks on a App buttons.

        Args:
            button (Buttons): The button object to be clicked.

        Raises:
            NoSuchElementException: If the button is not found.
            ElementNotInteractableException: If the button is not interactable.
        """
        button_locator = self.omni_driver.find_element(
            self._app_button.format(button.value), refresh=True
        )
        button_locator.click()

    def is_button_visible(self, button: Buttons) -> bool:
        """Checks if Button is visible on App or not

        Args:
            button (Buttons): The button enum to check.

        Returns:
            bool indicating if Button is visible or not
        """
        _button_element = self.omni_driver.find_element(
            self._app_button.format(button.value), refresh=True
        )
        _widget_path = "/".join(
            _button_element.find_parent_element_path().split("/")[:-2]
        )
        widget_element = self.omni_driver.find_element(_widget_path, refresh=True)
        visibility = widget_element.is_visible()
        self.log.info(f"Button {button.value} visibility is - {str(visibility)}")
        return visibility

    def get_avatar_options(self, enum_data: _all_types) -> list:
        """Returns avatar options from the given enum data.

        Args:
            enum_data: Enum class containing avatar options.

        Returns:
            A list of avatar options, excluding UI_LABEL, DEFAULT_VALUE (for certain enum types).

        Raises:
            None.
        """
        if issubclass(enum_data, self._combobox_types):
            _enum_keys_ignore = ["UI_LABEL"]
        elif issubclass(enum_data, self._colourbox_types):
            _enum_keys_ignore = ["UI_LABEL", "DEFAULT_VALUE"]
        elif issubclass(enum_data, self._filepicker_types):
            _enum_keys_ignore = ["UI_LABEL", "DEFAULT_VALUE"]

        ui_options = [
            option for option in enum_data if option.name not in _enum_keys_ignore
        ]
        return ui_options

    def get_str_repr(self, enum_data: _all_types) -> str:
        """Returns a string representation of the given enum data.

        Uses the value attribute for combobox types, and the name attribute for colourbox and filepicker types.
        """
        if isinstance(enum_data, self._combobox_types):
            _use_attr = "value"
        elif isinstance(enum_data, self._colourbox_types):
            _use_attr = "name"
        elif isinstance(enum_data, self._filepicker_types):
            _use_attr = "name"

        str_repr = enum_data.__class__.__name__ + "_" + getattr(enum_data, _use_attr)
        return str_repr

    def fetch_text_from_message(self, temp_window_name: str) -> str:
        """Reads text from message dialog that will be presented as pop-up (Message Dialog)

        Args:
            temp_window_name (str): Temporary Window identifier to read message.

        Returns:
            Message that is read from Message dialog.

        Logs:
            Info: Fetched Message Text.
        """
        text_locator = self.omni_driver.find_element(
            f"{temp_window_name}//Frame/**/Label[*]", refresh=True
        )
        window_text = text_locator.get_text()
        self.log.info(f"Fetched Text - {window_text}")
        return window_text

    def apply_property_filter(self, filter_text: str) -> None:
        """
        Sends text in the Search of the App

        Args:
            search_text (str): Text to search.

        Logs:
            Info: Fetched Message Text.
        """
        filter_locator = self.omni_driver.find_element(self._avatar_filter_field)
        filter_locator.send_keys(filter_text)
        self.omni_driver.wait(2)

    def fetch_visible_property_data(self) -> dict[str, str]:
        """
        Fetches visible Property Names list

        Returns:
            Dictionary containing Names and Value of Property that is visible

        Raises:
            ValueError: If label is not mapped with Enums in code..
        """
        visible_labels_data = {}
        label_locators = list(
            {
                prop.path
                for prop in self.omni_driver.find_elements(self._avatar_all_properties)
            }
        )
        for current_locator in label_locators:
            try:
                label_text_locator = self.omni_driver.find_element(
                    f"{current_locator}/**/Label[0]", refresh=True
                )
            except ElementNotFound:
                pass
            else:
                label_name = label_text_locator.get_text()
                # Skip blank label, which are seen below filepickers
                if len(label_name.strip()) == 0:
                    continue
                label_type = None
                for _current_type in self._all_types.__args__:
                    if _current_type.UI_LABEL.value == label_name:
                        label_type = _current_type
                        break
                if not label_type:
                    raise ValueError(
                        f"Failed to find Type of Label - {label_name} from enums"
                    )
                label_value = self.fetch_avatar_property(label_type)
                visible_labels_data[label_name] = label_value
        return visible_labels_data

    def fetch_default_property_value(self, property_name: str) -> str:
        """
        Fetches default value of Property using Name

        Args:
            property_name (str): Name of Property.

        Returns:
            string or None, if Property value is not found
        """
        default_value = next(
            (
                _current_type.DEFAULT_VALUE.value
                for _current_type in self._all_types.__args__
                if _current_type.UI_LABEL.value == property_name
            ),
            None,
        )
        return default_value
