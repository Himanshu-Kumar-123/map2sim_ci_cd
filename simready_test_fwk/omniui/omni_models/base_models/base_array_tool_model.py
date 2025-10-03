# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Content Model class
   This module contains the base methods for Base Array Tool Window
"""
import copy
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.omnielement import OmniElement


class BaseArrayToolModel(BaseModel):
    """Base model class for Array Tool window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for Array Tool window
    _array_tool_manupath = "Tools/Array"
    _array_tool_window = "Array Tool"
    _preview_btn = "Array Tool//Frame/**/HStack[0]/VStack[1]/Button[0]"
    _count = "Array Tool//Frame/**/HStack[1]/**/IntDrag[0]"
    _translate = "Array Tool//Frame/**/HStack[2]/**/MultiFloatDragField[*]"
    _rotate = "Array Tool//Frame/**/HStack[3]/**/MultiFloatDragField[*]"
    _scale = "Array Tool//Frame/**/HStack[4]/**/MultiFloatDragField[*]"
    _2d_replication_count = "Array Tool//Frame/**/HStack[5]/IntDrag[0]"
    _2d_replication_offset = "Array Tool//Frame/**/HStack[5]/**/MultiFloatDragField[0]"
    _3d_replication_count = "Array Tool//Frame/**/HStack[6]/IntDrag[0]"
    _3d_replication_offset = "Array Tool//Frame/**/HStack[6]/**/MultiFloatDragField[0]"
    _options_collapsible = "Array Tool//Frame/**/CollapsableFrame[*].title=='Options'"
    _instances_radio_btn = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[0]/**/RadioButton[0]"
    _copies_radio_btn = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[1]/**/RadioButton[0]"
    _group_results_chkbox = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[2]/**/CheckBox[0]"
    _follow_rotation_chkbox = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[3]/**/CheckBox[0]"
    _remember_values_chkbox = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[4]/**/CheckBox[0]"
    _auto_select_chkbox = "Array Tool//Frame/**/CollapsableFrame[0]/**/HStack[5]/**/CheckBox[0]"
    _apply_btn = "Array Tool//Frame/**/Button[*].text=='Apply'"

    def navigate_to_array_tool(self):
        """Navigates to the Array Tool window"""
        self.omni_driver.select_menu_option(self._array_tool_manupath)
        self.wait.element_to_be_located(self.omni_driver, self._array_tool_window)

    def toggle_preview(self, state: bool):
        """Toggles the Preview button
        Args:
            state (bool): expected state
        """
        btn: OmniElement = self.omni_driver.find_element(self._preview_btn, True)
        if btn.image_source(from_style=True).endswith("switch_on_dark.svg") and state is False:
            btn.click()
            assert btn.image_source(from_style=True).endswith("switch_off_dark.svg")
        elif btn.image_source(from_style=True).endswith("switch_off_dark.svg") and state is True:
            btn.click()
            assert btn.image_source(from_style=True).endswith("switch_on_dark.svg")
        else:
            self.log.info(f"Preview button is already {'on' if state else 'off'}")

        self.log_info_with_screenshot(
            f"Toggled preview button to '{'on' if state else 'off'}'",
            f"toggle_preview_{'on' if state else 'off'}",
        )

    def update_count(self, count: int):
        """Updates count
        Args:
            count (int): expected count
        """
        elm: OmniElement = self.omni_driver.find_element(self._count, True)
        elm.send_keys(str(count))
        self.log_info_with_screenshot(f"Updated count to: {count}", "update_count")

    def _refresh_coordinate_field(self, field: OmniElement):
        self.omni_driver.wait(1)
        x, y = field.get_widget_center()
        width = field.get_size_and_position("computed_width")
        self.omni_driver.click_at(x, y)
        self.omni_driver.wait(1)
        x1 = x + width / 2 - 20
        self.omni_driver.click_at(x1, y)
        self.omni_driver.wait(1)
        x2 = x - width / 2 + 20
        self.omni_driver.click_at(x2, y)
        self.omni_driver.wait(1)

    def transform_translate(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z translate values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        field: OmniElement = self.omni_driver.find_element(self._translate, True)
        vals = {}
        if x:
            vals[0] = x
        if y:
            vals[1] = y
        if z:
            vals[2] = z
        field.set_values_for_multifloatdragfield(vals)
        self._refresh_coordinate_field(field)
        self.log_info_with_screenshot(f"Updated translate values to: {x}, {y}, {z}", "translate")

    def transform_rotate(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z rotate values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        field: OmniElement = self.omni_driver.find_element(self._rotate, True)
        vals = {}
        if x:
            vals[0] = x
        if y:
            vals[1] = y
        if z:
            vals[2] = z
        field.set_values_for_multifloatdragfield(vals)
        self._refresh_coordinate_field(field)
        self.log_info_with_screenshot(f"Updated rotate values to: {x}, {y}, {z}", "rotate")

    def transform_scale(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z scale values for selected prim
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        field: OmniElement = self.omni_driver.find_element(self._scale, True)
        vals = {}
        if x:
            vals[0] = x
        if y:
            vals[1] = y
        if z:
            vals[2] = z
        field.set_values_for_multifloatdragfield(vals)
        self._refresh_coordinate_field(field)
        self.log_info_with_screenshot(f"Updated scale values to: {x}, {y}, {z}", "scale")

    def update_2d_replication_count(self, count):
        """Updates 2D replication count
        Args:
            count (int): expected count
        """
        elm: OmniElement = self.omni_driver.find_element(self._2d_replication_count, True)
        elm.send_keys(str(count))
        self.log_info_with_screenshot("Updated 2d replication count.", "2d_replication_count")

    def update_3d_replication_count(self, count):
        """Updates 3D replication count
        Args:
            count (int): expected count
        """
        elm: OmniElement = self.omni_driver.find_element(self._3d_replication_count, True)
        elm.send_keys(str(count))
        self.log_info_with_screenshot("Updated 3d replication count.", "3d_replication_count")

    def set_2d_replication_offset(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z offset values for 2d replication
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        field: OmniElement = self.omni_driver.find_element(self._2d_replication_offset, True)
        vals = {}
        if x:
            vals[0] = x
        if y:
            vals[1] = y
        if z:
            vals[2] = z
        field.set_values_for_multifloatdragfield(vals)
        self._refresh_coordinate_field(field)
        self.log_info_with_screenshot(f"Updated 2d replication offset to: {x}, {y}, {z}", "2d_replication_offset")

    def set_3d_replication_offset(self, x: float = None, y: float = None, z: float = None):
        """Adds X, Y and Z offset values for 3d replication
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        """
        field: OmniElement = self.omni_driver.find_element(self._3d_replication_offset, True)
        vals = {}
        if x:
            vals[0] = x
        if y:
            vals[1] = y
        if z:
            vals[2] = z
        field.set_values_for_multifloatdragfield(vals)
        self._refresh_coordinate_field(field)
        self.log_info_with_screenshot(f"Updated 2d replication offset to: {x}, {y}, {z}", "2d_replication_offset")

    def _open_options_collapsible(self):
        """Opens options collapsible"""
        elm: OmniElement = self.omni_driver.find_element(self._options_collapsible, True)
        if elm.is_collapsed():
            elm.click()
            # TODO: Remove retry steps after click issue is resolved: OM-102905
            retry = 4
            while elm.is_collapsed() and retry:
                elm.click()
                retry -= 1
            self.log_info_with_screenshot("Opened options collapsible", "options_collapsible")

    def select_create_instances(self):
        """Selects create instances radio button"""
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._instances_radio_btn, True)
        elm.click()
        self.log_info_with_screenshot("Selected create instances radio button", "create_instances")

    def select_create_copies(self):
        """Selects create copies radio button"""
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._copies_radio_btn, True)
        elm.click()
        self.log_info_with_screenshot("Selected create copies radio button", "create_copies")

    def toggle_group_results(self, state: bool):
        """Selects group results checkbox
        Args:
            state (bool): expected state
        """
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._group_results_chkbox, True)
        if elm.is_checked() and state is False:
            elm.click()
            assert not elm.is_checked(), "Clicking on group results did not disable the checkbox"
        elif not elm.is_checked() and state is True:
            elm.click()
            assert elm.is_checked(), "Clicking on group results did not enable the checkbox"
        else:
            self.log.info(f"Group results checkbox is already {'checked' if state else 'unchecked'}")

        self.log_info_with_screenshot(
            f"Group results checkbox is {'checked' if state else 'unchecked'}",
            f"group_results_{'checked' if state else 'unchecked'}",
        )

    def toggle_auto_select(self, state: bool):
        """Selects auto select checkbox
        Args:
            state (bool): expected state
        """
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._auto_select_chkbox, True)
        if elm.is_checked() and state is False:
            elm.click()
            assert not elm.is_checked(), "Clicking on auto select did not disable the checkbox"
        elif not elm.is_checked() and state is True:
            elm.click()
            assert elm.is_checked(), "Clicking on auto select did not enable the checkbox"
        else:
            self.log.info(f"Auto select checkbox is already {'checked' if state else 'unchecked'}")

        self.log_info_with_screenshot(
            f"Auto select checkbox is {'checked' if state else 'unchecked'}",
            f"auto_select_{'checked' if state else 'unchecked'}",
        )

    def toggle_follow_rotation(self, state: bool):
        """Selects follow rotation checkbox
        Args:
            state (bool): expected state
        """
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._follow_rotation_chkbox, True)
        if elm.is_checked() and state is False:
            elm.click()
            assert not elm.is_checked(), "Clicking on follow rotation did not disable the checkbox"
        elif not elm.is_checked() and state is True:
            elm.click()
            assert elm.is_checked(), "Clicking on follow rotation did not enable the checkbox"
        else:
            self.log.info(f"Follow rotation checkbox is already {'checked' if state else 'unchecked'}")

        self.log_info_with_screenshot(
            f"Follow rotation checkbox is {'checked' if state else 'unchecked'}",
            f"follow_rotation_{'checked' if state else 'unchecked'}",
        )

    def toggle_remember_values(self, state: bool):
        """Selects remember values checkbox
        Args:
            state (bool): expected state
        """
        self._open_options_collapsible()
        elm: OmniElement = self.omni_driver.find_element(self._remember_values_chkbox, True)
        if elm.is_checked() and state is False:
            elm.click()
            assert not elm.is_checked(), "Clicking on remember values did not disable the checkbox"
        elif not elm.is_checked() and state is True:
            elm.click()
            assert elm.is_checked(), "Clicking on remember values did not enable the checkbox"
        else:
            self.log.info(f"Remember values checkbox is already {'checked' if state else 'unchecked'}")

        self.log_info_with_screenshot(
            f"Remember values checkbox is {'checked' if state else 'unchecked'}",
            f"remember_values_{'checked' if state else 'unchecked'}",
        )

    def apply_settings(self):
        """Clicks on apply button"""
        elm = self.find_and_click(self._apply_btn, refresh=True)
        self.wait.window_to_be_invisible(self.omni_driver, self._array_tool_window)

    def numbered_asset_path(self, base_asset_path: str, num: int):
        """Returns the numbered asset path
        Args:
            base_asset_path (str): base asset path
            num (int): number to be appended
        """
        if num == 0:
            return base_asset_path
        elif num < 10:
            return f"{base_asset_path}_0{num}"
        else:
            return f"{base_asset_path}_{num}"

    def _convert_coordinates(
        self,
        original_coordinates,
        count,
        translate,
        rotate,
        scale,
        _2d_count,
        _2d_offset,
        _3d_count,
        _3d_offset,
    ):
        """Checks the new coordinates
        Args:
            original_coordinates (dict): previous coordinates
            count (int): expected count
            translate (list): expected translate values
            rotate (list): expected rotate values
            scale (list): expected scale values
            _2d_count (int): expected 2d count
            _2d_offset (list): expected offset values for 2d replication
            _3d_count (int): expected 3d count
            _3d_offset (list): expected offset values for 3d replication
        """
        coordinates = copy.deepcopy(original_coordinates)
        coordinates["translate"]["x"] += translate[0] * count
        coordinates["translate"]["y"] += translate[1] * count
        coordinates["translate"]["z"] += translate[2] * count
        coordinates["rotate"]["x"] += rotate[0] * count
        coordinates["rotate"]["y"] += rotate[1] * count
        coordinates["rotate"]["z"] += rotate[2] * count
        coordinates["scale"]["x"] += scale[0] * count
        coordinates["scale"]["y"] += scale[1] * count
        coordinates["scale"]["z"] += scale[2] * count
        coordinates["translate"]["x"] += _2d_offset[0] * _2d_count
        coordinates["translate"]["y"] += _2d_offset[1] * _2d_count
        coordinates["translate"]["z"] += _2d_offset[2] * _2d_count
        coordinates["translate"]["x"] += _3d_offset[0] * _3d_count
        coordinates["translate"]["y"] += _3d_offset[1] * _3d_count
        coordinates["translate"]["z"] += _3d_offset[2] * _3d_count

        return coordinates

    def validate(
        self,
        base_asset_path: str,
        count: int,
        translate: list,
        rotate: list,
        scale: list,
        _2d_count: int,
        _2d_offset: list,
        _3d_count: int,
        _3d_offset: list,
    ):
        """Validates the array tool settings
        Args:
            base_asset_path (str): path of asset which was used for array tool
            count (int): expected count
            translate (list): expected translate values
            rotate (list): expected rotate values
            scale (list): expected scale values
            _2d_count (int): expected 2d count
            _2d_offset (list): expected offset values for 2d replication
            _3d_count (int): expected 3d count
            _3d_offset (list): expected offset values for 3d replication
        """
        original_coordinates = self.omni_driver.get_prim_coordinates(base_asset_path)
        num = 0
        for _3d_cnt in range(_3d_count):
            for _2d_cnt in range(_2d_count):
                for cnt in range(count):
                    asset_path = self.numbered_asset_path(base_asset_path, num)
                    coordinates = self.omni_driver.get_prim_coordinates(asset_path)
                    expected_coordinates = self._convert_coordinates(
                        original_coordinates,
                        cnt,
                        translate,
                        rotate,
                        scale,
                        _2d_cnt,
                        _2d_offset,
                        _3d_cnt,
                        _3d_offset,
                    )
                    assert expected_coordinates == coordinates, (
                        f"CNT = {cnt}, For asset {asset_path}, expected coordinates are {expected_coordinates} but"
                        f" found {coordinates}"
                    )
                    num += 1

    def _get_group_path(self, base_asset_path: str):
        split_path = base_asset_path.split("/")
        base_asset_name = split_path[-1]
        split_path[-1] = "Group"
        split_path.append(base_asset_name)

        return "/".join(split_path)

    def validate_groups(self, base_asset_path: str, count: int):
        """Validates if new prims are grouped
        Args:
            base_asset_path (str): path of asset which was used for array tool
            count (int): expected count
        """
        base_asset_path = self._get_group_path(base_asset_path)
        for num in range(1, count):
            asset_path = self.numbered_asset_path(base_asset_path, num)
            try:
                self.omni_driver.get_prim_coordinates(asset_path)
            except Exception:
                assert False, f"Could not find asset at path: {asset_path}"

    def validate_auto_select(self, base_asset_path: str, count: int):
        """Validates if new prims are auto selected
        Args:
            base_asset_path (str): path of asset which was used for array tool
            count (int): expected count
        """
        expected_selected_prims = []
        for num in range(1, count):
            asset_path = self.numbered_asset_path(base_asset_path, num)
            expected_selected_prims.append(asset_path)

        selected_prims = [
            x.lstrip("Usd.Prim(<").rstrip(">)") for x in self.omni_driver.get_stage(get_selected_only=True)
        ]
        assert set(selected_prims).issubset(
            expected_selected_prims
        ), f"Expected selected prims: {expected_selected_prims}. Actual selected prims: {selected_prims}"

    def validate_remember_values(
        self,
        translate: list,
        rotate: list,
        scale: list,
        _2d_count: int,
        _2d_offset: list,
        _3d_count: int,
        _3d_offset: list,
    ):
        """Validates if previous values are retained by the Array Tool
        Args:
            translate (list): expected translate values
            rotate (list): expected rotate values
            scale (list): expected scale values
            _2d_count (int): expected 2d count
            _2d_offset (list): expected offset values for 2d replication
            _3d_count (int): expected 3d count
            _3d_offset (list): expected offset values for 3d replication
        """
        assert translate == self.omni_driver.find_element(self._translate, True).get_multifloatdragfield_values()
        assert rotate == self.omni_driver.find_element(self._rotate, True).get_multifloatdragfield_values()
        assert scale == self.omni_driver.find_element(self._scale, True).get_multifloatdragfield_values()
        assert _2d_count == int(self.omni_driver.find_element(self._2d_replication_count, True).get_value())
        assert (
            _2d_offset
            == self.omni_driver.find_element(self._2d_replication_offset, True).get_multifloatdragfield_values()
        )
        assert _3d_count == int(self.omni_driver.find_element(self._3d_replication_count, True).get_value())
        assert (
            _3d_offset
            == self.omni_driver.find_element(self._3d_replication_offset, True).get_multifloatdragfield_values()
        )
