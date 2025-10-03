# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base BaseDriveSimSDGModel Model class
   This module contains the base methods for BaseDriveSimSDGModel window
"""

from .base_model import BaseModel
from .base_main_toolbar_model import BaseMainToolBarModel
from .base_drive_sim_scenario_editor_model import BaseDriveSimScenarioEditorModel

class BaseDriveSimSDGModel(BaseMainToolBarModel,BaseDriveSimScenarioEditorModel):
    """Base model class for DriveSimSDGModel window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _sessions_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]")

    _load_toml = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/Button[0].text =='Load'")
    
    _setup = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/InvisibleButton[0]")

    _scrolling_frame = ("Drivesim Scenario Editor Tools Manager Window")
    
    _spawn_ego_run_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[0]")

    _environment_api_tab = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0] = 'Environment'")

    _weather_preset_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]")

    _set_environment_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/Button[0] = 'Set Environment'")

    _randomize_environment_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[4]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0]")

    _vehicles_api_label = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0] = 'Vehicles'")

    _vehicles_setup_label = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0] = 'setup()'")

    _vehicle_count_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/slider")

    _vehicle_create_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0] = 'Create Population'")

    _vehicle_delete_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[1] = 'Delete'")

    _vehicle_population_type_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]")

    _enable_vehicle_lights_checkbox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/CheckBox[0]")

    _vehicle_region_diameter_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/slider")

    _vehicle_offset_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/slider")

    _distance_between_vehicles_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/slider")

    _vehicles_surface_type_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/ComboBox[0]")

    _vehicles_shuffle_order_checkbox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/CheckBox[0]")

    _reposition_vehicles_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/Button[0]")

    _vehicles_random_color_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/Button[0]")

    _ego_api_label = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0]")

    _ego_advance_distance_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/slider")

    _reposition_ego_ahead = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[1]")

    _reposition_ego_back = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0]")

    _ego_region_diameter_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/slider")

    _turn_on_ego_lights_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[0] = 'Turn on Ego lights'")

    _turn_off_ego_lights_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/Button[1] = 'Turn off Ego lights'")

    _reposition_ego_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0] = 'Reposition Ego'")

    _signs_api_label = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0]")

    _sign_population_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]")

    _sign_count_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/slider")

    _sign_create_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0] = 'Create Population'")

    _sign_delete_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[1] = 'Delete'")

    _sign_surface_type_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/ComboBox[0]")

    _sign_spawn_diameter_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/slider")

    _signs_offset_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/slider")

    _distance_between_signs_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/slider")

    _signs_shuffle_order_checkbox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/CheckBox[0]")
    
    _reposition_signs_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[2]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/Button[0] = 'Reposition Signs'")

    _props_api_label = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/header/Label[0]")

    _props_population_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[0]/ComboBox[0]")

    _props_count_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/slider")

    _props_create_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[0]")

    _props_delete_population_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/Button[1]")

    _props_surface_type_combobox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[1]/ComboBox[0]")

    _props_spawn_radius_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[2]/slider")

    _distance_between_props_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[4]/slider")

    props_offset_from_ego_slider = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[3]/slider")

    _reposition_props_button = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/Button[0]")

    _props_shuffle_order_checkbox = ("Drivesim Scenario Editor Tools Manager Window//Frame/HStack[0]/Frame[0]/HStack[0]/VStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[3]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[1]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/HStack[5]/CheckBox[0]")

    _sdg_live_button = ("Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[5]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/SyntheticData")

    _ldrcolor_checkbox = ("Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[5]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/SyntheticData/LdrColor")

    _normal_sdg_live_checkbox = ("Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[5]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/SyntheticData/Normal")

    _instance_segmentation_checkbox = ("Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[5]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/SyntheticData/InstanceSegmentation")

    _show_window_button_sdg_live = ("Viewport//Frame/ZStack[0]/ZStack[0]/ZStack[5]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/SyntheticData/Show Window")

    def load_toml(self):
        """Clicks on load button to load a toml"""
        self.find_and_click(self._load_toml, refresh=True)
        
    def get_toml_list(self):
        """Clicks on load button to load a toml"""
        combobox_element = self.omni_driver.find_element(self._sessions_combobox)
        combobox_dict = combobox_element.get_combobox_info()
        combobox_list = combobox_dict["all_options"]
        return combobox_list

    def open_combobox_by_name(self, toml_name):
        """Clicks on ComboBox button to load a toml with name"""
        combobox_list = self.get_toml_list()
        toml_index = combobox_list.index(toml_name)
        self.select_item_from_stack_combo_box(self._sessions_combobox, toml_index)
        
    def spawn_ego(self):
        """spawns sdg ego"""
        self.toggle_drive_sim_scenario_editor()
        self.omni_driver.wait(5)
        
        self.open_data_studio_tab()
        self.omni_driver.wait(5)

        self.open_combobox_by_name("ego_config.toml")
        self.omni_driver.wait(5)

        self.load_toml()
        self.omni_driver.wait(15)
        
        self.find_and_click(self._setup, refresh=True)
        self.omni_driver.wait(5)
        
        self.find_and_click(self._spawn_ego_run_button, refresh=True)
        self.omni_driver.wait(15)


    # *************************** NEW CODE FROM HERE ***************************

    # Get Combobox list Generic function

    def get_combobox_list(self,combobox_locator):
        """Returns Combobox list"""
        combobox_element = self.omni_driver.find_element(combobox_locator)
        combobox_dict = combobox_element.get_combobox_info()
        combobox_list = combobox_dict["all_options"]
        return combobox_list

    # Environment API

    def change_environment_api(self, weather_preset=None):
        """Changes the environment based on weather preset or clicks on Randomize Environment button if preset is 'None'

        Args:
        weather_preset (str, optional): Specific weather preset to apply. If None, clicks on Randomize Environment button.
        """
        self.find_and_click(self._environment_api_tab, refresh=True)
        self.omni_driver.wait(2)

        if weather_preset is None:
            self.find_and_click(self._randomize_environment_button, refresh=True)
            self.omni_driver.wait(15)
            self.find_and_click(self._environment_api_tab, refresh=True)
            return

        ''' If you want to run only a specific weather'''
        combobox_list = self.get_combobox_list(self._weather_preset_combobox)
        element_index = combobox_list.index(weather_preset)
        
        self.select_item_from_stack_combo_box(self._weather_preset_combobox, element_index)
        self.find_and_click(self._set_environment_button, refresh=True)
        self.omni_driver.wait(15)

    # Ego API

    def ego_reposition_api(self, advance_distance, ego_region_diameter):
        """Repositions the ego based on the input"""
        self.find_and_click(self._ego_api_label, refresh=True)

        """Advance Distance is the distance by which the ego will be moved in the same lane(ahead or back)"""

        slider = self.omni_driver.find_element(self._ego_advance_distance_slider, refresh=True)
        slider.send_keys(str(advance_distance))

        self.find_and_click(self._reposition_ego_back,refresh=True)
        self.omni_driver.wait(5)
        self.find_and_click(self._reposition_ego_ahead,refresh=True)
        self.omni_driver.wait(5)
        self.find_and_click(self._reposition_ego_back,refresh=True)
        self.omni_driver.wait(5)
        self.find_and_click(self._reposition_ego_ahead,refresh=True)
        self.omni_driver.wait(5)

        """Region Diameter is the region within which the ego will can moved in the any lane(diagonal or ahead or back)"""
        
        slider = self.omni_driver.find_element(self._ego_region_diameter_slider, refresh=True)
        slider.send_keys(str(ego_region_diameter))
        self.omni_driver.wait(3)
        
        self.find_and_click(self._reposition_ego_button, refresh=True)
        self.omni_driver.wait(2)
        self.omni_driver.wait(3)
        self.find_and_click(self._reposition_ego_button, refresh=True)
        self.omni_driver.wait(2)
        self.omni_driver.wait(3)
        self.find_and_click(self._reposition_ego_button, refresh=True)
        self.omni_driver.wait(2)
        self.omni_driver.wait(3)

        '''code to run all weathers in the combobox'''
        combobox_list = self.get_combobox_list(self._weather_preset_combobox)
        self.find_and_click(self._environment_api_tab, refresh=True)

        for element in combobox_list :
            if(element == "night"):
                self.select_item_from_stack_combo_box(self._weather_preset_combobox, name=element)
                self.find_and_click(self._set_environment_button,refresh=True)
                self.omni_driver.wait(10)
                self.find_and_click(self._turn_on_ego_lights_button, refresh=True)
                self.omni_driver.wait(10)
                self.find_and_click(self._turn_off_ego_lights_button, refresh=True)
                self.omni_driver.wait(10)
                self.find_and_click(self._turn_on_ego_lights_button, refresh=True)
                self.omni_driver.wait(10)
            else:
                continue
            
            for element in combobox_list :
                if(element == "noon"):
                    self.select_item_from_stack_combo_box(self._weather_preset_combobox, name=element)
                    self.find_and_click(self._set_environment_button,refresh=True)
                    self.omni_driver.wait(10)
                    self.find_and_click(self._turn_on_ego_lights_button, refresh=True)
                    self.omni_driver.wait(10)
                    self.find_and_click(self._turn_off_ego_lights_button, refresh=True)
                    self.omni_driver.wait(10)
                else:
                    continue

            self.find_and_click(self._ego_api_label, refresh=True)

    # Signs API

    def signs_randomization_api(self, sign_count, spawn_diameter, signs_offset, distance_between_signs):
        self.find_and_click(self._signs_api_label, refresh=True)

        # Get all options from both comboboxes
        sign_population_types = self.get_combobox_list(self._sign_population_combobox)
        surface_types = self.get_combobox_list(self._sign_surface_type_combobox)

        # Iterate through each sign population type
        for sign_type in sign_population_types:
            element_index = sign_population_types.index(sign_type)
            self.select_item_from_stack_combo_box(self._sign_population_combobox, element_index)
            self.omni_driver.wait(2)

            slider = self.omni_driver.find_element(self._sign_count_slider, refresh=True)
            slider.send_keys(str(sign_count))
            self.omni_driver.wait(3)

            self.find_and_click(self._sign_create_population_button, refresh=True)
            self.omni_driver.wait(15)

            slider = self.omni_driver.find_element(self._sign_spawn_diameter_slider, refresh=True)
            slider.send_keys(str(spawn_diameter))
            self.omni_driver.wait(3)

            slider = self.omni_driver.find_element(self._signs_offset_slider, refresh=True)
            slider.send_keys(str(signs_offset))
            self.omni_driver.wait(3)

            slider = self.omni_driver.find_element(self._distance_between_signs_slider, refresh=True)
            slider.send_keys(str(distance_between_signs))
            self.omni_driver.wait(3)

            # Iterate through each surface type
            for surface in surface_types:
                element_index = surface_types.index(surface)
                self.select_item_from_stack_combo_box(self._sign_surface_type_combobox, element_index)
                self.omni_driver.wait(3)

                shuffle_order_checkbox = self.omni_driver.find_element(self._signs_shuffle_order_checkbox, refresh=True)
                ''' Get all size and position attributes at once '''
                checkbox_properties = shuffle_order_checkbox.get_size_and_position("all")
                pos_x = checkbox_properties["screen_position_x"]
                pos_y = checkbox_properties["screen_position_y"]

                self.omni_driver.click_at(pos_x, (pos_y+1))
                self.omni_driver.wait(5)

                self.find_and_click(self._reposition_signs_button, refresh=True)
                self.omni_driver.wait(10)

                self.find_and_click(self._reposition_signs_button, refresh=True)
                self.omni_driver.wait(10)

                self.omni_driver.click_at(pos_x, (pos_y+1))
                self.omni_driver.wait(5)

                self.find_and_click(self._reposition_signs_button, refresh=True)
                self.omni_driver.wait(10)

            self.find_and_click(self._sign_delete_population_button, refresh=True)
            self.omni_driver.wait(15)

        self.find_and_click(self._signs_api_label, refresh=True)

    # Props API

    def props_randomization_api(self, prop_count, spawn_radius, props_offset_from_ego, distance_between_props):
        self.find_and_click(self._props_api_label,refresh=True)
        
        # Get all options from both comboboxes
        props_population_types = self.get_combobox_list(self._props_population_combobox)
        surface_types = self.get_combobox_list(self._props_surface_type_combobox)
        
        # Iterate through each combination
        for population_type in props_population_types:
            element_index = props_population_types.index(population_type)
            self.select_item_from_stack_combo_box(self._props_population_combobox, element_index)
            self.omni_driver.wait(3)
        
            slider = self.omni_driver.find_element(self._props_count_slider, refresh=True)
            slider.send_keys(str(prop_count))
            self.omni_driver.wait(3)

            self.find_and_click(self._props_create_population_button, refresh=True)
            self.omni_driver.wait(15)

            slider = self.omni_driver.find_element(self._props_spawn_radius_slider, refresh=True)
            slider.send_keys(str(spawn_radius))
            self.omni_driver.wait(3)

            slider = self.omni_driver.find_element(self.props_offset_from_ego_slider, refresh=True)
            slider.send_keys(str(props_offset_from_ego))
            self.omni_driver.wait(3)

            slider = self.omni_driver.find_element(self._distance_between_props_slider, refresh=True)
            slider.send_keys(str(distance_between_props))
            self.omni_driver.wait(3)

            for surface in surface_types:
                element_index = surface_types.index(surface)
                self.select_item_from_stack_combo_box(self._props_surface_type_combobox, element_index)
                self.omni_driver.wait(3)

                shuffle_order_checkbox = self.omni_driver.find_element(self._props_shuffle_order_checkbox, refresh=True)
                ''' Get all size and position attributes at once '''
                checkbox_properties = shuffle_order_checkbox.get_size_and_position("all")
                pos_x = checkbox_properties["screen_position_x"]
                pos_y = checkbox_properties["screen_position_y"]

                self.omni_driver.click_at(pos_x, (pos_y+1))
                self.omni_driver.wait(5)

                self.find_and_click(self._reposition_props_button,refresh=True)
                self.omni_driver.wait(7)
                self.find_and_click(self._reposition_props_button,refresh=True)
                self.omni_driver.wait(10)

                self.omni_driver.click_at(pos_x, (pos_y+1))
                self.omni_driver.wait(5)

                self.find_and_click(self._reposition_props_button,refresh=True)
                self.omni_driver.wait(20)

            self.find_and_click(self._props_delete_population_button,refresh=True)
            self.omni_driver.wait(15)

        self.omni_driver.wait(5)
        self.find_and_click(self._props_api_label,refresh=True)

    # VEHICLES API
   
    def vehicles_randomization_api(self, vehicle_count, vehicle_region_diameter, vehicle_offset, distance_between_vehicles):
        self.find_and_click(self._vehicles_api_label, refresh=True)
        self.omni_driver.wait(2)

        '''Taking both the comboboxes lists viz - vehicles population type and vehicles surface type'''
        vehicles_population_types_list = self.get_combobox_list(self._vehicle_population_type_combobox)
        self.omni_driver.wait(2)
        vehicles_surface_types_list = self.get_combobox_list(self._vehicles_surface_type_combobox)
        self.omni_driver.wait(2)

        for vehicle_population_type in vehicles_population_types_list:
            element_index = vehicles_population_types_list.index(vehicle_population_type)
            self.select_item_from_stack_combo_box(self._vehicle_population_type_combobox, element_index)
            self.omni_driver.wait(3)

            vehicle_count_slider = self.omni_driver.find_element(self._vehicle_count_slider, refresh=True)
            vehicle_count_slider.send_keys(str(vehicle_count))
            self.omni_driver.wait(3)

            enable_vehicle_lights_checkbox = self.omni_driver.find_element(self._enable_vehicle_lights_checkbox, refresh=True)
            ''' Get all size and position attributes at once '''
            checkbox_properties = enable_vehicle_lights_checkbox.get_size_and_position("all")
            pos_x = checkbox_properties["screen_position_x"]
            pos_y = checkbox_properties["screen_position_y"]

            self.omni_driver.click_at(pos_x, (pos_y+1)) # Click at the checkbox to enable vehicle lights
            self.omni_driver.wait(5)

            self.find_and_click(self._vehicle_create_population_button, refresh=True)
            self.omni_driver.wait(20)

            vehicle_spawn_diameter_slider = self.omni_driver.find_element(self._vehicle_region_diameter_slider, refresh=True)
            vehicle_spawn_diameter_slider.send_keys(str(vehicle_region_diameter))
            self.omni_driver.wait(3)

            vehicle_offset_slider = self.omni_driver.find_element(self._vehicle_offset_slider, refresh=True)
            vehicle_offset_slider.send_keys(str(vehicle_offset))
            self.omni_driver.wait(3)

            vehicle_distance_between_vehicles_slider = self.omni_driver.find_element(self._distance_between_vehicles_slider, refresh=True)
            vehicle_distance_between_vehicles_slider.send_keys(str(distance_between_vehicles))
            self.omni_driver.wait(3)

            vehicle_shuffle_order_checkbox = self.omni_driver.find_element(self._vehicles_shuffle_order_checkbox, refresh=True)
            ''' Get all size and position attributes at once '''
            checkbox_properties = vehicle_shuffle_order_checkbox.get_size_and_position("all")
            pos_x = checkbox_properties["screen_position_x"]
            pos_y = checkbox_properties["screen_position_y"]

            for vehicle_surface_type in vehicles_surface_types_list:
                element_index = vehicles_surface_types_list.index(vehicle_surface_type)
                self.select_item_from_stack_combo_box(self._vehicles_surface_type_combobox, element_index)
                self.omni_driver.wait(3)

                self.find_and_click(self._reposition_vehicles_button, refresh=True)
                self.omni_driver.wait(10)
                self.find_and_click(self._reposition_vehicles_button, refresh=True)
                self.omni_driver.wait(10)

                self.omni_driver.click_at(pos_x, (pos_y+1)) # Click at the checkbox to enable vehicle shuffle order
                self.omni_driver.wait(5)

                self.find_and_click(self._reposition_vehicles_button, refresh=True)
                self.omni_driver.wait(10)

                self.find_and_click(self._vehicles_random_color_button, refresh=True)
                self.omni_driver.wait(15)

            self.find_and_click(self._vehicle_delete_population_button, refresh=True)
            self.omni_driver.wait(15)

        self.find_and_click(self._vehicles_api_label,refresh=True)
        self.omni_driver.wait(5)