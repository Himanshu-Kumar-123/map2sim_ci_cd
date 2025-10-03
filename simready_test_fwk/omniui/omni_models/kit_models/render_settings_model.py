# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Render Settings class
   This module contains the base methods for Render Settings window
"""


from random import randint, uniform
from omni_remote_ui_automator.common.enums import DlssModesRenderSettings

from omniui.omni_models.base_models.base_render_settings_model import (
    BaseRenderSettingsModel,
)
from omni_remote_ui_automator.common.enums import ScrollAmount, ScrollAxis


class RenderSettingsModel(BaseRenderSettingsModel):
    """Base model class for Render settings window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Tone Mapping - Post Processing Settings
    _tone_mapping_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[0].identifier=='Tone Mapping'"
    )
    _tone_mapping_operator_combo_box = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_tonemap_op'"
    )
    _tone_mapping_srgb_to_gamma_conversion_check_box = (
        "Render Settings//Frame/**/HStack____SRGB_To_Gamma_Conversion/**/CheckBox[0]"
    )
    _tone_mapping_cm2_factor_slider = (
        "Render Settings//Frame/**/HStack_cm^2_Factor/FloatSlider[0]"
    )
    _tone_mapping_film_iso_drag = (
        "Render Settings//Frame/**/HStack_Film_ISO/FloatDrag[0]"
    )
    _tone_mapping_camera_shutter_drag = (
        "Render Settings//Frame/**/HStack_Camera_Shutter/FloatDrag[0]"
    )
    _tone_mapping_fstop_slider = (
        "Render Settings//Frame/**/HStack_F-stop/FloatSlider[0]"
    )
    _tone_mapping_white_point_color_widget = (
        "Render Settings//Frame/**/HStack_White_Point/**/ColorWidget[0]"
    )
    _tone_mapping_wrap_value_drag = (
        "Render Settings//Frame/**/HStack_Wrap_Value/FloatDrag[0]"
    )
    _tone_mapping_dither_strength_slider = (
        "Render Settings//Frame/**/HStack_Dither_strength/FloatSlider[0]"
    )
    _tone_mapping_color_space = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_tonemap_colorMode'"

    # Auto Exposure - Post Processing Settings
    _auto_exposure_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Auto Exposure'"
    )
    _auto_exposure_enabled = (
        "Render Settings//Frame/**/PostSettingStack/Auto Exposure/**/CheckBox[0]"
    )
    _auto_exposure_adaptation_speed = (
        "Render Settings//Frame/**/HStack_Adaptation_Speed/FloatSlider[0]"
    )
    _auto_exposure_white_point_scale = (
        "Render Settings//Frame/**/HStack_White_Point_Scale/FloatSlider[0]"
    )
    _auto_exposure_min_value = (
        "Render Settings//Frame/**/HStack____Minimum_Value/FloatDrag[0]"
    )
    _auto_exposure_max_value = (
        "Render Settings//Frame/**/HStack____Maximum_Value/FloatDrag[0]"
    )
    _auto_exposure_value_clamping = (
        "Render Settings//Frame/**/HStack_Exposure_Value_Clamping/**/CheckBox[0]"
    )
    _auto_exposure_histogram_filter_type = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_histogram_filterType'"

    # Color Correction - Post Processing Settings
    _color_correction_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Color Correction'"
    )
    _color_correction_enable_checkbox = (
        "Render Settings//Frame/**/Color Correction/**/CheckBox[0]"
    )
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
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Color Grading'"
    )
    _color_grading_main_checkbox = (
        "Render Settings//Frame/**/Color Grading/**/CheckBox[0]"
    )

    # XR Composting - Post Processing Settings
    _xr_compositing_enabled_checkbox = (
        "Render Settings//Frame/**/XR Compositing/**/CheckBox[0]"
    )
    _xr_compositing_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='XR Compositing'"
    )
    _xr_compositing_composite_in_editor_checkbox = (
        "Render Settings//Frame/**/HStack_Composite_in_Editor/**/CheckBox[0]"
    )
    _xr_compositing_output_alpha_composited_image_checkbox = "Render Settings//Frame/**/HStack_Output_Alpha_in_Composited_Image/**/CheckBox[0]"
    _xr_compositing_output_black_background_composited_image_checkbox = "Render Settings//Frame/**/HStack_Output_Black_Background_in_Composited_Image/**/CheckBox[0]"
    _xr_compositing_backplate_color_widget = (
        "Render Settings//Frame/**/HStack_Backplate_Color/**/ColorWidget[0]"
    )
    _xr_compositing_backplate_texture_path_stringfield = (
        "Render Settings//Frame/**/StringField[0].identifier=='AssetPicker_path'"
    )
    _xr_compositing_asset_picker_select_backplate_button = (
        "Render Settings//Frame/**/Button[*].identifier=='AssetPicker_select'"
    )
    _xr_compositing_backplate_texture_locate_button = (
        "Render Settings//Frame/**/Button[*].identifier=='AssetPicker_locate'"
    )
    _xr_compositing_backplate_texture_is_linear_checkbox = (
        "Render Settings//Frame/**/HStack____Is_linear/**/CheckBox[0]"
    )
    _xr_compositing_backplate_luminance_scale_floatdrag = "Render Settings//Frame/**/VStack[0]/HStack____Luminance_Scale/FloatDrag[0]"
    _xr_compositing_enable_lens_distortion_correction_checkbox = (
        "Render Settings//Frame/**/HStack_Lens_Distortion/**/CheckBox[0]"
    )

    # Matte Object - Post Processing Settings
    _matte_object_collapsable_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Matte Object'"
    )
    _matte_object_main_checkbox = (
        "Render Settings//Frame/**/Matte Object/**/CheckBox[0]"
    )
    _matte_object_shadow_catcher_checkbox = (
        "Render Settings//Frame/**/HStack_Shadow_Catcher/**/CheckBox[0]"
    )

    # Chromatic Aberration - Post Processing Settings
    _chromatic_aberration_enabled = (
        "Render Settings//Frame/**/Chromatic Aberration/**/CheckBox[0]"
    )
    _chromatic_aberration_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Chromatic Aberration'"
    _chromatic_aberration_strength_red_slider = (
        "Render Settings//Frame/**/HStack_Strength_Red/FloatSlider[0]"
    )
    _chromatic_aberration_strength_green_slider = (
        "Render Settings//Frame/**/HStack_Strength_Green/FloatSlider[0]"
    )
    _chromatic_aberration_strength_blue_slider = (
        "Render Settings//Frame/**/HStack_Strength_Blue/FloatSlider[0]"
    )
    _chromatic_aberration_algorithm_red_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeR'"
    _chromatic_aberration_algorithm_green_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeG'"
    _chromatic_aberration_algorithm_blue_combobox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_chromaticAberration_modeB'"
    _chromatic_aberration_lanczos_sampler_checkbox = (
        "Render Settings//Frame/**/HStack_Use_Lanczos_Sampler/**/CheckBox[0]"
    )
    _chromatic_aberration_boundary_blending_collapsible_frame = (
        "Render Settings//Frame/**/Chromatic Aberration/**/CollapsableFrame[0]"
    )
    _chromatic_aberration_repeat_mirrored_checkbox = (
        "Render Settings//Frame/**/HStack_Repeat_Mirrored/**/CheckBox[0]"
    )
    _chromatic_aberration_blend_region_size_slider = (
        "Render Settings//Frame/**/HStack_Blend_Region_Size/FloatSlider[0]"
    )
    _chromatic_aberration_blend_region_falloff_slider = (
        "Render Settings//Frame/**/HStack_Blend_Region_Falloff/FloatSlider[0]"
    )

    # Depth of Field Camera Overrides - Post Processing Settings
    _depth_of_field_enabled_checkbox = (
        "Render Settings//Frame/**/Depth of Field Camera Overrides/**/CheckBox[0]"
    )
    _depth_of_field_collapsible_frame = "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Depth of Field Camera Overrides'"
    _depth_of_field_enable_checkbox = (
        "Render Settings//Frame/**/Depth of Field Camera Overrides/**/CheckBox[0]",
    )
    _depth_of_field_subject_distance_slider = (
        "Render Settings//Frame/**/HStack_Subject_Distance/FloatDrag[0]"
    )
    _depth_of_field_focal_length_slider = (
        "Render Settings//Frame/**/HStack_Focal_Length_(mm)/FloatDrag[0]"
    )
    _depth_of_field_f_stop_slider = (
        "Render Settings//Frame/**/HStack_F-stop/FloatDrag[0]"
    )
    _depth_of_field_anisotropy_slider = (
        "Render Settings//Frame/**/HStack_Anisotropy/FloatSlider[0]"
    )
    _depthOfField_overrideCheckbox = (
        "Render Settings//Frame/**/HStack_Enable_DOF/**/CheckBox[0]"
    )

    # Motion Blur - Post Processing Settings
    _motion_blur_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Motion Blur'"
    )
    _motion_blur_enabled_checkbox = (
        "Render Settings//Frame/**/Motion Blur/**/CheckBox[0]"
    )
    _motion_blur_diameter_fraction_slider = (
        "Render Settings//Frame/**/HStack_Blur_Diameter_Fraction/FloatSlider[0]"
    )
    _motion_blur_exposure_fraction_slider = (
        "Render Settings//Frame/**/HStack_Exposure_Fraction/FloatSlider[0]"
    )
    _motion_blur_number_of_samples_slider = (
        "Render Settings//Frame/**/HStack_Number_of_Samples/IntSlider[0]"
    )

    # TV Noise & Film Grain - Post Processing Settings
    _tv_noise_film_grain_collapsable_frame = "Render Settings//Frame/**/CollapsableFrame[*].identifier=='TV Noise & Film Grain'"
    _tv_noise_enable_checkbox = (
        "Render Settings//Frame/**/TV Noise & Film Grain/Frame[0]/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_random_splotches_checkbox = (
        "Render Settings//Frame/**/HStack_Enable_Random_Splotches/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_vertical_lines_checkbox = (
        "Render Settings//Frame/**/HStack_Enable_Vertical_Lines/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_wavy_distortion_checkbox = (
        "Render Settings//Frame/**/HStack_Enable_Wavy_Distortion/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_ghost_flickering_checkbox = (
        "Render Settings//Frame/**/HStack_Enable_Ghost_Flickering/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_vignetting_flickering_checkbox = "Render Settings//Frame/**/HStack____Enable_Vignetting_Flickering/**/CheckBox[0]"
    _tv_noise_vignettingEnableCheckbox = (
        "Render Settings//Frame/**/HStack_Enable_Vignetting/**/CheckBox[0]"
    )
    _tv_noise_film_grain_enable_scanlines_checkbox = (
        "Render Settings//Frame/**/HStack_Enable_Scanlines/**/CheckBox[0]"
    )
    _tv_noise_film_grain_scanline_spread_float_slider = (
        "Render Settings//Frame/**/HStack____Scanline_Spreading/FloatSlider[0]"
    )
    _tv_noise_film_grain_grain_amount_float_slider = (
        "Render Settings//Frame/**/HStack____Grain_Amount/FloatSlider[0]"
    )
    _tv_noise_film_grain_color_amount_float_slider = (
        "Render Settings//Frame/**/HStack____Color_Amount/FloatSlider[0]"
    )
    _tv_noise_film_grain_luminance_amount_float_slider = (
        "Render Settings//Frame/**/HStack____Luminance_Amount/FloatSlider[0]"
    )
    _tv_noise_film_grain_grain_size_float_slider = (
        "Render Settings//Frame/**/HStack____Grain_Size/FloatSlider[0]"
    )
    _tv_noise_film_grain_vignetting_size_float_drag = (
        "Render Settings//Frame/**/VStack[0]/HStack____Vignetting_Size/FloatDrag[0]"
    )
    _tv_noise_film_grain_vignetting_strength_float_slider = (
        "Render Settings//Frame/**/VStack[0]/HStack____Vignetting_Strength/FloatSlider[0]",
    )
    _tv_noise_film_grain_enable_checkbox = (
        "Render Settings//Frame/**/TV Noise & Film Grain/**/CheckBox[0]"
    )

    #  FFT Bloom - Post Processing Settings
    _fftBloom_enabled_checkBox = "Render Settings//Frame/**/FFT Bloom/**/CheckBox[0]"
    _fftBloom_collapsableFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='FFT Bloom'"
    )
    _fftBloom_scale_floatDrag = "Render Settings//Frame/**/HStack_Scale/FloatDrag[0]"
    _fftBloom_cutoffPoint_multiFloatDragField = (
        "Render Settings//Frame/**/MultiFloatDragField[0]"
    )
    _fftBloom_cutoffFuzziness_floatSlider = (
        "Render Settings//Frame/**/HStack_Cutoff_Fuzziness/FloatSlider[0]"
    )
    _fftBloom_alphaChannelScale_floatDrag = (
        "Render Settings//Frame/**/HStack_Alpha_channel_scale/FloatDrag[0]"
    )
    _fftBloom_energyConstrained_checkBox = (
        "Render Settings//Frame/**/HStack_Energy_Constrained/**/CheckBox[0]"
    )
    _fftBloom_physicalModel_checkBox = (
        "Render Settings//Frame/**/HStack_Physical_Model/**/CheckBox[0]"
    )
    _fftBloom_blades_intSlider = (
        "Render Settings//Frame/**/HStack____Blades/IntSlider[0]"
    )
    _fftBloom_apertureRotation_floatDrag = (
        "Render Settings//Frame/**/HStack____Aperture_Rotation/FloatDrag[0]"
    )
    _fftBloom_sensorDiagonal_floatDrag = (
        "Render Settings//Frame/**/HStack____Sensor_Diagonal/FloatDrag[0]"
    )
    _fftBloom_sensorAspectRatio_floatDrag = (
        "Render Settings//Frame/**/HStack____Sensor_Aspect_Ratio/FloatDrag[0]"
    )
    _fftBloom_fStop_floatDrag = (
        "Render Settings//Frame/**/HStack____F-stop/FloatDrag[0]"
    )
    _fftBloom_focalLength_floatDrag = (
        "Render Settings//Frame/**/HStack____Focal_Length_(mm)/FloatDrag[0]"
    )
    _fftBloom_haloFlareWeightFloatDrag = (
        "Render Settings//Frame/**/HStack____Halo_Flare_Weight/FloatDrag[0]"
    )
    _fftBloom_anisoFlareWeightFloatDrag = (
        "Render Settings//Frame/**/HStack____Aniso_Flare_Weight/FloatDrag[0]"
    )
    _fftBloom_isotropicFlareWeightFloatDrag = (
        "Render Settings//Frame/**/HStack____Isotropic_Flare_Weight/FloatDrag[0]"
    )

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
    _flowCategory_maxBlocksSlider = (
        "Render Settings//Frame/**/Flow/**/HStack_Max_Blocks/IntDrag[*]"
    )

    #  Materials - Common Settings
    _materials_collapsibleFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Materials'"
    )
    _materials_animationTimeOverrideFloatDrag = (
        "Render Settings//Frame/**/HStack_Animation_Time_Override/FloatDrag[0]"
    )
    _materials_animationTimeUseWallclockCheckBox = (
        "Render Settings//Frame/**/HStack_Animation_Time_Use_Wallclock/**/CheckBox[0]"
    )

    #  Lighting - Common Settings
    _lighting_collapsible_frame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Lighting'"
    )
    _lighting_ShowAreaLightsInPrimaryRays_ComboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_raytracing_showLights'"
    )
    _lighting_InvisibleLightsRoughnessThreshold_Slider = "Render Settings//Frame/**/HStack_Invisible_Lights_Roughness_Threshold/FloatSlider[0]"
    _lighting_ShadowBias_Slider = (
        "Render Settings//Frame/**/HStack_Shadow_Bias/FloatSlider[0]"
    )
    _lighting_UseFirstDistantLightAndFirstDomeLightOnly_Checkbox = "Render Settings//Frame/**/HStack_Use_First_Distant_Light_&_First_Dome_Light_Only/**/CheckBox[0]"
    _lighting_LightingMode_ComboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_domeLight_upperLowerStrategy'"
    _lighting_BakingResolution_ComboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_domeLight_baking_resolution'"

    #  Simple Fog - Common Settings
    _simpleFog_mainCheckBox = "Render Settings//Frame/**/Simple Fog/**/CheckBox[0]"
    _simpleFog_collapsibleFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Simple Fog'"
    )
    _simpleFog_intensityFloatDrag = (
        "Render Settings//Frame/**/HStack_Intensity/FloatDrag[0]"
    )
    _simpleFog_usePlusZAxisCheckBox = (
        "Render Settings//Frame/**/HStack_Height-based_Fog_-_Use_+Z_Axis/**/CheckBox[0]"
    )
    _simpleFog_planeHeightFloatDrag = (
        "Render Settings//Frame/**/HStack_Height-based_Fog_-_Plane_Height/FloatDrag[0]"
    )
    _simpleFog_heightDensityFloatSlider = (
        "Render Settings//Frame/**/HStack_Height_Density/FloatSlider[0]"
    )
    _simpleFog_heightFalloffFloatDrag = (
        "Render Settings//Frame/**/HStack_Height_Falloff/FloatDrag[0]"
    )
    _simpleFog_startDistanceToCameraFloatDrag = (
        "Render Settings//Frame/**/HStack_Start_Distance_to_Camera/FloatDrag[0]"
    )
    _simpleFog_endDistanceToCameraFloatDrag = (
        "Render Settings//Frame/**/HStack_End_Distance_to_Camera/FloatDrag[0]"
    )
    _simpleFog_distanceDensityFloatSlider = (
        "Render Settings//Frame/**/HStack_Distance_Density/FloatSlider[0]"
    )

    #  Global Volumetric Effects - Common Settings
    _globalVolumetricEffects_collapsibleFrame = "Render Settings//Frame/**/CollapsableFrame[*].identifier=='Global Volumetric Effects'"
    _globalVolumetricEffects_enabled_checkBox = (
        "Render Settings//Frame/**/Global Volumetric Effects/**/CheckBox[0]"
    )
    _inscatteringTransmittanceMeasurementDistance_FloatDrag = "Render Settings//Frame/**/HStack_Transmittance_Measurment_Distance/FloatDrag[0]"
    _pathTracingFogHeightFallOff_FloatDrag = (
        "Render Settings//Frame/**/HStack_Fog_Height_Fall_Off/FloatDrag[0]"
    )
    _inscatteringMaxDistance_FloatDrag = (
        "Render Settings//Frame/**/HStack_Maximum_inscattering_Distance/FloatDrag[0]"
    )
    _inscatteringAnisotropyFactor_FloatDrag = (
        "Render Settings//Frame/**/HStack_Anisotropy_Factor_(g)/FloatSlider[*]"
    )
    _inscatteringDensityMult_FloatSlider = (
        "Render Settings//Frame/**/HStack_Density_Multiplier/FloatSlider[0]"
    )
    _densityNoiseSettings_CollapsableFrame = (
        "Render Settings//Frame/**/Global Volumetric Effects/**/CollapsableFrame[0]"
    )
    _apply_density_noise_CheckBox = (
        "Render Settings//Frame/**/HStack_Apply_Density_Noise/**/CheckBox[0]"
    )
    _pathTracingAtmosphereHeight_FloatDrag = (
        "Render Settings//Frame/**/HStack_Fog_Height/FloatDrag[0]"
    )
    _densityNoise_WorldScale_Slider = (
        "Render Settings//Frame/**/HStack____World_Scale/FloatSlider[0]"
    )
    _densityNoise_AnimationSpeedX_Slider = (
        "Render Settings//Frame/**/HStack____Animation_Speed_X/FloatSlider[0]"
    )
    _densityNoise_AnimationSpeedY_Slider = (
        "Render Settings//Frame/**/HStack____Animation_Speed_Y/FloatSlider[0]"
    )
    _densityNoise_AnimationSpeedZ_Slider = (
        "Render Settings//Frame/**/HStack____Animation_Speed_Z/FloatSlider[0]"
    )
    _densityNoise_ScaleMin_Slider = (
        "Render Settings//Frame/**/HStack____Scale_Min/FloatSlider[0]"
    )
    _densityNoise_ScaleMax_Slider = (
        "Render Settings//Frame/**/HStack____Scale_Max/FloatSlider[0]"
    )
    _densityNoise_OctaveCount_Slider = (
        "Render Settings//Frame/**/HStack____Octave_Count/IntSlider[0]"
    )

    # NVIDIA DLSS category
    _dlss_collapsibleFrame = (
        "Render Settings//Frame/**/CollapsableFrame[*].identifier=='NVIDIA DLSS'"
    )
    _dlss_mode_comboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_dlss_execMode'"
    )
    _dlss_sharpness_floatSlider = "Render Settings//Frame/**/FloatSlider[0]"
    _dlss_exposureMode_comboBox = "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_aa_autoExposureMode'"
    _dlss_exposureMultiPlier_floatSlider = (
        "Render Settings//Frame/**/HStack____Auto_Exposure_Multiplier/FloatSlider[*]"
    )
    _dlss_exposureFixedValue_floatSlider = "Render Settings//Frame/**/FloatSlider[0]"

    _dlss_rayReconstruction_checkBox = "Render Settings//Frame/**/CheckBox[0]"
    _dlss_superResolution_comboBox = (
        "Render Settings//Frame/**/ComboBox[0].identifier=='_rtx_post_aa_op'"
    )

    def toggle_multiply_color_value_by_alpha_composite(self, check=True):
        """Toggles the Multiply Color Value by Alpha Composite checkbox.

        Args:
            check (bool): True to enable multiplying color value by alpha in composite, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        checkboxes = self.omni_driver.find_elements(self._xr_compositing_all_checkboxes)
        checkbox_element = checkboxes[4]
        current_state = checkbox_element.is_checked()
        self.omni_driver.wait(1)
        attempts = 10
        attempts_made = 0
        while current_state != check and attempts_made <= attempts:
            checkbox_element.click()
            self.omni_driver.wait(2)
            current_state = checkbox_element.is_checked()
            attempts_made += 1
        self.omni_driver.wait(1)
        new_state = checkbox_element.is_checked()
        self.log.info(
            f"After click, check box state: {new_state} but expected was {check}"
        )
        state_match = new_state == check
        assert (
            state_match
        ), f"Multiply Color Value by Alpha Composite checkbox is not getting toggled to {check}"

    def toggle_convert_refraction_to_opacity(self, check=True):
        """Toggles the Convert Refraction to Opacity checkbox.

        Args:
            check (bool): True to enable conversion of refraction to opacity, False to disable.
        """
        self._toggle_xr_compositing_frame_enabled()
        checkboxes = self.omni_driver.find_elements(self._xr_compositing_all_checkboxes)
        checkbox_element = checkboxes[5]
        current_state = checkbox_element.is_checked()
        self.omni_driver.wait(1)
        attempts = 10
        attempts_made = 0
        while current_state != check and attempts_made <= attempts:
            checkbox_element.click()
            self.omni_driver.wait(2)
            current_state = checkbox_element.is_checked()
            attempts_made += 1
        self.omni_driver.wait(1)
        new_state = checkbox_element.is_checked()
        self.log.info(
            f"After click, check box state: {new_state} but expected was {check}"
        )
        state_match = new_state == check
        assert (
            state_match
        ), f"Convert Refraction to Opacity checkbox is not getting toggled to {check}"
