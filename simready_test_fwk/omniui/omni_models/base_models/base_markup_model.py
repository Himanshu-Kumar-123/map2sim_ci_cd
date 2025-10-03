# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Markup class
   This module contains the base methods for Markup window"""


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.enums import (
    MarkupsSize,
    MarkupType,
    MarkupsArrow,
    MarkupsShape,
)
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis


class BaseMarkupModel(BaseModel):
    """Base model class for Markup window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Markup locators
    _add_markup_btn_navbar = "Viewport//Frame/**/Button[*].name=='markup'"
    markups_window = "Markups"
    _add_markup_btn = "Markups//Frame/**/Button[0].name=='add_markup'"
    all_markups_list = "Markups//Frame/VStack[0]/ScrollingFrame[0]/VStack[0]/ZStack[*]"
    _markups_collapse_bar = "Markups//Frame//ScrollingFrame[0]/VStack[0]/ZStack[__markup__]/**/CollapsableFrame[0]"
    _markups_name_change = "Markups//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__markup__]/**/StringField[0]"
    _markup_select_btn = "Viewport//Frame/**/_markup_select_btn"
    _markup_enable_btn = "Viewport//Frame/**/_markup___type___btn"
    _markup_comment_btn = "Viewport//Frame/**/_markup_comment_btn"
    _markup_draw_btn = "Viewport//Frame/**/_markup_draw_btn"
    _markup_line_btn = "Viewport//Frame/**/_markup_line_btn"
    _markup_arrow_btn = "Viewport//Frame/**/_markup_arrow_btn"
    _markup_shapes_btn = "Viewport//Frame/**/_markup_shapes_btn"
    markup_apply_btn = "Viewport//Frame/**/_markup_markup_apply_btn"
    _markup_cancel_btn = "Viewport//Frame/**/_markup_markup_cancel_btn"
    _markup_unlock_btn = "Viewport//Frame/**/_markup_markup_unlock_btn"
    _markup_exit_btn = "Viewport//Frame/**/_markup_markup_exit_btn"
    _markup_shapes_shape_rectangle_btn = (
        "Viewport//Frame/**/_markup_shapes_shape_rectangle_btn"
    )
    _markup_shapes_shape_circle_btn = (
        "Viewport//Frame/**/_markup_shapes_shape_circle_btn"
    )
    _markup_shapes_color_color_btn = "Viewport//Frame/**/_markup_shapes_color_color_btn"
    _markup_shapes_stroke_stroke_s_btn = (
        "Viewport//Frame/**/_markup_shapes_stroke_stroke_s_btn"
    )
    _markup_shapes_stroke_stroke_m_btn = (
        "Viewport//Frame/**/_markup_shapes_stroke_stroke_m_btn"
    )
    _markup_shapes_stroke_stroke_l_btn = (
        "Viewport//Frame/**/_markup_shapes_stroke_stroke_l_btn"
    )
    _markup_shapes_stroke_stroke_xl_btn = (
        "Viewport//Frame/**/_markup_shapes_stroke_stroke_xl_btn"
    )
    _markup_line_color_color_btn = "Viewport//Frame/**/_markup_line_color_color_btn"
    _markup_line_stroke_stroke_s_btn = (
        "Viewport//Frame/**/_markup_line_stroke_stroke_s_btn"
    )
    _markup_line_stroke_stroke_m_btn = (
        "Viewport//Frame/**/_markup_line_stroke_stroke_m_btn"
    )
    _markup_line_stroke_stroke_l_btn = (
        "Viewport//Frame/**/_markup_line_stroke_stroke_l_btn"
    )
    _markup_line_stroke_stroke_xl_btn = (
        "Viewport//Frame/**/_markup_line_stroke_stroke_xl_btn"
    )
    _markup_arrow_arrow_arrow_start_btn = (
        "Viewport//Frame/**/_markup_arrow_arrow_arrow_start_btn"
    )
    _markup_arrow_arrow_arrow_end_btn = (
        "Viewport//Frame/**/_markup_arrow_arrow_arrow_end_btn"
    )
    _markup_arrow_arrow_arrow_double_btn = (
        "Viewport//Frame/**/_markup_arrow_arrow_arrow_double_btn"
    )
    _markup_arrow_color_color_btn = "Viewport//Frame/**/_markup_arrow_color_color_btn"
    _markup_arrow_stroke_stroke_s_btn = (
        "Viewport//Frame/**/_markup_arrow_stroke_stroke_s_btn"
    )
    _markup_arrow_stroke_stroke_m_btn = (
        "Viewport//Frame/**/_markup_arrow_stroke_stroke_m_btn"
    )
    _markup_arrow_stroke_stroke_l_btn = (
        "Viewport//Frame/**/_markup_arrow_stroke_stroke_l_btn"
    )
    _markup_arrow_stroke_stroke_xl_btn = (
        "Viewport//Frame/**/_markup_arrow_stroke_stroke_xl_btn"
    )
    _markup_draw_color_color_btn = "Viewport//Frame/**/_markup_draw_color_color_btn"
    _markup_draw_stroke_stroke_s_btn = (
        "Viewport//Frame/**/_markup_draw_stroke_stroke_s_btn"
    )
    _markup_draw_stroke_stroke_m_btn = (
        "Viewport//Frame/**/_markup_draw_stroke_stroke_m_btn"
    )
    _markup_draw_stroke_stroke_l_btn = (
        "Viewport//Frame/**/_markup_draw_stroke_stroke_l_btn"
    )
    _markup_draw_stroke_stroke_xl_btn = (
        "Viewport//Frame/**/_markup_draw_stroke_stroke_xl_btn"
    )
    _markup_comment_color_color_btn = (
        "Viewport//Frame/**/_markup_comment_color_color_btn"
    )
    _markup_comment_text_text_s_btn = (
        "Viewport//Frame/**/_markup_comment_text_text_s_btn"
    )
    _markup_comment_text_text_m_btn = (
        "Viewport//Frame/**/_markup_comment_text_text_m_btn"
    )
    _markup_comment_text_text_l_btn = (
        "Viewport//Frame/**/_markup_comment_text_text_l_btn"
    )
    _markup_comment_text_text_xl_btn = (
        "Viewport//Frame/**/_markup_comment_text_text_xl_btn"
    )
    _markup_comment_text_input_box = "Viewport//Frame/**/ZStack[1]/text_input_field"
    delete_markup_btn = (
        "Markups//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__markup__]/**/Button[1]"
    )
    _rename_markup_contenxt_menu = "Rename Markup"
    _markup_collapse_bar = "Markups//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__markup__]/**/CollapsableFrame[0]"
    _markup_label = (
        "Markups//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[*]/**/Label[0]"
    )
    _specific_markup = (
        "Markups//Frame/**/ScrollingFrame[0]/VStack[0]/ZStack[__markup__]"
    )
    _edit_markup_btn = _specific_markup + "/**/Button[0].name=='edit'"

    _markups_shape_type_btn = (
        "Viewport//Frame/**/_markup_shapes_shape___markup_shape___btn"
    )
    _markup_comment_text_text_size_btn = (
        "Viewport//Frame/**/_markup_comment_text_text___size___btn"
    )
    _markups_shape_type_btn = (
        "Viewport//Frame/**/_markup_shapes_shape___markup_shape___btn"
    )
    _markup_comment_text_text_size_btn = (
        "Viewport//Frame/**/_markup_comment_text_text___size___btn"
    )
    _markup_size = "Viewport//Frame/**/_markup___type___stroke_stroke___size___btn"
    _markup_elements = "Viewport//Frame/**/CanvasFrame[0]/**/Placer[2]/VStack[0]/ZStack[0]/ZStack[0]/Frame[0]/ZStack[0]/ZStack[*]"
    _markup_previous_button = "Markups//Frame/**/Button[*].name=='previous'"
    _markup_play_button = "Markups//Frame/**/Button[*].name=='play'"
    _markup_next_button = "Markups//Frame/**/Button[*].name=='next'"
    _markup_pause_button = "Markups//Frame/**/Button[*].name=='pause'"
    _markup_thumbnail = (
        "Markups//Frame/**/ScrollingFrame[0]/**/ZStack[{}]/**/ImageWithProvider[0]"
    )
    _markup_arrow_type = (
        "Viewport//Frame/**/_markup_arrow_arrow_arrow___arrow_type___btn"
    )
    _markup_thumbnail = (
        "Markups//Frame/**/ScrollingFrame[0]/**/ZStack[{}]/**/ImageWithProvider[0]"
    )
    _markup_arrow_type = (
        "Viewport//Frame/**/_markup_arrow_arrow_arrow___arrow_type___btn"
    )

    _export_markup = "Markups//Frame/**/ExportButton"
    _markup_name = "Markups//Frame/**/Label[0].text=='__name__'"
    _markup_note = "Markups//Frame/**/CommentEditField"
    _close_markup_btn = (
        "Markups//Frame/VStack[0]/VStack[0]/ZStack[0]/HStack[0]/Frame[0]"
    )

    _secondary_toolbar_widget = "Viewport//Frame/**/_markup_element_toolbar_frame"
    _primary_toolbar_widget = "Viewport//Frame/**/_markup_toolbar_frame"
    _edit_toolbar_widget = "Viewport//Frame/**/Placer[*]/_markup_element_editbar_frame"

    _navigation_bar_btn = "Viewport//Frame/**/ZStack[4]/Frame[1]/ZStack[0]/VStack[0]/**/Menu[0]/MenuItem[0]"

    _markup_toolbar_frame = "Viewport//Frame/**/_markup_toolbar_frame"
    _navigation_bar_frame = "Viewport//Frame/**/_navigation_bar_frame"
    _markup_element_toolbar_frame = "Viewport//Frame/**/_markup_element_toolbar_frame"
    _all_markup_thumbnails = "Viewport//Frame/**/OuterVStack/ZStack[*]"

    # Edit markup locators
    _edit_line_style = _edit_toolbar_widget + "/**/elementbar_btn_stroke___size__"

    @property
    def markups_count(self):
        markups = self.omni_driver.find_elements(self.all_markups_list)
        return len(markups)

    def add_markup(self):
        """Adds markup and validate if appears in markup manager"""
        markup_btn = self.omni_driver.find_element(self._add_markup_btn, refresh=True)
        markup_btn.click()
        self.omni_driver.wait(1)

    def _check_ui_after_markup_is_added(self):
        assert (
            self.markups_window in self.omni_driver.get_windows()["visible_windows"]
        ), "Markups Window is not visible after markup creation"
        try:
            elem: OmniElement = self.omni_driver.find_element(
                self._primary_toolbar_widget, True
            )
            assert (
                not elem.is_visible()
            ), "The primary markup widget should disappear a after new markup is added."
        except ElementNotFound:
            pass
        try:
            elem: OmniElement = self.omni_driver.find_element(
                self._secondary_toolbar_widget, True
            )
            assert (
                not elem.is_visible()
            ), "The secondary markup widget should disappear a after new markup is added."
        except ElementNotFound:
            pass
        try:
            elem: OmniElement = self.omni_driver.find_element(
                self._add_markup_btn_navbar, True
            )
            assert (
                elem.is_visible()
            ), "The navbar should appear after new markup is added."
        except:
            assert False, "The navbar should appear after new markup is added."

    def initialize_markup(self):
        """Clears previous markup settings"""

        self.find_and_click(self._add_markup_btn)
        for type in MarkupType:
            self.wait.element_to_be_located(
                self.omni_driver,
                self._markup_enable_btn.replace("__type__", type.value),
            )
            self.find_and_click(
                self._markup_enable_btn.replace("__type__", type.value),
                refresh=True,
                bring_to_front=False,
            )
            self._select_size(type, MarkupsSize.SMALL)
            if type == MarkupType.ARROW:
                self._select_arrow_type(MarkupsArrow.START)
            elif type == MarkupType.SHAPES:
                self._select_shape_type(MarkupsShape.RECTANGLE)

        self.find_and_click(self._markup_cancel_btn, bring_to_front=False)

    def cancel_markup(self):
        """Cancels markup creation"""
        self.find_and_click(self._markup_cancel_btn)

    def shapes_markup(self):
        """Selects shapes markup option"""
        self.find_and_click(self._markup_shapes_btn)

    def apply_markup(self):
        """Selects apply markup option"""
        self.find_and_click(self.markup_apply_btn, refresh=True, bring_to_front=False)
        self.omni_driver.wait(2)
        self._check_ui_after_markup_is_added()

    def draw_markup_shape_box(self, x: float, y: float, scale: float):
        """Draws a markup shape box

        Args:
            x (float): Start X of the box
            y (float): Start Y of the box
            scale (float): Scale of box to draw
        """
        self.omni_driver.drag_from_and_drop_to(
            x - scale, y - scale, x + scale, y + scale
        )

    def delete_markup(self, markup_num: int):
        self.find_and_scroll_element_into_view(
            self._specific_markup.replace("__markup__", str(markup_num - 1)),
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        delete_btn = self.omni_driver.find_element(
            self.delete_markup_btn.replace("__markup__", str(markup_num - 1)),
            refresh=True,
        )
        center = delete_btn.get_widget_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        delete_btn.click()

    def verify_markup_added(self, prev_count: int):
        markups_after = self.omni_driver.find_elements(self.all_markups_list)
        assert len(markups_after) == prev_count + 1, "New markup was not created."

    def verify_markup_deleted(self, prev_count: int):
        markups_after = self.omni_driver.find_elements(self.all_markups_list)
        assert len(markups_after) == prev_count - 1, "markup was not deleted."

    def get_markup_count(self):
        markups = self.omni_driver.find_elements(self.all_markups_list)
        return len(markups)

    def rename_markup(self, markup_num: int, new_name: str):
        self.find_and_scroll_element_into_view(
            self._specific_markup.replace("__markup__", str(markup_num - 1)),
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        waypt = self.omni_driver.find_element(
            self._markup_collapse_bar.replace("__markup__", str(markup_num - 1)),
            refresh=True,
        )
        self.omni_driver.wait(2)
        waypt.right_click()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option(self._rename_markup_contenxt_menu)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(new_name)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_key_combo_press(KeyboardConstants.enter)
        self.omni_driver.wait(2)

    def verify_markup_with_name_exists(self, markup_name: str):
        self.omni_driver.wait(1)
        all_markups = self.omni_driver.find_elements(self._markup_label)
        for markup in all_markups:
            if markup.get_text() == markup_name:
                break
        else:
            assert False, f"No markup exists with name {markup_name}"

    def check_markup_ui(self):
        """Checks if all markup buttons are visible in UI"""
        try:
            self.omni_driver.find_element(self._markup_comment_btn)
            self.omni_driver.find_element(self._markup_draw_btn)
            self.omni_driver.find_element(self._markup_arrow_btn)
            self.omni_driver.find_element(self._markup_line_btn)
            self.omni_driver.find_element(self._markup_shapes_btn)
            self.omni_driver.find_element(self.markup_apply_btn)
            self.omni_driver.find_element(self._markup_cancel_btn)
        except Exception as e:
            self.log.error(e, exc_info=True)

    def assert_markup_exists(self, markup_name: str):
        """Asserts if a particular Markup exists

        Args:
            markup_name (str): Name of Markup
        """
        index = -1
        markups = self.omni_driver.find_elements(self.all_markups_list)
        for i, markup in enumerate(markups):
            try:
                markup.find_element(f"**/Label[0].text=='{markup_name}'", refresh=True)
                index = i
                break
            except ElementNotFound:
                pass
        assert index != -1, f"Markup with name {markup_name} does not exist"

    def _select_size(self, type: MarkupType, size: MarkupsSize):
        """Selects size of a markup

        Args:
            type (MarkupType): Type of Markup
            size (MarkupsSize): Size of Markup
        """
        self.omni_driver.wait(1)
        if type == MarkupType.COMMENT:
            self.omni_driver.find_element(
                self._markup_comment_text_text_size_btn.replace("__size__", size.value),
                True,
            ).click()
        else:
            self.omni_driver.find_element(
                self._markup_size.replace("__size__", size.value).replace(
                    "__type__", type.value
                ),
                True,
            ).click(False)

    def _click_and_enable_markup(self, type: MarkupType):
        """Clicks on respective markup and enables it

        Args:
            type (MarkupType): Type of Markup to enable
        """
        self.omni_driver.wait(1)
        markup_btn = self.omni_driver.find_element(
            self._markup_enable_btn.replace("__type__", type.value), refresh=True
        )
        if not markup_btn.tool_button_is_checked():
            markup_btn.click(False)

    def add_comment(self, size: MarkupsSize, text: str, x: float, y: float):
        """Adds comment markup

        Args:
            size (MarkupsSize): Size of Markup
            text (str): text to enter inside Comment
            x (float): x coordinate of markup
            y (float): y coordinate of markup
        """
        self._click_and_enable_markup(MarkupType.COMMENT)
        self._select_size(MarkupType.COMMENT, size)
        self.omni_driver.wait(2)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.wait(1)
        self.omni_driver.click_at(x, y)
        self.omni_driver.wait(3)
        self.omni_driver.emulate_char_press(text)

    def assert_markup_element_nos(self, expected_no: int):
        """Asserts the number of markups inside visible

        Args:
            expected_no (int): expected number of markups inside viewport

        Returns:
            _type_: _description_
        """
        try:
            markups = self.omni_driver.find_elements(self._markup_elements)
        except ElementNotFound:
            markups = []
        assert (
            len(markups) == expected_no
        ), f"Expected number of elements:{expected_no} do not match original:{len(markups)}"
        self.log.info(f"Number of markup elements - {len(markups)}")
        return len(markups)

    def add_draw(self, size: MarkupsSize, scale: int, x: float, y: float):
        """Adds Draw markup

        Args:
            size (MarkupsSize): size of markup
            scale (int): length of draw markup
            x (float): x coordinate of markup
            y (float): y coordinate of markup
        """
        self._click_and_enable_markup(MarkupType.DRAW)
        self._select_size(MarkupType.DRAW, size)
        self.omni_driver.wait(1)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.drag_from_and_drop_to(x, y, x + scale, y + scale)

    def add_line(self, size: MarkupsSize, scale: int, x: float, y: float):
        """Adds Line markup

        Args:
            size (MarkupsSize): size of markup
            scale (int): length of line markup
            x (float): x coordinate of markup
            y (float): y coordinate of markup
        """
        self._click_and_enable_markup(MarkupType.LINE)
        self._select_size(MarkupType.LINE, size)
        self.omni_driver.wait(1)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.drag_from_and_drop_to(x, y, x + scale, y + scale)

    def _select_shape_type(self, shape_type: MarkupsShape):
        """Selects shape for Shape markup

        Args:
            shape_type (MarkupsShape): shape type of Shape Markup
        """
        self.omni_driver.wait(1)
        self.find_and_click(
            self._markups_shape_type_btn.replace("__markup_shape__", shape_type.value),
            bring_to_front=False,
        )

    def add_shapes(
        self,
        shape_type: MarkupsShape,
        size: MarkupsSize,
        scale: int,
        x: float,
        y: float,
    ):
        """Adds Shape Markup

        Args:
            shape_type (MarkupsShape): Type of Shape in Shape Markup
            size (MarkupsSize): _description_
            scale (int): _description_
            x (float): _description_
            y (float): _description_
        """
        self._click_and_enable_markup(MarkupType.SHAPES)
        self._select_shape_type(shape_type)
        self._select_size(MarkupType.SHAPES, size)
        self.omni_driver.wait(1)
        self.omni_driver.emulate_mouse_move(x + scale, y + scale)
        self.omni_driver.drag_from_and_drop_to(x, y, x + scale, y + scale)

    def _select_arrow_type(self, arrow_type: MarkupsArrow):
        """Selects arrow markup

        Args:
            arrow_type (MarkupsArrow): Type of arrow
        """
        self.omni_driver.wait(3)
        self.find_and_click(
            self._markup_arrow_type.replace("__arrow_type__", arrow_type.value), True
        )

    def add_arrow(
        self,
        arrow_type: MarkupsArrow,
        size: MarkupsSize,
        scale: int,
        x: float,
        y: float,
    ):
        """Adds Arrow Markup

        Args:
            arrow_type (MarkupsArrow): Type of Arrow
            size (MarkupsSize): Size of Markup
            scale (int): Length of Arrow markup
            x (float): x coordinate of markup
            y (float): y coordinate of markup
        """
        self._click_and_enable_markup(MarkupType.ARROW)
        self._select_arrow_type(arrow_type)
        self._select_size(MarkupType.ARROW, size)
        self.omni_driver.wait(1)
        self.omni_driver.emulate_mouse_move(x, y)
        self.omni_driver.drag_from_and_drop_to(x, y, x + scale, y + scale)

    def open_previous_markup(self):
        """Navigate to Previous Markup"""
        self.find_and_click(self._markup_previous_button, refresh=True)
        self.omni_driver.wait(1)

    def play_markups(self):
        """Play Markup Playlist"""
        self.find_and_click(self._markup_play_button, refresh=True)
        self.omni_driver.wait(1)

    def pause_markups(self):
        """Pause Markup Playlist"""
        self.find_and_click(self._markup_pause_button, refresh=True)
        self.omni_driver.wait(1)

    def open_next_markup(self):
        """Navigate to Next Markup"""
        self.find_and_click(self._markup_next_button, refresh=True)
        self.omni_driver.wait(1)

    def go_to_markup(self, name: str):
        """Clicks on specific markup from the list

        Args:
        name(str): Markup name
        """
        _, index = self.get_child_element(
            self.all_markups_list, f"**/Label[0].text == '{name}'"
        )
        thumbnail = self.omni_driver.find_element(
            self._markup_thumbnail.format(index), True
        )
        thumbnail.click()
        self.omni_driver.wait(1)

    def unlock_markup(self, name: str):
        """Unlocks specific markup from the list

        Args:
        name(str): Markup name
        """
        self.go_to_markup(name)
        self.find_and_click(self._markup_unlock_btn)
        self.omni_driver.wait(1)

    def exit_markup(self):
        """Clicks on Exit markup button"""
        self.find_and_click(self._markup_exit_btn)
        self.omni_driver.wait(1)

    def toggle_markup_manager(self, enable=True):
        """Toggles markup Mode

        Args:
        enable(bool): Bool value to enable markup Mode"""
        element = self.omni_driver.find_element(self._add_markup_btn_navbar, True)
        current_state = (
            self.markups_window in self.omni_driver.get_windows()["visible_windows"]
        )
        self.screenshot("previous_markup_manager_state")
        self.log.info("markup manager_state is enabled: %s", current_state)
        if (enable and not current_state) or (not enable and current_state):
            self.log.info("Switching markup manager_state")
            element.click()
        self.screenshot("current_markup_manager_state")
        assert enable == (
            self.markups_window in self.omni_driver.get_windows()["visible_windows"]
        ), "Failed to toggle markup bar"

    def is_markup_manager_visible(self) -> bool:
        """Gets the visibility of the markup manager window
        Retuns:
            bool
        """
        return self.markups_window in self.omni_driver.get_windows()["visible_windows"]

    def get_primary_toolbar_position(self):
        """Gets the position info of Primary markup toolbar
        Retuns:
            dict
        """
        elm: OmniElement = self.omni_driver.find_element(
            self._primary_toolbar_widget, True
        )
        return elm.get_size_and_position("all")

    def get_secondary_toolbar_position(self):
        """Gets the position info of Secondary markup toolbar
        Retuns:
            dict
        """
        elm: OmniElement = self.omni_driver.find_element(
            self._secondary_toolbar_widget, True
        )
        return elm.get_size_and_position("all")

    def open_markup_creator(self):
        """Opens the markup creator by clicking on Add Markup button"""
        btn = self.omni_driver.find_element(self._add_markup_btn, refresh=True)
        btn.click()

    def enable_export_markup(self):
        """Enabled Export Markup Window"""
        self.find_and_click(self._export_markup)

    def add_markup_note(self, markup_name: str, note: str, markup_no: int):
        """Adds note to markup

        Args:
            markup_name (str): Name of markup to which note needs to be added
            note (str): The text in the note
            markup_no (int): The number at which the markup occurs in markup manager
        """
        self.find_and_click(self._markup_name.replace("__name__", markup_name))
        note_field = self.omni_driver.find_elements(self._markup_note)[markup_no]
        note_field.send_keys(note)
        self.screenshot(f"added note for {markup_name}")
        self.find_and_click(
            self._markup_name.replace("__name__", markup_name), refresh=True
        )

    def close_markup(self):
        """Close markup through cross button"""
        assert self.find_and_click(
            self._close_markup_btn
        ), "Unable to locate close button"

    def markup_manager_current_state(self):
        """Verifies Markup button and markup dashboard visibility"""

        element = self.omni_driver.find_element(self._add_markup_btn_navbar, True)
        current_state = element.tool_button_is_checked()
        return current_state

    def click_comment_input_box_scroll_bar(self):
        """Click at the scroll bar of comment markup input box"""
        markup_comment_text_input_box = self.omni_driver.find_element(
            self._markup_comment_text_input_box
        )
        widget_center = markup_comment_text_input_box.get_widget_center()
        widget_x = widget_center[0]
        widget_y = widget_center[1]
        self.omni_driver.click_at(x=widget_x + 80, y=widget_y)
        return widget_x, widget_y

    def edit_markup_size(self, size: MarkupsSize):
        """Selects size of a markup

        Args:
            type (MarkupType): Type of Markup
            size (MarkupsSize): Size of Markup
        """
        self.omni_driver.find_element(
            self._edit_line_style.replace("__size__", size.value), True
        ).click(False)
        self.screenshot(f"edited_markup_size_{size.value}")
