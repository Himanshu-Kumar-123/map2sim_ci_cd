# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Vehicles Ingest Model class
   This module contains the base methods for Ingest Window
"""
from omniui.omni_models.base_models.base_model import BaseModel


class BaseVehiclesIngestModel(BaseModel):
    """Base model class for Ingest window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _vehicle_ingest_btn = (
        "Vehicle Ingest//Frame/**/Button[0].text=='Ingest new vehicle'"
    )
    _input_folder_textfield = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[1]/StringField[0]"
    _input_folder_combobox = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[1]/VStack[0]/ComboBox[0]"
    _input_folder_icon = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[1]/Button[0]"

    _next_btn = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[1]/ScrollingFrame[0]/VStack[0]/HStack[2]/Button[0]=='Next'"
    _go_btn = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[2]/VStack[0]/HStack[0]/Button[0].text=='Go'"
    # _done_label = "Vehicle Ingest//Frame/**/Button[0].text='Done'"
    _done_btn_txt = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[3]/VStack[0]/HStack[0]/Button[0].text='Done'"
    _done_btn = "Vehicle Ingest//Frame/ZStack[0]/VStack[0]/Frame[3]/VStack[0]/HStack[0]/Button[0]"

    def wait_and_click_ingest(self):
        """Find and clicks vehicle ingest button"""
        # self.wait.element_to_be_located(self.omni_driver, self._vehicle_ingest_btn)
        # self.find_and_click(self._vehicle_ingest_btn)
        ingest_new_vehicle = self.omni_driver.find_element(self._vehicle_ingest_btn)
        ingest_new_vehicle.click()

    def enter_input_folder_path(self, path: str):
        """Find and enters text in input folder field

        Args:
            path (str): Path of input folder
        """
        self.find_and_enter_text(self._input_folder_textfield, path)

    def select_input_folder_icon(self):
        """Find and clicks folder icon"""
        self.find_and_click(self._input_folder_icon)

    def click_next(self):
        """Clicks on next button"""
        self.find_and_click(self._next_btn)

    def wait_and_click_go(self):
        """Clicks on go button"""
        self.wait.element_to_be_located(self.omni_driver, self._go_btn)
        self.find_and_click(self._go_btn)

    def click_done(self):
        """Waits for progress to finish and then click on done btn"""
        self.wait.element_to_be_located(self.omni_driver, self._done_btn)
        self.find_and_click(self._done_btn)
        # self.screenshot("vehicles_ingestion_success.png")
