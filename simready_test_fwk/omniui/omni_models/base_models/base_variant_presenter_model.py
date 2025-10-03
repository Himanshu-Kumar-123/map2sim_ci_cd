# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Variant Presenter Model class
   This module contains the base methods for Variant Presenter window
"""
from .base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement


class BaseVariantPresenterModel(BaseModel):
    """Base model class for Variant Presenter window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Variants window
    _variant_presenter_window = "Variant Presenter"
    _menupath = "Tools/Variants/Variant Presenter"
    _groups_btn = "Variant Presenter//Frame/**/RadioButton[1].text=='GROUPS'"
    _prims_btn = "Variant Presenter//Frame/**/RadioButton[1].text=='PRIMS'"
    _search_field = "Variant Presenter//Frame/**/StringField[0]"
    _car_paint_combobox = (
        "Variant Presenter//Frame/**/presenter_combo_variant_carpaint_color_variant"
    )

    _variant_combobox = "Variant Presenter//Frame/**/__name__"
    _prim_title_path = "Variant Presenter//Frame/**/Label[*].text=='{}'"

    def navigate_to_variant_presenter(self):
        """Navigates to the Variant Presenter window
        """        
        self.omni_driver.select_menu_option(self._menupath)
        self.wait.window_to_be_visible(self.omni_driver, self._variant_presenter_window)

    def open_groups(self):
        """Clicks on the Groups button
        """
        self.find_and_click(self._groups_btn)

    def is_group_selected(self):
        """Determines whether a group is selected

        Returns:
            bool: True if it is selected, else False
        """
        groups = self.omni_driver.find_element(self._groups_btn)
        return groups.is_selected()

    def search_group(self, group_name):
        """Searches for a group.

        Args:
            group_name (str): Name of the group to search
        """
        self.find_and_enter_text(self._search_field, group_name)

    def select_body_paint_variant(self, colour="Nvidia_Green"):
        """Selects value for body paint variant.

        Args:
            colour (str, optional): Name of colour to choose for body paint. Defaults to "Nvidia_Green".
        """
        self.select_item_by_name_from_combo_box(self._car_paint_combobox, colour)

    def select_variant(self, variant_combobox_name: str, variant: str):
        """A general method for selecting a variant.

        Args:
            variant_combobox_name (str): name/identifier of the variant combobox
            variant (str): Value to be selected
        """
        self.select_item_by_name_from_combo_box(
            self._variant_combobox.replace("__name__", variant_combobox_name), variant
        )
        self.omni_driver.wait(5)
        self.log_info_with_screenshot(f"Selected '{variant}' in '{variant_combobox_name}'", "select_variant")

    def _material_map_difference(self, old_material_map: dict, current_material_map: dict):
        """Generates a dictionary of materials which are present in current map but not in old map.

        Args:
            old_material_map (dict): old material mapping dictionary
            current_material_map (dict): current material mapping dictionary

        Returns:
            dict: a dictionary containing difference between two material maps
        """
        diff = dict()
        for key, value in current_material_map.items():
            if key not in old_material_map or old_material_map[key] != value:
                diff[key] = value
        return diff
    
    def _fetch_coordinates_of_all_prims(self):
        """Fetches coordinates of all prims present in the stage.

        Returns:
            dict: Dictionary containing prims mapped with their coordinates.
        """
        all_prims = self.omni_driver.get_stage()

        coordinates = dict()
        for prim in all_prims:
            prim_path = prim.lstrip("Usd.Prim(<").rstrip(">)")
            coordinates[prim_path] = self.omni_driver.get_prim_coordinates(prim_path)
        
        return coordinates

    def _coordinates_changed(self, old_coordinates: dict, current_coordinates: dict):
        """Returns the list of prims whose coordinates changed.

        Args:
            old_coordinates (dict): Current coordinates dictionary
            current_coordinates (dict): Old coordinates dictionary

        Returns:
            list: List of prims whose coordinates have changed
        """
        prim_list = list()
        for prim, coordinate in old_coordinates.items():
            if current_coordinates[prim] != coordinate:
                prim_list.append(prim)
        
        return prim_list

    def generate_reference_data(self, variant_names: list):
        """Cycles through variant values for various attributes and creates a dataset of changes in visibility and material of prims.
        
        Args:
            variant_names (list): A list of variant combobox names for which dataset is to be created.
        """
        data = dict()
        for variant_name in variant_names:
            data[variant_name] = dict()
            combobox = self.omni_driver.find_element(self._variant_combobox.replace("__name__", variant_name), True)
            values = combobox.get_combobox_info()["all_options"]
            values.remove("")
            old_visible = self.omni_driver.get_visible_prims()
            old_material_map = self.omni_driver.get_prim_material_mapping()
            for _ in range(2):
                for value in values:
                    curr_dict = dict()
                    self.select_variant(variant_name, value)
                    self.omni_driver.wait_for_stage_load(300)

                    current_visible = self.omni_driver.get_visible_prims()
                    current_material_map = self.omni_driver.get_prim_material_mapping()
                    new_visible = list(set(current_visible) - set(old_visible))
                    new_material_map = self._material_map_difference(old_material_map, current_material_map)
                    if len(new_visible):
                        curr_dict["visible prims"] = new_visible
                    if len(new_material_map.keys()):
                        curr_dict["material map"] = new_material_map
                    
                    data[variant_name][value] = curr_dict

                    old_visible = current_visible
                    old_material_map = current_material_map
            
        self.log.info(f"Generated reference data: {data}")


    def validate_prim_variants(self, variant_data: dict):
        """Cycles through variant values for various attributes and validates prim become visibility and material mapping.
        
        Args:
            variant_data (dict): a dictionary containing names of variant comboboxes mapped with their values and respective changes
        """
        for variant_name, mapping in variant_data.items():
            values = mapping.keys()
            for value in values:
                self.select_variant(variant_name, value)
                self.omni_driver.wait_for_stage_load(300)

                if "visible prims" in mapping[value]:
                    visible_prims = self.omni_driver.get_visible_prims()
                    assert all(
                        prim in visible_prims for prim in mapping[value]["visible prims"]
                    ), f"Prims of selected variant are not visible. Expected visible: {list(set(mapping[value]['visible prims']) - set(visible_prims))}"

                    # check that prims related to other variant values are not visible
                    for value_2 in values:
                        if value_2 != value and "visible prims" in mapping[value_2]:
                            assert all(
                                prim not in visible_prims for prim in mapping[value_2]["visible prims"]
                            ), f"Prims of unselected variant/s should be invisible. Found: {list(set(mapping[value_2]['visible prims']) - set(visible_prims))}"
                
                if "material map" in mapping[value]:
                    all_material_mapping = self.omni_driver.get_prim_material_mapping()

                    for prim, materials in mapping[value]["material map"].items():
                        if set(all_material_mapping[prim]) != set(materials):
                            assert False, f"Material mapping is not as per expectation. Found: {dict.fromkeys(mapping[value]['material map'])}"

    def get_variant_value(self, variant_combobox_name: str) -> str:
        """Returns value of the variant

        Args:
            variant_combobox_name (str): Name of the variant combobox to fetch value from

        Returns:
            str: Value of variant
        """
        elm: OmniElement = self.omni_driver.find_element(
            self._variant_combobox.replace("__name__", variant_combobox_name), True
        )
        return elm.get_combobox_info()["current_value"]

    def change_variant_values(self, variant_combobox_name: str) -> str:
        """Returns value of the variant

        Args:
            variant_combobox_name (str): Name of the variant combobox to fetch value from
            name (str) : Name of the value to change
        Returns:
            str: Value of variant
        """
        variants =  self.get_combobox_values(variant_combobox_name=variant_combobox_name)
        current_variant = self.get_variant_value(variant_combobox_name=variant_combobox_name)
        self.log.info(f"variant values: {variants}")
        for variant_name in variants:
            if len(variant_name)>0: 
                self.select_variant(variant_combobox_name=variant_combobox_name,variant=variant_name)
                self.omni_driver.wait(1)
        self.log.info("Changed all variant values")


    def open_variant_editor_window(self,prim_name: str):
        """Returns value of the variant

        Args:
            variant_combobox_name (str): Name of the variant combobox to fetch value from
            prim_name (str) : prim Name for which need to open variant editor 
        Returns:
            str: Value of variant
        """
        prim_locator = self.omni_driver.find_element(self._prim_title_path.format(prim_name), True)
        parent_path = prim_locator.find_parent_element_path()
        button = self.omni_driver.find_element(parent_path+'/VStack[0]/Button[0]')
        button.double_click()
        self.log.info(f"Opened varient editor window for prim {prim_name}")

    def get_combobox_values(self, variant_combobox_name: str) -> str:
        """Returns all the combobox values for variant

        Args:
            variant_combobox_name (str): Name of the variant combobox to fetch value from

        Returns:
            Values (list): All Value of variant
        """
        elm: OmniElement = self.omni_driver.find_element(
            self._variant_combobox.replace("__name__", variant_combobox_name), True
        )
        return elm.get_combobox_info()["all_options"]