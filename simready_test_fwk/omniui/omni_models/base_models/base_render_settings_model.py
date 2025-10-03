# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Render Settings class
   This module contains the base methods for Render Settings window
"""


from random import randint, uniform
import os
from omni_remote_ui_automator.common.enums import DlssModesRenderSettings
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from omni_remote_ui_automator.driver.waits import Wait
from omniui.utils.utility_functions import get_downloads_folder_path
import filecmp

class BaseRenderSettingsModel(BaseModel):
    """Base model class for Render settings window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to render settings window
    _render_settings_window = "Render Settings//Frame/VStack[0]"
    _path_tracing_options = (
        'Render Settings//Frame/**/RadioButton[*].text=="Path Tracing"'
    )
    _ray_tracing_options = (
        'Render Settings//Frame/**/RadioButton[*].text=="Ray Tracing"'
    )
    _iray_options = 'Render Settings//Frame/**/RadioButton[*].text=="Accurate (Iray)"'
    _denoising_chkbox = (
        "Render Settings//Frame/**/PTSettingStack/Denoising/**/CheckBox[0]"
    )
    _denoising_expand = "Render Settings//Frame/**/Denoising"
    _denoising_blend_factor = (
        "Render Settings//Frame/**/HStack_OptiX_Denoiser_Blend_Factor/FloatSlider[0]"
    )
    _direct_lighting_toggle_chkbox = (
        "Render Settings//Frame/**/Direct Lighting/**/CheckBox[0]"
    )
    _ray_reconstruction_toggle_chkbox = "Render Settings//Frame/**/NVIDIA DLSS/**/HStack_Ray_Reconstruction/**/CheckBox[0]"
    _new_denoiser_experimental_chkbox = (
        "Render Settings//Frame/**/HStack_New_Denoiser_(experimental)/**/CheckBox[0]"
    )
    _subsurface_scattering_chkbox = (
        "Render Settings//Frame/**/Subsurface Scattering/**/CheckBox[0]"
    )
    _direct_lighting_expand = "Render Settings//Frame/**/Direct Lighting"
    _nvidia_dlss_expand = "Render Settings//Frame/**/NVIDIA DLSS"
    _common_btn = "Render Settings//Frame/**/RadioButton[*].text=='Common'"
    _commonsetting_lighting = "Render Settings//Frame/**/Lighting/Frame[0]"
    _accurate_iray_btn = (
        "Render Settings//Frame/VStack[0]/VStack[0]/HStack[0]/RadioButton[1]"
    )
    _multi_gpu_expand = "Render Settings//Frame/**/Multi-GPU"
    _multi_gpu_toggle_chkbox = "Render Settings//Frame/**/Multi-GPU/**/CheckBox[0]"
    
   # Indirect Diffuse Lighting
    _indirect_diffuse_lighting_expand = (
        "Render Settings//Frame/**/Indirect Diffuse Lighting"
    )
    _indirect_diffuse_gi_chkbox = (
        "Render Settings//Frame/**/HStack_Indirect_Diffuse_GI/**/CheckBox[0]"
    )
    _indirect_diffuse_gi_kernel_radius_slider = "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse Lighting/**/HStack_______Kernel_Radius/IntSlider[0]"
    _indirect_diffuse_gi_iteration_count_slider = (
        "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse"
        " Lighting/**/HStack_______Iteration_Count/IntSlider[0]"
    )
    _indirect_diffuse_gi_max_history_length_slider = (
        "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse"
        " Lighting/**/HStack_______Max_History_Length/IntSlider[0]"
    )

    # Ambient Occlusion
    _ambient_occlusion_chkbox = "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse Lighting/**/HStack_Ambient_Occlusion/**/CheckBox[0]"
    _ambient_occlusion_ray_length_slider = "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse Lighting/**/HStack____Ray_Length_(cm)/FloatDrag[0]"
    _ambient_occlusion_min_samples_slider = (
        "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse"
        " Lighting/**/HStack____Minimum_Samples_Per_Pixel/IntSlider[0]"
    )
    _ambient_occlusion_max_samples_slider = (
        "Render Settings//Frame/**/RTSettingStack/Indirect Diffuse"
        " Lighting/**/HStack____Maximum_Samples_Per_Pixel/IntSlider[0]"
    )

    # Shadows
    _shadows_enable = "Render Settings//Frame/**/HStack_Shadows"
    _shadows_chkbox = "Render Settings//Frame/**/HStack_Shadows/**/CheckBox[0]"

    # Dome Lighting
    _dome_lighting_enable = "Render Settings//Frame/**/RTSettingStack/Direct Lighting/**/HStack____Dome_Lighting"
    _dome_lighting_chkbx = "Render Settings//Frame/**/RTSettingStack/Direct Lighting/**/HStack____Dome_Lighting/**/CheckBox[0]"
    _dome_lighting_in_reflections_chkbx = (
        "Render Settings//Frame/**/RTSettingStack/Direct"
        " Lighting/**/HStack_______Dome_Lighting_in_Reflections/**/CheckBox[0]"
    )

    # Reflections
    _reflections_expand = "Render Settings//Frame/**/Reflections"
    _reflections_toggle_checkbox = (
        "Render Settings//Frame/**/Reflections/**/CheckBox[0]"
    )

    # Translucency
    _translucency_expand = "Render Settings//Frame/**/Translucency"
    _translucency_toggle_checkbox = (
        "Render Settings//Frame/**/Translucency/**/CheckBox[0]"
    )

    # Anti-aliasing
    _anti_aliasing_expand = "Render Settings//Frame/**/Anti-Aliasing"

    _post_processing_options = (
        "Render Settings//Frame/VStack[0]/VStack[0]/HStack[0]/RadioButton[2]"
    )

    # Depth of field camera overrides
    _depth_of_field_camera_overrides_expand = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera Overrides"
    )
    _depth_of_field_camera_override_toggle_checkbox = (
        "Render Settings//Frame/**/Depth of Field Camera Overrides/**/CheckBox[0]"
    )
    _enable_depth_of_field_toggle_checkbox = "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera Overrides/**/HStack_Enable_DOF/**/CheckBox[0]"
    _subject_distance_slider = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera"
        " Overrides/**/HStack_Subject_Distance/FloatDrag[0]"
    )
    _subject_distance_slider_reset = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera"
        " Overrides/**/HStack_Subject_Distance/**/Rectangle[0]"
    )
    _focal_length_slider = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera"
        " Overrides/**/HStack_Focal_Length_(mm)/FloatDrag[0]"
    )
    _focal_length_slider_reset = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera"
        " Overrides/**/HStack_Focal_Length_(mm)/**/Rectangle[0]"
    )
    _f_stop_slider = "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera Overrides/**/HStack_F-stop/FloatDrag[0]"
    _f_stop_slider_reset = "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera Overrides/**/HStack_F-stop/**/Rectangle[0]"
    _anisotropy_slider = "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera Overrides/**/HStack_Anisotropy/FloatSlider[0]"
    _anisotropy_slider_reset = (
        "Render Settings//Frame/**/PostSettingStack/Depth of Field Camera"
        " Overrides/**/HStack_Anisotropy/**/Rectangle[0]"
    )

    # FFT bloom
    _fft_bloom_expand = "Render Settings//Frame/**/PostSettingStack/FFT Bloom"
    _fft_bloom_toggle_checkbox = "Render Settings//Frame/**/FFT Bloom/**/CheckBox[0]"
    _scale_slider = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Scale/FloatDrag[0]"
    _scale_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Scale/**/Rectangle[0]"
    _cutoff_fuzziness_slider = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Cutoff_Fuzziness/FloatSlider[0]"
    _cutoff_fuzziness_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Cutoff_Fuzziness/**/Rectangle[0]"
    _energy_constrained_checkbox = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Energy_Constrained/**/CheckBox[0]"
    _energy_constrained_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack_Energy_Constrained/**/Rectangle[0]"
    _halo_flare_weight_slider = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Halo_Flare_Weight/FloatDrag[0]"
    _halo_flare_weight_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Halo_Flare_Weight/**/Rectangle[0]"
    _aniso_flare_weight_slider = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Aniso_Flare_Weight/FloatDrag[0]"
    _aniso_flare_weight_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Aniso_Flare_Weight/**/Rectangle[0]"
    _isotropic_flare_weight_slider = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Isotropic_Flare_Weight/FloatDrag[0]"
    _isotropic_flare_weight_reset = "Render Settings//Frame/**/PostSettingStack/FFT Bloom/**/HStack____Isotropic_Flare_Weight/**/Rectangle[0]"
    _physical_model_chkbox = (
        "Render Settings//Frame/**/HStack_Physical_Model/**/CheckBox[0]"
    )
    _blades_slider = "Render Settings//Frame/**/HStack____Blades/IntSlider[0]"
    _aperture_rotation = (
        "Render Settings//Frame/**/HStack____Aperture_Rotation/FloatDrag[0]"
    )
    _sensor_diagonal_slider = (
        "Render Settings//Frame/**/HStack____Sensor_Diagonal/FloatDrag[0]"
    )
    _sensor_aspect_ratio_slider = (
        "Render Settings//Frame/**/HStack____Sensor_Aspect_Ratio/FloatDrag[0]"
    )
    _f_stop_slider = "Render Settings//Frame/**/HStack____F-stop/FloatDrag[0]"
    _focal_length_slider = (
        "Render Settings//Frame/**/HStack____Focal_Length_(mm)/FloatDrag[0]"
    )
    _blades_slider_reset = "Render Settings//Frame/**/HStack____Blades/**/Rectangle[0]"
    _aperture_rotation_reset = (
        "Render Settings//Frame/**/HStack____Aperture_Rotation/**/Rectangle[0]"
    )
    _sensor_diagonal_slider_reset = (
        "Render Settings//Frame/**/HStack____Sensor_Diagonal/**/Rectangle[0]"
    )
    _sensor_aspect_ratio_slider_reset = (
        "Render Settings//Frame/**/HStack____Sensor_Aspect_Ratio/**/Rectangle[0]"
    )
    _f_stop_slider_reset = "Render Settings//Frame/**/HStack____F-stop/**/Rectangle[0]"
    _focal_length_slider_reset = (
        "Render Settings//Frame/**/HStack____Focal_Length_(mm)/**/Rectangle[0]"
    )

    # Motion blur
    _motion_blur_expand = "Render Settings//Frame/**/PostSettingStack/Motion Blur"
    _motion_blur_toggle_checkbox = (
        "Render Settings//Frame/**/Motion Blur/**/CheckBox[0]"
    )
    _blur_diameter_fraction_slider = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Blur_Diameter_Fraction/FloatSlider[0]"
    _exposure_fraction_slider = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Exposure_Fraction/FloatSlider[0]"
    _no_of_samples_slider = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Number_of_Samples/IntSlider[0]"
    _blur_diameter_fraction_reset = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Blur_Diameter_Fraction/**/Rectangle[0]"
    _exposure_fraction_reset = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Exposure_Fraction/**/Rectangle[0]"
    _no_of_samples_reset = "Render Settings//Frame/**/PostSettingStack/Motion Blur/**/HStack_Number_of_Samples/**/Rectangle[0]"

    # NVIDIA DLSS
    _dlss_collapsebar = "Render Settings//Frame/**/NVIDIA DLSS"
    _frame_generator_toggle_chkbox = "Render Settings//Frame/**/NVIDIA DLSS/**/HStack_Frame_Generation/**/CheckBox[0]"
    _dlss_mode_combobox = (
        "Render Settings//Frame/**/NVIDIA DLSS/**/HStack____Mode/ComboBox[0]"
    )

    # Direct Sampled Lighting
    _direct_sampled_lighting_stack = (
        "Render Settings//Frame/**/HStack_Sampled_Direct_Lighting_Mode"
    )
    _direct_sampled_lighting_chkbox = (
        "Render Settings//Frame/**/HStack_Sampled_Direct_Lighting_Mode/**/CheckBox[0]"
    )

    #  Non-uniform Volumes
    _non_uniform_vol_collapse_bar = (
        "Render Settings//Frame/**/PTSettingStack/Non-uniform Volumes"
    )
    _non_uniform_vol_checkbox = (
        "Render Settings//Frame/**/PTSettingStack/Non-uniform Volumes/**/CheckBox[0]"
    )
    _non_uniform_vol_max_collision_stack = "Render Settings//Frame/**/PTSettingStack/Non-uniform Volumes/**/HStack_Max_Collision_Count"
    _non_uniform_vol_max_collision_drag = "Render Settings//Frame/**/PTSettingStack/Non-uniform Volumes/**/HStack_Max_Collision_Count/IntDrag[0]"

    # IRAY Device Settings
    _device_settings_collapse_bar = (
        "Render Settings//Frame/**/CommonIRaySettingStack/Device Settings"
    )
    _device_settings_all_chkboxes = "Render Settings//Frame/**/CommonIRaySettingStack/Device Settings/**/CheckBox[0]"

    # Common Settings
    _lighting_roughness_slider = "Render Settings//Frame/**/HStack_Invisible_Lights_Roughness_Threshold/FloatSlider[0]"
    _lighting_collapsebar = "Render Settings//Frame/**/Lighting"
    _light_visibility_settings_collapsebar = 'Render Settings//Frame/**/CollapsableFrame[*].title=="Light Visibility Settings"'

    # Accurate(Iray) Settings
    _device_settings = (
        "Render Settings//Frame/**/CommonIRaySettingStack/Device Settings"
    )
    _cpu_enable_chkbox = "Render Settings//Frame/**/HStack_CPU_Enabled/**/CheckBox[0]"
    _gpu_enable_chkbox = "Render Settings//Frame/**/HStack_GPU_0_Quadro_RTX_3000_with_Max-Q_Design/**/CheckBox[0]"
    _render_settings = (
        "Render Settings//Frame/**/CommonIRaySettingStack/Render Settings"
    )
    _denoiser_chkbox = "Render Settings//Frame/VStack[0]/**/Frame[0]/VStack[0]/HStack_Denoiser/**/CheckBox[0]"
    _caustic_sampler_chkbox = "Render Settings//Frame/VStack[0]/**/Frame[0]/VStack[0]/HStack_Caustic_Sampler/**/CheckBox[0]"
    _canvas_setting_combo_box = "Render Settings//Frame/**/CommonIRaySettingStack/Render Settings/**/HStack_Canvas/ComboBox[0]"
    _lighting_visible_combo_box = (
        "Render Settings//Frame/**/CommonIRaySettingStack/Render"
        " Settings/**/HStack_Light_Visibility_In_Primary_Rays/ComboBox[0]"
    )

    # Subsurface scattering settings
    _subsurface_scattering_expand = "Render Settings//Frame/**/Subsurface Scattering"
    _subsurface_denoiser = "Render Settings//Frame/**/HStack_Denoiser/**/CheckBox[0]"
    _subsurface_transmission = (
        "Render Settings//Frame/**/HStack_Transmission/**/CheckBox[0]"
    )
    _subsure_transmission_denoiser = (
        "Render Settings//Frame/**/HStack____Denoiser/**/CheckBox[0]"
    )

    # denoiseAOV
    _denoise_aov_checkbox = (
        "Render Settings//Frame/**/HStack_Denoise_AOVs/**/CheckBox[0]"
    )

    # Path traced samples per size
    _path_traced_expand = "Render Settings//Frame/**/PTSettingStack/Path-Tracing"
    _samples_per_pixel_drag = (
        "Render Settings//Frame/**/HStack_Total_Samples_per_Pixel_(0_=_inf)/IntDrag[0]"
    )

    # AOV settings
    _aov_expand = "Render Settings//Frame/**/PTSettingStack/AOV"
    _direct_illumination = "Render Settings//Frame/**/PTSettingStack/AOV/**/HStack_Direct_Illumation/**/CheckBox[0]"

    _debug_collapse_bar = "Render Settings//Frame/**/CommonSettingStack/Debug View"
    _render_target = (
        "Render Settings//Frame/**/CommonSettingStack/Debug View/**/StringField[0]"
    )

    # Tone Mapping - Post Processing Settings
    _tone_mapping_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[0].identifier=='Tone Mapping'"
    )
    _tone_mapping_operator_combo_box = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_tonemap_op'"
    )
    _tone_mapping_srgb_to_gamma_conversion_check_box = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tonemap/enableSrgbToGamma'"
    _tone_mapping_cm2_factor_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tonemap/cm2Factor'"
    _tone_mapping_film_iso_drag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/tonemap/filmIso'"
    )
    _tone_mapping_camera_shutter_drag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/tonemap/cameraShutter'"
    _tone_mapping_fstop_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tonemap/fNumber'"
    _tone_mapping_white_point_color_widget = (
        "Render Settings//Frame/**/HStack[0].identifier=='/rtx/post/tonemap/whitepoint'"
    )
    _tone_mapping_wrap_value_drag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/tonemap/wrapValue'"
    _tone_mapping_dither_strength_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tonemap/dither'"
    _tone_mapping_color_space = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_tonemap_colorMode'"

    # Auto Exposure - Post Processing Settings
    _auto_exposure_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[1].identifier=='Auto Exposure'"
    )
    _auto_exposure_enabled = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/histogram/enabled'"
    _auto_exposure_adaptation_speed = (
        "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/histogram/tau'"
    )
    _auto_exposure_white_point_scale = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/histogram/whiteScale'"
    _auto_exposure_min_value = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/histogram/minEV'"
    )
    _auto_exposure_max_value = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/histogram/maxEV'"
    )
    _auto_exposure_value_clamping = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/histogram/useExposureClamping'"
    _auto_exposure_histogram_filter_type = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_histogram_filterType'"

    # Color Correction - Post Processing Settings
    _color_correction_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[2].identifier=='Color Correction'"
    )
    _color_correction_enable_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/colorcorr/enabled'"
    _color_correction_output_color_space_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_colorcorr_outputMode'"
    _color_correction_mode = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_colorcorr_mode'"
    )

    # Color Grading - Post Processing Settings
    _color_grading_mode_combobox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_colorgrad_mode'"
    )
    _color_grading_output_space_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_colorgrad_outputMode'"
    _color_grading_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[3].identifier=='Color Grading'"
    )
    _color_grading_main_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/colorgrad/enabled'"

    # XR Composting - Post Processing Settings
    _xr_compositing_enabled_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/enabled'"
    _xr_compositing_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='XR Compositing'"
    )
    _xr_compositing_composite_in_editor_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/backgroundComposite'"
    _xr_compositing_output_alpha_composited_image_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/outputAlphaInComposite'"
    _xr_compositing_output_black_background_composited_image_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/blackBackgroundInComposite'"
    _xr_compositing_multiply_color_value_by_alpha_composite_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/premultiplyColorByAlpha'"
    _xr_compositing_convert_refraction_to_opacity_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/material/translucencyAsOpacity'"
    _xr_compositing_backplate_color_widget = "Render Settings//Frame/**/HStack[0].identifier=='/rtx/post/backgroundZeroAlpha/backgroundDefaultColor'"
    _xr_compositing_backplate_texture_path_stringfield = (
        "Render Settings//Frame/**/StringField[0].identifier=='AssetPicker_path'"
    )
    _xr_compositing_asset_picker_select_backplate_button = (
        "Render Settings//Frame/**/Button[0].identifier=='AssetPicker_select'"
    )
    _xr_compositing_backplate_texture_locate_button = (
        "Render Settings//Frame/**/Button[1].identifier=='AssetPicker_locate'"
    )
    _xr_compositing_backplate_texture_is_linear_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/backplateTextureIsLinear'"
    _xr_compositing_backplate_luminance_scale_floatdrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/backgroundZeroAlpha/backplateLuminanceScaleV2'"
    _xr_compositing_enable_lens_distortion_correction_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/backgroundZeroAlpha/enableLensDistortionCorrection'"
    _xr_compositing_all_checkboxes = (
        "Render Settings//Frame/**/XR Compositing/**/CheckBox[*]"
    )

    # Matte Object - Post Processing Settings
    _matte_object_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[5].identifier=='Matte Object'"
    )
    _matte_object_main_checkbox = (
        "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/matteObject/enabled'"
    )
    _matte_object_shadow_catcher_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/matteObject/enableShadowCatcher'"

    # Chromatic Aberration - Post Processing Settings
    _chromatic_aberration_enabled = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/chromaticAberration/enabled'"
    _chromatic_aberration_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[6].identifier=='Chromatic Aberration'"
    _chromatic_aberration_strength_red_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/chromaticAberration/strengthR'"
    _chromatic_aberration_strength_green_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/chromaticAberration/strengthG'"
    _chromatic_aberration_strength_blue_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/chromaticAberration/strengthB'"
    _chromatic_aberration_algorithm_red_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeR'"
    _chromatic_aberration_algorithm_green_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeG'"
    _chromatic_aberration_algorithm_blue_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeB'"
    _chromatic_aberration_lanczos_sampler_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/chromaticAberration/enableLanczos'"
    _chromatic_aberration_boundary_blending_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[6]/Frame[0]/ZStack[0]/VStack[0]/Frame[0]/VStack[0]/CollapsableFrame[0]"
    _chromatic_aberration_repeat_mirrored_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/chromaticAberration/mirroredRepeat'"
    _chromatic_aberration_blend_region_size_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/chromaticAberration/boundaryBlendRegionSize'"
    _chromatic_aberration_blend_region_falloff_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/chromaticAberration/boundaryBlendFalloff'"

    # Depth of Field Camera Overrides - Post Processing Settings
    _depth_of_field_enabled_checkbox = (
        "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/dof/enabled'"
    )
    _depth_of_field_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[7].identifier=='Depth of Field Camera Overrides'"
    _depth_of_field_enable_checkbox = (
        "Render Settings//Frame/**/HStack[0].identifier=='HStack_Enable_DOF'",
        "Render Settings//Frame/**/HStack_Enable_DOF/**/CheckBox[0]",
    )
    _depth_of_field_subject_distance_slider = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/dof/subjectDistance'"
    _depth_of_field_focal_length_slider = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/dof/focalLength'"
    )
    _depth_of_field_f_stop_slider = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/dof/fNumber'"
    )
    _depth_of_field_anisotropy_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/dof/anisotropy'"
    _depthOfField_overrideCheckbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/dof/overrideEnabled'"

    # Motion Blur - Post Processing Settings
    _motion_blur_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[8].identifier=='Motion Blur'"
    )
    _motion_blur_enabled_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/motionblur/enabled'"
    _motion_blur_diameter_fraction_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/motionblur/maxBlurDiameterFraction'"
    _motion_blur_exposure_fraction_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/motionblur/exposureFraction'"
    _motion_blur_number_of_samples_slider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/post/motionblur/numSamples'"

    # TV Noise & Film Grain - Post Processing Settings
    _tv_noise_film_grain_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[10]"
    )
    _tv_noise_enable_checkbox = "Render Settings//Frame/**/TV Noise & Film Grain/Frame[0]/**/CheckBox[*].identifier=='/rtx/post/tvNoise/enabled'"
    _tv_noise_film_grain_enable_random_splotches_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableRandomSplotches'"
    _tv_noise_film_grain_enable_vertical_lines_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableVerticalLines'"
    _tv_noise_film_grain_enable_wavy_distortion_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableWaveDistortion'"
    _tv_noise_film_grain_enable_ghost_flickering_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableGhostFlickering'"
    _tv_noise_film_grain_enable_vignetting_flickering_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableVignettingFlickering'"
    _tv_noise_vignettingEnableCheckbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableVignetting'"
    _tv_noise_film_grain_enable_scanlines_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableScanlines'"
    _tv_noise_film_grain_scanline_spread_float_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/scanlineSpread'"
    _tv_noise_film_grain_grain_amount_float_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/grainAmount'"
    _tv_noise_film_grain_color_amount_float_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/colorAmount'"
    _tv_noise_film_grain_luminance_amount_float_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/lumAmount'"
    _tv_noise_film_grain_grain_size_float_slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/grainSize'"
    _tv_noise_film_grain_vignetting_size_float_drag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/tvNoise/vignettingSize'"
    _tv_noise_film_grain_vignetting_strength_float_slider = (
        "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/tvNoise/vignettingStrength'",
    )
    _tv_noise_film_grain_enable_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/tvNoise/enableFilmGrain'"

    #  FFT Bloom - Post Processing Settings
    _fftBloom_enabled_checkBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/lensFlares/enabled'"
    _fftBloom_collapsableFrame = "Render Settings//Frame/**/CollapsableFrame[9]"
    _fftBloom_scale_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/flareScale'"
    _fftBloom_cutoffPoint_multiFloatDragField = (
        "Render Settings//Frame/**/MultiFloatDragField[0].name=='multivalue'"
    )
    _fftBloom_cutoffFuzziness_floatSlider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/lensFlares/cutoffFuzziness'"
    _fftBloom_alphaChannelScale_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/alphaExposureScale'"
    _fftBloom_energyConstrained_checkBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/lensFlares/energyConstrainingBlend'"
    _fftBloom_physicalModel_checkBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/post/lensFlares/physicalSettings'"
    _fftBloom_blades_intSlider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/post/lensFlares/blades'"
    _fftBloom_apertureRotation_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/apertureRotation'"
    _fftBloom_sensorDiagonal_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/sensorDiagonal'"
    _fftBloom_sensorAspectRatio_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/sensorAspectRatio'"
    _fftBloom_fStop_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/fNumber'"
    _fftBloom_focalLength_floatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/focalLength'"
    _fftBloom_haloFlareWeightFloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/haloFlareWeight'"
    _fftBloom_anisoFlareWeightFloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/anisoFlareWeight'"
    _fftBloom_isotropicFlareWeightFloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/post/lensFlares/isotropicFlareWeight'"

    #  Flow - Common Settings
    _flowCategory_enable_checkbox = "Render Settings//Frame/**/Flow/**/CheckBox[0]"
    _flowCategory_collapsibleFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Flow'"
    )
    _flowCategory_realTimeRayTracedShadowsCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Flow_in_Real-Time_Ray_Traced_Shadows/**/CheckBox[0]"
    _flowCategory_realTimeRayTracedReflectionsCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Flow_in_Real-Time_Ray_Traced_Reflections/**/CheckBox[0]"
    _flowCategory_realTimeRayTracedTranslucencyCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Flow_in_Real-Time_Ray_Traced_Translucency/**/CheckBox[0]"
    _flowCategory_pathTracedModeCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Flow_in_Path-Traced_Mode/**/CheckBox[0]"
    _flowCategory_pathTracedModeShadowsCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Flow_in_Path-Traced_Mode_Shadows/**/CheckBox[0]"
    _flowCategory_compositeWithFLowLibraryRendererCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Composite_with_Flow_Library_Renderer/**/CheckBox[0]"
    _flowCategory_useFlowLibrarySelfShadowCheckBox = "Render Settings//Frame/**/Flow/**/HStack_Use_Flow_Library_Self_Shadow/**/CheckBox[0]"
    _flowCategory_maxBlocksSlider = "Render Settings//Frame/**/Flow/**/HStack_Max_Blocks/IntDrag[*].identifier=='/rtx/flow/maxBlocks'"

    #  Materials - Common Settings
    _materials_collapsibleFrame = "Render Settings//Frame/**/Materials"
    _materials_animationTimeOverrideFloatDrag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/animationTime'"
    )
    _materials_animationTimeUseWallclockCheckBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/animationTimeUseWallclock'"

    #  Lighting - Common Settings
    _lighting_collapsible_frame = "Render Settings//Frame/**/Lighting"
    _lighting_ShowAreaLightsInPrimaryRays_ComboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_raytracing_showLights'"
    )
    _lighting_InvisibleLightsRoughnessThreshold_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/invisLightRoughnessThreshold'"
    _lighting_ShadowBias_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/shadowBias'"
    _lighting_UseFirstDistantLightAndFirstDomeLightOnly_Checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/scenedb/skipMostLights'"
    _lighting_LightingMode_ComboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_domeLight_upperLowerStrategy'"
    _lighting_BakingResolution_ComboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_domeLight_baking_resolution'"

    #  Simple Fog - Common Settings
    _simpleFog_mainCheckBox = (
        "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/fog/enabled'"
    )
    _simpleFog_collapsibleFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Simple Fog'"
    )
    _simpleFog_intensityFloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/fog/fogColorIntensity'"
    _simpleFog_usePlusZAxisCheckBox = (
        "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/fog/fogZup/enabled'"
    )
    _simpleFog_planeHeightFloatDrag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/fog/fogStartHeight'"
    )
    _simpleFog_heightDensityFloatSlider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/fog/fogHeightDensity'"
    _simpleFog_heightFalloffFloatDrag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/fog/fogHeightFalloff'"
    )
    _simpleFog_startDistanceToCameraFloatDrag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/fog/fogStartDist'"
    )
    _simpleFog_endDistanceToCameraFloatDrag = (
        "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/fog/fogEndDist'"
    )
    _simpleFog_distanceDensityFloatSlider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/fog/fogDistanceDensity'"

    #  Global Volumetric Effects - Common Settings
    _globalVolumetricEffects_collapsibleFrame = (
        "Render Settings//Frame/**/Global Volumetric Effects"
    )
    _globalVolumetricEffects_enabled_checkBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/raytracing/globalVolumetricEffects/enabled'"
    _inscatteringTransmittanceMeasurementDistance_FloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/raytracing/inscattering/transmittanceMeasurementDistance'"
    _pathTracingFogHeightFallOff_FloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/pathtracing/ptvol/fogHeightFallOff'"
    _inscatteringMaxDistance_FloatDrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/raytracing/inscattering/maxDistance'"
    _inscatteringAnisotropyFactor_FloatDrag = "Render Settings//Frame/**/HStack_Anisotropy_Factor_(g)/FloatSlider[*].identifier=='/rtx/raytracing/inscattering/anisotropyFactor'"
    _inscatteringDensityMult_FloatSlider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/densityMult'"
    _densityNoiseSettings_CollapsableFrame = "Render Settings//Frame/**/CollapsableFrame[0].identifier=='Density Noise Settings'"
    _apply_density_noise_CheckBox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/raytracing/inscattering/useDetailNoise'"
    _pathTracingAtmosphereHeight_FloatDrag = "Render Settings//Frame/**/HStack_Fog_Height/FloatDrag[0].identifier=='/rtx/raytracing/inscattering/atmosphereHeight'"
    _densityNoise_WorldScale_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/detailNoiseScale'"
    _densityNoise_AnimationSpeedX_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/noiseAnimationSpeedX'"
    _densityNoise_AnimationSpeedY_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/noiseAnimationSpeedY'"
    _densityNoise_AnimationSpeedZ_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/noiseAnimationSpeedZ'"
    _densityNoise_ScaleMin_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/noiseScaleRangeMin'"
    _densityNoise_ScaleMax_Slider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/raytracing/inscattering/noiseScaleRangeMax'"
    _densityNoise_OctaveCount_Slider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/raytracing/inscattering/noiseNumOctaves'"

    # NVIDIA DLSS category
    _dlss_collapsibleFrame = "Render Settings//Frame/**/NVIDIA DLSS"
    _dlss_mode_comboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_dlss_execMode'"
    )
    _dlss_sharpness_floatSlider = (
        "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/aa/sharpness'"
    )
    _dlss_exposureMode_comboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_aa_autoExposureMode'"
    _dlss_exposureMultiPlier_floatSlider = "Render Settings//Frame/**/HStack____Auto_Exposure_Multiplier/FloatSlider[*].identifier=='/rtx/post/aa/exposureMultiplier'"
    _dlss_exposureFixedValue_floatSlider = (
        "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/post/aa/exposure'"
    )

    _dlss_rayReconstruction_checkBox = (
        "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/newDenoiser/enabled'"
    )
    _dlss_superResolution_comboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_aa_op'"
    )
    
    # Direct Lighting Category
    _directLightingCategory_frame = "Render Settings//Frame/**/CollapsableFrame[2]"
    _directLightingCollapsible_frame = "Render Settings//Frame/**/RTSettingStack/Direct Lighting"
    _directLightingEnabled_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/directLighting/enabled'"
    _shadows_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/shadows/enabled'"
    _sampledDirectLightingMode_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/directLighting/sampledLighting/enabled'"
    _autoEnableSampledDirectLighting_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/directLighting/sampledLighting/autoEnable'"
    _lightCountThreshold_slider = "Render Settings//Frame/**/IntDrag[0].identifier=='/rtx/directLighting/sampledLighting/autoEnableLightCountThreshold'"
    _sampledDirectLightingSettings_header = "Render Settings//Frame/**/RTSettingStack/Direct Lighting/**/CollapsableFrame[0]"
    _samplesPerPixel_combobox = "Render Settings//Frame/**/_rtx_directLighting_sampledLighting_samplesPerPixel"
    _maxRayIntensity_slider = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/directLighting/sampledLighting/maxRayIntensity'"
    _reflectionsLightSamplesPerPixel_combobox = "Render Settings//Frame/**/_rtx_reflections_sampledLighting_samplesPerPixel"
    _reflectionsMaxRayIntensity_slider = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/reflections/sampledLighting/maxRayIntensity'"
    _meshLightSampling_checkbox = "Render Settings//Frame/**/CheckBox[0].identifier=='/rtx/directLighting/sampledLighting/ris/meshLights'"
    
    # Indirect Diffuse Lighting widgets
    _ray_tracing_indirect_diffuse_lighting_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[3].identifier=='Indirect Diffuse Lighting'"
    _ray_tracing_indirect_diffuse_lighting_enabled_checkbox = "Render Settings//Frame/**/HStack_Indirect_Diffuse_GI/**/CheckBox[*]"
    _ray_tracing_indirect_diffuse_lighting_samples_per_pixel_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/indirectDiffuse/fetchSampleCount'"
    _ray_tracing_indirect_diffuse_lighting_max_bounces_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/indirectDiffuse/maxBounces'"
    _ray_tracing_indirect_diffuse_lighting_intensity_floatslider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/indirectDiffuse/scalingFactor'"
    _ray_tracing_indirect_diffuse_lighting_denoising_mode_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_indirectDiffuse_denoiser_method'"
    _ray_tracing_indirect_diffuse_lighting_kernel_radius_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/indirectDiffuse/denoiser/kernelRadius'"
    _ray_tracing_indirect_diffuse_lighting_iteration_count_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/indirectDiffuse/denoiser/iterations'"
    _ray_tracing_indirect_diffuse_lighting_max_history_length_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/indirectDiffuse/denoiser/temporal/maxHistory'"
    _ray_tracing_indirect_diffuse_lighting_max_ray_intensity_floatdrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/indirectDiffuse/maxRayIntensity'"
    _ray_tracing_indirect_diffuse_lighting_ao_enabled_checkbox = "Render Settings//Frame/**/HStack_Ambient_Occlusion/**/CheckBox[*]"
    _ray_tracing_indirect_diffuse_lighting_ao_ray_length_floatdrag = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/ambientOcclusion/rayLength'"
    _ray_tracing_indirect_diffuse_lighting_ao_min_samples_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/ambientOcclusion/minSamples'"
    _ray_tracing_indirect_diffuse_lighting_ao_max_samples_intslider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/ambientOcclusion/maxSamples'"
    _ray_tracing_indirect_diffuse_lighting_ambient_light_intensity_floatslider = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/sceneDb/ambientLightIntensity'"
    _indirectDiffuseDenoisingMode_framesInHistory_intSlider = "Render Settings//Frame/**/IntSlider[0].identifier=='/rtx/lightspeed/NRD_ReblurDiffuse/maxAccumulatedFrameNum'"
    _indirectDiffuseDenoisingMode_planeDistanceSensitivity_floatSlider_path = "Render Settings//Frame/**/FloatSlider[0].identifier=='/rtx/lightspeed/NRD_ReblurDiffuse/planeDistanceSensitivity'"
    _indirectDiffuseDenoisingMode_blurRadius_floatDrag_path = "Render Settings//Frame/**/FloatDrag[0].identifier=='/rtx/lightspeed/NRD_ReblurDiffuse/blurRadius'"

    # Locators for presets
    _reset_to_default = "Viewport//Frame/**/Menu[0]/Menu[1]/MenuItem[1]"
    _render_menu_dropdown = "Viewport//Frame/**/Menu[0]/Menu[1]"
    _preset_default = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/SelectableMenuItem[0]"
    _wireframe = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/SelectableMenuItem[1]"
    _save_preset = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/MenuItem[0]"
    _load_from_preset = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/Menu[0]"
    _preset_type_draft = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/Menu[0]/MenuItem[0]"
    _preset_type_medium = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/Menu[0]/MenuItem[1]"
    _preset_type_final = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/Menu[0]/MenuItem[2]"
    _load_preset_from_file = "Viewport//Frame/**/ZStack[3]/Frame[1]/ZStack[0]/ZStack[0]/Frame[0]/Menu[0]/Menu[1]/Menu[0]/MenuItem[3]"
    _load_preset_text_area = "Load Settings File//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _load_preset_file_name = "Load Settings File//Frame/**/Placer[0]/StringField[0]"
    _load_preset_load = "Load Settings File//Frame/**/Button[*].text=='Load'"
   
    # Locators for Save Settings model
    _save_button = "Save Settings File//Frame/**/Button[*].text=='Save'"
    _file_name_textarea = "Save Settings File//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"
    _directory_path_picker = "Save Settings File//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _overwrite_ok_button = r"__exclamation_glyph__ Overwrite//Frame/VStack[0]/HStack[1]/Button[0]"
    _save_fail_ok_btn = " Save Layer(s) Failed//Frame/VStack[0]/HStack[1]/Button[0]"
    _save_fail_label = " Save Layer(s) Failed//Frame/VStack[0]/HStack[0]/Label[0]"
    _extension_btn = "Save Settings File//Frame/VStack[0]/HStack[2]/ZStack[2]/Button[0]"
    _extension_combobox_options = "ComboBoxMenu//Frame/ZStack[0]/HStack[0]/ScrollingFrame[0]/ZStack[0]/VStack[0]/ZStack[{}]/Button[0]"
    _please_wait_window = "Please Wait"

    # Verify renderer
    _active_renderer = "Render Settings//Frame/**/ComboBox[0].name == 'renderer_choice'"

    def _change_subsurface_settings(self):
        self.find_and_scroll_element_into_view(
            self._subsurface_scattering_expand,
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        subsurface_denoiser = self.omni_driver.find_element(self._subsurface_denoiser)

        if not subsurface_denoiser.is_checked():
            subsurface_denoiser.click()
        subsurface_transmission = self.omni_driver.find_element(
            self._subsurface_transmission
        )
        if not subsurface_transmission.is_checked():
            subsurface_transmission.click()
            self.find_and_scroll_element_into_view(
                self._subsurface_transmission,
                ScrollAxis.Y,
                ScrollAmount.TOP,
                refresh=True,
            )
            subsurface_transmission_denoiser = self.omni_driver.find_element(
                self._subsure_transmission_denoiser
            )
            if not subsurface_transmission_denoiser.is_checked():
                subsurface_transmission_denoiser.click()
        self.screenshot("changed subsurface internal settings")

    def toggle_optix_denoiser(self, status: bool, change_settings: bool = False):
        """Toggles Optix Denoiser

        Args:
            status (bool): Boolean to set status of settings
            change_settings (bool, optional): Boolean to change sub-settings. Defaults to False.
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._path_tracing_options)
        denoiser_expand = self.find_and_scroll_element_into_view(
            self._denoising_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        denoiser_chkbox = self.omni_driver.find_element(self._denoising_chkbox)

        if not status:
            if denoiser_chkbox.is_checked():
                denoiser_chkbox.click()
            self.screenshot("disabled_denoising")

        elif status:
            if not denoiser_chkbox.is_checked():
                denoiser_chkbox.click()
            self.screenshot("enabled_denoising")

            if change_settings:
                if denoiser_expand.is_collapsed():
                    denoiser_expand.click()
                self.select_value_for_slider(self._denoising_blend_factor)
                self.screenshot("changed_denoising_blend_factor")

    def toggle_direct_lighting(self, status: bool):
        """Toggles Direct Lighting

        Args:
            status (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        direct_light = self.find_and_scroll_element_into_view(
            self._direct_lighting_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if direct_light.is_collapsed():
            direct_light.click()

        direct_lighting_chkbox = self.omni_driver.find_element(
            self._direct_lighting_toggle_chkbox, refresh=True
        )
        if not status:
            if direct_lighting_chkbox.is_checked():
                direct_lighting_chkbox.click()
            self.screenshot("disabled_direct_lighting")
        else:
            if not direct_lighting_chkbox.is_checked():
                direct_lighting_chkbox.click()
            self.screenshot("enabled_direct_lighting")

    def toggle_multi_gpu(self, status: bool):
        """Toggles Multi - GPU

        Args:
            status (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        multi_gpu = self.find_and_scroll_element_into_view(
            self._multi_gpu_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if multi_gpu.is_collapsed():
            multi_gpu.click()

        multi_gpu_chkbox = self.omni_driver.find_element(self._multi_gpu_toggle_chkbox)
        if not status:
            if multi_gpu_chkbox.is_checked():
                multi_gpu_chkbox.click()
            self.screenshot("disabled_multi_gpu")
        else:
            if not multi_gpu_chkbox.is_checked():
                multi_gpu_chkbox.click()
            self.screenshot("enabled_multi_gpu")

    def toggle_dome_lighting(self, enable_dome_lighting: bool):
        """Enables/disables dome lighting

        Args:
            enable_dome_lighting (bool): Boolean flag to toggle the setting
        """
        self.toggle_direct_lighting(status=True)

        self.find_and_scroll_element_into_view(
            self._dome_lighting_enable, ScrollAxis.Y, ScrollAmount.CENTER
        )
        dome = self.omni_driver.find_element(self._dome_lighting_chkbx, refresh=True)

        if enable_dome_lighting:
            if not dome.is_checked():
                dome.click()
            self.screenshot("enabled_dome_lighting")
        else:
            if dome.is_checked():
                dome.click()
            self.screenshot("disabled_dome_lighting")

    def toggle_dome_lighting_reflections(self, enable_dome_reflections_lighting: bool):
        """Enables/disables dome lighting reflections

        Args:
            enable_dome_reflections_lighting (bool): Boolean flag to toggle the setting
        """
        self.toggle_direct_lighting(status=True)
        self.toggle_dome_lighting(enable_dome_lighting=True)

        dome_reflections = self.omni_driver.find_element(
            self._dome_lighting_in_reflections_chkbx, refresh=True
        )

        if enable_dome_reflections_lighting:
            if not dome_reflections.is_checked():
                dome_reflections.click()
            self.screenshot("enabled_dome_reflections_lighting")
        else:
            if dome_reflections.is_checked():
                dome_reflections.click()
            self.screenshot("disabled_dome_reflections_lighting")

    def toggle_shadows(self, enable_shadows_options: bool):
        """Enables/disables shadows

        Args:
            enable_shadows_options (bool): Boolean flag to toggle the setting
        """
        self.toggle_direct_lighting(status=True)

        self.find_and_scroll_element_into_view(
            self._shadows_enable, ScrollAxis.Y, ScrollAmount.CENTER
        )
        shadow = self.omni_driver.find_element(self._shadows_chkbox)

        if enable_shadows_options:
            if not shadow.is_checked():
                shadow.click()
            self.screenshot("enabled_shadows")
        else:
            if shadow.is_checked():
                shadow.click()
            self.screenshot("disabled_shadows")

    def toggle_indirect_diffuse_lighting(
        self, status: bool, change_settings: bool = False
    ):
        """Toggles Indirect Diffuse Lighting

        Args:
            status (bool): Boolean to set status of settings
            change_settings (bool, optional): Boolean to change sub-settings. Defaults to False.
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        indirect_diffuse_lighting = self.find_and_scroll_element_into_view(
            self._indirect_diffuse_lighting_expand,
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        if indirect_diffuse_lighting.is_collapsed():
            indirect_diffuse_lighting.click()
        indirect_diffuse_gi_chkbox = self.omni_driver.find_element(
            self._indirect_diffuse_gi_chkbox
        )
        if not status:
            if indirect_diffuse_gi_chkbox.is_checked():
                indirect_diffuse_gi_chkbox.click()
            self.screenshot("disabled_indirect_diffused_GI")
        else:
            if not indirect_diffuse_gi_chkbox.is_checked():
                indirect_diffuse_gi_chkbox.click()
            self.screenshot("enabled_indirect_diffused_GI")
            if change_settings:
                max_history = self.find_and_scroll_element_into_view(
                    self._indirect_diffuse_gi_max_history_length_slider.rsplit("/", 1)[
                        0
                    ],
                    ScrollAxis.Y,
                    ScrollAmount.CENTER,
                )
                self.find_and_click(self._indirect_diffuse_gi_kernel_radius_slider)
                self.find_and_click(self._indirect_diffuse_gi_iteration_count_slider)
                max_history.click()
                self.screenshot("changed_indirect_diffused_GI_settings")

    def toggle_ambient_occlusion(self, status: bool, change_settings: bool = False):
        """Toggles Ambient Occlusion

        Args:
            status (bool): Boolean to set status of settings
            change_settings (bool, optional): Boolean to change sub-settings. Defaults to False.
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        indirect_diffuse_lighting = self.find_and_scroll_element_into_view(
            self._indirect_diffuse_lighting_expand,
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        if indirect_diffuse_lighting.is_collapsed():
            indirect_diffuse_lighting.click()
        ambient_occlusion_chkbox = self.omni_driver.find_element(
            self._ambient_occlusion_chkbox
        )
        if not status:
            if ambient_occlusion_chkbox.is_checked():
                ambient_occlusion_chkbox.click()
            self.screenshot("disabled_ambient_occlussion")
        else:
            if not ambient_occlusion_chkbox.is_checked():
                ambient_occlusion_chkbox.click()
            self.screenshot("enabled_ambient_occlussion")
            if change_settings:
                self.find_and_scroll_element_into_view(
                    self._ambient_occlusion_max_samples_slider.rsplit("/", 1)[
                        0
                    ],  # NOTE Need to split since scroll does not work on Sliders
                    ScrollAxis.Y,
                    ScrollAmount.CENTER,
                )
                self.select_value_for_slider(self._ambient_occlusion_ray_length_slider)
                self.select_value_for_slider(self._ambient_occlusion_min_samples_slider)
                self.select_value_for_slider(self._ambient_occlusion_max_samples_slider)
                self.screenshot("changed_ambient_occlussion_settings")

    def toggle_subsurface_scattering(self, status: bool, change_settings: bool):
        """Toggles Subsurface Scattering

        Args:
            status (bool): Boolean to set status of settings
            change_settings (bool, optional): Boolean to change sub-settings. Defaults to False.
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        subsurface_scattering = self.find_and_scroll_element_into_view(
            self._subsurface_scattering_expand,
            ScrollAxis.Y,
            ScrollAmount.TOP,
        )
        subsurface_scattering_checkbox = self.omni_driver.find_element(
            self._subsurface_scattering_chkbox
        )
        if subsurface_scattering.is_collapsed():
            subsurface_scattering.click()
        if status:
            if not subsurface_scattering_checkbox.is_checked():
                subsurface_scattering_checkbox.click()
            self.screenshot("enabled_subsurface_scattering")
        else:
            if subsurface_scattering_checkbox.is_checked():
                subsurface_scattering_checkbox.click()
            self.screenshot("disabled_subsurface_scattering")
        if change_settings:
            self._change_subsurface_settings()

    def toggle_reflections(self, status: bool):
        """Toggles Reflections

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        self.find_and_scroll_element_into_view(
            self._reflections_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        reflections_chkbox = self.omni_driver.find_element(
            self._reflections_toggle_checkbox
        )
        if not status:
            if reflections_chkbox.is_checked():
                reflections_chkbox.click()
            self.screenshot("disabled_reflections")
        else:
            if not reflections_chkbox.is_checked():
                reflections_chkbox.click()
            self.screenshot("enabled_reflections")

    def toggle_translucency(self, status: bool):
        """Toggles Transluency

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        self.find_and_scroll_element_into_view(
            self._translucency_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        translucency_chkbox = self.omni_driver.find_element(
            self._translucency_toggle_checkbox
        )
        if not status:
            if translucency_chkbox.is_checked():
                translucency_chkbox.click()
            self.screenshot("disabled_translucency")
        else:
            if not translucency_chkbox.is_checked():
                translucency_chkbox.click()
            self.screenshot("enabled_translucency")

    def toggle_depth_of_field_camera_overrides(self, status: bool):
        """Toggles depth of field camera overrides

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        self.find_and_scroll_element_into_view(
            self._depth_of_field_camera_overrides_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        depth_of_field_camera_override_chkbox = self.omni_driver.find_element(
            self._depth_of_field_camera_override_toggle_checkbox
        )
        if not status:
            if depth_of_field_camera_override_chkbox.is_checked():
                depth_of_field_camera_override_chkbox.click()
            self.screenshot("disabled_depth_of_field_camera_override")
        else:
            if not depth_of_field_camera_override_chkbox.is_checked():
                depth_of_field_camera_override_chkbox.click()
            self.screenshot("enabled_depth_of_field_camera_override")

    def toggle_depth_of_field(self, status: bool):
        """Toggles depth of field

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        depth_of_field_camera_overrides = self.find_and_scroll_element_into_view(
            self._depth_of_field_camera_overrides_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if depth_of_field_camera_overrides.is_collapsed():
            depth_of_field_camera_overrides.click()

        depth_of_field_chkbox = self.omni_driver.find_element(
            self._enable_depth_of_field_toggle_checkbox
        )
        if not status:
            if depth_of_field_chkbox.is_checked():
                depth_of_field_chkbox.click()
            self.screenshot("disabled_depth_of_field")
        else:
            if not depth_of_field_chkbox.is_checked():
                depth_of_field_chkbox.click()
            self.screenshot("enabled_depth_of_field")

    def toggle_fft_bloom(self, status: bool):
        """Toggles FFT bloom

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        fft_bloom = self.find_and_scroll_element_into_view(
            self._fft_bloom_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if fft_bloom.is_collapsed():
            fft_bloom.click()
        fft_bloom_chkbox = self.omni_driver.find_element(
            self._fft_bloom_toggle_checkbox
        )
        if not status:
            if fft_bloom_chkbox.is_checked():
                fft_bloom_chkbox.click()
            self.screenshot("disabled_fft_bloom")
        else:
            if not fft_bloom_chkbox.is_checked():
                fft_bloom_chkbox.click()
            self.screenshot("enabled_fft_bloom")

    def change_DOF_settings(self):
        """Changes internal Depth of field settings to random values"""

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        depth_of_field_camera_overrides = self.find_and_scroll_element_into_view(
            self._depth_of_field_camera_overrides_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if depth_of_field_camera_overrides.is_collapsed():
            depth_of_field_camera_overrides.click()
        self.select_value_for_slider(self._subject_distance_slider)
        self.select_value_for_slider(self._focal_length_slider)
        self.select_value_for_slider(self._f_stop_slider)
        self.select_value_for_slider(self._anisotropy_slider)

    def reset_DOF_settings(self):
        """Resets all Depth of Field internal settings to default"""

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        depth_of_field_camera_overrides = self.find_and_scroll_element_into_view(
            self._depth_of_field_camera_overrides_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if depth_of_field_camera_overrides.is_collapsed():
            depth_of_field_camera_overrides.click()
        subject_distance_slider_reset = self.omni_driver.find_element(
            self._subject_distance_slider_reset
        )
        subject_distance_slider_reset.click()

        focal_length_slider_reset = self.omni_driver.find_element(
            self._focal_length_slider_reset
        )
        focal_length_slider_reset.click()

        f_stop_slider_reset = self.omni_driver.find_element(self._f_stop_slider_reset)
        f_stop_slider_reset.click()

        anisotropy_slider_reset = self.omni_driver.find_element(
            self._anisotropy_slider_reset
        )
        anisotropy_slider_reset.click()

    def toggle_motion_blur(self, status: bool):
        """Toggles Motion Blur

        Args:
            staus (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        motion_blur = self.find_and_scroll_element_into_view(
            self._motion_blur_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if motion_blur.is_collapsed():
            motion_blur.click()
        motion_blur_checkbox = self.omni_driver.find_element(
            self._motion_blur_toggle_checkbox
        )
        if not status:
            if motion_blur_checkbox.is_checked():
                motion_blur_checkbox.click()
            self.screenshot("disabled_motion_blur")
        else:
            if not motion_blur_checkbox.is_checked():
                motion_blur_checkbox.click()
            self.screenshot("enabled_motion_blur")

    def change_motion_blur_settings(self):
        """Changes internal Motion Blur settings to random values"""

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        motion_blur = self.find_and_scroll_element_into_view(
            self._motion_blur_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if motion_blur.is_collapsed():
            motion_blur.click()
        self.select_value_for_slider(self._blur_diameter_fraction_slider)
        self.select_value_for_slider(self._exposure_fraction_slider)
        self.select_value_for_slider(self._no_of_samples_slider)

    def reset_motion_blur_settings(self):
        """Resets all Motion Blur internal settings to default"""

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        motion_blur = self.find_and_scroll_element_into_view(
            self._motion_blur_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if motion_blur.is_collapsed():
            motion_blur.click()

        blur_diameter_fraction_reset = self.omni_driver.find_element(
            self._blur_diameter_fraction_reset
        )
        blur_diameter_fraction_reset.click()

        exposure_fraction_reset = self.omni_driver.find_element(
            self._exposure_fraction_reset
        )
        exposure_fraction_reset.click()

        no_of_samples_reset = self.omni_driver.find_element(self._no_of_samples_reset)
        no_of_samples_reset.click()

    def change_fft_bloom_settings(self, physical_model: bool, energy_constraint: bool):
        """Changes internal Motion Blur settings to random values

        Args:
            physical_model (bool): Toggle to enable or disable physical model setting
            energy_constraint (bool): Toggle to enable or disable energy constraint setting
        """

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        fft_bloom = self.find_and_scroll_element_into_view(
            self._fft_bloom_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if fft_bloom.is_collapsed():
            fft_bloom.click()

        self.select_value_for_slider(self._scale_slider)
        self.select_value_for_slider(self._cutoff_fuzziness_slider)

        if energy_constraint:
            self.find_and_click(self._energy_constrained_checkbox)

        physical_model_chkbox = self.omni_driver.find_element(
            self._physical_model_chkbox
        )
        if physical_model:
            if not physical_model_chkbox.is_checked():
                physical_model_chkbox.click()
            focal_length_chkbox_element = self.find_and_scroll_element_into_view(
                self._focal_length_slider.replace("/FloatDrag[0]", ""),
                ScrollAxis.Y,
                ScrollAmount.TOP,
            )
            self.select_value_for_slider(self._blades_slider)
            self.select_value_for_slider(self._aperture_rotation)
            self.select_value_for_slider(self._sensor_diagonal_slider)
            self.select_value_for_slider(self._sensor_aspect_ratio_slider)
            self.select_value_for_slider(self._f_stop_slider)
            focal_length_chkbox_element.click()
        else:
            if physical_model_chkbox.is_checked():
                physical_model_chkbox.click()

    def reset_fft_bloom_settings(
        self, reset_physical_model: bool, reset_energy_constraint: bool
    ):
        """Resets all fft bloom internal settings to default

        Args:
            reset_physical_model (bool): Reset physical model or not
            reset_energy_constraint (bool): Reset energy constraint or not
        """

        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)
        fft_bloom = self.find_and_scroll_element_into_view(
            self._fft_bloom_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if fft_bloom.is_collapsed():
            fft_bloom.click()

        if reset_physical_model:
            physical_model_chkbox = self.omni_driver.find_element(
                self._physical_model_chkbox
            )
            if not physical_model_chkbox.is_checked():
                physical_model_chkbox.click()

        if reset_energy_constraint:
            energy_constraint_chkbox = self.omni_driver.find_element(
                self._energy_constrained_checkbox
            )
            if energy_constraint_chkbox.is_checked():
                energy_constraint_chkbox.click()

        self.find_and_click(self._scale_reset)
        self.find_and_click(self._cutoff_fuzziness_reset)
        self.find_and_click(self._energy_constrained_reset)
        self.find_and_click(self._blades_slider_reset)
        self.find_and_click(self._aperture_rotation_reset)
        self.find_and_click(self._sensor_diagonal_slider_reset)
        self.find_and_click(self._sensor_aspect_ratio_slider_reset)
        self.find_and_click(self._f_stop_slider_reset)
        self.find_and_click(self._focal_length_slider_reset)

    def toggle_frame_generation(self, status: bool):
        """Toggles NVIDIA DLSS Frame Generation

        Args:
            status (bool): Boolean to set status of settings
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        dlss_collapse = self.find_and_scroll_element_into_view(
            self._dlss_collapsebar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if dlss_collapse.is_collapsed():
            dlss_collapse.click()

        frame_generator_chkbox = self.omni_driver.find_element(
            self._frame_generator_toggle_chkbox
        )
        if not status:
            if frame_generator_chkbox.is_checked():
                frame_generator_chkbox.click()
            self.screenshot("disabled_frame_generation")
        else:
            if not frame_generator_chkbox.is_checked():
                frame_generator_chkbox.click()
            self.screenshot("enabled_frame_generation")

    def change_dlss_modes(self, mode: DlssModesRenderSettings):
        """DLSS Modes selection

        Args:
            mode (DlssModesRenderSettings): Mode to be selected
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        dlss_collapse = self.find_and_scroll_element_into_view(
            self._dlss_collapsebar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if dlss_collapse.is_collapsed():
            dlss_collapse.click()
        self.select_item_from_stack_combo_box(self._dlss_mode_combobox, mode.value)

    def toggle_sampled_direct_lighting(self, enable_sampled_direct_lighting: bool):
        """Enables/disables sampled direct lighting

        Args:
            enable_sampled_direct_lighting (bool): Boolean flag to toggle the setting
        """
        self.toggle_direct_lighting(status=True)

        self.find_and_scroll_element_into_view(
            self._direct_sampled_lighting_stack,
            ScrollAxis.Y,
            ScrollAmount.CENTER,
            refresh=True,
        )
        sampled_lighting = self.omni_driver.find_element(
            self._direct_sampled_lighting_chkbox, refresh=True
        )

        if enable_sampled_direct_lighting:
            if not sampled_lighting.is_checked():
                sampled_lighting.click()
            self.screenshot("enabled_sampled_direct_lighting")
        else:
            if sampled_lighting.is_checked():
                sampled_lighting.click()
            self.screenshot("disabled_sampled_direct_lighting")

    def toggle_non_uniform_volumes(self, enable: bool):
        """Enables/disables non uniform volumes

        Args:
            enable (bool): Boolean flag to toggle the setting
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._path_tracing_options)
        collapse_bar = self.find_and_scroll_element_into_view(
            self._non_uniform_vol_collapse_bar, ScrollAxis.Y, ScrollAmount.CENTER
        )
        chkbox = self.omni_driver.find_element(self._non_uniform_vol_checkbox)

        if collapse_bar.is_collapsed():
            collapse_bar.click()

        if enable:
            if not chkbox.is_checked():
                chkbox.click()
            self.screenshot("enabled_non_uniform_volumes")
        else:
            if chkbox.is_checked():
                chkbox.click()
            self.screenshot("disabled_non_uniform_volumes")

    def change_max_ligh_collision_count(self):
        """Changes value for max collision count in non uniform volumes"""

        self.toggle_non_uniform_volumes(enable=True)

        self.find_and_scroll_element_into_view(
            self._non_uniform_vol_max_collision_stack, ScrollAxis.Y, ScrollAmount.CENTER
        )
        self.select_value_for_slider(self._non_uniform_vol_max_collision_drag, 1024)
        self.screenshot("changed_value_of_max_collision_count")

    def set_iray_device_settings(
        self, cpu: bool, gpu: bool, enable_specific_gpu: list = []
    ):
        """Sets the CPU & GPU device settings for IRAY

        Args:
            cpu (bool): Flag to set CPU settings
            gpu (bool): Flag to set GPU settings
            enable_specific_gpu list(bool): Flag to set specific GPU settings. If provided,
            it will override gpu parameter. If index is not provided, it will default to False.
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._iray_options)
        device_settings_collapse = self.find_and_scroll_element_into_view(
            self._device_settings_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP
        )

        if device_settings_collapse.is_collapsed():
            device_settings_collapse.click()

        all_checkboxes = self.omni_driver.find_elements(
            self._device_settings_all_chkboxes
        )

        if not cpu:
            if all_checkboxes[0].is_checked():
                all_checkboxes[0].click()
        else:
            if not all_checkboxes[0].is_checked():
                all_checkboxes[0].click()

        for index, checkbox in enumerate(all_checkboxes[1:]):
            if enable_specific_gpu:
                index_exists = len(enable_specific_gpu) > index
                if index_exists:
                    gpu = enable_specific_gpu[index]
                else:
                    self.log.info("Index not found. Defaulting to False.")
                    gpu = False
            if not gpu:
                if checkbox.is_checked():
                    checkbox.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retry = 4
                while checkbox.is_checked() and retry > 0:
                    checkbox.click()
                    self.omni_driver.wait(1)
                    retry -= 1
            else:
                if not checkbox.is_checked():
                    checkbox.click()
                # TODO: Remove retry steps after click issue is resolved: OM-102905
                retry = 4
                while not checkbox.is_checked() and retry > 0:
                    checkbox.click()
                    self.omni_driver.wait(1)
                    retry -= 1
        self.screenshot("changed_iray_device_settings")

    def navigate_to_lighting(self):
        """Navigates to Lighting option in Common under Render Settings"""
        self.find_and_click(locator=self._render_settings_window)
        self.find_and_click(locator=self._common_btn)
        lighting_collapse = self.find_and_scroll_element_into_view(
            self._lighting_collapsebar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if lighting_collapse.is_collapsed():
            self.log.info("Light collapse bar is collapsed")
            lighting_collapse.click()
        else:
            self.log.info("Light collapse bar is not collapsed")
        light_visibility_collapsebar = self.find_and_scroll_element_into_view(
            self._light_visibility_settings_collapsebar, ScrollAxis.Y, ScrollAmount.TOP
        )
        if light_visibility_collapsebar.is_collapsed():
            self.log.info("Light visibility collapse bar is collapsed")
            light_visibility_collapsebar.click()
        else:
            self.log.info("Light visibility collapse bar is not collapsed")
        self.find_and_scroll_element_into_view(
            self._commonsetting_lighting, ScrollAxis.Y, ScrollAmount.CENTER
        )

    def check_light_roughness(self):
        """Changes the value of Invisible Lights Roughness Threshold"""

        self.select_value_for_slider(self._lighting_roughness_slider)

    def navigate_to_iray_render_settings(self):
        """Navigates to Render settings under Accurate (Iray)"""

        render_settings_collapse = self.find_and_scroll_element_into_view(
            self._render_settings, ScrollAxis.Y, ScrollAmount.TOP
        )
        if render_settings_collapse.is_collapsed():
            self.log.info("Render Settings collapse bar is collapsed")
            render_settings_collapse.click()
        else:
            self.log.info("Render Settings collapse bar is not collapsed")
        self.log.info("Navigated to Iray Render Settings.")

    def change_canvas_settings_for_iray(self, canvas_index: int = 0):
        """Changes Canvas Settings under Iray render settings"""

        self.navigate_to_iray_render_settings()
        self.wait.element_to_be_located(self.omni_driver, self._render_settings)
        self.select_item_from_stack_combo_box(
            self._canvas_setting_combo_box, index=canvas_index
        )
        self.log.info("Changed canvas setting successfully")
        self.screenshot("canvas_setting_changed")

    def enable_denoiser(self):
        """Enables denoiser for Iray render settings"""

        denoiser_enable_chkbox = self.omni_driver.find_element(self._denoiser_chkbox)
        if not denoiser_enable_chkbox.is_checked():
            denoiser_enable_chkbox.click()
        self.omni_driver.wait_for_stage_load()
        self.log.info("Enabled deboiser")
        self.screenshot("enabled_denoising")

    def enable_caustic_sampler(self):
        """Enables Caustic sampler for Iray render settings"""

        caustic_sampler_enable_chkbox = self.omni_driver.find_element(
            self._caustic_sampler_chkbox
        )
        if not caustic_sampler_enable_chkbox.is_checked():
            caustic_sampler_enable_chkbox.click()
        self.omni_driver.wait_for_stage_load()
        self.log.info("Enables caustic sampler")
        self.screenshot("enabled_caustic_sampler")

    def change_light_visibility(self):
        """Changes light visibility to Per - Light Enable, Force Enable and Force disable under Iray render settings"""

        self.select_item_from_stack_combo_box(self._lighting_visible_combo_box, index=0)
        self.wait.element_to_be_located(
            self.omni_driver, self._lighting_visible_combo_box
        )
        self.log.info("Light visibility is changed to 'Per light enable'")
        self.screenshot("Per_light_enable")
        self.select_item_from_stack_combo_box(self._lighting_visible_combo_box, index=1)
        self.wait.element_to_be_located(
            self.omni_driver, self._lighting_visible_combo_box
        )
        self.log.info("Light visibility is changed to 'force enable'")
        self.screenshot("force_enable")
        self.select_item_from_stack_combo_box(self._lighting_visible_combo_box, index=2)
        self.wait.element_to_be_located(
            self.omni_driver, self._lighting_visible_combo_box
        )
        self.log.info("Light visibility is changed to 'force disable")
        self.screenshot("force_disable")

    def toggle_denoise_aov(self, status: bool):
        """Toggle denoise AOV in render settings

        Args:
            status (bool): _description_
        """
        denoiser_expand = self.find_and_scroll_element_into_view(
            self._denoising_expand, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        denoise_aov_checkbox = self.omni_driver.find_element(
            self._denoise_aov_checkbox, True
        )
        if denoiser_expand.is_collapsed():
            denoiser_expand.click()
        if status:
            if not denoise_aov_checkbox.is_checked():
                denoise_aov_checkbox.click()
            self.screenshot("denoise_aov_checked")
        else:
            if denoise_aov_checkbox.is_checked():
                denoise_aov_checkbox.click()
            self.screenshot("denoise_aov_unchecked")

    def change_samples_per_pixel(self, num: int):
        """Changes samples per pixel in path traced settings

        Args:
            num (int): no of sample per pixel

        """
        path_traced_expand = self.find_and_scroll_element_into_view(
            self._path_traced_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        samples_per_pixel = self.omni_driver.find_element(self._samples_per_pixel_drag)
        if path_traced_expand.is_collapsed():
            path_traced_expand.click()
        samples_per_pixel.send_keys(str(num))
        self.log.info(f"changed samples per pixel to {num}")
        self.screenshot("changed_samples_per_pixel")

    def toggle_aov_direct_illumination(self, status: bool):
        """Toggles direct illumination in AOV settings

        Args:
            status (bool): status of direct illumination
        """
        aov_expand = self.find_and_scroll_element_into_view(
            self._aov_expand, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        if aov_expand.is_collapsed():
            aov_expand.click()
        aov_expand = self.find_and_scroll_element_into_view(
            self._aov_expand, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        direct_illumination = self.find_and_scroll_element_into_view(
            self._direct_illumination, ScrollAxis.Y, ScrollAmount.TOP, refresh=True
        )
        if status:
            if not direct_illumination.is_checked():
                direct_illumination.click()
            self.screenshot("direct_illumination_aov_checked")
        else:
            if direct_illumination.is_checked():
                direct_illumination.click()
            self.screenshot("direct_illumination_aov_unchecked")

    def get_debug_view_renderer(self):
        """Returns renderer result from debug view"""
        self.find_and_click(locator=self._render_settings_window)
        self.find_and_click(locator=self._common_btn)
        debug_view_expand = self.find_and_scroll_element_into_view(
            self._debug_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        if debug_view_expand.is_collapsed():
            debug_view_expand.click()
        debug_view_expand = self.find_and_scroll_element_into_view(
            self._debug_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        render_result = self.omni_driver.find_element(self._render_target).get_text()
        return render_result

    # RTX Methods
    def _ensure_tone_mapping_expanded(self):
        """Ensures the Tone Mapping collapsible frame is expanded before interacting with its widgets."""
        self.expand_collapsible_frame(self._tone_mapping_collapsible_frame)

    def select_tone_mapping_operator(self, name):
        """Selects an operator in the Tone Mapping settings by name after expanding the collapsible frame.

        Args:
            name (str): The name of the operator to select.
        """
        self._ensure_tone_mapping_expanded()
        self.select_item_by_name_from_combo_box(
            self._tone_mapping_operator_combo_box, name
        )

    def select_tone_mapping_color_space(self, name):
        """Selects an color space in the Tone Mapping settings by name after expanding the collapsible frame.

        Args:
            name (str): The name of the operator to select.
        """
        self._ensure_tone_mapping_expanded()
        self.select_item_by_name_from_combo_box(self._tone_mapping_color_space, name)

    def toggle_tone_mapping_srgb_to_gamma_conversion(self, check=True):
        """Toggles the SRGB to Gamma conversion checkbox in Tone Mapping settings after expanding the collapsible frame.

        Args:
            check (bool, optional): Desired state of the checkbox. Defaults to True.
        """
        self._ensure_tone_mapping_expanded()
        self.toggle_checkbox(
            self._tone_mapping_srgb_to_gamma_conversion_check_box, check
        )

    def set_tone_mapping_cm2_factor(self, value):
        """Sets the CM2 Factor in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_cm2_factor_slider, value)

    def set_tone_mapping_film_iso(self, value):
        """Sets the Film ISO in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_film_iso_drag, value)

    def set_tone_mapping_camera_shutter(self, value):
        """Sets the Camera Shutter speed in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_camera_shutter_drag, value)

    def set_tone_mapping_fstop(self, value):
        """Sets the F-Stop in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_fstop_slider, value)

    def set_tone_mapping_white_point_color(self, value):
        """Sets the White Point color in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (tuple): The color value to set for the White Point color widget.

        Note:
            This method is a placeholder and should be implemented with the correct interaction logic.
        """
        self._ensure_tone_mapping_expanded()
        raise NotImplementedError("Setting White Point color is not implemented.")

    def set_tone_mapping_wrap_value(self, value):
        """Sets the Wrap Value in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_wrap_value_drag, value)

    def set_tone_mapping_dither_strength(self, value):
        """Sets the Dither Strength in the Tone Mapping settings after expanding the collapsible frame.

        Args:
            value (float): The value to set on the slider.
        """
        self._ensure_tone_mapping_expanded()
        self.set_slider_value(self._tone_mapping_dither_strength_slider, value)

    def navigate_to_post_processing_options(self):
        """Find and clicks on the post processing option"""
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._post_processing_options)

    def _toggle_auto_exposure_enabled(self, check=True):
        """Expands the auto exposure collapsable frame and toggles the auto exposure enabled checkbox.

        Args:
            check (bool): True to enable auto exposure, False to disable.
        """
        self.expand_collapsible_frame(self._auto_exposure_collapsable_frame)
        self.toggle_checkbox(self._auto_exposure_enabled, check)

    def set_auto_exposure_adaptation_speed(self, value):
        """Sets the adaptation speed value for auto exposure, ensuring the category is expanded and enabled.

        Args:
            value (float): The value to set on the adaptation speed slider.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.set_slider_value(self._auto_exposure_adaptation_speed, value)

    def set_auto_exposure_white_point_scale(self, value):
        """Sets the white point scale value for auto exposure, ensuring the category is expanded and enabled.

        Args:
            value (float): The value to set on the white point scale slider.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.set_slider_value(self._auto_exposure_white_point_scale, value)

    def set_auto_exposure_min_value(self, value):
        """Sets the minimum exposure value for auto exposure, ensuring the category is expanded and enabled.

        Args:
            value (float): The value to set on the minimum exposure value field.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.set_slider_value(self._auto_exposure_min_value, value)

    def set_auto_exposure_max_value(self, value):
        """Sets the maximum exposure value for auto exposure, ensuring the category is expanded and enabled.

        Args:
            value (float): The value to set on the maximum exposure value field.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.set_slider_value(self._auto_exposure_max_value, value)

    def toggle_auto_exposure_value_clamping(self, check=True):
        """Toggles the exposure value clamping checkbox for auto exposure, ensuring the category is expanded and enabled.

        Args:
            check (bool): True to enable exposure value clamping, False to disable.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.toggle_checkbox(self._auto_exposure_value_clamping, check)

    def select_auto_exposure_histogram_filter_type(self, name):
        """Selects a filter type from the histogram filter type combobox for auto exposure, ensuring the category is expanded and enabled.

        Args:
            name (str): The name of the filter type to select.

        Raises:
            ValueError: If the name is not an option in the combobox.
        """
        self._toggle_auto_exposure_enabled(check=True)
        self.select_item_by_name_from_combo_box(
            self._auto_exposure_histogram_filter_type, name
        )

    def _toggle_color_correction_enabled(self, check=True):
        """Expands the Color correction collapsable frame and toggles the auto exposure enabled checkbox.

        Args:
            check (bool): True to enable auto exposure, False to disable.
        """
        self.expand_collapsible_frame(self._color_correction_collapsable_frame)
        self.toggle_checkbox(self._color_correction_enable_checkbox, check)

    def set_color_correction_output_color_space(self, color_space_name):
        """Sets the output color space in the Color Correction settings.

        Args:
            color_space_name (str): The name of the color space to select in the combobox.

        Raises:
            ValueError: If the color space name is not an option in the combobox.
        """
        self._toggle_color_correction_enabled()
        self.select_item_by_name_from_combo_box(
            self._color_correction_output_color_space_combobox, color_space_name
        )

    def set_color_correction_mode(self, mode_name):
        """Sets the mode in the Color Correction settings.

        Args:
            mode_name (str): The name of the mode to select in the combobox.

        Raises:
            ValueError: If the mode name is not an option in the combobox.
        """
        self._toggle_color_correction_enabled()
        self.select_item_by_name_from_combo_box(self._color_correction_mode, mode_name)

    def _toggle_color_grading_enabled(self, check=True):
        """Expands the Color Grading collapsible frame and toggles the color grading enabled checkbox.

        Args:
            check (bool): True to enable color grading, False to disable.
        """
        self.expand_collapsible_frame(self._color_grading_collapsible_frame)
        self.toggle_checkbox(self._color_grading_main_checkbox, check)

    def set_color_grading_mode(self, mode_name):
        """Sets the color grading mode in the Render Settings.

        Args:
            mode_name (str): The name of the color grading mode to select in the combobox.

        Raises:
            ValueError: If the mode name is not an option in the combobox.
        """
        self._toggle_color_grading_enabled()
        self.select_item_by_name_from_combo_box(
            self._color_grading_mode_combobox, mode_name
        )

    def set_color_grading_output_color_space(self, color_space_name):
        """Sets the color grading output color space in the Render Settings.

        Args:
            color_space_name (str): The name of the output color space to select in the combobox.

        Raises:
            ValueError: If the color space name is not an option in the combobox.
        """
        self._toggle_color_grading_enabled()
        self.select_item_by_name_from_combo_box(
            self._color_grading_output_space_combobox, color_space_name
        )

    def _toggle_xr_compositing_frame_enabled(self, check=True):
        """Expands and toggles the XR Compositing to access its settings."""
        self.expand_collapsible_frame(self._xr_compositing_collapsible_frame)
        self.toggle_checkbox(self._xr_compositing_enabled_checkbox, check)

    def toggle_composite_in_editor(self, check=True):
        """Toggles the Composite In Editor checkbox.

        Args:
            check (bool): True to enable compositing in editor, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(self._xr_compositing_composite_in_editor_checkbox, check)

    def toggle_output_alpha_composited_image(self, check=True):
        """Toggles the Output Alpha Composited Image checkbox.

        Args:
            check (bool): True to enable outputting alpha composited image, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(
            self._xr_compositing_output_alpha_composited_image_checkbox, check
        )

    def toggle_output_black_background_composited_image(self, check=True):
        """Toggles the Output Black Background Composited Image checkbox.

        Args:
            check (bool): True to enable outputting black background composited image, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(
            self._xr_compositing_output_black_background_composited_image_checkbox,
            check,
        )

    def toggle_multiply_color_value_by_alpha_composite(self, check=True):
        """Toggles the Multiply Color Value by Alpha Composite checkbox.

        Args:
            check (bool): True to enable multiplying color value by alpha in composite, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(
            self._xr_compositing_multiply_color_value_by_alpha_composite_checkbox, check
        )

    def toggle_convert_refraction_to_opacity(self, check=True):
        """Toggles the Convert Refraction to Opacity checkbox.

        Args:
            check (bool): True to enable conversion of refraction to opacity, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(
            self._xr_compositing_convert_refraction_to_opacity_checkbox, check
        )

    def toggle_enable_lens_distortion_correction(self, check=True):
        """Toggles the Enable Lens Distortion Correction checkbox.

        Args:
            check (bool): True to enable lens distortion correction, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        self.toggle_checkbox(
            self._xr_compositing_enable_lens_distortion_correction_checkbox, check
        )

    def _toggle_matte_object_enabled(self, check=True):
        """Expands and Toggles the Matte Object setting within the Matte Object collapsible frame.

        Args:
            check (bool): True to enable Matte Object, False to disable.
        """

        self.expand_collapsible_frame(self._matte_object_collapsable_frame)
        self.toggle_checkbox(self._matte_object_main_checkbox, check)

    def toggle_matte_object_shadow_catcher(self, check=True):
        """Toggles the Shadow Catcher setting within the Matte Object collapsible frame.

        Args:
            check (bool): True to enable Shadow Catcher, False to disable.
        """
        self._toggle_matte_object_enabled()
        self.toggle_checkbox(self._matte_object_shadow_catcher_checkbox, check)

    def _toggle_chromatic_aberration_enabled(self, check=True):
        """Expands the Chromatic Aberration collapsible frame and toggles the chromatic aberration enabled checkbox.

        Args:
            check (bool): True to enable chromatic aberration, False to disable.
        """
        self.expand_collapsible_frame(self._chromatic_aberration_collapsible_frame)
        self.toggle_checkbox(self._chromatic_aberration_enabled, check)

    def set_chromatic_aberration_strength_red(self, value):
        """Sets the strength red slider value for chromatic aberration.

        Args:
            value (float): The value to set on the strength red slider.
        """
        self._toggle_chromatic_aberration_enabled()
        self.set_slider_value(self._chromatic_aberration_strength_red_slider, value)

    def set_chromatic_aberration_strength_green(self, value):
        """Sets the strength green slider value for chromatic aberration.

        Args:
            value (float): The value to set on the strength green slider.
        """
        self._toggle_chromatic_aberration_enabled()
        self.set_slider_value(self._chromatic_aberration_strength_green_slider, value)

    def set_chromatic_aberration_strength_blue(self, value):
        """Sets the strength blue slider value for chromatic aberration.

        Args:
            value (float): The value to set on the strength blue slider.
        """
        self._toggle_chromatic_aberration_enabled()
        self.set_slider_value(self._chromatic_aberration_strength_blue_slider, value)

    def select_chromatic_aberration_algorithm_red(self, algorithm_name):
        """Selects the algorithm for red component in chromatic aberration from the dropdown.

        Args:
            algorithm_name (str): The name of the algorithm to select for the red component.
        """
        self._toggle_chromatic_aberration_enabled()
        self.select_item_by_name_from_combo_box(
            self._chromatic_aberration_algorithm_red_combobox, algorithm_name
        )

    def select_chromatic_aberration_algorithm_green(self, algorithm_name):
        """Selects the algorithm for green component in chromatic aberration from the dropdown.

        Args:
            algorithm_name (str): The name of the algorithm to select for the green component.
        """
        self._toggle_chromatic_aberration_enabled()
        self.select_item_by_name_from_combo_box(
            self._chromatic_aberration_algorithm_green_combobox, algorithm_name
        )

    def select_chromatic_aberration_algorithm_blue(self, algorithm_name):
        """Selects the algorithm for blue component in chromatic aberration from the dropdown.

        Args:
            algorithm_name (str): The name of the algorithm to select for the blue component.
        """
        self._toggle_chromatic_aberration_enabled()
        self.select_item_by_name_from_combo_box(
            self._chromatic_aberration_algorithm_blue_combobox, algorithm_name
        )

    def _toggle_chromatic_aberration_lanczos_sampler(self, check=True):
        """Toggles the Lanczos sampler checkbox for chromatic aberration.

        Args:
            check (bool): True to enable the Lanczos sampler, False to disable.
        """
        self._toggle_chromatic_aberration_enabled()
        self.toggle_checkbox(self._chromatic_aberration_lanczos_sampler_checkbox, check)

    def _expand_chromatic_aberration_boundary_blending(self):
        """Expands the Boundary Blending collapsible frame inside Chromatic Aberration."""
        self._toggle_chromatic_aberration_enabled()
        self.expand_collapsible_frame(
            self._chromatic_aberration_boundary_blending_collapsible_frame
        )

    def toggle_chromatic_aberration_repeat_mirrored(self, check=True):
        """Toggles the Repeat Mirrored checkbox within Boundary Blending of chromatic aberration.

        Args:
            check (bool): True to enable Repeat Mirrored, False to disable.
        """
        self._expand_chromatic_aberration_boundary_blending()
        self.toggle_checkbox(self._chromatic_aberration_repeat_mirrored_checkbox, check)

    def set_chromatic_aberration_blend_region_size(self, value):
        """Sets the blend region size slider value within Boundary Blending of chromatic aberration.

        Args:
            value (float): The value to set on the blend region size slider.
        """
        self._expand_chromatic_aberration_boundary_blending()
        self.set_slider_value(
            self._chromatic_aberration_blend_region_size_slider, value
        )

    def set_chromatic_aberration_blend_region_falloff(self, value):
        """Sets the blend region falloff slider value within Boundary Blending of chromatic aberration.

        Args:
            value (float): The value to set on the blend region falloff slider.
        """
        self._expand_chromatic_aberration_boundary_blending()
        self.set_slider_value(
            self._chromatic_aberration_blend_region_falloff_slider, value
        )

    def _toggle_depth_of_field_enabled(self, check=True):
        """Toggles the Depth of Field enabled checkbox within the collapsible frame.

        Args:
            check (bool): True to enable Depth of Field, False to disable.
        """
        self.expand_collapsible_frame(self._depth_of_field_collapsible_frame)
        self.toggle_checkbox(self._depthOfField_overrideCheckbox, check)
        self.toggle_checkbox(self._depth_of_field_enable_checkbox, check)

    def set_depth_of_field_subject_distance(self, value):
        """Sets the subject distance value for Depth of Field.

        Args:
            value (float): The value to set for the subject distance.
        """
        self._toggle_depth_of_field_enabled(check=True)
        self.set_slider_value(self._depth_of_field_subject_distance_slider, value)

    def set_depth_of_field_focal_length(self, value):
        """Sets the focal length value for Depth of Field.

        Args:
            value (float): The value to set for the focal length.
        """
        self._toggle_depth_of_field_enabled(check=True)
        self.set_slider_value(self._depth_of_field_focal_length_slider, value)

    def set_depth_of_field_f_stop(self, value):
        """Sets the f-stop value for Depth of Field.

        Args:
            value (float): The value to set for the f-stop.
        """
        self._toggle_depth_of_field_enabled(check=True)
        self.set_slider_value(self._depth_of_field_f_stop_slider, value)

    def set_depth_of_field_anisotropy(self, value):
        """Sets the anisotropy value for Depth of Field.

        Args:
            value (float): The value to set for anisotropy.
        """
        self._toggle_depth_of_field_enabled(check=True)
        self.set_slider_value(self._depth_of_field_anisotropy_slider, value)

    def _toggle_motion_blur_settings_enabled(self, check=True):
        """Toggles the Motion Blur settings by expanding the collapsible frame and enabling/disabling the checkbox.

        Args:
            check (bool): True to enable Motion Blur, False to disable.
        """
        self.expand_collapsible_frame(self._motion_blur_collapsible_frame)
        self.toggle_checkbox(self._motion_blur_enabled_checkbox, check)

    def set_motion_blur_diameter_fraction(self, value):
        """Sets the Motion Blur diameter fraction slider to the specified value.

        Args:
            value (float): The value to set on the diameter fraction slider.
        """
        self._toggle_motion_blur_settings_enabled(check=True)
        self.set_slider_value(self._motion_blur_diameter_fraction_slider, value)

    def set_motion_blur_exposure_fraction(self, value):
        """Sets the Motion Blur exposure fraction slider to the specified value.

        Args:
            value (float): The value to set on the exposure fraction slider.
        """
        self._toggle_motion_blur_settings_enabled(check=True)
        self.set_slider_value(self._motion_blur_exposure_fraction_slider, value)

    def set_motion_blur_number_of_samples(self, value):
        """Sets the Motion Blur number of samples slider to the specified value.

        Args:
            value (int): The value to set on the number of samples slider.
        """
        self._toggle_motion_blur_settings_enabled(check=True)
        self.set_slider_value(self._motion_blur_number_of_samples_slider, value)

    def _toggle_tv_noise_film_grain(self, check=True):
        """Expands and Toggles the TV Noise & Film Grain setting.

        Args:
            check (bool): Desired state of the TV Noise & Film Grain setting.
        """
        self.expand_collapsible_frame(self._tv_noise_film_grain_collapsable_frame)
        self.toggle_checkbox(self._tv_noise_enable_checkbox, check)

    def toggle_tv_noise_random_splotches(self, check=True):
        """Toggles the Random Splotches setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Random Splotches setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(
            self._tv_noise_film_grain_enable_random_splotches_checkbox, check
        )

    def toggle_tv_noise_vertical_lines(self, check=True):
        """Toggles the Vertical Lines setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Vertical Lines setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(
            self._tv_noise_film_grain_enable_vertical_lines_checkbox, check
        )

    def toggle_tv_noise_wavy_distortion(self, check=True):
        """Toggles the Wavy Distortion setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Wavy Distortion setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(
            self._tv_noise_film_grain_enable_wavy_distortion_checkbox, check
        )

    def toggle_tv_noise_ghost_flickering(self, check=True):
        """Toggles the Ghost Flickering setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Ghost Flickering setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(
            self._tv_noise_film_grain_enable_ghost_flickering_checkbox, check
        )

    def _toggle_tv_noise_vignetting_enable(self, check=True):
        """Toggles the Vignetting setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Vignetting setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(self._tv_noise_vignettingEnableCheckbox, check)

    def toggle_tv_noise_vignetting_flickering(self, check=True):
        """Toggles the Vignetting Flickering setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Vignetting Flickering setting.
        """
        self._toggle_tv_noise_vignetting_enable()
        self.toggle_checkbox(
            self._tv_noise_film_grain_enable_vignetting_flickering_checkbox, check
        )

    def toggle_tv_noise_scanlines(self, check=True):
        """Toggles the Scanlines setting under TV Noise & Film Grain.

        Args:
            check (bool): Desired state of the Scanlines setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(self._tv_noise_film_grain_enable_scanlines_checkbox, check)

    def set_tv_noise_scanline_spread(self, value):
        """Sets the Scanline Spread value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Scanline Spread slider.
        """
        self.toggle_tv_noise_scanlines()
        self.set_slider_value(
            self._tv_noise_film_grain_scanline_spread_float_slider, value
        )

    def toggle_tv_noise_film_grain(self, check=True):
        """Toggles the Film Grain setting.

        This method ensures that the TV Noise & Film Grain collapsible frame is expanded and the film grain is enabled or disabled based on the provided argument.

        Args:
            check (bool): Desired state of the Film Grain setting.
        """
        self._toggle_tv_noise_film_grain()
        self.toggle_checkbox(self._tv_noise_film_grain_enable_checkbox, check)

    def set_tv_noise_grain_amount(self, value):
        """Sets the Grain Amount value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Grain Amount slider.
        """
        self.toggle_tv_noise_film_grain()
        self.set_slider_value(
            self._tv_noise_film_grain_grain_amount_float_slider, value
        )

    def set_tv_noise_color_amount(self, value):
        """Sets the Color Amount value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Color Amount slider.
        """
        self.toggle_tv_noise_film_grain()
        self.set_slider_value(
            self._tv_noise_film_grain_color_amount_float_slider, value
        )

    def set_tv_noise_luminance_amount(self, value):
        """Sets the Luminance Amount value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Luminance Amount slider.
        """
        self.toggle_tv_noise_film_grain()
        self.set_slider_value(
            self._tv_noise_film_grain_luminance_amount_float_slider, value
        )

    def set_tv_noise_grain_size(self, value):
        """Sets the Grain Size value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Grain Size slider.
        """
        self.toggle_tv_noise_film_grain()
        self.set_slider_value(self._tv_noise_film_grain_grain_size_float_slider, value)

    def set_tv_noise_vignetting_size(self, value):
        """Sets the Vignetting Size value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Vignetting Size slider.
        """
        self._toggle_tv_noise_vignetting_enable()
        self.set_slider_value(
            self._tv_noise_film_grain_vignetting_size_float_drag, value
        )

    def set_tv_noise_vignetting_strength(self, value):
        """Sets the Vignetting Strength value under TV Noise & Film Grain.

        Args:
            value (float): The value to set on the Vignetting Strength slider.
        """
        self._toggle_tv_noise_vignetting_enable()
        self.set_slider_value(
            self._tv_noise_film_grain_vignetting_strength_float_slider, value
        )

    def _toggle_fftBloom_enabled(self, check=True):
        """
        Toggles the FFT Bloom enabled checkbox after expanding its collapsible frame.

        Args:
            check (bool): True to enable the feature, False to disable it.
        """
        self.expand_collapsible_frame(self._fftBloom_collapsableFrame)
        self.toggle_checkbox(self._fftBloom_enabled_checkBox, check)

    def set_fftBloom_scale(self, value):
        """
        Sets the FFT Bloom scale value.

        Args:
            value (float): The value to set for the scale.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_enabled()
        self.set_slider_value(self._fftBloom_scale_floatDrag, value)

    def set_fftBloom_cutoffFuzziness(self, value):
        """
        Sets the FFT Bloom cutoff fuzziness value.

        Args:
            value (float): The value to set for the cutoff fuzziness.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_enabled()
        self.set_slider_value(self._fftBloom_cutoffFuzziness_floatSlider, value)

    def set_fftBloom_alphaChannelScale(self, value):
        """
        Sets the FFT Bloom alpha channel scale value.

        Args:
            value (float): The value to set for the alpha channel scale.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_enabled()
        self.set_slider_value(self._fftBloom_alphaChannelScale_floatDrag, value)

    def toggle_fftBloom_energyConstrained(self, check=True):
        """
        Toggles the FFT Bloom energy constrained checkbox.

        Args:
            check (bool): True to enable energy constraining, False to disable it.
        """
        self._toggle_fftBloom_enabled()
        self.toggle_checkbox(self._fftBloom_energyConstrained_checkBox, check)

    def _toggle_fftBloom_physicalModel(self, check=True):
        """
        Toggles the FFT Bloom physical model checkbox.

        Args:
            check (bool): True to enable the physical model, False to disable it.
        """
        self._toggle_fftBloom_enabled()
        self.toggle_checkbox(self._fftBloom_physicalModel_checkBox, check)

    def set_fftBloom_blades(self, value):
        """
        Sets the number of blades for FFT Bloom effect.

        Args:
            value (int): The number of blades to set for the FFT Bloom effect.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_blades_intSlider, value)

    def set_fftBloom_apertureRotation(self, value):
        """
        Sets the aperture rotation value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the aperture rotation.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_apertureRotation_floatDrag, value)

    def set_fftBloom_sensorDiagonal(self, value):
        """
        Sets the sensor diagonal value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the sensor diagonal.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_sensorDiagonal_floatDrag, value)

    def set_fftBloom_sensorAspectRatio(self, value):
        """
        Sets the sensor aspect ratio value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the sensor aspect ratio.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_sensorAspectRatio_floatDrag, value)

    def set_fftBloom_fStop(self, value):
        """
        Sets the f-stop value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the f-stop.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_fStop_floatDrag, value)

    def set_fftBloom_focalLength(self, value):
        """
        Sets the focal length value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the focal length.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel()
        self.set_slider_value(self._fftBloom_focalLength_floatDrag, value)

    def set_fftBloom_haloFlareWeight(self, value):
        """
        Sets the halo flare weight value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the halo flare weight.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel(check=False)
        self.set_slider_value(self._fftBloom_haloFlareWeightFloatDrag, value)

    def set_fftBloom_anisoFlareWeight(self, value):
        """
        Sets the anisotropic flare weight value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the anisotropic flare weight.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel(check=False)
        self.set_slider_value(self._fftBloom_anisoFlareWeightFloatDrag, value)

    def set_fftBloom_isotropicFlareWeight(self, value):
        """
        Sets the isotropic flare weight value for the FFT Bloom effect.

        Args:
            value (float): The value to set for the isotropic flare weight.

        Raises:
            ValueError: If the `value` provided is outside the valid range of the slider.
        """
        self._toggle_fftBloom_physicalModel(check=False)
        self.set_slider_value(self._fftBloom_isotropicFlareWeightFloatDrag, value)

    def navigate_to_common_options(self):
        """Find and clicks on the common options"""
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._common_btn)

    def _toggle_flow_category_enabled(self, check=True):
        """Expands and Toggles the Flow category setting.

        Args:
            check (bool): True to enable the Flow category, False to disable.
        """
        self.expand_collapsible_frame(self._flowCategory_collapsibleFrame)
        self.toggle_checkbox(self._flowCategory_enable_checkbox, check)

    def toggle_flow_real_time_ray_traced_shadows(self, check=True):
        """Toggles the Real-Time Ray Traced Shadows checkbox in the Flow category.

        Args:
            check (bool): True to enable shadows, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(self._flowCategory_realTimeRayTracedShadowsCheckBox, check)

    def toggle_flow_real_time_ray_traced_reflections(self, check=True):
        """Toggles the Real-Time Ray Traced Reflections checkbox in the Flow category.

        Args:
            check (bool): True to enable reflections, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(
            self._flowCategory_realTimeRayTracedReflectionsCheckBox, check
        )

    def toggle_flow_real_time_ray_traced_translucency(self, check=True):
        """Toggles the Real-Time Ray Traced Translucency checkbox in the Flow category.

        Args:
            check (bool): True to enable translucency, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(
            self._flowCategory_realTimeRayTracedTranslucencyCheckBox, check
        )

    def toggle_flow_path_traced_mode(self, check=True):
        """Toggles the Path-Traced Mode checkbox in the Flow category.

        Args:
            check (bool): True to enable Path-Traced Mode, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(self._flowCategory_pathTracedModeCheckBox, check)

    def toggle_flow_path_traced_mode_shadows(self, check=True):
        """Toggles the Path-Traced Mode Shadows checkbox in the Flow category.

        Args:
            check (bool): True to enable shadows in Path-Traced Mode, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(self._flowCategory_pathTracedModeShadowsCheckBox, check)

    def toggle_flow_composite_with_flow_library_renderer(self, check=True):
        """Toggles the Composite with Flow Library Renderer checkbox in the Flow category.

        Args:
            check (bool): True to enable compositing with Flow Library Renderer, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(
            self._flowCategory_compositeWithFLowLibraryRendererCheckBox, check
        )

    def toggle_flow_use_flow_library_self_shadow(self, check=True):
        """Toggles the Use Flow Library Self-Shadow checkbox in the Flow category.

        Args:
            check (bool): True to enable Flow Library Self-Shadow, False to disable.
        """
        self._toggle_flow_category_enabled()
        self.toggle_checkbox(self._flowCategory_useFlowLibrarySelfShadowCheckBox, check)

    def set_flow_max_blocks(self, value):
        """Sets the value of the Max Blocks slider in the Flow category.

        Args:
            value (int): The value to set on the Max Blocks slider.
        """
        self._toggle_flow_category_enabled()
        self.set_slider_value(self._flowCategory_maxBlocksSlider, value)

    def _expand_materials_collapsible_frame(self):
        """Expands the Materials collapsible frame if it is collapsed."""
        self.expand_collapsible_frame(self._materials_collapsibleFrame)

    def toggle_materials_animation_time_use_wallclock(self, check=True):
        """Expands the Materials collapsible frame and toggles the 'Use Wallclock Time' checkbox for animation.

        Args:
            check (bool): True to check the 'Use Wallclock Time' option, False to uncheck.
        """
        self._expand_materials_collapsible_frame()
        self.toggle_checkbox(self._materials_animationTimeUseWallclockCheckBox, check)

    def set_materials_animation_time_override(self, value):
        """Expands the Materials collapsible frame and sets the animation time override value.

        Args:
            value (float): The value to set for the animation time override.

        Raises:
            ValueError: If the value is outside the allowed range of the slider.
        """

        self._expand_materials_collapsible_frame()
        self.set_slider_value(self._materials_animationTimeOverrideFloatDrag, value)

    def _expand_lighting_settings(self):
        """Expands the Lighting collapsible frame."""
        self.expand_collapsible_frame(self._lighting_collapsible_frame)

    def set_lighting_show_area_lights(self, option_name: str):
        """Sets the option for showing area lights in primary rays.

        Args:
            option_name (str): The option name to select in the combobox.
        """
        self._expand_lighting_settings()
        self.select_item_by_name_from_combo_box(
            self._lighting_ShowAreaLightsInPrimaryRays_ComboBox, option_name
        )

    def set_lighting_invisible_lights_roughness_threshold(self, value: float):
        """Sets the roughness threshold for invisible lights.

        Args:
            value (float): The value to set on the slider.
        """
        self._expand_lighting_settings()
        self.set_slider_value(
            self._lighting_InvisibleLightsRoughnessThreshold_Slider, value
        )

    def set_lighting_shadow_bias(self, value: float):
        """Sets the shadow bias value.

        Args:
            value (float): The value to set on the slider.
        """
        self._expand_lighting_settings()
        self.set_slider_value(self._lighting_ShadowBias_Slider, value)

    def toggle_lighting_use_first_distant_and_dome_only(self, check: bool = True):
        """Toggles the checkbox to use only the first distant light and first dome light.

        Args:
            check (bool): True to enable the setting, False to disable.
        """
        self._expand_lighting_settings()
        self.toggle_checkbox(
            self._lighting_UseFirstDistantLightAndFirstDomeLightOnly_Checkbox, check
        )

    def select_lighting_mode(self, option_name: str):
        """Selects the lighting mode from the combobox.

        Args:
            option_name (str): The lighting mode to select.
        """
        self._expand_lighting_settings()
        self.select_item_by_name_from_combo_box(
            self._lighting_LightingMode_ComboBox, option_name
        )

    def select_lighting_baking_resolution(self, resolution: str):
        """Selects the baking resolution for lighting.

        Args:
            resolution (str): The resolution to select from the combobox.
        """
        self._expand_lighting_settings()
        self.select_item_by_name_from_combo_box(
            self._lighting_BakingResolution_ComboBox, resolution
        )

    def _toggle_simple_fog_enabled(self, check=True):
        """Expand and Toggles the Simple Fog setting.

        Args:
            check (bool): True to enable Simple Fog, False to disable.
        """
        self.expand_collapsible_frame(self._simpleFog_collapsibleFrame)
        self.toggle_checkbox(self._simpleFog_mainCheckBox, check)

    def set_simple_fog_intensity(self, value):
        """Sets the Simple Fog intensity value.

        Args:
            value (float): The value to set for the fog intensity.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_intensityFloatDrag, value)

    def toggle_simple_fog_use_plus_z_axis(self, check=True):
        """Toggles the Simple Fog use Plus Z Axis checkbox.

        Args:
            check (bool): True to use Plus Z Axis for Simple Fog, False otherwise.
        """
        self._toggle_simple_fog_enabled()
        self.toggle_checkbox(self._simpleFog_usePlusZAxisCheckBox, check)

    def set_simple_fog_plane_height(self, value):
        """Sets the Simple Fog plane height value.

        Args:
            value (float): The value to set for the fog plane height.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_planeHeightFloatDrag, value)

    def set_simple_fog_height_density(self, value):
        """Sets the Simple Fog height density value.

        Args:
            value (float): The value to set for the fog height density.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_heightDensityFloatSlider, value)

    def set_simple_fog_height_falloff(self, value):
        """Sets the Simple Fog height falloff value.

        Args:
            value (float): The value to set for the fog height falloff.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_heightFalloffFloatDrag, value)

    def set_simple_fog_start_distance_to_camera(self, value):
        """Sets the Simple Fog start distance to camera value.

        Args:
            value (float): The value to set for the fog start distance to camera.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_startDistanceToCameraFloatDrag, value)

    def set_simple_fog_end_distance_to_camera(self, value):
        """Sets the Simple Fog end distance to camera value.

        Args:
            value (float): The value to set for the fog end distance to camera.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_endDistanceToCameraFloatDrag, value)

    def set_simple_fog_distance_density(self, value):
        """Sets the Simple Fog distance density value.

        Args:
            value (float): The value to set for the fog distance density.
        """
        self._toggle_simple_fog_enabled()
        self.set_slider_value(self._simpleFog_distanceDensityFloatSlider, value)

    def _toggle_global_volumetric_effects_enabled(self, check=True):
        """Expands and Toggles Global Volumetric Effects.

        Args:
            check (bool): True to enable Global Volumetric Effects, False to disable.
        """
        self.expand_collapsible_frame(self._globalVolumetricEffects_collapsibleFrame)
        self.toggle_checkbox(self._globalVolumetricEffects_enabled_checkBox, check)

    def set_transmittance_measurement_distance(self, value):
        """Sets the Transmittance Measurement Distance value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(
            self._inscatteringTransmittanceMeasurementDistance_FloatDrag, value
        )

    def set_fog_height_fall_off(self, value):
        """Sets the Fog Height Fall Off value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(self._pathTracingFogHeightFallOff_FloatDrag, value)

    def set_inscattering_max_distance(self, value):
        """Sets the Inscattering Max Distance value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(self._inscatteringMaxDistance_FloatDrag, value)

    def set_anisotropy_factor(self, value):
        """Sets the Anisotropy Factor value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(self._inscatteringAnisotropyFactor_FloatDrag, value)

    def set_density_mult(self, value):
        """Sets the Inscattering Density Mult value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(self._inscatteringDensityMult_FloatSlider, value)

    def _expand_density_noise_settings(self):
        """Expands the Density Noise Settings collapsible frame."""
        self.expand_collapsible_frame(self._densityNoiseSettings_CollapsableFrame)

    def _toggle_use_detail_noise(self, check=True):
        """Enables or disables the use of detail noise.

        Args:
            check (bool): True to enable the use of detail noise, False to disable.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        # self._expand_density_noise_settings()
        self.toggle_checkbox(self._apply_density_noise_CheckBox, check)

    def set_fog_height(self, value):
        """Sets the Fog Height value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_global_volumetric_effects_enabled(check=True)
        self.set_slider_value(self._pathTracingAtmosphereHeight_FloatDrag, value)

    def set_density_noise_world_scale(self, value):
        """Sets the Density Noise World Scale value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_WorldScale_Slider, value)

    def set_density_noise_animation_speed_x(self, value):
        """Sets the Density Noise Animation Speed X value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_AnimationSpeedX_Slider, value)

    def set_density_noise_animation_speed_y(self, value):
        """Sets the Density Noise Animation Speed Y value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_AnimationSpeedY_Slider, value)

    def set_density_noise_animation_speed_z(self, value):
        """Sets the Density Noise Animation Speed Z value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_AnimationSpeedZ_Slider, value)

    def set_density_noise_scale_min(self, value):
        """Sets the Density Noise Scale Min value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_ScaleMin_Slider, value)

    def set_density_noise_scale_max(self, value):
        """Sets the Density Noise Scale Max value.

        Args:
            value (float): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_ScaleMax_Slider, value)

    def set_density_noise_octave_count(self, value):
        """Sets the Density Noise Octave Count value.

        Args:
            value (int): The value to set on the slider.
        """
        self._toggle_use_detail_noise(check=True)
        self.set_slider_value(self._densityNoise_OctaveCount_Slider, value)

    def _expand_dlss_settings(self):
        """Expands the NVIDIA DLSS collapsible frame to access the contained settings."""
        self.expand_collapsible_frame(self._dlss_collapsibleFrame)

    def navigate_to_ray_tracing_options(self):
        """Find and clicks on the ray tracing option"""
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)

    def navigate_to_path_tracing_options(self):
        """Find and clicks on the path tracing option"""
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._path_tracing_options)

    def set_dlss_mode(self, mode_name: str):
        """Sets the DLSS mode by selecting the specified mode from the DLSS Mode combobox.

        Args:
            mode_name (str): The name of the DLSS mode to select.
        """
        self._expand_dlss_settings()
        self.select_item_by_name_from_combo_box(self._dlss_mode_comboBox, mode_name)

    def set_dlss_sharpness(self, sharpness_value: float):
        """Sets the DLSS sharpness by moving the sharpness slider to the specified value.

        Args:
            sharpness_value (float): The sharpness value to set on the slider.
        """
        self._expand_dlss_settings()
        self.set_slider_value(self._dlss_sharpness_floatSlider, sharpness_value)

    def set_dlss_exposure_mode(self, exposure_mode: str):
        """Sets the exposure mode by selecting the specified mode from the Exposure Mode combobox.

        Args:
            exposure_mode (str): The name of the exposure mode to select.
        """
        self._expand_dlss_settings()
        self.select_item_by_name_from_combo_box(
            self._dlss_exposureMode_comboBox, exposure_mode
        )

    def set_dlss_exposure_multiplier_value(self, value: float):
        """Sets the exposure by moving the exposure multiplier value slider to the specified value.

        Args:
            value (float): The exposure value to set on the slider.
        """
        self._expand_dlss_settings()
        self.set_slider_value(self._dlss_exposureMultiPlier_floatSlider, value)

    def set_dlss_exposure_fixed_value(self, value: float):
        """Sets the exposure by moving the exposure fixed value slider to the specified value.

        Args:
            value (float): The exposure value to set on the slider.
        """
        self._expand_dlss_settings()
        self.set_slider_value(self._dlss_exposureFixedValue_floatSlider, value)

    def toggle_dlss_ray_reconstruction(self, check: bool = True):
        """Toggles the DLSS ray reconstruction checkbox to the specified state.

        Args:
            check (bool): True to enable ray reconstruction, False to disable.
        """
        self._expand_dlss_settings()
        self.toggle_checkbox(self._dlss_rayReconstruction_checkBox, check)

    def set_dlss_super_resolution(self, resolution_option: str):
        """Sets the super resolution by selecting the specified option from the Super Resolution combobox.

        Args:
            resolution_option (str): The name of the super resolution option to select.
        """
        self._expand_dlss_settings()
        self.select_item_by_name_from_combo_box(
            self._dlss_superResolution_comboBox, resolution_option
        )

    def direct_lighting_status(self):
        """Gives status about direct lighting it its ON or OFF

        Returns:
            status (bool): True if direct lighting is ON else False
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        direct_light = self.find_and_scroll_element_into_view(
            self._direct_lighting_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if direct_light.is_collapsed():
            direct_light.click()

        direct_lighting_chkbox = self.omni_driver.find_element(
            self._direct_lighting_toggle_chkbox, refresh=True
        )
        if direct_lighting_chkbox.is_checked():
            self.screenshot("direct_lighting_enabled")
            self.log.info("Direct lighting is ON")
            return True
        else:
            self.screenshot("direct_lighting_disabled")
            self.log.info("Direct lighting in OFF")
        return False

    def ray_reconstruction_status(self):
        """Gives status about ray reconstruction if it is enabled or disabled

        Returns:
            status (bool): True if ray reconstruction is Enabled else False
        """
        self.find_and_focus(self._render_settings_window)
        self.find_and_click(self._ray_tracing_options)
        direct_light = self.find_and_scroll_element_into_view(
            self._nvidia_dlss_expand, ScrollAxis.Y, ScrollAmount.TOP
        )
        if direct_light.is_collapsed():
            direct_light.click()

        ray_reconstruction_chkbox = self.omni_driver.find_element(
            self._ray_reconstruction_toggle_chkbox, refresh=True
        )
        if ray_reconstruction_chkbox.is_checked():
            self.screenshot("ray_reconstruction_enabled")
            self.log.info("Ray Reconstrucion is enabled")
            return True
        else:
            self.screenshot("ray_reconstruction_disabled")
            self.log.info("Ray Reconstrucion is disabled")
        return False
      
    def _expand_direct_lighting_collapsible_frame(self):
        """Expands the Direct Lighting collapsible frame to access the direct lighting settings."""
        self.expand_collapsible_frame(self._directLightingCollapsible_frame)

    def _toggle_direct_lighting_enabled(self, check=True):
        """Toggles the direct lighting enabled checkbox under the Direct Lighting category.

        Args:
            check (bool): True to enable direct lighting, False to disable.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.toggle_checkbox(self._directLightingEnabled_checkbox, check)

    def _toggle_shadows_enabled(self, check=True):
        """Toggles the shadows enabled checkbox under the Direct Lighting category.

        Args:
            check (bool): True to enable shadows, False to disable.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.toggle_checkbox(self._shadows_checkbox, check)

    def _toggle_sampled_direct_lighting_mode_enabled(self, check=True):
        """Toggles the sampled direct lighting mode checkbox under the Direct Lighting category.

        Args:
            check (bool): True to enable sampled direct lighting mode, False to disable.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.toggle_checkbox(self._sampledDirectLightingMode_checkbox, check)

    def _toggle_auto_enable_sampled_direct_lighting(self, check=True):
        """Toggles the auto-enable sampled direct lighting above light count threshold checkbox under the Direct Lighting category.

        Args:
            check (bool): True to enable auto-enable, False to disable.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.toggle_checkbox(self._autoEnableSampledDirectLighting_checkbox, check)

    def _set_light_count_threshold_value(self, value):
        """Sets the light count threshold slider to a specific value under the Direct Lighting category.

        Args:
            value (int): The value to set on the light count threshold slider.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.set_slider_value(self._lightCountThreshold_slider, value)

    def _expand_sampled_direct_lighting_settings(self):
        """Expands the Sampled Direct Lighting Settings header to access more detailed settings."""
        self.expand_collapsible_frame(self._sampledDirectLightingSettings_header)

    def _select_samples_per_pixel(self, item_name):
        """Selects the given item from the Samples per Pixel combobox under the Sampled Direct Lighting settings.

        Args:
            item_name (str): The name of the item to select in the combobox.
        """
        self._expand_sampled_direct_lighting_settings()
        self.select_item_by_name_from_combo_box(self._samplesPerPixel_combobox, item_name)

    def _set_max_ray_intensity_value(self, value):
        """Sets the max ray intensity slider to a specific value under the Sampled Direct Lighting settings.

        Args:
            value (float): The value to set on the max ray intensity slider.
        """
        self._expand_sampled_direct_lighting_settings()
        self.set_slider_value(self._maxRayIntensity_slider, value)

    def _select_reflections_light_samples_per_pixel(self, item_name):
        """Selects the given item from the Reflections: Light Samples per Pixel combobox under the Reflections category.

        Args:
            item_name (str): The name of the item to select in the combobox.
        """
        self._expand_direct_lighting_collapsible_frame()
        self.select_item_by_name_from_combo_box(self._reflectionsLightSamplesPerPixel_combobox, item_name)

    def _set_reflections_max_ray_intensity_value(self, value):
        """Sets the reflections max ray intensity slider to a specific value under the Reflections category.

        Args:
            value (float): The value to set on the reflections max ray intensity slider.
        """
        self._expand_direct_lighting_collapsible_frame()      
        self.set_slider_value(self._reflectionsMaxRayIntensity_slider, value)

    def _toggle_mesh_light_sampling_enabled(self, check=True):
        """Toggles the mesh-light sampling checkbox under the Sampled Direct Lighting settings.

        Args:
            check (bool): True to enable mesh-light sampling, False to disable.
        """
        self._expand_sampled_direct_lighting_settings()
        self.toggle_checkbox(self._meshLightSampling_checkbox, check)
        
    def _expand_indirect_diffuse_lighting_collapsible_frame(self):
        """Expands the Indirect Diffuse Lighting collapsible frame if it is collapsed."""
        self.expand_collapsible_frame(self._ray_tracing_indirect_diffuse_lighting_collapsible_frame)

    def _toggle_indirect_diffuse_lighting_enabled(self, check=True):
        """Toggles the Indirect Diffuse Lighting enabled checkbox.

        Args:
            check (bool): True to enable Indirect Diffuse Lighting, False to disable.
        """
        self.expand_collapsible_frame(self._ray_tracing_indirect_diffuse_lighting_collapsible_frame)
        self.toggle_checkbox(self._ray_tracing_indirect_diffuse_lighting_enabled_checkbox, check)

    def set_samples_per_pixel(self, value):
        """Sets the value for the Samples Per Pixel setting for Indirect Diffuse Lighting.

        Args:
            value (int): The value to set the Samples Per Pixel slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_samples_per_pixel_intslider, value)

    def set_max_bounces(self, value):
        """Sets the value for the Maximum Bounces setting for Indirect Diffuse Lighting.

        Args:
            value (int): The value to set the Maximum Bounces slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_max_bounces_intslider, value)

    def set_intensity(self, value):
        """Sets the value for the Intensity setting for Indirect Diffuse Lighting.

        Args:
            value (float): The value to set the Intensity slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_intensity_floatslider, value)

    def select_denoising_mode(self, mode_name):
        """Selects the denoising mode for Indirect Diffuse Lighting.

        Args:
            mode_name (str): The name of the denoising mode to select from the combobox.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.select_item_by_name_from_combo_box(self._ray_tracing_indirect_diffuse_lighting_denoising_mode_combobox, mode_name)

    def set_kernel_radius(self, value):
        """Sets the value for the Kernel Radius setting for Indirect Diffuse Lighting denoising.

        Args:
            value (int): The value to set the Kernel Radius slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_kernel_radius_intslider, value)

    def set_iteration_count(self, value):
        """Sets the value for the Iteration Count setting for Indirect Diffuse Lighting denoising.

        Args:
            value (int): The value to set the Iteration Count slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_iteration_count_intslider, value)
        
    def set_frames_in_history(self, value):
        """Sets the number of frames in history for Indirect Diffuse Denoising Mode.

        Args:
            value (int): The value to set on the frames in history slider.
        """
        # self.expand_collapsible_frame(self._indirectDiffuseDenoisingMode_framesInHistory_intSlider)
        self.set_slider_value(self._indirectDiffuseDenoisingMode_framesInHistory_intSlider, value)

    def set_plane_distance_sensitivity(self, value):
        """Sets the plane distance sensitivity for Indirect Diffuse Denoising Mode.

        Args:
            value (float): The value to set on the plane distance sensitivity slider.
        """
        # self.expand_collapsible_frame(self._indirectDiffuseDenoisingMode_planeDistanceSensitivity_floatSlider_path)
        self.set_slider_value(self._indirectDiffuseDenoisingMode_planeDistanceSensitivity_floatSlider_path, value)

    def set_blur_radius(self, value):
        """Sets the blur radius for Indirect Diffuse Denoising Mode.

        Args:
            value (float): The value to set on the blur radius drag field.
        """
        # self.expand_collapsible_frame(self._indirectDiffuseDenoisingMode_blurRadius_floatDrag_path)
        self.set_slider_value(self._indirectDiffuseDenoisingMode_blurRadius_floatDrag_path, value)

    def set_max_history_length(self, value):
        """Sets the value for the Maximum History Length setting for Indirect Diffuse Lighting denoising.

        Args:
            value (int): The value to set the Maximum History Length slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_max_history_length_intslider, value)

    def set_max_ray_intensity(self, value):
        """Sets the value for the Maximum Ray Intensity setting for Indirect Diffuse Lighting.

        Args:
            value (float): The value to set the Maximum Ray Intensity drag control to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_max_ray_intensity_floatdrag, value)

    def _toggle_ambient_occlusion_enabled(self, check=True):
        """Toggles the Ambient Occlusion enabled checkbox for Indirect Diffuse Lighting.

        Args:
            check (bool): True to enable Ambient Occlusion, False to disable.
        """
        self.expand_collapsible_frame(self._ray_tracing_indirect_diffuse_lighting_collapsible_frame)
        self.toggle_checkbox(self._ray_tracing_indirect_diffuse_lighting_ao_enabled_checkbox, check)

    def set_ray_length(self, value):
        """Sets the value for the Ray Length setting for Ambient Occlusion in Indirect Diffuse Lighting.

        Args:
            value (float): The value to set the Ray Length drag control to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_ao_ray_length_floatdrag, value)

    def set_min_samples(self, value):
        """Sets the value for the Minimum Samples setting for Ambient Occlusion in Indirect Diffuse Lighting.

        Args:
            value (int): The value to set the Minimum Samples slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_ao_min_samples_intslider, value)

    def set_max_samples(self, value):
        """Sets the value for the Maximum Samples setting for Ambient Occlusion in Indirect Diffuse Lighting.

        Args:
            value (int): The value to set the Maximum Samples slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_ao_max_samples_intslider, value)

    def set_ambient_light_intensity(self, value):
        """Sets the value for the Ambient Light Intensity setting for Indirect Diffuse Lighting.

        Args:
            value (float): The value to set the Ambient Light Intensity slider to.
        """
        self._expand_indirect_diffuse_lighting_collapsible_frame()
        self.set_slider_value(self._ray_tracing_indirect_diffuse_lighting_ambient_light_intensity_floatslider, value)

    def reset_to_default(self):
        """Resets to default preset

        """
        default_elem = self.omni_driver.find_element(self._reset_to_default, True)
        default_elem.click()    
        
    def save_preset_settings(
        self,
        file_name,
        extension: str,
        folder_path="",
        overwrite=False,
        please_wait_timeout=120
    ):
        """Saves the changes done in viewport
        Args:
            file_name: file name to be saved
            overwrite: True if changes to be saved in existing file, False otherwise
            folder_path: path of the folder to save the file to
            extension: file extension to select
        Return: None
        """
        element = self.omni_driver.find_element(self._file_name_textarea)
        element.double_click()
        self.omni_driver.wait(2)
        self.omni_driver.emulate_char_press(file_name)
        self.omni_driver.wait(2)

        if folder_path:
            folder_path = self._updated_path(folder_path) if not folder_path.startswith("file") else folder_path
            for i in range(2):
                path_field = self.omni_driver.find_element(self._directory_path_picker)
                path_field.click(bring_to_front=True)
                self.omni_driver.wait(2)
                path_field.send_keys(folder_path)

        if extension:
            ext_btn = self.find_and_click(self._extension_btn)
            center = ext_btn.get_widget_center()
            if extension.lower() == "usd":
                self.find_and_click(self._extension_combobox_options.format("0"))
            elif extension.lower() == "usda":
                self.find_and_click(self._extension_combobox_options.format("1"))
            elif extension.lower() == "usdc":
                self.find_and_click(self._extension_combobox_options.format("2"))
            else:
                assert (
                    False
                ), f"Incorrect extension name provided, Provided was {extension}, available options usd, usda and usdc"
        self.find_and_click(self._save_button)
        if overwrite:
            try:
                btn = self.wait.element_to_be_located(self.omni_driver, self._overwrite_ok_button.replace(
                    "__exclamation_glyph__", self.get_glyph_code("exclamation.svg")))
                btn.click()
                self.log.info("Overwritten existing file.")
            except ElementNotFound:
                self.log.info("File was not present, saved it for first time.")

        wait = Wait(please_wait_timeout)
        wait.element_to_be_invisible(self.omni_driver, self._please_wait_window)

    def load_preset_from_file(
        self,
        file_name,
        folder_path="",
        please_wait_timeout=120
    ):
        """Loads a preset file from local drive
        Args:
            file_name: file name to be saved
            folder_path: path of the folder to save the file to
            extension: file extension to select
        Return: None
        """
        element = self.omni_driver.find_element(self._load_preset_file_name)
        self.omni_driver.wait(1)
        element.send_keys(folder_path)
        self.omni_driver.wait(5)
        
    def select_and_load_preset(self, preset: str):
        """Changes preset mode in load from preset menu

        Args:
            preset: Preset name
        """
        render_dropdown = self.omni_driver.find_element(self._render_menu_dropdown, True)
        render_dropdown.click()
        self.find_and_click(self._load_from_preset, False, True)
        load_preset_menu = self.find_and_scroll_element_into_view(preset, ScrollAxis.Y, ScrollAmount.TOP, refresh=True)
        load_preset_menu.click(False)
        self.omni_driver.wait(5)

    def apply_preset(self, preset:str):
        """Apply any of the preset Draft, Medium or Final
        Args:
            preset: Preset name
        Return: None
        """
        # Reset to defauls
        
        
        self.reset_to_default()

        self.find_and_click(locator=self._render_settings_window)
        self.find_and_click(locator=self._load_from_preset)
        debug_view_expand = self.find_and_scroll_element_into_view(
            self._debug_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        if debug_view_expand.is_collapsed():
            debug_view_expand.click()
        debug_view_expand = self.find_and_scroll_element_into_view(
            self._debug_collapse_bar, ScrollAxis.Y, ScrollAmount.TOP, True
        )
        render_result = self.omni_driver.find_element(self._render_target).get_text()
        return render_result
    

    def apply_preset_and_verify(self, folder_path:str, preset:str):
        """Apply a preset from UI, save preset to a file and verify with pre-defined preset file
        Args:
            folder_path: Extension path on local drive
            preset: Preset name
        Return: True/False
        """
        # Get file details
        file_from_preset = os.path.join(get_downloads_folder_path() + f"/{preset}.settings.usda")
        predefined_preset = os.path.join(folder_path + f"/data/presets/{preset}.settings.usda")
        if os.name == 'nt':
            file_from_preset = file_from_preset.replace("/","\\")
            predefined_preset = predefined_preset.replace("/","\\")

        if os.path.exists(file_from_preset):
            os.remove(file_from_preset)

        self.log.info("Saved File Path : " + file_from_preset)
        self.log.info("File Settings Path : " + predefined_preset)

        # Apply Preset
        preset_identifier = self._preset_type_draft
        if preset == 'medium':
            preset_identifier = self._preset_type_medium
        if preset == 'final':
            preset_identifier = self._preset_type_final
        self.select_and_load_preset(preset_identifier)

        # Save the current preset in download folder
        render_dropdown = self.omni_driver.find_element(self._render_menu_dropdown)
        render_dropdown.click()
        self.omni_driver.wait(1)

        self.find_and_click(self._save_preset, False, True)
        folder_path = "file://"+ get_downloads_folder_path()
        self.save_preset_settings(file_name=preset,extension="usda", folder_path = folder_path)

        # Compare files
        cmp_result = filecmp.cmp(file_from_preset, predefined_preset)
        self.log.info(f"{preset} set vs pre-defined preset match : " + str(cmp_result))
        return cmp_result

    def verify_renderer(self, renderer:str):
        """Verify renderer applied
        Args:
            renderer: renderer name
        Return: True/False
        """
        elem = self.omni_driver.find_element(self._active_renderer, True)
        # Returns values like "Real-time", without "RTX - " string
        if elem.get_combobox_info()["current_value"] in renderer:
            return True
        else:
            return False