# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Examples Window class
   This module contains the base methods for Example window
"""
import time

from omni_remote_ui_automator.driver.exceptions import ElementNotFound


from ..base_models.base_model import BaseModel


class BaseExampleModel(BaseModel):
    """Base model class for example window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to example window
    _window_title = "Examples"
    _example_window = "Examples//Frame/VStack[0]"
    _rendering_submenu = "Examples//Frame/**/CategoryView[0]/**/Label[*].text=='RENDERING'"
    _example_scene = 'Examples//Frame/**/ThumbnailView[0]/**/Label[0].text=="example_name"'
    _all_examples = "Examples//Frame/**/ThumbnailView[0]/HStack[*]"
    _all_category_btn = "Examples//Frame/**/ScrollingFrame[0]/CategoryView[0]/HStack[1]/Label[0]"
    _search_example_scene = "Examples//Frame/**/HStack[0]/StringField[0]"
    _animation_submenu = "Examples//Frame/**/CategoryView[0]/**/Label[*].text=='ANIMATION'"
    # DeskFan example locator
    _reset_fan = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/FanStack/FanReset"

    # LightBulb Example locator
    _light_switch = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/LightStack/LightSwitch"
    _colour_switch = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/LightStack/ColorSwitch"

    # Clock example locator
    _start_clock = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/ClockStack/StartClock"
    _reset_clock = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/ClockStack/ResetClock"
    _reset_clock_speed = "Viewport//Frame/ZStack[0]/Frame[9]/OG_overlay/Placer[0]/ClockStack/ResetSpeed"

    
    def enable_example_window(self):
        "Enables example window"

        if "Examples" in self.omni_driver.get_windows()["visible_windows"]:
            return True

        else:
            self.omni_driver.select_menu_option(f"Window/Browsers/{self._window_title}")
            self.omni_driver.wait(2)
            assert (
                "Examples" in self.omni_driver.get_windows()["visible_windows"]
            ), f"Cannot find window for '{self._window_title}'."
            self.log.info("Navigated to Examples window successfully.")

    def navigate_to_example_window(self):
        """Navigate to examples window"""
        example_window = self.omni_driver.find_element(self._example_window)
        example_window.click()
        self.screenshot("navigated_to_example")

    def _select_rendering_submenu(self):
        """Select rendering submenu from examples window"""
        # rendering_submenu = self.omni_driver.find_element(self._rendering_submenu)
        rendering_submenu = self.wait.element_to_be_located(self.omni_driver, self._rendering_submenu)
        rendering_submenu.click()
        self.screenshot("navigated_to_rendering_menu")

    def _open_example(self, example_name):
        """Open a example scene and wait for specified time. Takes screenshot after scene load"""
        example_scene = self._example_scene.replace("example_name", example_name)
        example = self.wait.element_to_be_located(self.omni_driver, example_scene)
        example.double_click()
        self.omni_driver.wait(10)
        self.omni_driver.wait_for_stage_load(600)
        self.viewport_screenshot("opened_example_scene")

    
    def open_example_scene(self, example_name="Attic_NVIDIA"):
        """Method to open a scene from examples window

        Args:
            example_name (str, optional): Class object of Example_Scene. Defaults to "Attic_NVIDIA".
        """
        self.enable_example_window()
        self.navigate_to_example_window()
        self.omni_driver.wait(2)
        self._select_rendering_submenu()
        self.omni_driver.wait(2)
        self._open_example(example_name)

    def _select_all_category(self):
        """Select ALL submenu from examples window"""
        all_category_btn = self.omni_driver.find_element(self._all_category_btn)
        all_category_btn.double_click()
        self.screenshot("navigated_to_all_category")

    
    def open_example_scene_under_all(self, example_name: str):
        self.enable_example_window()
        self.navigate_to_example_window()
        self.omni_driver.wait(2)
        self._select_all_category()
        self.omni_driver.wait(2)
        search_example_scene = self.omni_driver.find_element(self._search_example_scene)
        search_example_scene.send_keys(example_name)
        self._open_example(example_name)

    def _select_animation_submenu(self):
        """Select rendering submenu from examples window"""
        animation_submenu = self.omni_driver.find_element(self._animation_submenu)
        animation_submenu.click()
        self.screenshot("navigated_to_animation_menu")

    
    def open_example_scene_under_animation(self, example_name: str):
        self.enable_example_window()
        self.navigate_to_example_window()
        self.omni_driver.wait(2)
        self._select_animation_submenu()
        self.omni_driver.wait(2)
        search_example_scene = self.omni_driver.find_element(self._search_example_scene)
        search_example_scene.send_keys(example_name)
        self._open_example(example_name)

    class SelectScene:
        """Class having constants for Example scenes"""

        attic_scene = "Attic_NVIDIA"
        astronaut_scene = "Astronaut"
        euclid_scene = "EuclidVR_Stage"
        flight_scene = "Flight"
        marbles_scene = "Marbles_Assets"
        example_deform = "example_deform"
        example_cloth = "example_cloth"
        filter = "filter"
        example_marching_cubes = "marching_cubes"
        fx_smoke_column = "fx_smoke_column"
        fx_sphere_collision_stick = "fx_sphere_collision_stick"
        fx_fireball_2 = "fx_fireball_2"
        fx_sphere_collision = "fx_sphere_collision"
        fx_tornado_magic = "fx_tornado_magic"
        path_curve = "path-curve"
        path_points = "path-points"
        retargeting_clip = "retargeting-clip"
        retargeting_graph = "retargeting-graph"
        fx_fireball_1 = "fx_fireball_1"
        fx_campfire_particles = "fx_campfire_particles"
        fx_campfire_flow = "fx_campfire_flow"
        fx_cold_magic_flow = "fx_cold_magic_flow"
        fx_explode_particles = "fx_explode_particles"
        fx_collision = "fx_collision"
        example_wave = "example_wave"
        example_particles = "example_particles"
        dense_smoke = "DenseSmoke"
        dark_smoke = "DarkSmoke"
        dust = "Dust"
        fire = "Fire"
        blend = "blend"
        instancing = "instancing"
        Marbles_Assets = "Marbles_Assets"
        Steam = "Steam"
        WispyFire = "WispyFire"
        desk_fan = "DeskFan"
        clock = "Clock"
        light_bulb = "LightBulb"
        look_at = "look-at"
        automotive_mdl = "Automotive_Material_Library"
        labyrinth_maze = "Labyrinth_Maze"
        claire_lookdev = "claire_lookdev"
        claire_lookdev_init = "claire_lookdev_init"
        state_machine = "state-machine"
        ragnarok_configurator_basic = "ragnarok_configurator_basic"
        ragnarok_configurator = "Ragnarok_Configurator"
        cloth_simulation = "cloth_simulation"
        mesh_deformation = "mesh_deformation"
        mesh_deformation_kernel_node = "mesh_deformation_kernel_node"
        particles_simulation_drop = "particles_simulation_drop"
        particles_simulation_throw = "particles_simulation_throw"
        prim_flocking = "prim_flocking"
        texture_mandelbrot = "texture_mandelbrot"
        wave_deformation = "wave_deformation"
        wave_solver = "wave_solver"
