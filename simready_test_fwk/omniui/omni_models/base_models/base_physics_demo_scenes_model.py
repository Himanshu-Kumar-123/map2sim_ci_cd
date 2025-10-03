# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Physics Demo Scenes Model class
   This module contains the base methods for Physics Demo Scenes
"""
from ..base_models.base_model import BaseModel


class BasePhysicsDemoScenesModel(BaseModel):
    """Base model class for Physics Demo Scenes

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to main toolbar window
    _window_name = "Physics Demo Scenes"
    _window_root = _window_name + "//Frame/VStack[0]"
    _search_box_locator = _window_name + "//Frame/VStack[0]/HStack[0]/StringField[0]"
    _scene_main = _window_name + "//Frame/**/ScrollingFrame[0]/TreeView[0]"
    _selected_scene_label = (
        _window_name
        + "//Frame/VStack[0]/HStack[1]/ScrollingFrame[0]/ZStack[0]/VStack[0]/Label[0]"
    )
    _load_scene_btn = _window_name + "//Frame/**/Button[*].text=='Load scene'"

    def is_window_visible(self):
        """Method to check if Physics Demo Scenes is visible"""
        self.omni_driver.wait(2)
        return self._window_name in self.omni_driver.get_windows()["visible_windows"]

    def navigate_to_window(self):
        """Method to navigate to Physics Demo Scenes"""
        window = self.omni_driver.find_element(self._window_root)
        window.click()
        self.screenshot("navigate_to_physics_demo_scenes")
        self.omni_driver.wait(1)

    def filter_scenes(self, filter_text):
        """Method to filter scenes

        Args:
            filter_text (str): Text to filter scenes
        """
        _search_box_element = self.omni_driver.find_element(
            self._search_box_locator, refresh=True
        )
        _search_box_element.send_keys(filter_text)
        self.omni_driver.wait(2)
        _image_text = filter_text.replace(" ", "_")
        self.log_info_with_screenshot(f"filtered_scenes_with_text_{_image_text}")

    def get_scene_names(self):
        """Method to get scene names

        Returns:
            list: List of scene names
        """
        _scene_names = []
        _scene_elements = self.omni_driver.find_element(self._scene_main)
        _leaf_scenes_indicator = _scene_elements.find_elements("**/Label[0].text==''")
        for _leaf_scene_indicator in _leaf_scenes_indicator:
            label_parent_path = _leaf_scene_indicator.find_parent_element_path().split(
                "/"
            )
            node_num_start = label_parent_path[-1].find("[") + 1
            node_num_end = label_parent_path[-1].find("]")
            label_visibility_node_num = (
                int(label_parent_path[-1][node_num_start:node_num_end]) + 1
            )
            label_visibility_node_name = (
                label_parent_path[-1][:node_num_start]
                + str(label_visibility_node_num)
                + label_parent_path[-1][node_num_end:]
            )
            label_parent_path[-1] = label_visibility_node_name
            label_parent_path.append("Label[0]")
            scene_name_path = "/".join(label_parent_path)
            scene_element = self.omni_driver.find_element(scene_name_path, refresh=True)
            _scene_names.append(scene_element.get_text())
        self.log.info(f"Scene names: {_scene_names}")
        return _scene_names

    def select_scene(self, scene_name):
        """Method to select scene

        Args:
            scene_name (str): Scene name to select and load
        """
        is_scene_selected = False
        for _ in range(3):
            _scene_element = self.omni_driver.find_element(
                f"{self._scene_main}/**/Label[0].text=='{scene_name}'"
            )
            _scene_element.click()
            _selected_scene_name = self.omni_driver.find_element(
                self._selected_scene_label
            ).get_text()
            if _selected_scene_name == scene_name:
                is_scene_selected = True
                break

        if not is_scene_selected:
            raise ValueError("Failed to select Scene")
        self.omni_driver.wait(2)

    def select_and_load_scene(self, scene_name):
        """Method to select and load scene

        Args:
            scene_name (str): Scene name to select and load
        """
        self.select_scene(scene_name)
        self.omni_driver.find_element(self._load_scene_btn, refresh=True).click()
        self.omni_driver.wait(2)
