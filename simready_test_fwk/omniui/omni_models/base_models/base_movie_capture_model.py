# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Movie Capture Model class
   This module contains the base methods for Movie Capture modal
"""
import os
import time
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import (
    ElementNotInteractable,
    ElementNotFound,
)
from omni_remote_ui_automator.common.constants import KeyboardConstants


class BaseMovieCaptureModel(BaseModel):
    """Base model class for Movie Capture window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for movie capture window
    _end_frames_drag = (
        "Movie"
        " Capture//Frame/ScrollingFrame[*]/VStack[0]/CollapsableFrame[0]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/VStack[1]/VStack[0]/HStack[1]/HStack[2]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/IntDrag[0]"
    )
    _resolution_width_drag = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/VStack[2]/HStack[1]/HStack[1]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/IntDrag[0]"
    )
    _resolution_height_drag = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[0]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/VStack[2]/HStack[1]/HStack[1]/VStack[1]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/IntDrag[0]"
    )
    _samples_per_pixel_per_subframe = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/VStack[0]/VStack[1]/HStack[1]/VStack[0]/HStack[0]/ZStack[0]/HStack[0]/VStack[0]/IntDrag[0]"
    )
    _capture_sequence_button = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/HStack[0]/VStack[0]/HStack[3]/Stack[0]/HStack[0]/Button[0]"
    )
    _file_name_txtbox = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/HStack[0]/VStack[0]/HStack[1]/HStack[1]/StringField[0]"
    )
    _file_type_combobox = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/HStack[0]/VStack[0]/HStack[1]/HStack[1]/ComboBox[1]"
    )
    _file_path_txtbox = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/HStack[0]/VStack[0]/HStack[0]/VStack[0]/StringField[0]"
    )

    _render_preset_combobox = (
        "Movie"
        " Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[1]/Frame[*]/ZStack[0]/VStack[0]/Frame[*]/VStack[0]/VStack[0]/HStack[0]/ComboBox[0]"
    )
    _capture_window = "Capture Progress//Frame/VStack[0]"
    _frame_rate = "Movie Capture//Frame/**/cap_setting_id_combo_fps"
    _camera = "Movie Capture//Frame/**/cap_setting_id_combo_camera_type"
    _ratio = "Movie Capture//Frame/**/cap_setting_id_combo_res_ratio"
    width = "Movie Capture//Frame/**/cap_setting_id_drag_res_width_input"
    height = "Movie Capture//Frame/**/cap_setting_id_drag_res_height_input"
    _capture_every_nth_frame_checkbox = (
        "Movie Capture//Frame/**/cap_setting_id_check_nth_frame"
    )
    _capture_every_nth_frame_input = (
        "Movie Capture//Frame/**/cap_setting_id_drag_nth_frame_input"
    )
    _scale_latency_input = (
        "Movie Capture//Frame/**/render_setting_id_drag_settle_latency_input"
    )
    _output_frame = (
        "Movie Capture//Frame/ScrollingFrame[0]/VStack[0]/CollapsableFrame[3]"
    )
    _submit_to_queue = (
        "Movie Capture//Frame/**/output_setting_id_button_submit_to_queue"
    )
    _queue_settings_collapse = (
        "Movie Capture//Frame/**/CollapsableFrame[*].title=='Queue settings'"
    )
    _queue_instance = "Movie Capture//Frame/**/farm_setting_id_stringfield_farm"
    _task_comment = "Movie Capture//Frame/**/farm_setting_id_stringfield_task_comment"
    _job_type = "Movie Capture//Frame/**/farm_setting_id_stringfield_task_type"

    def navigate_to_movie_capture(self):
        """Navigates to movie capture window"""
        self.omni_driver.select_menu_option("Window/Rendering/Movie Capture")
        self.log.info("Navigated to Movie Capture Window")

    def set_end_frames(self, end_frames: int):
        """Enters the number of frames to capture

        Args:
            end_frames (int): Number of last frame to capture
        """
        end_drag = self.omni_driver.find_element(self._end_frames_drag)
        end_drag.send_keys(end_frames)

    def _set_resolution_width(self, width: int):
        """Enters the resolution width

        Args:
            width (int): Width to be set for resolution
        """
        width_drag = self.omni_driver.find_element(self._resolution_width_drag)
        width_drag.send_keys(width)

    def _set_resolution_height(self, height: int):
        """Enters the resolution height

        Args:
            height (int): height to be set for resolution
        """
        height_drag = self.omni_driver.find_element(self._resolution_height_drag)
        height_drag.send_keys(height)

    def set_resolution(self, width: int, height: int):
        """Sets the resolution width and height

        Args:
            width (int): Width to be set for resolution
            height (int): height to be set for resolution
        """
        self._set_resolution_width(width)
        self._set_resolution_height(height)

    def set_samples_per_pixel(self, count: int):
        """Enters the samples to be taken per pixel

        Args:
            count (int): Samples count
        """
        samples_drag = self.omni_driver.find_element(
            self._samples_per_pixel_per_subframe
        )
        samples_drag.send_keys(count)

    def set_output_path(self, path: str):
        """Sets the output path for capture

        Args:
            path (str): File path
        """
        path_widget = self.find_and_scroll_element_into_view(
            self._file_path_txtbox, ScrollAxis.Y, ScrollAmount.CENTER
        )
        path_widget.send_keys(path)

    def set_output_name(self, name: str):
        """Sets the output name for capture

        Args:
            name (str): File name
        """
        name_widget = self.omni_driver.find_element(self._file_name_txtbox)
        name_widget.send_keys(name)

    def set_output_format(self, format: str):
        """Sets the output format for capture

        Args:
            format (str): File format
        """
        self.select_item_by_index_from_combo_box(self._file_type_combobox, format)

    def click_capture_sequence(self):
        """Clicks on capture sequence to start capturing"""
        self.find_and_click(self._capture_sequence_button)

    def wait_for_capture_completion(
        self, mins: float, frames: int, test_name: str, format: str = "png"
    ):
        """Waits of rcapture to complete

        Args:
            mins (float): Max Minutes to wait
            frames (int): Frames to be captured
            test_name (str): Test method name
            format (str, optional): Format of the output file . Defaults to "png".
        """
        self.wait.element_to_be_located(self.omni_driver, self._capture_window)
        dir = os.path.join(self.ss_dir, test_name + "_frames")
        assert os.path.exists(dir), f"Capture folder was not created at path {dir}"
        start = time.time()
        end = start + (mins * 60)
        while time.time() < end:
            files = len(os.listdir(dir))
            if files == frames + 1:
                self.log.info(f"{frames+1} frames captured in png.")
                break
            else:
                self.log.info(
                    f"Captured frames {files}, Expected frames {frames+1}, Waiting for capture to finish"
                )
                time.sleep(10)
        else:
            assert False, f"Movie capture did not finish in {mins} minutes."

        if format == "mp4":
            assert os.path.isfile(
                os.path.join(self.ss_dir, test_name) + ".mp4"
            ), "MP4 file was not created."

    def select_render_preset(self, preset: str):
        """Selects the render preset for capture

        Args:
            preset (str): Render engine to be used as preset
        """

        self.select_item_by_index_from_combo_box(self._render_preset_combobox, preset)

    def select_frame_rate(self, index: int = None, name: str = None):
        """Selects the appropriate framerate from combobox as per the index provided

        Args:
            index (int): name of option
            name (str, optional): name of option. Defaults to None.
        """
        frame_rate = self.omni_driver.find_element(self._frame_rate)
        frame_rate.select_item_from_combo_box(name=name, index=index, stack_combo=False)

    @property
    def get_selected_frame_rate(self):
        """Returns the selected framerate from combobox

        Returns:
            str: selected framerate
        """
        frame_rate = self.omni_driver.find_element(self._frame_rate)
        return frame_rate.get_combobox_info()["current_value"]

    @property
    def get_frame_rate_options(self):
        """Returns all framerate options from combobox

        Returns:
            list: list of all framerate options
        """
        frame_rate = self.omni_driver.find_element(self._frame_rate)
        return frame_rate.get_combobox_info()["all_options"]

    def select_camera(self, index: int = None, name: str = None):
        """Selects the appropriate camera from combobox as per the index provided

        Args:
            index (int): index of option
            name (str, optional): name of option. Defaults to None.
        """
        camera = self.omni_driver.find_element(self._camera)
        camera.select_item_from_combo_box(name=name, index=index, stack_combo=False)

    @property
    def get_selected_camera(self):
        """Returns the selected camera from combobox

        Returns:
            str: selected camera
        """
        camera = self.omni_driver.find_element(self._camera)
        return camera.get_combobox_info()["current_value"]

    @property
    def get_camera_options(self):
        """Returns all camera options from combobox

        Returns:
            list: list of all camera options
        """
        camera = self.omni_driver.find_element(self._camera)
        return camera.get_combobox_info()["all_options"]

    def select_ratio(self, index: int = None, name: str = None):
        """Selects the appropriate ratio from combobox as per the index provided

        Args:
            index (int): index of option
            name (str, optional): name of option. Defaults to None.
        """
        ratio = self.omni_driver.find_element(self._ratio)
        ratio.select_item_from_combo_box(name=name, index=index, stack_combo=False)

    @property
    def get_selected_ratio(self):
        """Returns the selected ratio from combobox

        Returns:
            str: selected ratio
        """
        ratio = self.omni_driver.find_element(self._ratio)
        return ratio.get_combobox_info()["current_value"]

    @property
    def get_ratio_options(self):
        """Returns all ratio options from combobox

        Returns:
            list: list of all ratio options
        """
        ratio = self.omni_driver.find_element(self._ratio)
        return ratio.get_combobox_info()["all_options"]

    @property
    def get_resolution_width_height(self):
        """Returns the resolution width and height

        Returns:
            tuple: resolution width and height
        """
        width = self.omni_driver.find_element(self.width).get_text()
        height = self.omni_driver.find_element(self.height).get_text()
        return width, height

    def set_resolution_width_height(self, width: int, height: int):
        """Sets the resolution width and height

        Args:
            width (int): Width to be set for resolution
            height (int): height to be set for resolution
        """

        self.omni_driver.find_element(self.width).send_keys(width)
        self.omni_driver.find_element(self.height).send_keys(height)


    def toggle_capture_every_nth_frame(self, checked: bool):
        """Toggles checkbox for field capture nth frame

        Args:
            checked (bool): bool value for field
        """
        checkbox = self.omni_driver.find_element(self._capture_every_nth_frame_checkbox)
        if checked:
            if not checkbox.is_checked():
                checkbox.click()
        else:
            if checkbox.is_checked():
                checkbox.click()

    def change_capture_nth_frame(self, frame_count: int):
        """changes value for field capture nth frame

        Args:
            frame_count (int): value for field capture nth frame
        """
        input = self.omni_driver.find_element(self._capture_every_nth_frame_input)
        input.send_keys(frame_count)

    def change_scale_latency(self, latency: int):
        """Changes scale latency

        Args:
            latency (int): value for scale latency
        """
        latency_input = self.omni_driver.find_element(self._scale_latency_input)
        latency_input.send_keys(latency)

    def submit_to_queue(self):
        """Submits task into queue"""
        self.find_and_click(self._output_frame)
        self.find_and_scroll_element_into_view(
            self._output_frame, ScrollAxis.Y, ScrollAmount.TOP
        )
        self.find_and_click(self._submit_to_queue)
        if (
            "Movie Capture - unsaved changes"
            in self.omni_driver.get_windows()["visible_windows"]
        ):
            self.omni_driver.emulate_key_press(button=KeyboardConstants.enter)
        if (
            "Movie Capture - confirm submission to Omniverse Queue"
            in self.omni_driver.get_windows()["visible_windows"]
        ):
            self.omni_driver.emulate_key_press(button=KeyboardConstants.enter)

    def open_queue_settings(self):
        """Opens Queue instance collapse bar and scrolls it into view"""
        queue_settings = self.omni_driver.find_element(self._queue_settings_collapse)
        if queue_settings.is_collapsed():
            queue_settings.click()
        self.find_and_scroll_element_into_view(
            self._queue_settings_collapse, ScrollAxis.Y, ScrollAmount.TOP
        )

    def set_queue_instance(self, value: str):
        """sets queue instance

        Args:
            value (str): value for queue instance
        """
        self.find_and_enter_text(self._queue_instance, value)

    def set_task_comment(self, comment: str):
        """sets comment for task

        Args:
            comment (str): comment for task
        """
        self.find_and_enter_text(self._task_comment, comment)

    def set_job_type(self, job_type: str):
        """Sets job type

        Args:
            job_type (str): job type
        """
        self.find_and_enter_text(self._job_type, job_type)
