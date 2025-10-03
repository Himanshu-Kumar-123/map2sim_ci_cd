# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base OGC Map Tile Loader class
   This module contains the base methods for OGC Map Tile Loader window
"""
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.common.constants import KeyboardConstants


class BaseOGCMapTileLoaderModel(BaseModel):
    """Base model class for OGC Map Tile Loader window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to OGC Map Tile Loader window
    _window_title = "OGC Map Tile Loader"
    _global_map_settings_collapsable = "OGC Map Tile Loader//Frame/**/CollapsableFrame[*].title=='Global Map Settings'"
    _map_tile_settings_collapsable = "OGC Map Tile Loader//Frame/**/CollapsableFrame[*].title=='Map Tile Settings'"
    _generate_tile_btn = "OGC Map Tile Loader//Frame/**/Button[*].text=='Generate Tile'"
    _latitude_field = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/HStack[1]/HStack[0]/HStack[0]/FloatField[0]"
    )
    _longitude_field = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/HStack[1]/HStack[1]/HStack[0]/FloatField[0]"
    )
    _northing_field = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/HStack[1]/HStack[0]/FloatField[0]"
    )
    _easting_field = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/HStack[1]/HStack[1]/FloatField[0]"
    )

    # should be used as child for Global Map Settings collapsable
    _image_download_url = "**/StringField[*]"

    # Elevation Data selection locators
    _elevation_data_selection_collapsable = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/**/VStack[0]/CollapsableFrame[1].title=='Elevation"
        " Data Selection'"
    )
    _elevation_custom_server_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/**/VStack[0]/CollapsableFrame[1]/**/VStack[0]/HStack[2]/HStack[0]/RadioButton[0]"
    )
    _custom_server_base_url = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/**/VStack[0]/CollapsableFrame[1]/**/VStack[0]/VStack[1]/HStack[0]/StringField[0]"
    )
    _ogc_api_radio_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/**/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/**/HStack[1]/HStack[0]/RadioButton[0]"
    )
    _ogc_api_base_url = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/**/HStack[0]/StringField[0]"
    )
    _ogc_collection_id = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/**/HStack[1]/HStack[0]/StringField[0]"
    )
    _elevation_data_preset_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/**/HStack[0]/HStack[0]/RadioButton[0]"
    )
    _elevation_data_preset_combo_box = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/**/HStack[0]/HStack[1]/ComboBox[0]"
    )

    # Map Imagery Selection
    _map_imagery_selection_collapsable = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/**/VStack[0]/CollapsableFrame[0].title=='Map"
        " Imagery Selection'"
    )
    _map_imagery_ogc_api_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[1]/HStack[0]/RadioButton[0]"
    )
    _map_imagery_ogc_api_base_url = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[0]/StringField[0]"
    )
    _map_imagery_ogc_api_collection_id = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[1]/HStack[0]/StringField[0]"
    )
    _map_imagery_custom_server_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[2]/HStack[0]/RadioButton[0]"
    )
    _map_imagery_custom_server_base_url = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/VStack[1]/HStack[0]/StringField[0]"
    )
    _map_imagery_preset_btn = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[0]/HStack[0]/RadioButton[0]"
    )
    _map_imagery_preset_combo_box = (
        "OGC Map Tile"
        " Loader//Frame/ScrollingFrame[0]/**/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/**/HStack[0]/HStack[1]/ComboBox[0]"
    )

    
    def navigate_to_ogc_map_tile_loader(self):
        self.omni_driver.select_menu_option(f"Window/{self._window_title}")
        self.omni_driver.wait(2)

        assert (
            "OGC Map Tile Loader" in self.omni_driver.get_windows()["visible_windows"]
        ), f"Cannot find window for '{self._window_title}'."
        self.log.info("Navigated to OGC Map Tile Loader window successfully.")

    
    def edit_image_download_url(self, path: str):
        """Edits the Image Download Url field
        :param path: path of file/folder
        """
        global_map_settings: OmniElement = self.omni_driver.find_element(self._global_map_settings_collapsable, True)
        if global_map_settings.is_collapsed():
            global_map_settings.click()
            self.omni_driver.wait(2)
            assert not global_map_settings.is_collapsed(), "Could not expand 'Global Map Settings'"
            self.log.info("'Global Map Settings' collapsable expanded successfully.")

        image_url_field: OmniElement = global_map_settings.find_element(self._image_download_url)
        image_url_field.double_click()
        self.omni_driver.wait(1)
        self.omni_driver.emulate_key_combo_press(f"{KeyboardConstants.control}+{KeyboardConstants.a_key}")
        if len(path) == 0:
            self.omni_driver.emulate_key_press(KeyboardConstants.backspace)
            self.log.info("Empty path sent to URL field.")
        else:
            self.omni_driver.emulate_char_press(path)
            self.log.info(f"Path '{path}' sent to URL field")

    
    def edit_latitude_field(self, value: str):
        """Edits the Latitude field under Map Tile Settings
        :param value: value that is to be assigned
        """
        self._expand_map_tile_settings()
        latitude_field: OmniElement = self.omni_driver.find_element(self._latitude_field, True)
        latitude_field.send_keys(value)
        self.log.info(f"Value {value} sent to Latitude field")

    
    def edit_longitude_field(self, value: str):
        """Edits the Longitude field under Map Tile Settings
        :param value: value that is to be assigned
        """
        self._expand_map_tile_settings()
        longitude_field: OmniElement = self.omni_driver.find_element(self._longitude_field, True)
        longitude_field.send_keys(value)
        self.log.info(f"Value {value} sent to Longitude field")

    
    def edit_northing_field(self, value: str):
        """Edits the Northing field under Map Tile Settings
        :param value: value that is to be assigned
        """
        self._expand_map_tile_settings()
        northing_field: OmniElement = self.omni_driver.find_element(self._northing_field, True)
        northing_field.send_keys(value)
        self.log.info(f"Value {value} sent to Northing field")

    
    def edit_easting_field(self, value: str):
        """Edits the Easting field under Map Tile Settings
        :param value: value that is to be assigned
        """
        self._expand_map_tile_settings()
        easting_field: OmniElement = self.omni_driver.find_element(self._easting_field, True)
        easting_field.send_keys(value)
        self.log.info(f"Value {value} sent to Easting field")

    
    def generate_tile(self):
        self._expand_map_tile_settings()
        generate_btn: OmniElement = self.find_and_scroll_element_into_view(
            self._generate_tile_btn, ScrollAxis.Y, ScrollAmount.CENTER, True
        )
        generate_btn.click()
        self.omni_driver.wait_for_stage_load()
        self.log.info("Clicked on 'Generate Tile' button.")

    def _expand_map_tile_settings(self):
        map_tile_settings: OmniElement = self.omni_driver.find_element(self._global_map_settings_collapsable, True)
        if map_tile_settings.is_collapsed():
            map_tile_settings.click()
            self.omni_driver.wait(2)
            assert not map_tile_settings.is_collapsed(), "Could not expand 'Map Tile Settings'"
            self.log.info("'Map Tile Settings' collapsable expanded successfully.")
        return map_tile_settings

    
    def _expand_elevation_data_selection(self):
        self._expand_map_tile_settings()
        elevation_data_selection_collapsebar = self.find_and_scroll_element_into_view(
            self._elevation_data_selection_collapsable, ScrollAxis.Y, ScrollAmount.CENTER, refresh=True
        )

        if elevation_data_selection_collapsebar.is_collapsed():
            elevation_data_selection_collapsebar.click()
            self.omni_driver.wait(2)
            assert (
                not elevation_data_selection_collapsebar.is_collapsed()
            ), "Could not expand 'Elevation Data Selection'"
            self.log.info("'Elevation Data Selection' collapsable expanded successfully.")
        return elevation_data_selection_collapsebar

    
    def edit_elevation_data_base_url(self, base_url: str):
        self._expand_elevation_data_selection()
        custom_server_btn: OmniElement = self.omni_driver.find_element(self._elevation_custom_server_btn, True)
        custom_server_btn.click()
        custom_server_base_url: OmniElement = self.omni_driver.find_element(self._custom_server_base_url, True)
        custom_server_base_url.double_click()
        self.omni_driver.emulate_char_press(base_url)
        self.log.info(f"Value {base_url} sent to base url")

    
    def edit_elevation_data_ogc_api(self, base_url: str, collection_id: str):
        self._expand_elevation_data_selection()
        ogc_api_radio_btn: OmniElement = self.omni_driver.find_element(self._ogc_api_radio_btn, True)
        ogc_api_radio_btn.click()
        ogc_api_base_url: OmniElement = self.omni_driver.find_element(self._ogc_api_base_url, True)
        ogc_api_base_url.double_click()
        self.omni_driver.emulate_char_press(base_url)
        self.log.info(f"Value {base_url} sent to base url")
        ogc_collection_id: OmniElement = self.omni_driver.find_element(self._ogc_collection_id, True)
        ogc_collection_id.double_click()
        self.omni_driver.emulate_char_press(collection_id)
        self.log.info(f"Value {collection_id} sent to collection Id")

    
    def _expand_map_imagery_selection(self):
        self._expand_map_tile_settings()
        map_imagery_selection_collapsebar = self.find_and_scroll_element_into_view(
            self._map_imagery_selection_collapsable, ScrollAxis.Y, ScrollAmount.CENTER, refresh=True
        )

        if map_imagery_selection_collapsebar.is_collapsed():
            map_imagery_selection_collapsebar.click()
            self.omni_driver.wait(2)
            assert not map_imagery_selection_collapsebar.is_collapsed(), "Could not expand 'Map Imagery Selection'"
            self.log.info("'Map Imagery Selection' collapsable expanded successfully.")
        return map_imagery_selection_collapsebar

    
    def edit_map_imagery_ogc_api(self, base_url: str, collection_id: str):
        self._expand_map_imagery_selection()
        map_imagery_ogc_api_radio_btn: OmniElement = self.omni_driver.find_element(self._map_imagery_ogc_api_btn, True)
        map_imagery_ogc_api_radio_btn.click()
        map_imagery_ogc_api_base_url: OmniElement = self.omni_driver.find_element(
            self._map_imagery_ogc_api_base_url, True
        )
        map_imagery_ogc_api_base_url.double_click()
        self.omni_driver.emulate_char_press(base_url)
        self.log.info(f"Value {base_url} sent to base url")
        map_imagery_ogc_api_collection_id: OmniElement = self.omni_driver.find_element(
            self._map_imagery_ogc_api_collection_id, True
        )
        map_imagery_ogc_api_collection_id.double_click()
        self.omni_driver.emulate_char_press(collection_id)
        self.log.info(f"Value {collection_id} sent to collection Id")

    
    def edit_map_imagery_custom_server(self, base_url: str):
        self._expand_map_imagery_selection()
        map_imagery_custom_server_btn: OmniElement = self.omni_driver.find_element(
            self._map_imagery_custom_server_btn, True
        )
        map_imagery_custom_server_btn.click()
        map_imagery_custom_server_base_url: OmniElement = self.omni_driver.find_element(
            self._map_imagery_custom_server_base_url, True
        )
        map_imagery_custom_server_base_url.double_click()
        self.omni_driver.emulate_char_press(base_url)
        self.log.info(f"Value {base_url} sent to base url")

    
    def edit_preset(self):
        self._expand_map_imagery_selection()
        map_imagery_preset_btn: OmniElement = self.omni_driver.find_element(self._map_imagery_preset_btn, True)
        map_imagery_preset_btn.click()
        self.select_item_from_stack_combo_box(self._map_imagery_preset_combo_box, index=0)
        self.wait.element_to_be_located(self.omni_driver, self._map_imagery_preset_combo_box)
        self.log.info("Map Imagery Preset changed to 'terrestris (Topography and Roads)'")

        self._expand_elevation_data_selection()
        elevation_data_preset_btn: OmniElement = self.omni_driver.find_element(self._elevation_data_preset_btn, True)
        elevation_data_preset_btn.click()
        self.select_item_from_stack_combo_box(self._elevation_data_preset_combo_box, index=0)
        self.wait.element_to_be_located(self.omni_driver, self._elevation_data_preset_combo_box)
        self.log.info("Map Imagery Preset changed to 'National Oceanic and Atmospheric Administration'")
