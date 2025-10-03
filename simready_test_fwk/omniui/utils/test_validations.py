# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import os
import pandas as pd
from PyPDF2 import PdfReader
from typing import List
from omniui.framework_lib.softassert import SoftAssert
from omniui.omni_models.base_models.base_property_model import BasePropertyModel
from omniui.omni_models.base_models.base_viewport_model import BaseViewportModel
from omniui.omni_models.base_models.base_section_model import BaseSectionModel
from omniui.omni_models.base_models.base_array_tool_model import BaseArrayToolModel
from omniui.omni_models.base_models.base_stage_model import BaseStageModel
from omniui.utils.utility_functions import get_value_from_json


def validate_dock_status(stage, window_name, dock_status, dock_id, dock_order, assertion_var):
    """
    Validates the dock status for a window.
    Args:
        stage: self.stage
        window_name: Name of the window
        dock_status: Expected dock status of the window
        dock_id: Expected dock id of the window
        dock_order: Expected dock order of the window
        assertion_var: Soft assertion variable
    """

    after_dock = stage.get_dock_status(window_name=window_name)

    assertion_var.expect(
        after_dock["dock_status"] == dock_status,
        f"[{window_name}] Actual dock status:{after_dock['dock_status']} Expected dock status:{dock_status}",
    )
    assertion_var.expect(
        after_dock["dock_id"] == dock_id,
        f"[{window_name}] Actual dock id:{after_dock['dock_id']} Expected dock id:{dock_id}",
    )
    assertion_var.expect(
        after_dock["dock_order"] == dock_order,
        f"[{window_name}] Actual dock order:{after_dock['dock_order']} Expected dock order:{dock_order}",
    )


def verify_present_mode_options(viewport: BaseViewportModel):
    """Verifies all the present mode options visible on screen"""
    soft_assert = SoftAssert()
    options = viewport.nav_bar_options()
    exp_options = get_value_from_json("present_mode", "usdp_test_data.json")
    unexp_options = ["markup_btn", "waypoint_btn"]
    for _ in exp_options:
        soft_assert.expect(options[_].is_visible(), f"{_} is not visible")
    for _ in unexp_options:
        soft_assert.expect(options[_] is None, f"{_} is visible")

    soft_assert.assert_all()


def verify_comment_mode_options(viewport):
    """Verifies all the comment mode options visible on screen"""
    soft_assert = SoftAssert()
    options = viewport.nav_bar_options()
    exp_options = get_value_from_json("comment_mode", "usdp_test_data.json")
    for _ in exp_options:
        soft_assert.expect(options[_].is_visible(), f"{_} is not visible")

    soft_assert.assert_all()


def verify_approve_mode_options(viewport):
    """Verifies all the approve mode options visible on screen"""
    soft_assert = SoftAssert()
    options = viewport.nav_bar_options()
    exp_options = get_value_from_json("approve_mode", "usdp_test_data.json")
    for _ in exp_options:
        soft_assert.expect(options[_].is_visible(), f"{_} is not visible")

    soft_assert.assert_all()


def validate_lights_menu(viewport: BaseViewportModel, render_engine, omnidriver, log):
    """Validatesif every light in lighting menu works properly

    Args:
        viewport (omni model): self.viewport
        render_engine (RenderEngine): Name of renderer
        omnidriver (driver): self.omnidriver
        log: logger
    """
    viewport.select_rendering_engine(render_engine)
    for i in range(7):
        if i == 2:
            continue
        light_name = viewport.select_lights(i).split()[0].lower()
        current_light = omnidriver.get_lighting_mode().split()[0].lower()
        log.info(f"Current lighting mode is {current_light}")
        assert light_name == current_light, "Lights don't match"
        viewport.screenshot(f"{render_engine}_{current_light}")


def verify_nav_bar_tooltips(viewport: BaseViewportModel, tooltip_data: List[dict]):
    """Verify the tooltips for navbar tools"""
    soft_assert = SoftAssert()
    options = viewport.nav_bar_options()

    # Collect data into different lists
    tool_list = [x["name"] for x in tooltip_data]
    tool_texts = [x.get("text") for x in tooltip_data]
    tool_images = [x.get("images") for x in tooltip_data]

    for i, tool in enumerate(tool_list):
        coord = options[tool].get_widget_center()
        viewport.omni_driver.emulate_mouse_move(int(coord[0]), int(coord[1]))
        if viewport.is_nav_bar_tooltip_visible():
            # Verify tooltip text
            if tool_texts[i]:
                text = viewport.get_tooltip_text()
                soft_assert.expect(
                    text == tool_texts[i],
                    f"{tool} -> Text unequal: Expected: {tool_texts[i]}, Actual: {text}",
                )

            # Verify tooltip Image
            if tool_images[i]:
                image_elements = viewport.get_tooltip_images()
                urls = [os.path.split(ele.image_source())[-1] for ele in image_elements]
                soft_assert.expect(
                    urls == tool_images[i],
                    f"{tool} -> Image url are not equal, Expected: {tool_images[i]}, Actual: {urls}",
                )
        else:
            raise ValueError(f"{tool} -> tooltip is not visible")

    soft_assert.assert_all()


def validate_gpu_usage(viewport_vram_info: list, enabled_gpu: list, log, max_variation_percent: int = 2):
    """Validates GPU Usage with expected Usage

    Args:
        viewport_vram_info (list): viewport vram info
        enabled_gpu (list): GPUs that are enabled
        soft_assert (SoftAssert): Soft Assertion Object
        max_variation_percent (int, default: 2): Maximum variation in Percentage
    """
    soft_assert = SoftAssert()
    ref_gpu_utilization_percent = None
    ref_gpu_utilization_index = None
    for index, gpu_status in enumerate(enabled_gpu):
        gpu_percent_utilization = (viewport_vram_info[index]["usage"] / viewport_vram_info[index]["budget"]) * 100
        log.info(f"GPU {index} Utilization: {gpu_percent_utilization}")
        if not gpu_status:
            soft_assert.expect(gpu_percent_utilization <= 1, f"GPU {index} should not be utilized")
        if gpu_status:
            if ref_gpu_utilization_index is None:
                ref_gpu_utilization_percent = gpu_percent_utilization
                ref_gpu_utilization_index = index
            else:
                utilization_diff = abs(ref_gpu_utilization_percent - gpu_percent_utilization)
                log.info(f"GPU {index} Utilization Diff: {utilization_diff}")
                soft_assert.expect(
                    utilization_diff <= max_variation_percent,
                    f"GPU {index} shows {utilization_diff}% Utilzation more than GPU {ref_gpu_utilization_index}",
                )
    soft_assert.assert_all()


def validate_section_navigation(section: BaseSectionModel):
    """Validates if navigation buttons of section tool are working

    Args:
        section (BaseSectionModel): OmniModel
    """
    count = section.get_sections_count()
    section.select_section(0)
    assert section.get_current_section_index() == 0, "Section with index 0 did not get selected"
    i = 0
    while i < count - 1:
        section.next_section()
        i += 1
        assert section.get_current_section_index() == i, "Next section did not work"

    while i != 0:
        section.prev_section()
        i -= 1
        assert section.get_current_section_index() == i, "Previous section did not work"


def check_memory_leak(vram_list: List, threshold: int):
    """Checks viewport memory leak

    Args:
        vram_list (List): List containing vrams captured at different intervals
        threshold (int): Maximum allowed deviation of vram
    """
    for i in range(1, len(vram_list)):
        increase = vram_list[i] - vram_list[i - 1]
        if increase > threshold:
            return True  # VRAM increase exceeded the threshold

    return False


def validate_array_tool_copies(
    base_asset_path: str,
    count: int,
    array_tool: BaseArrayToolModel,
    stage: BaseStageModel,
    property: BasePropertyModel,
):
    """Validates if actual copies have been created by the Array Tool
    Args:
        base_asset_path (str): path of asset which was used for array tool
        count (int): expected count
        array_tool (BaseArrayToolModel): array tool model
        stage (BaseStageModel): stage model
        property (BasePropertyModel): property model
    """
    for num in range(1, count):
        asset_path = array_tool.numbered_asset_path(base_asset_path, num)
        stage.search_and_select_asset(asset_path)
        stage.omni_driver.wait(3)
        assert not property.reference_to_prim_path_exists(
            base_asset_path
        ), f"Asset {asset_path} is not a copy. It is an instance of {base_asset_path}"


def validate_array_tool_instances(
    base_asset_path: str,
    count: int,
    array_tool: BaseArrayToolModel,
    stage: BaseStageModel,
    property: BasePropertyModel,
):
    """Validates if actual copies have been created by the Array Tool
    Args:
        base_asset_path (str): path of asset which was used for array tool
        count (int): expected count
        array_tool (BaseArrayToolModel): array tool model
        stage (BaseStageModel): stage model
        property (BasePropertyModel): property model
    """
    for num in range(1, count):
        asset_path = array_tool.numbered_asset_path(base_asset_path, num)
        stage.search_and_select_asset(asset_path)
        stage.omni_driver.wait(3)
        assert property.reference_to_prim_path_exists(
            base_asset_path
        ), f"Asset {asset_path} is not an instance of {base_asset_path}"


def check_physics_applied(
    property_model: BasePropertyModel,
    create_object: str,
    expected_collosion_approximation: str,
    expected_physics_enabled: bool,
    assertion: SoftAssert,
):
    """Checks if physics is applied to the object

    Args:
        property_model (BasePropertyModel): OmniModel
        object (str): Object name
        expected_collosion_approximation (str): Expected collision approximation
        expected_physics_enabled (bool): Expected physics enabled
        assertion (SoftAssert): Soft Assertion Object
    """
    actual_physics_enabled = property_model.is_physics_collision_visible()
    assertion.expect(
        actual_physics_enabled is expected_physics_enabled,
        (
            f"Physics is unexpected for: {create_object}. Expected: {expected_physics_enabled}, Found:"
            f" {actual_physics_enabled}"
        ),
    )
    if actual_physics_enabled is True:
        assertion.expect(
            property_model.physics_collision_enabled() is True,
            f"Physics Collision is not enabled for: {create_object}",
        )
        actual_collosion_approximation = property_model.physics_collision_approximation()
        if expected_collosion_approximation is not None:
            assertion.expect(
                expected_collosion_approximation == actual_collosion_approximation,
                (
                    f"Collision Approximation is not same for: {create_object}. Expected:"
                    f" {expected_collosion_approximation}, Found: {actual_collosion_approximation}"
                ),
            )


def validate_phrases(df, log):
    phrases_to_check = [
        "Markup_00",
        "Markup_01",
        "markup comment 1",
        "markup comment 2",
        "This is note 1",
        "This is note 2",
    ]
    for phrase in phrases_to_check:
        if phrase in df:
            log.info(f"file contains '{phrase}'")
        else:
            assert False, f"{phrase} not present in file"
            log.info(f"file does not contain '{phrase}'")


def validate_csv(file_path, log):
    try:
        df = str(pd.read_csv(file_path))
        log.info(df)
        validate_phrases(df, log)
        log.info(f"CSV file {file_path} is valid.")
    except Exception as e:
        log.info(f"CSV file {file_path} is not valid: {str(e)}")


def validate_xlsx(file_path, log):
    try:
        df = str(pd.read_excel(file_path))
        # Add your validation logic for the XLSX file here
        # For example, check if certain sheets exist or meet specific criteria

        validate_phrases(df, log)
        log.info(f"XLSX file {file_path} is valid.")
    except Exception as e:
        log.info(f"XLSX file {file_path} is not valid: {str(e)}")


def validate_pdf(file_path, log):
    try:
        df = PdfReader(open(file_path, "rb"))
        # Add your validation logic for the PDF file here
        # For example, check the number of pages, text content, etc.
        text = ""
        for page_number in range(len(df.pages)):
            page = df.pages[page_number]
            page_text = page.extract_text()
            text += page_text
        validate_phrases(text, log)
        log.info(f"PDF file {file_path} is valid.")
    except Exception as e:
        log.info(f"PDF file {file_path} is not valid: {str(e)}")


def validate_markup_export(directory_path, log):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.lower().endswith(".csv"):
            validate_csv(file_path, log)
        elif filename.lower().endswith((".xlsx", ".xls")):
            validate_xlsx(file_path, log)
        elif filename.lower().endswith(".pdf"):
            validate_pdf(file_path, log)
        else:
            log.info(f"Ignoring file {file_path} as it is not a supported format.")
