# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Action Graph Model class
   This module contains the base methods for Action Graph window
"""
import os
from omni_remote_ui_automator.driver.omnielement import OmniElement
import re
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import CreateNodeForPrim
from pynput.keyboard import Key, Controller


class BaseActionGraphModel(BaseModel):
    """Base model class for Action Graph window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _window_name = "Action Graph"
    _action_graph_edit_btn = "Action Graph//Frame/**/Button[*].text == 'Edit Action Graph'"
    _action_graph_new_btn = "Action Graph//Frame/**/Button[*].text == 'New Action Graph'"
    _node_label = "Action Graph//Frame/Frame[0]/**/VStack[0]/ScrollingFrame[0]/TreeView[0]/**/Label[0].text == '{}'"
    _search_node = "Action Graph//Frame/**/VStack[0]/ZStack[0]/Frame[0]/Frame[0]/**/StringField[0]"
    _clear_search_btn = "Action Graph//Frame/**/VStack[0]/ZStack[0]/Frame[0]/Frame[0]/**/Button[0]"
    _select_graph_window = "Select Graph To Open"
    _select_graph_btn = "Select Graph To Open//Frame/**/Button[{}]"
    _select_graph_by_path_btn = "Select Graph To Open//Frame/**/Button[*].text=='{}'"
    _graph_canvas = "Action Graph//Frame/**/CanvasFrame[0]"
    _graph_node_title = "Action Graph//Frame/**/CanvasFrame[0]/**/Label[*].text=='{}'"
    _node_placer = "Action Graph//Frame/**/CanvasFrame[0]/**/Placer[{}]"
    _view_btn = "Action Graph//Frame/Frame[0]/VStack[0]/Frame[0]/HStack[0]/Button[6]"
    _tick = "**/ZStack[0]/VStack[0]/HStack[1]/**/Frame[0]/ZStack[0]/HStack[0]/Image[0]"
    _exec_in =  "**/ZStack[0]/VStack[0]/HStack[1]/**/ZStack[0]/HStack[0]/VStack[0]/Image[0]"
    _animation_time = "**/ZStack[0]/VStack[0]/HStack[4]/**/Frame[0]/ZStack[0]/ZStack[0]/HStack[0]/Circle[0]"
    _time = "**/ZStack[0]/VStack[0]/HStack[4]/**/ZStack[0]/ZStack[0]/HStack[0]/VStack[0]/ImageWithProvider[0]"
    _exec_out = "**/ZStack[0]/VStack[0]/HStack[2]/**/Frame[0]/ZStack[0]/HStack[0]/Image[0]"
    _position = "**/ZStack[0]/VStack[0]/HStack[5]/**/Frame[0]/ZStack[0]/ZStack[0]/HStack[0]/Circle[0]"
    _value = "**/ZStack[0]/VStack[0]/HStack[7]/**/ZStack[0]/ZStack[0]/HStack[0]/VStack[0]/ImageWithProvider[0]"
    # On Keyboard Input action graph connector nodes
    _key_pressed_node = "**/ZStack[0]/VStack[0]/HStack[1]/ZStack[1]/Frame[0]/ZStack[0]/HStack[0]/Image[0]"
    _timer_play_node = "**/ZStack[0]/ZStack[0]/VStack[0]/HStack[1]/ZStack[0]/Frame[0]/ZStack[0]/HStack[0]/VStack[0]/Image[0]"
    _timer_updated_node = "**/ZStack[0]/ZStack[0]/VStack[0]/HStack[3]/ZStack[1]/Frame[0]/ZStack[0]/HStack[0]/Image[0]"
    _blend_variant_exec_in_node = "**/ZStack[0]/ZStack[0]/VStack[0]/HStack[1]/ZStack[0]/Frame[0]/ZStack[0]/HStack[0]/VStack[0]/Image[0]"
    _timer_value_node = "**/ZStack[0]/ZStack[0]/VStack[0]/HStack[7]/ZStack[1]/Frame[0]/ZStack[0]/ZStack[0]/HStack[0]/Circle[0]"
    _blend_variant_blend_node = "/ZStack[0]/ZStack[0]/VStack[0]/HStack[3]/ZStack[0]/Frame[0]/ZStack[0]/ZStack[0]/HStack[0]/VStack[0]/ImageWithProvider[0]"
    _create_node_for_prim_window = "Create Node for Prim"
    _create_node_for_prim_option = "Create Node for Prim//Frame/**/Label[*].text=='{}'"

    def enable_action_graph_window(self):
        """Enables Action Graph window from menubar"""
        self.omni_driver.select_menu_option("Window/Visual Scripting/Action Graph")
        assert self._window_name in self.omni_driver.get_windows()[
            "visible_windows"], "Action Graph window was not enabled."

    def new_action_graph(self):
        """Clicks on 'New Action Graph' button in the Action Graph Window"""
        count = len(self.omni_driver.get_stage())
        self.find_and_click(self._action_graph_new_btn)
        self.omni_driver.wait(1)
        new_count = len(self.omni_driver.get_stage())

        attempt = 3
        while new_count < count:
            new_count = len(self.omni_driver.get_stage())
            if attempt == 0:
                break
            attempt -= 1
            self.omni_driver.wait(1)
        assert new_count > count, "New Action Graph was not created. Count of prims should have increased"

    def edit_action_graph(self, index: int = 0, graph_path: str = None):
        """Opens an action graph for editing. Can either use index or graph path.
        Args:
            index (int, optional): Index of the action graph in Select Graph To Open window . Defaults to 0.
            graph_path (str, optional): path of the graph to select. Defaults to None.
        """
        self.find_and_click(self._action_graph_edit_btn)
        if graph_path is not None:
            btn = self.wait.element_to_be_located(self.omni_driver, self._select_graph_by_path_btn.format(graph_path))
        else:
            btn = self.wait.element_to_be_located(self.omni_driver, self._select_graph_btn.format(index))
        btn.click()
        self.wait.window_to_be_invisible(self.omni_driver, self._select_graph_window)
    

    def drag_node_to_graph(self, node_name: str, x: int, y: int):
        """Drags the given node to the Action Graph

        Args:
        node_name(str): name of the node
        x(str): offset from center of canvas
        y(str): offset from center of canvas
        """
        count = len(self.omni_driver.get_stage())
        self.clear_search_field()
        self.find_and_enter_text(self._search_node, node_name)
        center = self.get_canvas_center
        node = self.omni_driver.find_element(self._node_label.format(node_name), True)
        node.drag_and_drop(center[0] + x, center[1] + y)
        self.omni_driver.wait(1)

        new_count = len(self.omni_driver.get_stage())
        attempt = 3
        while new_count < count:
            new_count = len(self.omni_driver.get_stage())
            if attempt==0:
                break
            attempt -= 1
            self.omni_driver.wait(1)
        assert new_count > count, f"{node_name} node was not added. Count of prims should have increased"

    def clear_search_field(self):
        """Clears search field"""
        btn = self.omni_driver.find_element(self._clear_search_btn, True)
        self.log.info(f"Clear Button Visible: {btn.is_visible()}")
        if btn.is_visible():
            btn.click()
            self.omni_driver.wait(1)

    @property
    def get_canvas_center(self):
        """Returns Canvas Center"""
        canvas = self.omni_driver.find_element(self._graph_canvas, True)
        return canvas.get_widget_center()

    @property
    def get_canvas_dimensions(self):
        """Returns all dimensions of the Canvas
        """
        canvas: OmniElement = self.omni_driver.find_element(self._graph_canvas, True)
        return canvas.get_size_and_position("all")

    def select_node_in_canvas(self, x: int, y: int):
        """Selects node in canvas
        Args:
            x: x- coordinate of node
            y: y- coordinate of node
        """
        self.omni_driver.click_at(x, y)

    def convert_graph_coordinates_to_screen(self, x: float, y: float) -> tuple:
        """Converts given graph coordinates to screen coordinates

        Args:
            x (float): x coordinate
            y (float): y coordinate

        Returns:
            tuple: converted x and y coordinates
        """
        canvas_elm: OmniElement = self.omni_driver.find_element(self._graph_canvas, True)
        canvas_coordinates = canvas_elm.get_size_and_position("all")
        canvas_properties = canvas_elm.get_canvas_properties()
        pan_x = canvas_properties["pan_x"]
        pan_y = canvas_properties["pan_y"]
        zoom = canvas_properties["zoom"]

        new_x = x * zoom + pan_x + canvas_coordinates["screen_position_x"]
        new_y = y * zoom + pan_y + canvas_coordinates["screen_position_y"]

        return (new_x, new_y)

    def find_placer_for_node(self, node: str) -> OmniElement:
        """Finds the Placer widget the node is contained in.

        Args:
            node (str): Name of the node

        Returns:
            OmniElement: Placer widget
        """
        node_elm: OmniElement = self.omni_driver.find_element(self._graph_node_title.format(node), True)
        node_path = node_elm.path
        re_pattern = r"Placer\[(\d+)\]"
        match = re.search(re_pattern, node_path)
        assert match, f"Could not find Placer Widget of {node} Node."
        node_placer_index = match.group(1)

        node_placer: OmniElement = self.omni_driver.find_element(self._node_placer.format(node_placer_index), True)
        return node_placer

    def connect_ports(self, from_node: str, from_port: str, to_node: str, to_port: str):
        """Creates a connection between two ports of two graph nodes.
        Make sure to select "View/Node Header/Prim Name" in Action Graph window to have unique node names.

        Args:
            from_node (str): Name of the node to create connection from.
            from_port (str): Locator of the port, relative to its node's Placer widget, to create connection from.
            to_node (str): Name of the node to create connection to.
            to_port (str): Locator of the port, relative to its node's Placer widget, to create connection to.
        """
        from_node_placer: OmniElement = self.find_placer_for_node(from_node)
        to_node_placer: OmniElement = self.find_placer_for_node(to_node)

        from_port_elm: OmniElement = from_node_placer.find_element(from_port, True)
        to_port_elm: OmniElement = to_node_placer.find_element(to_port, True)

        from_port_center = from_port_elm.get_widget_center()
        to_port_center = to_port_elm.get_widget_center()

        from_x, from_y = self.convert_graph_coordinates_to_screen(from_port_center[0], from_port_center[1])
        to_x, to_y = self.convert_graph_coordinates_to_screen(to_port_center[0], to_port_center[1])

        self.omni_driver.emulate_mouse_move(from_x + 1, from_y + 1)  # to get more accuracy in actions.
        self.omni_driver.drag_from_and_drop_to(from_x, from_y, to_x, to_y)
        self.log_info_with_screenshot(f"Created connection from {from_node} to {to_node}", "action_graph_connection")

    def disconnect_port(self, node_name: str, port: str):
        """Disconnects the connections at given port of given node

        Args:
            node_name (str): name of the node
            port (str): name of the port to disconnect
        """
        node_placer: OmniElement = self.find_placer_for_node(node_name)
        port_elm: OmniElement = node_placer.find_element(port, True)

        port_center = port_elm.get_widget_center()
        x, y = self.convert_graph_coordinates_to_screen(port_center[0], port_center[1])
        self.omni_driver.click_at(x, y, right=True)
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Disconnect")

        self.log_info_with_screenshot(f"Disconnected the port of {node_name} node.", "node_disconnect")

    def select_node(self, node_name: str, stage_name: str = ""):
        """Selects the node with given name

        Args:
            node_name (str): Name of the node
            stage_name (str): Stage name of the asset if different
        """
        node_elm: OmniElement = self.omni_driver.find_element(self._graph_node_title.format(node_name), True)
        x, y = node_elm.get_widget_center()

        new_x, new_y = self.convert_graph_coordinates_to_screen(x, y)

        self.omni_driver.emulate_mouse_move(new_x + 1, new_y + 1)  # to get more accuracy in actions.
        self.omni_driver.click_at(new_x, new_y)
        self.omni_driver.wait(1)

        is_selected = False
        all_selected = self.omni_driver.get_stage(get_selected_only=True)
        for selected in all_selected:
            if node_name in selected:
                is_selected = True
                break

        # for some node node_name and stage_name are different if stage name is different we can validate with satge name
        if len(stage_name) > 0:
            for selected in all_selected:
                if stage_name in selected:
                    is_selected = True
                    break

        assert is_selected, f"Failed to select {node_name} node"
        self.log_info_with_screenshot(f"Clicked on node {node_name} to select it", "node_selected")

    def select_multiple_nodes(self, nodes: list):
        """Selects multiple nodes with given names

        Args:
            nodes (list): namaes of nodes to select
        """
        keyboard = Controller()
        with keyboard.pressed(Key.ctrl.value):
            for node in nodes:
                self.select_node(node)

        assert len(nodes) == len(self.omni_driver.get_stage(get_selected_only=True)), "Could not select multiple nodes."

    def select_prim_name(self):
        self.find_and_click(self._view_btn)
        self.omni_driver.select_context_menu_option("Node Header/Use Prim Name")

    def get_port(self, port_name):
        """ returns the locator of required port """
        ports = {}
        ports['tick'] = self._tick
        ports['exec_in'] = self._exec_in
        ports['animation_time'] = self._animation_time
        ports['time'] = self._time
        ports['exec_out'] = self._exec_out
        ports['position'] = self._position
        ports['value'] = self._value
        ports['pressed'] = self._key_pressed_node
        ports['timer_play'] = self._timer_play_node
        ports['timer_updated'] = self._timer_updated_node
        ports['timer_value'] = self._timer_value_node
        ports['blend_variant_exec_in'] = self._blend_variant_exec_in_node
        ports['blend_variant_blend'] = self._blend_variant_blend_node
        return ports[port_name]

    def create_node_for_prim(self, node_type: CreateNodeForPrim):
        """Selects appropriate option from the 'Create Node For Prim' window

        Args:
            node_type (CreateNodeForPrim): option to be selected in Create Node For Prim window.
        """
        self.wait.window_to_be_visible(self.omni_driver, self._create_node_for_prim_window)
        self.find_and_click(self._create_node_for_prim_option.format(node_type.value), refresh=True)

    def zoom_out_graph(self, count=5, x: float = None, y: float = None):
        """Zooms out graph window for given number of times

        Args:
            count (int): Number of time to scroll
        """
        if x is None or y is None:
            x, y = self.get_canvas_center
        self.omni_driver.emulate_mouse_move(x, y)
        for _ in range(count):
            self.omni_driver.emulate_mouse_scroll("out", 0, 50)
        self.log_info_with_screenshot("Zoomed out of graph", "zoom_out_graph")
    
    def zoom_in_graph(self, count=5, x: float = None, y: float = None):
        """Zooms in graph window for given number of times

        Args:
            count (int): Number of time to scroll
        """
        if x is None or y is None:
            x, y = self.get_canvas_center
        self.omni_driver.emulate_mouse_move(x, y)
        for _ in range(count):
            self.omni_driver.emulate_mouse_scroll("in", 0, 50)
        self.log_info_with_screenshot("Zoomed in of graph", "zoom_in_graph")

    def move_node(self, node_name: str, to_x: float, to_y: float):
        """Moves the node to given coordinates (w.r.t Graph canvas center) by dragging it.

        Args:
            node_name (str): name of the node
            to_x (float): x coordinate offset from Graph canvas Center
            to_y (float): y coordinate offset from Graph canvas Center
        """
        self.select_node(node_name)

        node_elm: OmniElement = self.omni_driver.find_element(self._graph_node_title.format(node_name), True)
        x, y = node_elm.get_widget_center()

        new_x, new_y = self.convert_graph_coordinates_to_screen(x, y)
        canvas_center = self.get_canvas_center

        self.omni_driver.emulate_mouse_move(new_x + 1, new_y + 1)  # to get more accuracy in actions.
        self.omni_driver.wait(1)
        self.omni_driver.drag_from_and_drop_to(new_x, new_y, canvas_center[0] + to_x, canvas_center[1] + to_y)
        self.omni_driver.wait(1)

        self.log_info_with_screenshot(f"Moved the '{node_name}' node to ({to_x}, {to_y}) w.r.t graph canvas center",
                                      "moved_node")

    def get_node_label_center(self, node_name: str):
        """Gets the coordinates of center of a node label

        Args:
            node_name (str): Name of the node
        """
        node_elm: OmniElement = self.omni_driver.find_element(self._graph_node_title.format(node_name), True)
        x, y = node_elm.get_widget_center()

        new_x, new_y = self.convert_graph_coordinates_to_screen(x, y)

        return (new_x, new_y)