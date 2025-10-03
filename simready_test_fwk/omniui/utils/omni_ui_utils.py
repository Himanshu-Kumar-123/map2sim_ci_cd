# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import logging
import requests
import time
from enum import Enum
from typing import Callable
from omni_remote_ui_automator.common.constants import KeyboardConstants
from omni_remote_ui_automator.common.enums import Mesh
from omni_remote_ui_automator.driver.omnidriver import OmniDriver
from omni_remote_ui_automator.utils import get_random_enum

from omniui.utils.omni_models import OmniModel
from omniui.utils.utility_functions import remote_server_port_and_url, get_window_model


def create_sublayer_and_add_prim(layer, viewport, property, stage, sublayer_path: str, sublayer_name: str):
    layer.navigate_to_window()
    viewport.screenshot("test_start")
    layer.create_sublayer(sublayer_name=sublayer_name, save_path=sublayer_path)
    fetched_sublayer_name = property.get_sublayer_name()
    assert sublayer_name == fetched_sublayer_name, "Sublayer names don't match"
    layer.make_sublayer_authorising(sublayer_name=sublayer_name)
    viewport.screenshot(f"created_{sublayer_name}_authorising")
    prim_1: Enum = get_random_enum(Mesh)
    viewport.create_prim(prim_1)
    stage.navigate_to_stage()
    stage.assert_item_exits(prim_1.value)
    viewport.screenshot(f"created_{prim_1.value}_in_{sublayer_name}")
    layer.navigate_to_window()
    layer.save_sublayer_changes(sublayer_name, Authoring=True)


def move_camera(app: str, tool_name: str, tool_fun: Callable, omni_driver: OmniDriver):
    """
    Move camera in all four directions

    Arguments:
    tool_name(str): name of tool to add in screenshot name
    tool_fun(function): function to enable and disable tool
    """
    log = logging.getLogger()
    viewport = get_window_model(omni_driver, OmniModel.viewport_model, app)

    tool_fun()
    window_data = omni_driver.get_window_dimensions("Viewport")
    x_pos, y_pos = window_data["position_x"], window_data["position_y"]
    width, height = window_data["width"], window_data["height"]

    def move(x, y):
        omni_driver.click_at_and_hold(width // 2, height // 2, hold_click=True)
        omni_driver.emulate_mouse_move(x, y)
        omni_driver.wait(1)
        omni_driver.click_at(x, y)
        omni_driver.wait(1)

    # Bottom Rotation
    log.info("Perform bottom rotation")
    move(width // 2 - 200, height - 200)
    viewport.screenshot(f"bottom_{tool_name}")

    # Right Rotation
    log.info("Perform right rotation")
    move(width // 2 - 200, height // 2 - 200)
    viewport.screenshot(f"right_{tool_name}")

    # Left Rotation
    move(x_pos + 100, height // 2 - 200)
    log.info("Perform left rotation")
    viewport.screenshot(f"left_{tool_name}")

    # Top Rotation
    move(width // 2 - 200, y_pos + 100)
    log.info("Perform top rotation")
    viewport.screenshot(f"top_{tool_name}")
    tool_fun(False)

    viewport.drag_viewport_element(x_pos, width - 100)
    omni_driver.emulate_key_press(KeyboardConstants.escape)
    viewport.screenshot(f"disable_{tool_name}")


def select_assert_rotate_reset(stage, property, viewport, ss_name: str, asset_path: str, rotate_values: list):
    """Selects asset from stage and rotates it from property window, takes screenshot and resets

    Args:
        stage (_type_): omni model for stage
        property (_type_): omni model for property
        viewport (_type_): omni model for viewport
        ss_name (str): name of screenshot after rotating
        asset_path (str): path of asset in stage
        rotate_values (list): list of rotate values for x, y and z
    """
    old_rotate_values = []
    stage.search_and_select_asset(asset_path)
    old_rotate_values = property.get_rotate_coordinates()
    property.transform_rotate(rotate_values)
    assert rotate_values == property.get_rotate_coordinates(), "Rotate coordinates not updated"
    viewport.viewport_screenshot(f"{ss_name}")
    property.transform_rotate(old_rotate_values)


def section_add_align_save(section, axis: str):
    """Creates section, aligns it to given axis and saves it

    Args:
        section (_type_): OmniModel
        axis (str): axis (X,Y,Z)
    """
    section.add_section()
    section.align_section_to(axis)
    section.save_section()


def wait_for_scene_load(baseurl, logger, timeout=240):
    """Waits for scene to completely load

    Args:
        omni_driver: omnidriver object
        logger: log object
        timeout: time for timeout
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            resp = requests.get(f"{baseurl}/perf", verify=False, timeout=3.05).json()
            if resp["scene_status"] == "loaded":
                logger.info("Scene is loaded.")
                return True
            elif resp["scene_status"] == "opening":
                logger.info("Scene is opening.")

        except Exception as e:
            logger.error(str(e))

    logger.error("Failed to load stage in given time")
    raise RuntimeError("Failed to load stage in given time")
