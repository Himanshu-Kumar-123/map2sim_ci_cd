# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Markup Export Window Model class
   This module contains the base methods for Markup Export window
"""
from ..base_models.base_model import BaseModel
from omniui.utils.utility_functions import get_images_dir
import os
from omniui.utils.test_validations import validate_markup_export


class BaseExportMarkupModel(BaseModel):
    """Base model class for Markup Export window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _markup_export_window = "Markup Export//Frame/VStack[0]"
    _checkbox_csv = "Markup Export//Frame/**/FormatCheckCSV"
    _checkbox_pdf = "Markup Export//Frame/**/FormatCheckPDF"
    _checkbox_xlsx = "Markup Export//Frame/**/FormatCheckXLSX"
    _export_directory_path = "Markup Export//Frame/**/ExportDirField"
    _export_button = "Markup Export//Frame/**/ExportButton"
    _open_folder = "Markup Export//Frame/**/BrowseButton"
    _file_picker = "Select Markup Export Directory//Frame/**/filepicker_directory_path"
    _select_folder = "Select Markup Export Directory//Frame/**/Button[0].text=='Select'"

    def navigate_to_markup_export(self):
        """Navigate to Markup Export Window"""
        window = self.omni_driver.find_element(self._markup_export_window)
        window.click()
        self.screenshot("navigate_to_export_markup")
        self.omni_driver.wait(1)

    def _enter_markup_export_path(self):
        path = os.getcwd() + "/" + get_images_dir()
        path = path.replace("\\", "/")
        self.find_and_click(self._open_folder)
        self.find_and_enter_text(self._file_picker, path)
        self.find_and_click(self._select_folder)
        return path

    def _assert_markup_export_notification(self):
        text = self.get_notification_text(timeout=20)
        self.log.info(text)
        assert text == "Markup data exported.", "Notification for markup data exported didn't show up"

    def export_markup(self):
        """Exports markups in csv format to the path specified"""
        self.navigate_to_markup_export()
        if not self.omni_driver.find_element(self._checkbox_csv).is_checked():
            self.find_and_click(self._checkbox_csv)
        self._enter_markup_export_path()
        self.find_and_click(self._export_button)
        self._assert_markup_export_notification()
    
    def export_markups_in_all_formats(self):
        """Exports markups in all formats to the path specified"""
        self.navigate_to_markup_export()
        if not self.omni_driver.find_element(self._checkbox_csv).is_checked():
            self.find_and_click(self._checkbox_csv)
        if not self.omni_driver.find_element(self._checkbox_xlsx).is_checked():
            self.find_and_click(self._checkbox_xlsx)
        if not self.omni_driver.find_element(self._checkbox_pdf).is_checked():
            self.find_and_click(self._checkbox_pdf)
        path=self._enter_markup_export_path()
        self.find_and_click(self._export_button)
        self._assert_markup_export_notification()
        validate_markup_export(path, self.log)
