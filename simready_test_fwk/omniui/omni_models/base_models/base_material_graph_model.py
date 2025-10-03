"""Base Material Graph Model class
   This module contains the base methods for Material Graph toolbar window
"""
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement
import re
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis


class BaseMaterialGraphModel(BaseModel):
    """Base model class for Material Graph Model window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _material_graph_window = "Material Graph//Frame/*"
    _material_graph_treeview = "Material Graph//Frame/**/TreeView[*].visible==True"
    _material_graph_node = "**/Label[*].text=='{0}'"
    _material_graph_new_btn = "Material Graph//Frame/**/ZStack[0]/**/Button[1]"
    _play_btn = "Material Graph//Frame/Frame[0]/VStack[0]/Frame[0]/HStack[0]/Button[7]"
    _search_node = "Material Graph//Frame/**/Frame[0]/**/StringField[0]"
    _clear_search_btn = "Material Graph//Frame/**/Frame[1]/**/Frame[0]/**/VStack[0]/Button[0]"
    _graph_canvas = "Material Graph//Frame/**/CanvasFrame[0]"
    _node_label = "Material Graph//Frame/**/ScrollingFrame[0]/TreeView[0]/HStack[0]/VStack[0]/Label[*].text == '{}'"
    _omni_pbr_out_port = "**/ZStack[0]/VStack[0]/HStack[1]/ZStack[1]/Frame[0]/ZStack[0]/Circle[1]"
    _mdl_surface_port = "**/ZStack[0]/VStack[0]/HStack[5]/ZStack[0]/Frame[0]/Frame[0]/HStack[0]/ZStack[0]/Circle[0]"
    _alfredo_color_port = "**/ZStack[0]/VStack[0]/HStack[3]/ZStack[0]/Frame[0]/HStack[0]/ZStack[0]/Circle[1]"
    _opacity_amount_port = "**/ZStack[0]/VStack[0]/HStack[16]/ZStack[0]/Frame[0]/HStack[0]/ZStack[0]/Circle[0]"
    _mono_port = "**/ZStack[0]/VStack[0]/HStack[1]/**/Frame[0]/ZStack[0]/Circle[1]"
    _color_port = "**/ZStack[0]/VStack[0]/HStack[1]/VStack[1]/HStack[1]/ZStack[0]/Frame[0]/ZStack[0]/Circle[1]"
    _node_title = "Material Graph//Frame/**/CanvasFrame[0]/**/Label[*].text=='{}'"
    _node_placer = "Material Graph//Frame/**/CanvasFrame[0]/**/Placer[{}]"

    def navigate_to_window(self):
        """Navigates to Material Graph window"""
        _window = self.omni_driver.find_element(self._material_graph_window)
        _window.click()
        self.screenshot("navigated_to_material_graph")
    
    def fetch_node_count_from_tree_view(self, node_name: str):
        """
            Fetches Node Count of particular Node from Tree View

        Args:
            node_name (str): Name of the Node
        """
        tree_main_view = self.omni_driver.find_element(self._material_graph_treeview)
        tree_child_node = tree_main_view.find_element(self._material_graph_node.format(node_name))
        tree_child_node.scroll_into_view(
            axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM
        )
        tree_child_first_parent_list = tree_child_node.find_parent_element_path().split("/")[:-1]
        tree_child_first_parent_path = "/".join(tree_child_first_parent_list)
        tree_first_parent_element = self.omni_driver.find_element(tree_child_first_parent_path)
        node_count = int(tree_first_parent_element.find_element("**/Label[1]").get_text())
        return node_count

    def expand_node_from_tree_view(self, node_name: str):
        """
            Expands particular Node from Tree View

        Args:
            node_name (str): Name of the Node
        """
        tree_main_view = self.omni_driver.find_element(self._material_graph_treeview)
        tree_child_node = tree_main_view.find_element(self._material_graph_node.format(node_name))
        tree_child_node.scroll_into_view(
            axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM
        )
        tree_child_first_parent_list = tree_child_node.find_parent_element_path().split("/")[:-1]
        tree_child_first_parent_name = tree_child_first_parent_list[-1]
        node_num_start = tree_child_first_parent_name.find("[")+1
        node_num_end = tree_child_first_parent_name.find("]")
        tree_child_expand_node_num = int(
            tree_child_first_parent_name[node_num_start:node_num_end]) - 1
        tree_child_expand_path = tree_child_first_parent_name[:node_num_start] + \
            str(tree_child_expand_node_num) + \
            tree_child_first_parent_name[node_num_end:]
        tree_child_first_parent_list[-1] = tree_child_expand_path
        tree_child_expand_path = "/".join(tree_child_first_parent_list)
        tree_child_expand_element = self.omni_driver.find_element(tree_child_expand_path)
        tree_child_expand_element.find_element("**/ImageWithProvider[0]").click()
        self.omni_driver.wait(seconds=2)

    def fetch_subnode_under_node_from_tree_view(self, node_name: str):
        """
            Fetches Sub-Nodes of particular Node from Tree View

        Args:
            node_name (str): Name of the Node
        """
        tree_main_view = self.omni_driver.find_element(self._material_graph_treeview)
        tree_child_node = tree_main_view.find_element(self._material_graph_node.format(node_name))
        tree_child_node.scroll_into_view(
            axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM
        )
        tree_child_second_parent_list = tree_child_node.find_parent_element_path().split("/")[:-2]
        tree_child_second_parent_path = "/".join(tree_child_second_parent_list)
        tree_second_parent_element = self.omni_driver.find_element(tree_child_second_parent_path)
        subnode_all_elements = tree_second_parent_element.find_elements("HStack[*]")
        subnode_names = []
        for subnode_element in subnode_all_elements:
            subnode_element.scroll_into_view(
                axis=ScrollAxis.Y, scroll_amount=ScrollAmount.BOTTOM
            )
            subnode_label = subnode_element.find_element("**/Label[0]")
            subnode_names.append(subnode_label.get_text())
        return subnode_names

    def enable_material_graph_window(self):
        """Enables Material Graph window from menubar"""
        self.omni_driver.select_menu_option("Window/Rendering/MDL Material Graph")

    def new_material_graph(self):
        """Clicks on 'New Material Graph' button in the Material Graph Window"""
        self.find_and_click(self._material_graph_new_btn)
        self.omni_driver.wait(1)

    def select_node_in_canvas(self, x: int, y: int):
        """Selects node in canvas
        Args:
            x: x- coordinate of node
            y: y- coordinate of node
        """
        self.omni_driver.click_at(x, y)

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

    def drag_node_to_material_graph(self, node_name: str, x: int, y: int):
        """Drags the given node to the Material Graph

        Args:
        node_name(str): name of the node
        x(str): offset from center of canvas
        y(str): offset from center of canvas
        """
        self.clear_search_field()
        self.find_and_enter_text(self._search_node, node_name)
        center = self.get_canvas_center
        node = self.omni_driver.find_element(self._node_label.format(node_name), True)
        node.drag_and_drop(center[0] + x, center[1] + y)
        self.omni_driver.wait(1)

    def select_node_material(self, node_name: str, stage_name: str = ""):
        """Selects the node with given name

        Args:
            node_name (str): Name of the node
            stage_name (str): Stage name of the asset if different
        """
        node_elm: OmniElement = self.omni_driver.find_element(self._node_title.format(node_name), True)
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

    def connect_ports_material(self, from_node: str, from_port: str, to_node: str, to_port: str):
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
        node_elm: OmniElement = self.omni_driver.find_element(self._node_title.format(node), True)
        node_path = node_elm.path
        re_pattern = r"Placer\[(\d+)\]"
        match = re.search(re_pattern, node_path)
        assert match, f"Could not find Placer Widget of {node} Node."
        node_placer_index = match.group(1)

        node_placer: OmniElement = self.omni_driver.find_element(self._node_placer.format(node_placer_index),
                                                                 True)
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

    def click_play_button(self):
        """Clicks on play button in the Material Graph Window"""
        self.find_and_click(self._play_btn)
        self.omni_driver.wait(1)