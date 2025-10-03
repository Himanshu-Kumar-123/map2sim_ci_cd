# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Live Session class
   This module contains the base methods for Live Session window
"""
import re


from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.driver.waits import Wait


class BaseLiveSessionModel(BaseModel):
    """Base model class for Live Session window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Common locators
    _live_status = "Content//Frame/**/Label[*].text=='.live'"
    _join_session_radio_btn = (
        "Live Session//Frame/**/RadioButton[*].name=='join_session_radio_button'"
    )
    _create_session_radio_btn = (
        "Live Session//Frame/**/RadioButton[*].name=='create_session_radio_button'"
    )
    _sessions_combobox = "Live Session//Frame/**/ComboBox[*]"
    _join_btn = "Live Session//Frame/**/Button[*].text=='JOIN'"
    _session_name_stringfield = (
        "Live Session//Frame/**/StringField[*].name=='new_session_name_field'"
    )
    create_btn = "Live Session//Frame/**/Button[*].text=='CREATE'"
    _live_session_window = "Live Session"
    _session_exists_error = "Live Session//Frame/**/Label[0].text=='Failed to create session, please check console for more details.'"
    join_session_unsaved_btn = "Join Session//Frame/VStack[0]/HStack[1]/Button[0]"
    leave_session_button = "Leave Session//Frame/**/Button[*].text=='LEAVE'"
    _cancelleave_session_button = "Leave Session//Frame/**/Button[1]"
    _link_paste_btn = "JOIN LIVE SESSION WITH LINK//Frame/**/ToolButton[0]"
    _join_through_link_btn = (
        "JOIN LIVE SESSION WITH LINK//Frame/VStack[0]/HStack[1]/Button[0]"
    )
    _join_session_with_link = "JOIN LIVE SESSION WITH LINK//Frame/VStack[0]"
    _share_link_combobox = "SHARE LIVE SESSION LINK//Frame/**/ComboBox[0]"
    _copy_link_button = "SHARE LIVE SESSION LINK//Frame/**/InvisibleButton[0]"

    _leave_session_window = "Leave Session"

    def create_live_session(
        self,
        session_name="demo",
        assert_live: bool = False,
        assert_presenter=False,
    ):
        """Creates a new live session

        Args:
            session_name (str, optional): Session name. Defaults to "demo".
        """

        self._enter_live_session_name_to_create(session_name)
        self.find_and_click(self.create_btn)

        if assert_presenter:
            message = self.get_notification_text()
            if message:
                assert message == "You are now the timeline presenter.", (
                    "Notification message do not match, Expected: You are now the timeline presenter., Actual:"
                    f" {message}"
                )
        try:
            self.wait.element_to_be_located(
                self.omni_driver, self._session_exists_error
            )
            self.log.error("Session exists error appeared which is unexpected.")
            raise RuntimeError("Session exists")
        except ElementNotFound:
            self.log.info("Session exists error did not appear.")
        self.log.info("Successfully joined Live Session by creating a new one.")
        self._join_with_unsaved_changed()

        if assert_live:
            self.wait.element_to_be_located(self.omni_driver, self._live_status)

    def join_live_session(self, session_name="demo", x_offset=35):
        """Joins an existing live session

        Args:
            session_name (str, optional): Name of session. Defaults to "demo".
        """
        self._click_on_live_session_dropdown(x_offset)
        self.omni_driver.select_context_menu_option("Join Session")
        join_radiobtn = self.omni_driver.find_element(self._join_session_radio_btn)
        if not join_radiobtn.is_checked():
            join_radiobtn.click()
        self.omni_driver.wait(2)
        self.select_item_by_name_from_combo_box(
            self._sessions_combobox, name=session_name
        )
        self.omni_driver.wait(2)
        self.find_and_click(self._join_btn)
        self._join_with_unsaved_changed()

    def start_live_session(self, session_name="demo"):
        """Joins session if existing otherwise create a new session and then start live edit

        Args:
            session_name (str, optional): Name of session. Defaults to "demo".
        """
        try:
            self.join_live_session(session_name=session_name)
        except Exception:
            self.omni_driver.close_window("Live Session")
            self.create_live_session(session_name=session_name, assert_live=False)

    def _join_with_unsaved_changed(self):
        try:
            join_unsaved_btn = self.omni_driver.find_element(
                self.join_session_unsaved_btn
            )
            join_unsaved_btn.click()
            self.log.info("Join with unsaved changes window visible and handled.")
        except ElementNotFound:
            self.log.info("Join with unsaved changes window not visible.")

    def open_timeline_window(self):
        """Opens timeline window in lIve session"""
        self._click_on_live_session_dropdown()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Open Timeline Window")
        self.log.info("Clicked on TimeLine Window option")

    def request_for_presenter(self):
        """Request for Timeline Presenter"""
        self._click_on_live_session_dropdown()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Request Timeline Ownership")
        self.log.info("Clicked on TimeLine Window option")

    def revoke_presenter_req(self):
        """Request for Timeline Presenter"""
        self._click_on_live_session_dropdown()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option(
            "Withdraw Timeline Ownership Request"
        )
        self.log.info("Clicked on TimeLine Window option")

    def leave_session(self):
        """Leaves live session"""

        self._click_on_live_session_dropdown_with_users()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Leave Session")
        self.omni_driver.wait(1)

        try:
            leave_session_widget = Wait(timeout=5).element_to_be_located(
                self.omni_driver, self.leave_session_button
            )
            leave_session_widget.click()
            self.log.warning("Confirm leave session modal present")

        except ElementNotFound:
            self.log.warning("Confirm leave session modal not present")

    def join_live_session_with_link(self, x_offset=35):
        """Joins an existing live session with live session link"""

        self._click_on_live_session_dropdown(x_offset)
        self.omni_driver.select_context_menu_option("Join With Session Link")
        self.omni_driver.wait(2)
        assert self.find_and_click(self._link_paste_btn), "Paste button is not present"
        self.omni_driver.wait(2)
        assert self.find_and_click(
            self._join_through_link_btn
        ), "Failed to join through link"
        self._join_with_unsaved_changed()

    def copy_session_link(self, session_name="demo"):
        self.log.info("Inside new ")
        self._click_on_live_session_dropdown_with_users()
        self.omni_driver.select_context_menu_option("Share Session Link")
        self.select_item_by_name_from_combo_box(
            self._share_link_combobox, name=session_name
        )
        self.omni_driver.wait(2)
        assert self.find_and_click(self._copy_link_button), "Copy Link Failure"

    def _enter_live_session_name_to_create(
        self,
        session_name: str = "Perf_Session",
    ):
        """This method clicks on the Live widget, waits for Live Session window to open and types the name of live session.

        Args:
            session_name (str): name of session to be created
        """
        self._click_on_live_session_btn()
        assert (
            self._live_session_window
            in self.omni_driver.get_windows()["visible_windows"]
        ), "Failed to open 'Live Session' window"
        create_session_radiobtn = self.omni_driver.find_element(
            self._create_session_radio_btn
        )
        if not create_session_radiobtn.is_checked():
            create_session_radiobtn.click()
        text_field = self.omni_driver.find_element(self._session_name_stringfield, True)
        self.clear_textbox(text_field)
        self.omni_driver.emulate_char_press(session_name)

    def perf_leave_live_session(
        self,
        assert_leave_session: bool = True,
    ):
        """This method clicks on the Live widget and waits for Leave Session window to appear"""
        self._click_on_live_session_dropdown_with_users()
        self.omni_driver.wait(2)
        self.omni_driver.select_context_menu_option("Leave Session")

        if assert_leave_session:
            self.wait.element_to_be_located(
                self.omni_driver, self._leave_session_window
            )

    def _click_on_live_session_btn(self):
        """This method clicks on the Live Button on top right."""

        center = self.omni_driver.get_live_menu_center()
        self.omni_driver.emulate_mouse_move(center[0], center[1])
        self.omni_driver.wait(1)
        self.omni_driver.click_at(center[0], center[1])

    def _click_on_live_session_dropdown(self, x_offset=35):
        """This method clicks on the Dropdown on the right of Live Button."""
        center = self.omni_driver.get_live_menu_center()
        self.omni_driver.emulate_mouse_move(center[0] + x_offset, center[1])
        self.omni_driver.wait(1)
        self.omni_driver.click_at(center[0] + x_offset, center[1])

    def _click_on_live_session_dropdown_with_users(self):
        """This method clicks on the Dropdown on the right of Live Button. This is a special case for session with multiple participants.
        Here we calculate the app width and them take -x_offset from it for ease of calculation.
        """
        x_offset = 10
        center = self.omni_driver.get_live_menu_center()
        app_dim = self.omni_driver.get_app_window_dimension()
        self.omni_driver.click_at(app_dim["app_width"] - x_offset, center[1])
