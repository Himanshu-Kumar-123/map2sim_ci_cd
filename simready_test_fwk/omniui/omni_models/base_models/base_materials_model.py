# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Materials class
   This module contains the base methods for Materials window
"""
import random
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound


class BaseMaterialsModel(BaseModel):
    """Base model class for Materials window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Materials window
    _materials_window = "Materials//Frame/**/VStack[0]"
    _search_field = "Materials//Frame/Frame[0]/VStack[0]/ZStack[0]/**/StringField[0]"
    _all_materials = "Materials//Frame/**/HStack[0]/ZStack[1]/ZStack[0]/ScrollingFrame[0]/HStack[0]/VStack[0]/ThumbnailView[0]/Frame[*]"
    _all_materials_labels = "Materials//Frame/Frame[0]/VStack[0]/ZStack[1]/Frame[0]/HStack[0]/ZStack[1]/ZStack[0]/ScrollingFrame[0]/HStack[0]/VStack[0]/ThumbnailView[0]/**/Label[*]"
    _materials_slider = "Materials//Frame/**/IntSlider[0]"
    _material_label = "Materials//Frame/**/ThumbnailView[0]/**/Label[0].text=='__material_name__'"
    _loading_spinner = "Materials//Frame/**/SceneView[*]"
    _all_materials_number = "Materials//Frame/Frame[0]/VStack[0]/ZStack[1]/Frame[0]/HStack[0]/ZStack[0]/VStack[0]/ScrollingFrame[0]/CategoryView[0]/HStack[1]/Label[1]"
    _category = "Materials//Frame/**/CategoryView[*]/**/Label[*].text=='__category_name__'"

    
    def navigate_to_materials(self):
        """Navigates to materials window"""
        stage_window = self.omni_driver.find_element(self._materials_window)
        stage_window.click()
        self.screenshot("navigated_to_materials")
        try:
            self.wait.timeout = 30
            self.wait.polling_interval = 2
            self.wait.element_to_be_located(self.omni_driver, self._loading_spinner)
        except ElementNotFound:
            self.log.info("Unable to find loading spinner, model should be loaded")
        else:
            self.log.info("Found loading spinner, waiting for model to load")
            self.wait.timeout = 360
            self.wait.polling_interval = 60
            self.wait.element_to_be_invisible(self.omni_driver, self._loading_spinner)
        material_slider = self.omni_driver.find_element(self._materials_slider, refresh=True)
        material_slider.send_keys(128)
        material_slider.send_keys(128)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(60)
        self.wait.element_to_be_located(
        self.omni_driver, self._material_label.replace("__material_name__", "Adobe_Brick")
        )
    
    def select_and_apply_material_by(self, mode: str, *args):
        """Selects materials from window and apply to prim in viewport center by dragging

        Args:
            position (Float): X and Y position of destination co ordinate

        Returns:
            Material Name: Returns the material name of applied material
        """
        material_slider = self.omni_driver.find_element(self._materials_slider, refresh=True)
        material_slider.send_keys(128)
        material_slider.send_keys(128)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(360)

        materials = self.omni_driver.find_elements(self._all_materials)
        rand_value = random.randrange(0, len(materials))
        self.log.info(f"Total number of materials = {len(materials)} and random value = {rand_value}")
        material_label = materials[rand_value].find_element("**/Label[0]").get_text()
        self.log.info(f"Selected Material Label: {material_label}")

        material_slider.send_keys(5)
        material_slider.send_keys(5)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(360)

        if mode == "drag":
            position = args[0]
            materials[rand_value].drag_and_drop(position[0], position[1])
        elif mode == "double_click":
            materials[rand_value].double_click()
        elif mode == "right_click":
            self.omni_driver.wait(2)
            materials[rand_value].right_click()
            self.omni_driver.wait(10)
            self.omni_driver.select_context_menu_option("Apply to Selected")
        elif mode == "right_click_add_to_stage":
            materials[rand_value].right_click()
            self.omni_driver.select_context_menu_option("Add to Stage")
        else:
            self.log.info(
                f"Mode passed - {mode} is not recognised, please use from 'drag' or 'double_click' or 'right_click' or"
                " 'right_click_add_to_stage' "
            )
            assert (
                False
            ), f"Mode passed - {mode} is not recognised, please use from 'drag' or 'double_click' or 'right_click'"
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(240)
        return material_label

    
    def select_category(self, category: str):
        """Selects the specified category
        Args:
            category (str): category to be selected
        """
        label: OmniElement = self.omni_driver.find_element(
            self._category.replace("__category_name__", category.upper()), True
        )
        label.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.omni_driver.wait(1)

        # TODO: remove the retries after click issue gets resolved (OM-102905)
        retry = 4
        while not label.is_selected():
            if retry == 0:
                break
            label.click()
            self.omni_driver.wait(1)
            retry -= 1
        assert label.is_selected(), f"Category label for {category} was clicked 4 times but failed to select it."
        self.omni_driver.wait(3)
        self.omni_driver.wait_for_stage_load(120)

    
    def expand_category(self, category: str, check_sub_category: str = None):
        """Expands a category
        Args:
            category (str): category to expand
            check_sub_category (str): presence of sub category to be checked
        """
        label: OmniElement = self.omni_driver.find_element(
            self._category.replace("__category_name__", category.upper()), True
        )
        label.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.omni_driver.wait(1)
        y = label.get_widget_center()[1]
        x = label.get_size_and_position("screen_position_x")

        # TODO: remove the retries after click issue gets resolved (OM-102905)
        retry = 4
        while retry:
            try:
                self.omni_driver.click_at(x - 5, y)
                self.omni_driver.wait(1)
                self.omni_driver.find_element(
                    self._category.replace("__category_name__", check_sub_category.upper()), True
                )
                break
            except ElementNotFound:
                retry -= 1
        if retry == 0:
            self.log.info(f"Could not expand {category} category in 4 tries.")

    
    def minimize_category(self, category: str, check_sub_category: str = None):
        """Minimizes a category
        Args:
            category (str): category to minimize
            check_sub_category (str): presence of sub category to be checked
        """
        label: OmniElement = self.omni_driver.find_element(
            self._category.replace("__category_name__", category.upper()), True
        )
        label.scroll_into_view(ScrollAxis.Y, ScrollAmount.CENTER)
        self.omni_driver.wait(1)
        y = label.get_widget_center()[1]
        x = label.get_size_and_position("screen_position_x")

        # TODO: remove the retries after click issue gets resolved (OM-102905)
        retry = 4
        while retry:
            try:
                self.omni_driver.click_at(x - 5, y)
                self.omni_driver.wait(1)
                self.omni_driver.find_element(
                    self._category.replace("__category_name__", check_sub_category.upper()), True
                )
                retry -= 1
            except ElementNotFound:
                break
        if retry == 0:
            self.log.info(f"Could not minimize {category} category in 4 tries.")

    def check_materials_visible(self, materials_data: list):
        """This method checks if given list of materials is visible
        Args:
            materials_data (list): list of materials to verify
        """
        visible_labels = self.omni_driver.find_elements(self._all_materials_labels)
        visible_set = set([x.get_text() for x in visible_labels])

        expected_set = set()
        for material in materials_data:
            if material.endswith(".mdl"):
                idx = material.rfind(".mdl")
                expected_set.add(material[:idx])
            elif material.endswith(".usd"):
                idx = material.rfind(".usd")
                expected_set.add(material[:idx])
            else:
                expected_set.add(material)

        if expected_set != visible_set:
            self.log_info_with_screenshot("Material check failed", "material_check_failed")
            assert (
                expected_set == visible_set
            ), f"Expected materials: {expected_set}. \nObserved materials: {visible_set}"

    
    def verify_materials_under_category(self, category: str, config: dict):
        """Verifies the presence of materials in all subcategories for given category and
        based on given data config
        Args:
            category (str): category to traverse and verify
            config (dict): category-wise data of materials
        """

        def traverse_categories(cat, data):
            # this method performs DFS over the category-subcategory tree
            self.log.info(f"Checking materials under '{cat}' category")
            self.select_category(cat)
            if type(data) == list:
                self.log.info(f"'{cat}' category does not have any sub categories.")
                self.check_materials_visible(data)
                return
            elif type(data) == dict:
                # self denotes the materials which are visible when a parent category is selected
                self.check_materials_visible(data["self"])
                data.pop("self")
                self.log.info(f"Checking sub categories under '{cat}' category")
                self.expand_category(cat, list(data.keys())[0])
                for sub_cat in data:
                    traverse_categories(sub_cat, data[sub_cat])
                self.minimize_category(cat, list(data.keys())[0])

        traverse_categories(category, config)

    @property
    def get_all_materials_count(self):
        """Gets the count for all materials in the Materials Window"""
        all_materials_label = self.omni_driver.find_element(self._all_materials_number, refresh=True)
        count = all_materials_label.get_text()
        self.log.info(f"All materials count: {count}")
        return count

    def apply_material_by_index(self, index: int):
        """Selects materials from window and apply to prim in viewport by index value

        Returns:
            Material Name: Returns the material name of applied material
        """
        material_slider = self.omni_driver.find_element(self._materials_slider)
        material_slider.send_keys(128)
        materials = self.omni_driver.find_elements(self._all_materials)
        count = self.get_all_materials_count
        self.log.info(f"Total number of materials = {count} and random value = {index}")
        material_label = materials[index].find_element("**/Label[0]").get_text()
        self.log.info(f"Selected Material Label: {material_label}")
        material_slider.send_keys(5)
        material_slider.send_keys(5)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(360)

        materials[index].double_click()
        
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load(240)
        return material_label

    def search_material(self, key: str):
        """Searches for a material using the search field
        Args: 
            key (str): key to search
        """
        elm = self.omni_driver.find_element(self._search_field, True)
        elm.send_keys(key)
        self.log.info(f"Searched for materials with key: {key}")

    def select_texture_by_index_and_drop_to_position(self, position, index:int):
        """Applies texture to prim properties

        Args:
            position (_type_): Position to drag texture to
            normal_map (bool): If material is for normal map.
        """
        material_slider = self.omni_driver.find_element(self._materials_slider)
        material_slider.send_keys(128)
        materials = self.omni_driver.find_elements(self._all_materials)
        count = self.get_all_materials_count
        self.log.info(f"Total number of materials = {count} and random value = {index}")
        material_label = materials[index].find_element("**/Label[0]",refresh=True).get_text()
        self.omni_driver.wait(2)
        self.log.info(f"Selected Material Label: {material_label}")
        material_slider = self.omni_driver.find_element(self._materials_slider)
        material_slider.send_keys(5)
        material_slider.send_keys(5)
        self.omni_driver.wait_frames(5)
        self.omni_driver.wait_for_stage_load(360)
        self.omni_driver.wait(2)
        self.log.info(f"position  x = {position['x']} and y = {position['y']}")
        materials[index].drag_and_drop(position['x'], position['y'])
        self.screenshot("applied_material")
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()

        return material_label