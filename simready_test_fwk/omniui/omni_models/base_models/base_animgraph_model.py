# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base AnimGraph Model class
   This module contains the base methods for Animation Graph window
"""
import os
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis


class BaseAnimGraphModel(BaseModel):
    """Base model class for Animation Graph window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _window_name = "Animation Graph"

    _edit_animgraph_btn = "Animation Graph//Frame/**/Button[*].text == 'Edit Animation Graph'"
    _new_animgraph_btn = "Animation Graph//Frame/**/Button[*].text == 'New Animation Graph'"

    # Nodes Tree View Locators
    _nodes_treeview = (
        "Animation Graph//Frame/**/Frame[1]/**/Frame[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/TreeView[0]"
    )
    _root_node_names = _nodes_treeview + "/ZStack[*]/HStack[0]/Label[0]"
    _root_node_images = _nodes_treeview + "/ZStack[*]/HStack[0]/VStack[0]/ZStack[0]/HStack[0]/Image[0]"
    _node_label = _nodes_treeview + "/**/Label[0].text == '{}'"
    _node_expand_btn = _nodes_treeview + "/ZStack[*]/VStack[1]/ImageWithProvider[0]"
    _child_node_list = _nodes_treeview + "/HStack[*]/VStack[1]/Label[0]"
    _child_node_image_list = _nodes_treeview + "/HStack[*]/VStack[0]/ZStack[0]/HStack[0]/Image[0]"
    _search_node = "Animation Graph//Frame/**/VStack[0]/ZStack[0]/Frame[0]/Frame[0]/**/StringField[0]"
    _clear_search_btn = "Animation Graph//Frame/**/VStack[0]/ZStack[0]/Frame[0]/Frame[0]/**/Button[0]"
    _nodes_tab_btn = "Animation Graph//Frame/**/RadioButton[*].text == 'Nodes'"
    _variables_tab_btn = "Animation Graph//Frame/**/RadioButton[*].text == 'Variables'"

    # Create Animation Graph Window Locators
    _select_from_stage_btn = "Create Animation Graph//Frame/**/Button[*].text == 'Select From Stage'"
    _skeleton_path_picker = "Create Animation Graph//Frame/**/HStack[1]/ZStack[0]/VStack[0]/HStack[0]/StringField[0]"
    _cancel_animgraph_btn = "Create Animation Graph//Frame/**/Button[*].text == 'Cancel'"
    _create_animgraph_btn = "Create Animation Graph//Frame/**/Button[*].text == 'Create'"

    # Select Skeleton Window Locators
    _asset_locator = "Select Skeleton//Frame/**/TreeView[0]/**/Label[0].text == '{}'"
    _select_skeleton_btn = "Select Skeleton//Frame/**/Button[*].text == 'Select'"

    # Animation Graph Locators
    _graph_canvas = "Animation Graph//Frame/**/Frame[1]/**/Frame[0]/ZStack[0]/ZStack[0]/CanvasFrame[0]"
    _graph_nodes = _graph_canvas + "/ZStack[0]/Placer[*]"
    _node_container = _graph_canvas + "/ZStack[0]/Placer[{}]"
    _node_output = _node_container + "/**/ZStack[0]/VStack[0]/HStack[1]/**/Circle[0].name == 'Object'"
    _node_title = _node_container + "/**/ZStack[0]/VStack[0]/**/Label[*]"
    _node_input = _node_container + "/**/ZStack[0]/**/ImageWithProvider[0].name == 'Object'"

    # Variables Tab Locators
    _var_add_btn = r"Animation Graph//Frame/**/Frame[0]/VStack[0]/ZStack[0]/Frame[1]/HStack[0]/**/Button[0]"
    _var_node = (
        "Animation Graph//Frame/**/Frame[1]/HStack[0]/VStack[0]/ScrollingFrame[0]/TreeView[0]/**/Label[0].text == '{}'"
    )
    _var_rename = "Animation Graph//Frame/**/Label[0].text == 'Name'"

    def enable_animgraph_window(self):
        """Enables AnimGraph window from menubar"""
        self.omni_driver.select_menu_option("Window/Animation/Animation Graph")
        self.omni_driver.wait(2)

    def create_new_animgraph_from_stage(self, asset_name: str):
        """Creates new animgraph from stage

        Args:
        asset_name(str): Name of asset
        """
        self.find_and_click(self._new_animgraph_btn)
        self.wait.element_to_be_located(self.omni_driver, self._select_from_stage_btn)
        self.find_and_click(self._select_from_stage_btn)
        self.wait.element_to_be_located(self.omni_driver, self._select_skeleton_btn)
        self.find_and_scroll_element_into_view(
            self._asset_locator.format(asset_name), ScrollAxis.Y, ScrollAmount.TOP, True
        )
        self.find_and_click(self._asset_locator.format(asset_name))
        self.find_and_click(self._select_skeleton_btn)
        self.wait.element_to_be_located(self.omni_driver, self._skeleton_path_picker)
        skeleton_path = self.omni_driver.find_element(self._skeleton_path_picker, True).get_text()
        if asset_name not in skeleton_path:
            raise ValueError(f"Failed to asset in the skeleton path, skeleton_path: {skeleton_path}")
        self.find_and_click(self._create_animgraph_btn)

    def drag_node_to_graph(self, node_name: str, x: int, y: int):
        """Drags the given node to the Animation Graph

        Args:
        node_name(str): name of the node
        x(str): offset from center of canvas
        y(str): offset from center of canvas
        """
        self.clear_search_field()
        self.find_and_enter_text(self._search_node, node_name)
        center = self.get_canvas_center
        node = self.omni_driver.find_element(self._node_label.format(node_name))
        node.drag_and_drop(center[0] + x, center[1] + y)
        self.omni_driver.wait(1)

    def switch_to_variables_tab(self):
        """Switch to Variables Tab"""
        self.find_and_click(self._variables_tab_btn)
        self.omni_driver.wait(1)

    def drag_variable_to_graph(self, name: str, x: int, y: int):
        """Drags the var into the graph

        Args:
        name(str): Name of the var
        x(str): offset from center of canvas
        y(str): offset from center of canvas
        """
        var = self.omni_driver.find_element(self._var_node.format(name), True)
        center = self.get_canvas_center
        var.drag_and_drop(center[0] + x, center[1] + y)
        self.omni_driver.wait(1)

    def rename_variable(self, name: str, rename_to: str):
        """Rename variable to a given name

        Args:
        name(str): name of the variable
        rename_to(str): Rename it to
        """
        self.find_and_click(self._var_node.format(name), True)
        label = self.omni_driver.find_element(self._var_rename, True)
        rename_field = self.omni_driver.find_element(label.find_parent_element_path() + "/StringField[0]", True)
        rename_field.double_click()
        self.omni_driver.wait(1)
        rename_field.send_keys(rename_to)
        self.omni_driver.wait(1)

    def get_node_count(self, name: str):
        """Returns number of nodes in the given root node

        Args:
        name(str): Name of the root node
        """
        label = self.omni_driver.find_element(self._node_label.format(name), True)
        count_label = self.omni_driver.find_element(label.find_parent_element_path() + "/Label[1]", True)
        return count_label.get_text()

    def expand_all_nodes(self):
        """Expands all nodes in the list"""
        btns = self.omni_driver.find_elements(self._node_expand_btn)
        for btn in btns[::-1]:
            btn.scroll_into_view(ScrollAxis.Y, ScrollAmount.TOP)
            btn.click()
            self.omni_driver.wait(1)

    def clear_search_field(self):
        """Clears search field"""
        btn = self.omni_driver.find_element(self._clear_search_btn, True)
        self.log.info(f"Clear Button Visible: {btn.is_visible()}")
        if btn.is_visible():
            btn.click()
            self.omni_driver.wait(1)

    def zoom_out_graph(self, count=5):
        """Zooms out graph window for given number of times

        Args(self):
        count(int): Number of time to scroll
        """
        center = self.get_canvas_center
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        for _ in range(count):
            self.omni_driver.emulate_mouse_scroll("out", center[0], center[1])

    def add_new_variable(self):
        """Adds new variable to the list"""
        self.find_and_click(self._var_add_btn)
        self.omni_driver.wait(1)

    @property
    def skeleton_path(self):
        """Returns Skeleton path in the Create Animation Graph Window"""
        return self.omni_driver.find_element(self._skeleton_path_picker, True).get_text()

    @property
    def nodes_list(self):
        """Returns List containing names of all the nodes"""
        nodes_list = self.omni_driver.find_elements(self._root_node_names)
        return [node.get_text() for node in nodes_list]

    @property
    def chid_node_list(self):
        """Returns List containing names of all the child nodes"""
        nodes_list = self.omni_driver.find_elements(self._child_node_list)
        return [node.get_text() for node in nodes_list]

    @property
    def root_node_image_list(self):
        """Returns List containing names of all images for the root nodes"""
        image_urls = self.omni_driver.find_elements(self._root_node_images)
        return [os.path.split(image.image_source())[-1] for image in image_urls]

    @property
    def child_node_image_list(self):
        """Returns List containing names of all images for the child nodes"""
        image_urls = self.omni_driver.find_elements(self._child_node_image_list)
        return [os.path.split(image.image_source())[-1] for image in image_urls]

    @property
    def get_canvas_center(self):
        """Returns Canvas Center"""
        canvas = self.omni_driver.find_element(self._graph_canvas, True)
        return canvas.get_widget_center()
