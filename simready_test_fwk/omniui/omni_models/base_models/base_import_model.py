# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Import Model class
   This module contains the base methods for Import Window
"""
# from omniui.omni_models.base_models.base_model import BaseModel
from omniui.omni_models.base_models.base_model import BaseModel


class BaseImportModel(BaseModel):
    """Base model class for Import window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _import_btn = "SimReady Studio ModeBar//Frame/**/Label[0].text=='Import'"
    _common_assets_btn = "Static Prop Ingest//Frame/**/Button[0].text=='Common Assets'"
    _input_folder_textfield = "Static Prop Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[1]/StringField[0]"
    _category_combobox = "Static Prop Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[4]/ComboBox[0]"
    _next_btn = "Static Prop Ingest//Frame/**/Button[0].text=='Next'"
    _go_btn = "Static Prop Ingest//Frame/**/Button[*].text=='Go'"
    _finished_label = "Static Prop Ingest//Frame/**/Label[0].text=='Finished!'"
    _success_btn = "Static Prop Ingest//Frame/**/Button[*].text=='Success'"

    def click(self):
        """Find and clicks import button"""
        self.find_and_click(self._import_btn)

    def select_common_assets(self):
        """Find and clicks common assets button"""
        self.find_and_click(self._common_assets_btn)

    def enter_input_folder_path(self, path: str):
        """Find and enters text in input folder field

        Args:
            path (str): Path of input folder
        """
        self.find_and_enter_text(self._input_folder_textfield, path)

    def select_category(self, category: str):
        """Selects category from dropdown

        Args:
            category (str): Name of category
        """
        self.select_item_by_name_from_combo_box(self._category_combobox, category)

    def click_next(self):
        """Clicks on next button"""
        self.find_and_click(self._next_btn)

    def click_go(self):
        """Clicks on go button"""
        self.find_and_click(self._go_btn)

    def wait_and_click_success(self):
        """Waits for progress to finish and then click on success btn"""
        self.wait.element_to_be_located(self.omni_driver, self._finished_label)
        self.find_and_click(self._success_btn)
