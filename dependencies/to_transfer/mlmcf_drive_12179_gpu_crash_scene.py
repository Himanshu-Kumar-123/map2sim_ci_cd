import py_drivesim2.scenarios.api
import pxr.Gf


remote_ip = "127.0.0.1"
remote_port = "1066"
scenario_context = py_drivesim2.scenarios.api.ScenarioContext(remote_ip, remote_port)
if not scenario_context.ok():
   error_message = scenario_context.error_message()
   print("Error initializing py_drivesim2: " + error_message + ", quitting")
   quit()

#action: 1
action_1=py_drivesim2.scenarios.api.ActionControl(control="close_stage")
action_1_sim_control=scenario_context.control(action_1,None,None)
scenario_context.publish_sync(action_1_sim_control)

#action: 2
action_2=py_drivesim2.scenarios.api.ActionSetMap(map_asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/usa/scene_oval/levels/main/main.usd",xodr="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/usa/scene_oval/levels/main/main.xodr",force_reload=False,enabled_payloads=['*'])
action_2_sim_control=scenario_context.control(action_2,None,None)
scenario_context.publish_sync(action_2_sim_control)

#action: 3
action_3=py_drivesim2.scenarios.api.ActionGlobalOlcToggle(olc_enabled=False)
action_3_sim_control=scenario_context.control(action_3,None,None)
scenario_context.publish_async(action_3_sim_control)

#action: 4
action_4=py_drivesim2.scenarios.api.ActionSetWeatherState(foginess=0.01,cloudiness=0.13013909519505804,transition_duration=0)
action_4_sim_control=scenario_context.control(action_4,None,None)
scenario_context.publish_async(action_4_sim_control)

#action: 5
action_5=py_drivesim2.scenarios.api.ActionPass()
action_5_sim_control=scenario_context.control(action_5,None,None)
scenario_context.publish_async(action_5_sim_control)

#action: 6
action_6=py_drivesim2.scenarios.api.ActionSetWeatherState(foginess=0.05968005577837321,cloudiness=0.13013909519505804,transition_duration=0)
action_6_sim_control=scenario_context.control(action_6,None,None)
scenario_context.publish_async(action_6_sim_control)

#action: 7
action_7=py_drivesim2.scenarios.api.ActionSetSun(elevation_angle=2.94,azimuth_angle=241.72)
action_7_sim_control=scenario_context.control(action_7,None,None)
scenario_context.publish_async(action_7_sim_control)

#action: 8
action_8_0_transform=py_drivesim2.scenarios.api.TransformRls(road_id=3,lane_id=1,lane_s=993.9537713963409)
action_8_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_8=py_drivesim2.scenarios.api.ActionImportEgo(transform=action_8_0_transform,cartesian_offset=action_8_0_cartesianOffset,asset="omniverse://drivesim2-rel.ov.nvidia.com/Projects/ds2_scenarios/Users/jjoo/sdg_vehicle_mb_sclass2021-v223-h81-8cam-042723-sm.usda",name="Ego")
action_8_sim_control=scenario_context.control(action_8,None,None)
scenario_context.publish_sync(action_8_sim_control)

#action: 9
action_9=py_drivesim2.scenarios.api.ActionSetEntityParam(name="Ego")
action_9.set_driving_state("drive")
action_9_sim_control=scenario_context.control(action_9,None,None)
scenario_context.publish_async(action_9_sim_control)

#action: 10
action_10=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="Ego",km_per_hour=60.282489596818856,disregard_longitudinal_safety=False)
action_10_sim_control=scenario_context.control(action_10,None,None)
scenario_context.publish_async(action_10_sim_control)

#action: 11
action_11=py_drivesim2.scenarios.api.ActionVehicleUI(name="Ego",event="ACC_RES_CNCL")
action_11_sim_control=scenario_context.control(action_11,None,None)
scenario_context.publish_async(action_11_sim_control)

#action: 12
action_12=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="Ego",km_per_hour=64.35999999999999,disregard_longitudinal_safety=False)
action_12_sim_control=scenario_context.control(action_12,None,None)
scenario_context.publish_async(action_12_sim_control)

#action: 13
action_13_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=0,delta_longitude=-30)
action_13_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_13=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_13_0_transform,cartesian_offset=action_13_0_cartesianOffset,entity_id=1,name="moreactor0",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_13_sim_control=scenario_context.control(action_13,None,None)
scenario_context.publish_async(action_13_sim_control)

#action: 14
action_14=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor0",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_14_sim_control=scenario_context.control(action_14,None,None)
scenario_context.publish_async(action_14_sim_control)

#action: 15
action_15_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=0,delta_longitude=30)
action_15_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_15=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_15_0_transform,cartesian_offset=action_15_0_cartesianOffset,entity_id=2,name="moreactor1",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_15_sim_control=scenario_context.control(action_15,None,None)
scenario_context.publish_async(action_15_sim_control)

#action: 16
action_16=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor1",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_16_sim_control=scenario_context.control(action_16,None,None)
scenario_context.publish_async(action_16_sim_control)

#action: 17
action_17_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=0,delta_longitude=50)
action_17_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_17=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_17_0_transform,cartesian_offset=action_17_0_cartesianOffset,entity_id=3,name="moreactor2",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_17_sim_control=scenario_context.control(action_17,None,None)
scenario_context.publish_async(action_17_sim_control)

#action: 18
action_18=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor2",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_18_sim_control=scenario_context.control(action_18,None,None)
scenario_context.publish_async(action_18_sim_control)

#action: 19
action_19_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=-15)
action_19_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_19=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_19_0_transform,cartesian_offset=action_19_0_cartesianOffset,entity_id=4,name="moreactor3",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_19_sim_control=scenario_context.control(action_19,None,None)
scenario_context.publish_async(action_19_sim_control)

#action: 20
action_20=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor3",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_20_sim_control=scenario_context.control(action_20,None,None)
scenario_context.publish_async(action_20_sim_control)

#action: 21
action_21_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=-35)
action_21_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_21=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_21_0_transform,cartesian_offset=action_21_0_cartesianOffset,entity_id=5,name="moreactor4",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_21_sim_control=scenario_context.control(action_21,None,None)
scenario_context.publish_async(action_21_sim_control)

#action: 22
action_22=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor4",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_22_sim_control=scenario_context.control(action_22,None,None)
scenario_context.publish_async(action_22_sim_control)

#action: 23
action_23_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=5)
action_23_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_23=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_23_0_transform,cartesian_offset=action_23_0_cartesianOffset,entity_id=6,name="moreactor5",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_23_sim_control=scenario_context.control(action_23,None,None)
scenario_context.publish_async(action_23_sim_control)

#action: 24
action_24=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor5",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_24_sim_control=scenario_context.control(action_24,None,None)
scenario_context.publish_async(action_24_sim_control)

#action: 25
action_25_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=70)
action_25_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_25=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_25_0_transform,cartesian_offset=action_25_0_cartesianOffset,entity_id=7,name="moreactor6",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_25_sim_control=scenario_context.control(action_25,None,None)
scenario_context.publish_async(action_25_sim_control)

#action: 26
action_26=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor6",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_26_sim_control=scenario_context.control(action_26,None,None)
scenario_context.publish_async(action_26_sim_control)

#action: 27
action_27_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=110)
action_27_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_27=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_27_0_transform,cartesian_offset=action_27_0_cartesianOffset,entity_id=8,name="moreactor7",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_27_sim_control=scenario_context.control(action_27,None,None)
scenario_context.publish_async(action_27_sim_control)

#action: 28
action_28=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor7",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_28_sim_control=scenario_context.control(action_28,None,None)
scenario_context.publish_async(action_28_sim_control)

#action: 29
action_29_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=180)
action_29_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_29=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_29_0_transform,cartesian_offset=action_29_0_cartesianOffset,entity_id=9,name="moreactor8",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_29_sim_control=scenario_context.control(action_29,None,None)
scenario_context.publish_async(action_29_sim_control)

#action: 30
action_30=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor8",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_30_sim_control=scenario_context.control(action_30,None,None)
scenario_context.publish_async(action_30_sim_control)

#action: 31
action_31_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=-60)
action_31_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_31=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_31_0_transform,cartesian_offset=action_31_0_cartesianOffset,entity_id=10,name="moreactor9",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_31_sim_control=scenario_context.control(action_31,None,None)
scenario_context.publish_async(action_31_sim_control)

#action: 32
action_32=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor9",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_32_sim_control=scenario_context.control(action_32,None,None)
scenario_context.publish_async(action_32_sim_control)

#action: 33
action_33_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=-90)
action_33_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_33=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_33_0_transform,cartesian_offset=action_33_0_cartesianOffset,entity_id=11,name="moreactor10",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_33_sim_control=scenario_context.control(action_33,None,None)
scenario_context.publish_async(action_33_sim_control)

#action: 34
action_34=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor10",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_34_sim_control=scenario_context.control(action_34,None,None)
scenario_context.publish_async(action_34_sim_control)

#action: 35
action_35_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=-130)
action_35_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_35=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_35_0_transform,cartesian_offset=action_35_0_cartesianOffset,entity_id=12,name="moreactor11",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_35_sim_control=scenario_context.control(action_35,None,None)
scenario_context.publish_async(action_35_sim_control)

#action: 36
action_36=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor11",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_36_sim_control=scenario_context.control(action_36,None,None)
scenario_context.publish_async(action_36_sim_control)

#action: 37
action_37_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=2,delta_longitude=-200)
action_37_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_37=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_37_0_transform,cartesian_offset=action_37_0_cartesianOffset,entity_id=13,name="moreactor12",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_37_sim_control=scenario_context.control(action_37,None,None)
scenario_context.publish_async(action_37_sim_control)

#action: 38
action_38=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor12",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_38_sim_control=scenario_context.control(action_38,None,None)
scenario_context.publish_async(action_38_sim_control)

#action: 39
action_39_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=2,delta_longitude=-100)
action_39_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_39=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_39_0_transform,cartesian_offset=action_39_0_cartesianOffset,entity_id=14,name="moreactor13",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/infiniti/g37_sedan/2009/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_39_sim_control=scenario_context.control(action_39,None,None)
scenario_context.publish_async(action_39_sim_control)

#action: 40
action_40=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor13",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_40_sim_control=scenario_context.control(action_40,None,None)
scenario_context.publish_async(action_40_sim_control)

#action: 41
action_41_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=2,delta_longitude=35)
action_41_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_41=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_41_0_transform,cartesian_offset=action_41_0_cartesianOffset,entity_id=15,name="moreactor14",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_41_sim_control=scenario_context.control(action_41,None,None)
scenario_context.publish_async(action_41_sim_control)

#action: 42
action_42=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor14",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_42_sim_control=scenario_context.control(action_42,None,None)
scenario_context.publish_async(action_42_sim_control)

#action: 43
action_43_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=2,delta_longitude=150)
action_43_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_43=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_43_0_transform,cartesian_offset=action_43_0_cartesianOffset,entity_id=16,name="moreactor15",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_43_sim_control=scenario_context.control(action_43,None,None)
scenario_context.publish_async(action_43_sim_control)

#action: 44
action_44=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor15",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_44_sim_control=scenario_context.control(action_44,None,None)
scenario_context.publish_async(action_44_sim_control)

#action: 45
action_45_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=2,delta_longitude=250)
action_45_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_45=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_45_0_transform,cartesian_offset=action_45_0_cartesianOffset,entity_id=17,name="moreactor16",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_45_sim_control=scenario_context.control(action_45,None,None)
scenario_context.publish_async(action_45_sim_control)

#action: 46
action_46=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor16",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_46_sim_control=scenario_context.control(action_46,None,None)
scenario_context.publish_async(action_46_sim_control)

#action: 47
action_47_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=130)
action_47_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_47=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_47_0_transform,cartesian_offset=action_47_0_cartesianOffset,entity_id=18,name="moreactor17",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_47_sim_control=scenario_context.control(action_47,None,None)
scenario_context.publish_async(action_47_sim_control)

#action: 48
action_48=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor17",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_48_sim_control=scenario_context.control(action_48,None,None)
scenario_context.publish_async(action_48_sim_control)

#action: 49
action_49_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=50)
action_49_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_49=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_49_0_transform,cartesian_offset=action_49_0_cartesianOffset,entity_id=19,name="moreactor18",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_49_sim_control=scenario_context.control(action_49,None,None)
scenario_context.publish_async(action_49_sim_control)

#action: 50
action_50=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor18",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_50_sim_control=scenario_context.control(action_50,None,None)
scenario_context.publish_async(action_50_sim_control)

#action: 51
action_51_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-50)
action_51_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_51=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_51_0_transform,cartesian_offset=action_51_0_cartesianOffset,entity_id=20,name="moreactor19",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_51_sim_control=scenario_context.control(action_51,None,None)
scenario_context.publish_async(action_51_sim_control)

#action: 52
action_52=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor19",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_52_sim_control=scenario_context.control(action_52,None,None)
scenario_context.publish_async(action_52_sim_control)

#action: 53
action_53_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-85)
action_53_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_53=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_53_0_transform,cartesian_offset=action_53_0_cartesianOffset,entity_id=21,name="moreactor20",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_53_sim_control=scenario_context.control(action_53,None,None)
scenario_context.publish_async(action_53_sim_control)

#action: 54
action_54=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor20",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_54_sim_control=scenario_context.control(action_54,None,None)
scenario_context.publish_async(action_54_sim_control)

#action: 55
action_55_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-188)
action_55_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_55=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_55_0_transform,cartesian_offset=action_55_0_cartesianOffset,entity_id=22,name="moreactor21",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_55_sim_control=scenario_context.control(action_55,None,None)
scenario_context.publish_async(action_55_sim_control)

#action: 56
action_56=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor21",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_56_sim_control=scenario_context.control(action_56,None,None)
scenario_context.publish_async(action_56_sim_control)

#action: 57
action_57_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-264)
action_57_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_57=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_57_0_transform,cartesian_offset=action_57_0_cartesianOffset,entity_id=23,name="moreactor22",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_57_sim_control=scenario_context.control(action_57,None,None)
scenario_context.publish_async(action_57_sim_control)

#action: 58
action_58=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor22",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_58_sim_control=scenario_context.control(action_58,None,None)
scenario_context.publish_async(action_58_sim_control)

#action: 59
action_59_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-355)
action_59_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_59=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_59_0_transform,cartesian_offset=action_59_0_cartesianOffset,entity_id=24,name="moreactor23",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_59_sim_control=scenario_context.control(action_59,None,None)
scenario_context.publish_async(action_59_sim_control)

#action: 60
action_60=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor23",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_60_sim_control=scenario_context.control(action_60,None,None)
scenario_context.publish_async(action_60_sim_control)

#action: 61
action_61_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-407)
action_61_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_61=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_61_0_transform,cartesian_offset=action_61_0_cartesianOffset,entity_id=25,name="moreactor24",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_61_sim_control=scenario_context.control(action_61,None,None)
scenario_context.publish_async(action_61_sim_control)

#action: 62
action_62=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor24",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_62_sim_control=scenario_context.control(action_62,None,None)
scenario_context.publish_async(action_62_sim_control)

#action: 63
action_63_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-450)
action_63_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_63=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_63_0_transform,cartesian_offset=action_63_0_cartesianOffset,entity_id=26,name="moreactor25",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_63_sim_control=scenario_context.control(action_63,None,None)
scenario_context.publish_async(action_63_sim_control)

#action: 64
action_64=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor25",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_64_sim_control=scenario_context.control(action_64,None,None)
scenario_context.publish_async(action_64_sim_control)

#action: 65
action_65_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-536)
action_65_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_65=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_65_0_transform,cartesian_offset=action_65_0_cartesianOffset,entity_id=27,name="moreactor26",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_65_sim_control=scenario_context.control(action_65,None,None)
scenario_context.publish_async(action_65_sim_control)

#action: 66
action_66=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor26",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_66_sim_control=scenario_context.control(action_66,None,None)
scenario_context.publish_async(action_66_sim_control)

#action: 67
action_67_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-635)
action_67_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_67=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_67_0_transform,cartesian_offset=action_67_0_cartesianOffset,entity_id=28,name="moreactor27",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_67_sim_control=scenario_context.control(action_67,None,None)
scenario_context.publish_async(action_67_sim_control)

#action: 68
action_68=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor27",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_68_sim_control=scenario_context.control(action_68,None,None)
scenario_context.publish_async(action_68_sim_control)

#action: 69
action_69_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-685)
action_69_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_69=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_69_0_transform,cartesian_offset=action_69_0_cartesianOffset,entity_id=29,name="moreactor28",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_69_sim_control=scenario_context.control(action_69,None,None)
scenario_context.publish_async(action_69_sim_control)

#action: 70
action_70=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor28",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_70_sim_control=scenario_context.control(action_70,None,None)
scenario_context.publish_async(action_70_sim_control)

#action: 71
action_71_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-740)
action_71_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_71=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_71_0_transform,cartesian_offset=action_71_0_cartesianOffset,entity_id=30,name="moreactor29",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_71_sim_control=scenario_context.control(action_71,None,None)
scenario_context.publish_async(action_71_sim_control)

#action: 72
action_72=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor29",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_72_sim_control=scenario_context.control(action_72,None,None)
scenario_context.publish_async(action_72_sim_control)

#action: 73
action_73_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-782)
action_73_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_73=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_73_0_transform,cartesian_offset=action_73_0_cartesianOffset,entity_id=31,name="moreactor30",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_73_sim_control=scenario_context.control(action_73,None,None)
scenario_context.publish_async(action_73_sim_control)

#action: 74
action_74=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor30",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_74_sim_control=scenario_context.control(action_74,None,None)
scenario_context.publish_async(action_74_sim_control)

#action: 75
action_75_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-843)
action_75_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_75=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_75_0_transform,cartesian_offset=action_75_0_cartesianOffset,entity_id=32,name="moreactor31",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_75_sim_control=scenario_context.control(action_75,None,None)
scenario_context.publish_async(action_75_sim_control)

#action: 76
action_76=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor31",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_76_sim_control=scenario_context.control(action_76,None,None)
scenario_context.publish_async(action_76_sim_control)

#action: 77
action_77_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-898)
action_77_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_77=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_77_0_transform,cartesian_offset=action_77_0_cartesianOffset,entity_id=33,name="moreactor32",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_77_sim_control=scenario_context.control(action_77,None,None)
scenario_context.publish_async(action_77_sim_control)

#action: 78
action_78=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor32",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_78_sim_control=scenario_context.control(action_78,None,None)
scenario_context.publish_async(action_78_sim_control)

#action: 79
action_79_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-975)
action_79_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_79=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_79_0_transform,cartesian_offset=action_79_0_cartesianOffset,entity_id=34,name="moreactor33",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_79_sim_control=scenario_context.control(action_79,None,None)
scenario_context.publish_async(action_79_sim_control)

#action: 80
action_80=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor33",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_80_sim_control=scenario_context.control(action_80,None,None)
scenario_context.publish_async(action_80_sim_control)

#action: 81
action_81_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1057)
action_81_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_81=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_81_0_transform,cartesian_offset=action_81_0_cartesianOffset,entity_id=35,name="moreactor34",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_81_sim_control=scenario_context.control(action_81,None,None)
scenario_context.publish_async(action_81_sim_control)

#action: 82
action_82=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor34",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_82_sim_control=scenario_context.control(action_82,None,None)
scenario_context.publish_async(action_82_sim_control)

#action: 83
action_83_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1136)
action_83_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_83=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_83_0_transform,cartesian_offset=action_83_0_cartesianOffset,entity_id=36,name="moreactor35",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_83_sim_control=scenario_context.control(action_83,None,None)
scenario_context.publish_async(action_83_sim_control)

#action: 84
action_84=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor35",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_84_sim_control=scenario_context.control(action_84,None,None)
scenario_context.publish_async(action_84_sim_control)

#action: 85
action_85_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1194)
action_85_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_85=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_85_0_transform,cartesian_offset=action_85_0_cartesianOffset,entity_id=37,name="moreactor36",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_85_sim_control=scenario_context.control(action_85,None,None)
scenario_context.publish_async(action_85_sim_control)

#action: 86
action_86=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor36",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_86_sim_control=scenario_context.control(action_86,None,None)
scenario_context.publish_async(action_86_sim_control)

#action: 87
action_87_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1281)
action_87_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_87=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_87_0_transform,cartesian_offset=action_87_0_cartesianOffset,entity_id=38,name="moreactor37",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_87_sim_control=scenario_context.control(action_87,None,None)
scenario_context.publish_async(action_87_sim_control)

#action: 88
action_88=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor37",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_88_sim_control=scenario_context.control(action_88,None,None)
scenario_context.publish_async(action_88_sim_control)

#action: 89
action_89_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1370)
action_89_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_89=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_89_0_transform,cartesian_offset=action_89_0_cartesianOffset,entity_id=39,name="moreactor38",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_89_sim_control=scenario_context.control(action_89,None,None)
scenario_context.publish_async(action_89_sim_control)

#action: 90
action_90=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor38",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_90_sim_control=scenario_context.control(action_90,None,None)
scenario_context.publish_async(action_90_sim_control)

#action: 91
action_91_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1420)
action_91_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_91=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_91_0_transform,cartesian_offset=action_91_0_cartesianOffset,entity_id=40,name="moreactor39",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_91_sim_control=scenario_context.control(action_91,None,None)
scenario_context.publish_async(action_91_sim_control)

#action: 92
action_92=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor39",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_92_sim_control=scenario_context.control(action_92,None,None)
scenario_context.publish_async(action_92_sim_control)

#action: 93
action_93_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1501)
action_93_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_93=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_93_0_transform,cartesian_offset=action_93_0_cartesianOffset,entity_id=41,name="moreactor40",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_93_sim_control=scenario_context.control(action_93,None,None)
scenario_context.publish_async(action_93_sim_control)

#action: 94
action_94=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor40",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_94_sim_control=scenario_context.control(action_94,None,None)
scenario_context.publish_async(action_94_sim_control)

#action: 95
action_95_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1572)
action_95_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_95=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_95_0_transform,cartesian_offset=action_95_0_cartesianOffset,entity_id=42,name="moreactor41",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_95_sim_control=scenario_context.control(action_95,None,None)
scenario_context.publish_async(action_95_sim_control)

#action: 96
action_96=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor41",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_96_sim_control=scenario_context.control(action_96,None,None)
scenario_context.publish_async(action_96_sim_control)

#action: 97
action_97_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1639)
action_97_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_97=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_97_0_transform,cartesian_offset=action_97_0_cartesianOffset,entity_id=43,name="moreactor42",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_97_sim_control=scenario_context.control(action_97,None,None)
scenario_context.publish_async(action_97_sim_control)

#action: 98
action_98=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor42",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_98_sim_control=scenario_context.control(action_98,None,None)
scenario_context.publish_async(action_98_sim_control)

#action: 99
action_99_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1711)
action_99_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_99=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_99_0_transform,cartesian_offset=action_99_0_cartesianOffset,entity_id=44,name="moreactor43",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_99_sim_control=scenario_context.control(action_99,None,None)
scenario_context.publish_async(action_99_sim_control)

#action: 100
action_100=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor43",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_100_sim_control=scenario_context.control(action_100,None,None)
scenario_context.publish_async(action_100_sim_control)

#action: 101
action_101_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1765)
action_101_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_101=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_101_0_transform,cartesian_offset=action_101_0_cartesianOffset,entity_id=45,name="moreactor44",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_101_sim_control=scenario_context.control(action_101,None,None)
scenario_context.publish_async(action_101_sim_control)

#action: 102
action_102=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor44",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_102_sim_control=scenario_context.control(action_102,None,None)
scenario_context.publish_async(action_102_sim_control)

#action: 103
action_103_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1862)
action_103_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_103=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_103_0_transform,cartesian_offset=action_103_0_cartesianOffset,entity_id=46,name="moreactor45",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_103_sim_control=scenario_context.control(action_103,None,None)
scenario_context.publish_async(action_103_sim_control)

#action: 104
action_104=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor45",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_104_sim_control=scenario_context.control(action_104,None,None)
scenario_context.publish_async(action_104_sim_control)

#action: 105
action_105_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1918)
action_105_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_105=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_105_0_transform,cartesian_offset=action_105_0_cartesianOffset,entity_id=47,name="moreactor46",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_105_sim_control=scenario_context.control(action_105,None,None)
scenario_context.publish_async(action_105_sim_control)

#action: 106
action_106=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor46",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_106_sim_control=scenario_context.control(action_106,None,None)
scenario_context.publish_async(action_106_sim_control)

#action: 107
action_107_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-1994)
action_107_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_107=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_107_0_transform,cartesian_offset=action_107_0_cartesianOffset,entity_id=48,name="moreactor47",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_107_sim_control=scenario_context.control(action_107,None,None)
scenario_context.publish_async(action_107_sim_control)

#action: 108
action_108=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor47",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_108_sim_control=scenario_context.control(action_108,None,None)
scenario_context.publish_async(action_108_sim_control)

#action: 109
action_109_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2055)
action_109_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_109=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_109_0_transform,cartesian_offset=action_109_0_cartesianOffset,entity_id=49,name="moreactor48",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_109_sim_control=scenario_context.control(action_109,None,None)
scenario_context.publish_async(action_109_sim_control)

#action: 110
action_110=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor48",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_110_sim_control=scenario_context.control(action_110,None,None)
scenario_context.publish_async(action_110_sim_control)

#action: 111
action_111_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2119)
action_111_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_111=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_111_0_transform,cartesian_offset=action_111_0_cartesianOffset,entity_id=50,name="moreactor49",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_111_sim_control=scenario_context.control(action_111,None,None)
scenario_context.publish_async(action_111_sim_control)

#action: 112
action_112=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor49",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_112_sim_control=scenario_context.control(action_112,None,None)
scenario_context.publish_async(action_112_sim_control)

#action: 113
action_113_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2200)
action_113_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_113=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_113_0_transform,cartesian_offset=action_113_0_cartesianOffset,entity_id=51,name="moreactor50",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_113_sim_control=scenario_context.control(action_113,None,None)
scenario_context.publish_async(action_113_sim_control)

#action: 114
action_114=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor50",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_114_sim_control=scenario_context.control(action_114,None,None)
scenario_context.publish_async(action_114_sim_control)

#action: 115
action_115_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2287)
action_115_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_115=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_115_0_transform,cartesian_offset=action_115_0_cartesianOffset,entity_id=52,name="moreactor51",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_115_sim_control=scenario_context.control(action_115,None,None)
scenario_context.publish_async(action_115_sim_control)

#action: 116
action_116=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor51",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_116_sim_control=scenario_context.control(action_116,None,None)
scenario_context.publish_async(action_116_sim_control)

#action: 117
action_117_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2358)
action_117_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_117=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_117_0_transform,cartesian_offset=action_117_0_cartesianOffset,entity_id=53,name="moreactor52",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_117_sim_control=scenario_context.control(action_117,None,None)
scenario_context.publish_async(action_117_sim_control)

#action: 118
action_118=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor52",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_118_sim_control=scenario_context.control(action_118,None,None)
scenario_context.publish_async(action_118_sim_control)

#action: 119
action_119_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2444)
action_119_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_119=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_119_0_transform,cartesian_offset=action_119_0_cartesianOffset,entity_id=54,name="moreactor53",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_119_sim_control=scenario_context.control(action_119,None,None)
scenario_context.publish_async(action_119_sim_control)

#action: 120
action_120=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor53",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_120_sim_control=scenario_context.control(action_120,None,None)
scenario_context.publish_async(action_120_sim_control)

#action: 121
action_121_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2505)
action_121_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_121=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_121_0_transform,cartesian_offset=action_121_0_cartesianOffset,entity_id=55,name="moreactor54",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_121_sim_control=scenario_context.control(action_121,None,None)
scenario_context.publish_async(action_121_sim_control)

#action: 122
action_122=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor54",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_122_sim_control=scenario_context.control(action_122,None,None)
scenario_context.publish_async(action_122_sim_control)

#action: 123
action_123_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2601)
action_123_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_123=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_123_0_transform,cartesian_offset=action_123_0_cartesianOffset,entity_id=56,name="moreactor55",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_123_sim_control=scenario_context.control(action_123,None,None)
scenario_context.publish_async(action_123_sim_control)

#action: 124
action_124=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor55",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_124_sim_control=scenario_context.control(action_124,None,None)
scenario_context.publish_async(action_124_sim_control)

#action: 125
action_125_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2693)
action_125_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_125=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_125_0_transform,cartesian_offset=action_125_0_cartesianOffset,entity_id=57,name="moreactor56",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_125_sim_control=scenario_context.control(action_125,None,None)
scenario_context.publish_async(action_125_sim_control)

#action: 126
action_126=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor56",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_126_sim_control=scenario_context.control(action_126,None,None)
scenario_context.publish_async(action_126_sim_control)

#action: 127
action_127_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2782)
action_127_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_127=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_127_0_transform,cartesian_offset=action_127_0_cartesianOffset,entity_id=58,name="moreactor57",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_127_sim_control=scenario_context.control(action_127,None,None)
scenario_context.publish_async(action_127_sim_control)

#action: 128
action_128=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor57",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_128_sim_control=scenario_context.control(action_128,None,None)
scenario_context.publish_async(action_128_sim_control)

#action: 129
action_129_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2852)
action_129_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_129=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_129_0_transform,cartesian_offset=action_129_0_cartesianOffset,entity_id=59,name="moreactor58",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/infiniti/g37_sedan/2009/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_129_sim_control=scenario_context.control(action_129,None,None)
scenario_context.publish_async(action_129_sim_control)

#action: 130
action_130=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor58",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_130_sim_control=scenario_context.control(action_130,None,None)
scenario_context.publish_async(action_130_sim_control)

#action: 131
action_131_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2895)
action_131_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_131=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_131_0_transform,cartesian_offset=action_131_0_cartesianOffset,entity_id=60,name="moreactor59",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_131_sim_control=scenario_context.control(action_131,None,None)
scenario_context.publish_async(action_131_sim_control)

#action: 132
action_132=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor59",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_132_sim_control=scenario_context.control(action_132,None,None)
scenario_context.publish_async(action_132_sim_control)

#action: 133
action_133_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-1,delta_longitude=-2935)
action_133_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_133=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_133_0_transform,cartesian_offset=action_133_0_cartesianOffset,entity_id=61,name="moreactor60",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_133_sim_control=scenario_context.control(action_133,None,None)
scenario_context.publish_async(action_133_sim_control)

#action: 134
action_134=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor60",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_134_sim_control=scenario_context.control(action_134,None,None)
scenario_context.publish_async(action_134_sim_control)

#action: 135
action_135_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=80)
action_135_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_135=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_135_0_transform,cartesian_offset=action_135_0_cartesianOffset,entity_id=62,name="moreactor61",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_135_sim_control=scenario_context.control(action_135,None,None)
scenario_context.publish_async(action_135_sim_control)

#action: 136
action_136=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor61",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_136_sim_control=scenario_context.control(action_136,None,None)
scenario_context.publish_async(action_136_sim_control)

#action: 137
action_137_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=40)
action_137_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_137=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_137_0_transform,cartesian_offset=action_137_0_cartesianOffset,entity_id=63,name="moreactor62",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_137_sim_control=scenario_context.control(action_137,None,None)
scenario_context.publish_async(action_137_sim_control)

#action: 138
action_138=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor62",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_138_sim_control=scenario_context.control(action_138,None,None)
scenario_context.publish_async(action_138_sim_control)

#action: 139
action_139_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=5)
action_139_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_139=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_139_0_transform,cartesian_offset=action_139_0_cartesianOffset,entity_id=64,name="moreactor63",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_139_sim_control=scenario_context.control(action_139,None,None)
scenario_context.publish_async(action_139_sim_control)

#action: 140
action_140=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor63",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_140_sim_control=scenario_context.control(action_140,None,None)
scenario_context.publish_async(action_140_sim_control)

#action: 141
action_141_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-20)
action_141_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_141=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_141_0_transform,cartesian_offset=action_141_0_cartesianOffset,entity_id=65,name="moreactor64",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_141_sim_control=scenario_context.control(action_141,None,None)
scenario_context.publish_async(action_141_sim_control)

#action: 142
action_142=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor64",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_142_sim_control=scenario_context.control(action_142,None,None)
scenario_context.publish_async(action_142_sim_control)

#action: 143
action_143_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-60)
action_143_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_143=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_143_0_transform,cartesian_offset=action_143_0_cartesianOffset,entity_id=66,name="moreactor65",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_143_sim_control=scenario_context.control(action_143,None,None)
scenario_context.publish_async(action_143_sim_control)

#action: 144
action_144=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor65",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_144_sim_control=scenario_context.control(action_144,None,None)
scenario_context.publish_async(action_144_sim_control)

#action: 145
action_145_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-164)
action_145_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_145=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_145_0_transform,cartesian_offset=action_145_0_cartesianOffset,entity_id=67,name="moreactor66",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_145_sim_control=scenario_context.control(action_145,None,None)
scenario_context.publish_async(action_145_sim_control)

#action: 146
action_146=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor66",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_146_sim_control=scenario_context.control(action_146,None,None)
scenario_context.publish_async(action_146_sim_control)

#action: 147
action_147_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-219)
action_147_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_147=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_147_0_transform,cartesian_offset=action_147_0_cartesianOffset,entity_id=68,name="moreactor67",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_147_sim_control=scenario_context.control(action_147,None,None)
scenario_context.publish_async(action_147_sim_control)

#action: 148
action_148=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor67",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_148_sim_control=scenario_context.control(action_148,None,None)
scenario_context.publish_async(action_148_sim_control)

#action: 149
action_149_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-284)
action_149_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_149=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_149_0_transform,cartesian_offset=action_149_0_cartesianOffset,entity_id=69,name="moreactor68",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_149_sim_control=scenario_context.control(action_149,None,None)
scenario_context.publish_async(action_149_sim_control)

#action: 150
action_150=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor68",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_150_sim_control=scenario_context.control(action_150,None,None)
scenario_context.publish_async(action_150_sim_control)

#action: 151
action_151_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-373)
action_151_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_151=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_151_0_transform,cartesian_offset=action_151_0_cartesianOffset,entity_id=70,name="moreactor69",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_151_sim_control=scenario_context.control(action_151,None,None)
scenario_context.publish_async(action_151_sim_control)

#action: 152
action_152=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor69",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_152_sim_control=scenario_context.control(action_152,None,None)
scenario_context.publish_async(action_152_sim_control)

#action: 153
action_153_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-426)
action_153_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_153=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_153_0_transform,cartesian_offset=action_153_0_cartesianOffset,entity_id=71,name="moreactor70",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_153_sim_control=scenario_context.control(action_153,None,None)
scenario_context.publish_async(action_153_sim_control)

#action: 154
action_154=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor70",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_154_sim_control=scenario_context.control(action_154,None,None)
scenario_context.publish_async(action_154_sim_control)

#action: 155
action_155_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-471)
action_155_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_155=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_155_0_transform,cartesian_offset=action_155_0_cartesianOffset,entity_id=72,name="moreactor71",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_155_sim_control=scenario_context.control(action_155,None,None)
scenario_context.publish_async(action_155_sim_control)

#action: 156
action_156=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor71",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_156_sim_control=scenario_context.control(action_156,None,None)
scenario_context.publish_async(action_156_sim_control)

#action: 157
action_157_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-517)
action_157_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_157=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_157_0_transform,cartesian_offset=action_157_0_cartesianOffset,entity_id=73,name="moreactor72",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_157_sim_control=scenario_context.control(action_157,None,None)
scenario_context.publish_async(action_157_sim_control)

#action: 158
action_158=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor72",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_158_sim_control=scenario_context.control(action_158,None,None)
scenario_context.publish_async(action_158_sim_control)

#action: 159
action_159_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-566)
action_159_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_159=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_159_0_transform,cartesian_offset=action_159_0_cartesianOffset,entity_id=74,name="moreactor73",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_159_sim_control=scenario_context.control(action_159,None,None)
scenario_context.publish_async(action_159_sim_control)

#action: 160
action_160=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor73",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_160_sim_control=scenario_context.control(action_160,None,None)
scenario_context.publish_async(action_160_sim_control)

#action: 161
action_161_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-660)
action_161_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_161=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_161_0_transform,cartesian_offset=action_161_0_cartesianOffset,entity_id=75,name="moreactor74",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_161_sim_control=scenario_context.control(action_161,None,None)
scenario_context.publish_async(action_161_sim_control)

#action: 162
action_162=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor74",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_162_sim_control=scenario_context.control(action_162,None,None)
scenario_context.publish_async(action_162_sim_control)

#action: 163
action_163_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-729)
action_163_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_163=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_163_0_transform,cartesian_offset=action_163_0_cartesianOffset,entity_id=76,name="moreactor75",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_163_sim_control=scenario_context.control(action_163,None,None)
scenario_context.publish_async(action_163_sim_control)

#action: 164
action_164=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor75",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_164_sim_control=scenario_context.control(action_164,None,None)
scenario_context.publish_async(action_164_sim_control)

#action: 165
action_165_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-798)
action_165_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_165=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_165_0_transform,cartesian_offset=action_165_0_cartesianOffset,entity_id=77,name="moreactor76",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_165_sim_control=scenario_context.control(action_165,None,None)
scenario_context.publish_async(action_165_sim_control)

#action: 166
action_166=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor76",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_166_sim_control=scenario_context.control(action_166,None,None)
scenario_context.publish_async(action_166_sim_control)

#action: 167
action_167_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-852)
action_167_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_167=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_167_0_transform,cartesian_offset=action_167_0_cartesianOffset,entity_id=78,name="moreactor77",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_167_sim_control=scenario_context.control(action_167,None,None)
scenario_context.publish_async(action_167_sim_control)

#action: 168
action_168=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor77",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_168_sim_control=scenario_context.control(action_168,None,None)
scenario_context.publish_async(action_168_sim_control)

#action: 169
action_169_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-914)
action_169_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_169=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_169_0_transform,cartesian_offset=action_169_0_cartesianOffset,entity_id=79,name="moreactor78",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_169_sim_control=scenario_context.control(action_169,None,None)
scenario_context.publish_async(action_169_sim_control)

#action: 170
action_170=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor78",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_170_sim_control=scenario_context.control(action_170,None,None)
scenario_context.publish_async(action_170_sim_control)

#action: 171
action_171_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1012)
action_171_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_171=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_171_0_transform,cartesian_offset=action_171_0_cartesianOffset,entity_id=80,name="moreactor79",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/porsche/panamera/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_171_sim_control=scenario_context.control(action_171,None,None)
scenario_context.publish_async(action_171_sim_control)

#action: 172
action_172=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor79",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_172_sim_control=scenario_context.control(action_172,None,None)
scenario_context.publish_async(action_172_sim_control)

#action: 173
action_173_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1106)
action_173_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_173=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_173_0_transform,cartesian_offset=action_173_0_cartesianOffset,entity_id=81,name="moreactor80",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_173_sim_control=scenario_context.control(action_173,None,None)
scenario_context.publish_async(action_173_sim_control)

#action: 174
action_174=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor80",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_174_sim_control=scenario_context.control(action_174,None,None)
scenario_context.publish_async(action_174_sim_control)

#action: 175
action_175_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1169)
action_175_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_175=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_175_0_transform,cartesian_offset=action_175_0_cartesianOffset,entity_id=82,name="moreactor81",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_175_sim_control=scenario_context.control(action_175,None,None)
scenario_context.publish_async(action_175_sim_control)

#action: 176
action_176=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor81",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_176_sim_control=scenario_context.control(action_176,None,None)
scenario_context.publish_async(action_176_sim_control)

#action: 177
action_177_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1263)
action_177_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_177=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_177_0_transform,cartesian_offset=action_177_0_cartesianOffset,entity_id=83,name="moreactor82",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_177_sim_control=scenario_context.control(action_177,None,None)
scenario_context.publish_async(action_177_sim_control)

#action: 178
action_178=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor82",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_178_sim_control=scenario_context.control(action_178,None,None)
scenario_context.publish_async(action_178_sim_control)

#action: 179
action_179_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1334)
action_179_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_179=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_179_0_transform,cartesian_offset=action_179_0_cartesianOffset,entity_id=84,name="moreactor83",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_179_sim_control=scenario_context.control(action_179,None,None)
scenario_context.publish_async(action_179_sim_control)

#action: 180
action_180=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor83",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_180_sim_control=scenario_context.control(action_180,None,None)
scenario_context.publish_async(action_180_sim_control)

#action: 181
action_181_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1378)
action_181_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_181=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_181_0_transform,cartesian_offset=action_181_0_cartesianOffset,entity_id=85,name="moreactor84",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_181_sim_control=scenario_context.control(action_181,None,None)
scenario_context.publish_async(action_181_sim_control)

#action: 182
action_182=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor84",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_182_sim_control=scenario_context.control(action_182,None,None)
scenario_context.publish_async(action_182_sim_control)

#action: 183
action_183_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1423)
action_183_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_183=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_183_0_transform,cartesian_offset=action_183_0_cartesianOffset,entity_id=86,name="moreactor85",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_183_sim_control=scenario_context.control(action_183,None,None)
scenario_context.publish_async(action_183_sim_control)

#action: 184
action_184=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor85",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_184_sim_control=scenario_context.control(action_184,None,None)
scenario_context.publish_async(action_184_sim_control)

#action: 185
action_185_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1468)
action_185_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_185=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_185_0_transform,cartesian_offset=action_185_0_cartesianOffset,entity_id=87,name="moreactor86",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_185_sim_control=scenario_context.control(action_185,None,None)
scenario_context.publish_async(action_185_sim_control)

#action: 186
action_186=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor86",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_186_sim_control=scenario_context.control(action_186,None,None)
scenario_context.publish_async(action_186_sim_control)

#action: 187
action_187_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1526)
action_187_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_187=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_187_0_transform,cartesian_offset=action_187_0_cartesianOffset,entity_id=88,name="moreactor87",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/camry/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_187_sim_control=scenario_context.control(action_187,None,None)
scenario_context.publish_async(action_187_sim_control)

#action: 188
action_188=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor87",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_188_sim_control=scenario_context.control(action_188,None,None)
scenario_context.publish_async(action_188_sim_control)

#action: 189
action_189_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1590)
action_189_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_189=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_189_0_transform,cartesian_offset=action_189_0_cartesianOffset,entity_id=89,name="moreactor88",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_189_sim_control=scenario_context.control(action_189,None,None)
scenario_context.publish_async(action_189_sim_control)

#action: 190
action_190=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor88",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_190_sim_control=scenario_context.control(action_190,None,None)
scenario_context.publish_async(action_190_sim_control)

#action: 191
action_191_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1690)
action_191_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_191=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_191_0_transform,cartesian_offset=action_191_0_cartesianOffset,entity_id=90,name="moreactor89",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_191_sim_control=scenario_context.control(action_191,None,None)
scenario_context.publish_async(action_191_sim_control)

#action: 192
action_192=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor89",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_192_sim_control=scenario_context.control(action_192,None,None)
scenario_context.publish_async(action_192_sim_control)

#action: 193
action_193_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1734)
action_193_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_193=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_193_0_transform,cartesian_offset=action_193_0_cartesianOffset,entity_id=91,name="moreactor90",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/infiniti/g37_sedan/2009/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_193_sim_control=scenario_context.control(action_193,None,None)
scenario_context.publish_async(action_193_sim_control)

#action: 194
action_194=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor90",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_194_sim_control=scenario_context.control(action_194,None,None)
scenario_context.publish_async(action_194_sim_control)

#action: 195
action_195_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1808)
action_195_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_195=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_195_0_transform,cartesian_offset=action_195_0_cartesianOffset,entity_id=92,name="moreactor91",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_195_sim_control=scenario_context.control(action_195,None,None)
scenario_context.publish_async(action_195_sim_control)

#action: 196
action_196=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor91",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_196_sim_control=scenario_context.control(action_196,None,None)
scenario_context.publish_async(action_196_sim_control)

#action: 197
action_197_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1893)
action_197_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_197=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_197_0_transform,cartesian_offset=action_197_0_cartesianOffset,entity_id=93,name="moreactor92",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_197_sim_control=scenario_context.control(action_197,None,None)
scenario_context.publish_async(action_197_sim_control)

#action: 198
action_198=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor92",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_198_sim_control=scenario_context.control(action_198,None,None)
scenario_context.publish_async(action_198_sim_control)

#action: 199
action_199_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-1955)
action_199_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_199=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_199_0_transform,cartesian_offset=action_199_0_cartesianOffset,entity_id=94,name="moreactor93",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_199_sim_control=scenario_context.control(action_199,None,None)
scenario_context.publish_async(action_199_sim_control)

#action: 200
action_200=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor93",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_200_sim_control=scenario_context.control(action_200,None,None)
scenario_context.publish_async(action_200_sim_control)

#action: 201
action_201_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2041)
action_201_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_201=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_201_0_transform,cartesian_offset=action_201_0_cartesianOffset,entity_id=95,name="moreactor94",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_201_sim_control=scenario_context.control(action_201,None,None)
scenario_context.publish_async(action_201_sim_control)

#action: 202
action_202=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor94",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_202_sim_control=scenario_context.control(action_202,None,None)
scenario_context.publish_async(action_202_sim_control)

#action: 203
action_203_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2137)
action_203_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_203=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_203_0_transform,cartesian_offset=action_203_0_cartesianOffset,entity_id=96,name="moreactor95",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_203_sim_control=scenario_context.control(action_203,None,None)
scenario_context.publish_async(action_203_sim_control)

#action: 204
action_204=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor95",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_204_sim_control=scenario_context.control(action_204,None,None)
scenario_context.publish_async(action_204_sim_control)

#action: 205
action_205_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2197)
action_205_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_205=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_205_0_transform,cartesian_offset=action_205_0_cartesianOffset,entity_id=97,name="moreactor96",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_205_sim_control=scenario_context.control(action_205,None,None)
scenario_context.publish_async(action_205_sim_control)

#action: 206
action_206=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor96",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_206_sim_control=scenario_context.control(action_206,None,None)
scenario_context.publish_async(action_206_sim_control)

#action: 207
action_207_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2289)
action_207_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_207=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_207_0_transform,cartesian_offset=action_207_0_cartesianOffset,entity_id=98,name="moreactor97",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_207_sim_control=scenario_context.control(action_207,None,None)
scenario_context.publish_async(action_207_sim_control)

#action: 208
action_208=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor97",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_208_sim_control=scenario_context.control(action_208,None,None)
scenario_context.publish_async(action_208_sim_control)

#action: 209
action_209_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2385)
action_209_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_209=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_209_0_transform,cartesian_offset=action_209_0_cartesianOffset,entity_id=99,name="moreactor98",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_209_sim_control=scenario_context.control(action_209,None,None)
scenario_context.publish_async(action_209_sim_control)

#action: 210
action_210=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor98",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_210_sim_control=scenario_context.control(action_210,None,None)
scenario_context.publish_async(action_210_sim_control)

#action: 211
action_211_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2442)
action_211_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_211=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_211_0_transform,cartesian_offset=action_211_0_cartesianOffset,entity_id=100,name="moreactor99",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_211_sim_control=scenario_context.control(action_211,None,None)
scenario_context.publish_async(action_211_sim_control)

#action: 212
action_212=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor99",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_212_sim_control=scenario_context.control(action_212,None,None)
scenario_context.publish_async(action_212_sim_control)

#action: 213
action_213_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2483)
action_213_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_213=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_213_0_transform,cartesian_offset=action_213_0_cartesianOffset,entity_id=101,name="moreactor100",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_213_sim_control=scenario_context.control(action_213,None,None)
scenario_context.publish_async(action_213_sim_control)

#action: 214
action_214=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor100",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_214_sim_control=scenario_context.control(action_214,None,None)
scenario_context.publish_async(action_214_sim_control)

#action: 215
action_215_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2538)
action_215_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_215=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_215_0_transform,cartesian_offset=action_215_0_cartesianOffset,entity_id=102,name="moreactor101",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_215_sim_control=scenario_context.control(action_215,None,None)
scenario_context.publish_async(action_215_sim_control)

#action: 216
action_216=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor101",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_216_sim_control=scenario_context.control(action_216,None,None)
scenario_context.publish_async(action_216_sim_control)

#action: 217
action_217_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2606)
action_217_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_217=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_217_0_transform,cartesian_offset=action_217_0_cartesianOffset,entity_id=103,name="moreactor102",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_217_sim_control=scenario_context.control(action_217,None,None)
scenario_context.publish_async(action_217_sim_control)

#action: 218
action_218=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor102",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_218_sim_control=scenario_context.control(action_218,None,None)
scenario_context.publish_async(action_218_sim_control)

#action: 219
action_219_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2646)
action_219_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_219=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_219_0_transform,cartesian_offset=action_219_0_cartesianOffset,entity_id=104,name="moreactor103",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_219_sim_control=scenario_context.control(action_219,None,None)
scenario_context.publish_async(action_219_sim_control)

#action: 220
action_220=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor103",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_220_sim_control=scenario_context.control(action_220,None,None)
scenario_context.publish_async(action_220_sim_control)

#action: 221
action_221_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2717)
action_221_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_221=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_221_0_transform,cartesian_offset=action_221_0_cartesianOffset,entity_id=105,name="moreactor104",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_221_sim_control=scenario_context.control(action_221,None,None)
scenario_context.publish_async(action_221_sim_control)

#action: 222
action_222=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor104",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_222_sim_control=scenario_context.control(action_222,None,None)
scenario_context.publish_async(action_222_sim_control)

#action: 223
action_223_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-2,delta_longitude=-2765)
action_223_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_223=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_223_0_transform,cartesian_offset=action_223_0_cartesianOffset,entity_id=106,name="moreactor105",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_223_sim_control=scenario_context.control(action_223,None,None)
scenario_context.publish_async(action_223_sim_control)

#action: 224
action_224=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor105",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_224_sim_control=scenario_context.control(action_224,None,None)
scenario_context.publish_async(action_224_sim_control)

#action: 225
action_225_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-70)
action_225_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_225=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_225_0_transform,cartesian_offset=action_225_0_cartesianOffset,entity_id=107,name="moreactor106",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/hatchback_5door/2019/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_225_sim_control=scenario_context.control(action_225,None,None)
scenario_context.publish_async(action_225_sim_control)

#action: 226
action_226=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor106",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_226_sim_control=scenario_context.control(action_226,None,None)
scenario_context.publish_async(action_226_sim_control)

#action: 227
action_227_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-170)
action_227_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_227=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_227_0_transform,cartesian_offset=action_227_0_cartesianOffset,entity_id=108,name="moreactor107",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_227_sim_control=scenario_context.control(action_227,None,None)
scenario_context.publish_async(action_227_sim_control)

#action: 228
action_228=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor107",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_228_sim_control=scenario_context.control(action_228,None,None)
scenario_context.publish_async(action_228_sim_control)

#action: 229
action_229_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-211)
action_229_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_229=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_229_0_transform,cartesian_offset=action_229_0_cartesianOffset,entity_id=109,name="moreactor108",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class_nvidia/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_229_sim_control=scenario_context.control(action_229,None,None)
scenario_context.publish_async(action_229_sim_control)

#action: 230
action_230=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor108",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_230_sim_control=scenario_context.control(action_230,None,None)
scenario_context.publish_async(action_230_sim_control)

#action: 231
action_231_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-251)
action_231_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_231=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_231_0_transform,cartesian_offset=action_231_0_cartesianOffset,entity_id=110,name="moreactor109",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/infiniti/g37_sedan/2009/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_231_sim_control=scenario_context.control(action_231,None,None)
scenario_context.publish_async(action_231_sim_control)

#action: 232
action_232=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor109",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_232_sim_control=scenario_context.control(action_232,None,None)
scenario_context.publish_async(action_232_sim_control)

#action: 233
action_233_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-318)
action_233_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_233=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_233_0_transform,cartesian_offset=action_233_0_cartesianOffset,entity_id=111,name="moreactor110",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class_nvidia/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_233_sim_control=scenario_context.control(action_233,None,None)
scenario_context.publish_async(action_233_sim_control)

#action: 234
action_234=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor110",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_234_sim_control=scenario_context.control(action_234,None,None)
scenario_context.publish_async(action_234_sim_control)

#action: 235
action_235_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-404)
action_235_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_235=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_235_0_transform,cartesian_offset=action_235_0_cartesianOffset,entity_id=112,name="moreactor111",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_235_sim_control=scenario_context.control(action_235,None,None)
scenario_context.publish_async(action_235_sim_control)

#action: 236
action_236=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor111",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_236_sim_control=scenario_context.control(action_236,None,None)
scenario_context.publish_async(action_236_sim_control)

#action: 237
action_237_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-450)
action_237_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_237=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_237_0_transform,cartesian_offset=action_237_0_cartesianOffset,entity_id=113,name="moreactor112",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_237_sim_control=scenario_context.control(action_237,None,None)
scenario_context.publish_async(action_237_sim_control)

#action: 238
action_238=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor112",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_238_sim_control=scenario_context.control(action_238,None,None)
scenario_context.publish_async(action_238_sim_control)

#action: 239
action_239_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-531)
action_239_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_239=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_239_0_transform,cartesian_offset=action_239_0_cartesianOffset,entity_id=114,name="moreactor113",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_239_sim_control=scenario_context.control(action_239,None,None)
scenario_context.publish_async(action_239_sim_control)

#action: 240
action_240=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor113",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_240_sim_control=scenario_context.control(action_240,None,None)
scenario_context.publish_async(action_240_sim_control)

#action: 241
action_241_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-589)
action_241_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_241=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_241_0_transform,cartesian_offset=action_241_0_cartesianOffset,entity_id=115,name="moreactor114",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class_nvidia/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_241_sim_control=scenario_context.control(action_241,None,None)
scenario_context.publish_async(action_241_sim_control)

#action: 242
action_242=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor114",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_242_sim_control=scenario_context.control(action_242,None,None)
scenario_context.publish_async(action_242_sim_control)

#action: 243
action_243_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-644)
action_243_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_243=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_243_0_transform,cartesian_offset=action_243_0_cartesianOffset,entity_id=116,name="moreactor115",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_243_sim_control=scenario_context.control(action_243,None,None)
scenario_context.publish_async(action_243_sim_control)

#action: 244
action_244=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor115",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_244_sim_control=scenario_context.control(action_244,None,None)
scenario_context.publish_async(action_244_sim_control)

#action: 245
action_245_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-685)
action_245_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_245=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_245_0_transform,cartesian_offset=action_245_0_cartesianOffset,entity_id=117,name="moreactor116",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_245_sim_control=scenario_context.control(action_245,None,None)
scenario_context.publish_async(action_245_sim_control)

#action: 246
action_246=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor116",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_246_sim_control=scenario_context.control(action_246,None,None)
scenario_context.publish_async(action_246_sim_control)

#action: 247
action_247_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-769)
action_247_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_247=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_247_0_transform,cartesian_offset=action_247_0_cartesianOffset,entity_id=118,name="moreactor117",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_247_sim_control=scenario_context.control(action_247,None,None)
scenario_context.publish_async(action_247_sim_control)

#action: 248
action_248=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor117",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_248_sim_control=scenario_context.control(action_248,None,None)
scenario_context.publish_async(action_248_sim_control)

#action: 249
action_249_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-849)
action_249_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_249=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_249_0_transform,cartesian_offset=action_249_0_cartesianOffset,entity_id=119,name="moreactor118",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/ford/fusion/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_249_sim_control=scenario_context.control(action_249,None,None)
scenario_context.publish_async(action_249_sim_control)

#action: 250
action_250=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor118",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_250_sim_control=scenario_context.control(action_250,None,None)
scenario_context.publish_async(action_250_sim_control)

#action: 251
action_251_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-943)
action_251_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_251=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_251_0_transform,cartesian_offset=action_251_0_cartesianOffset,entity_id=120,name="moreactor119",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/porsche/panamera/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_251_sim_control=scenario_context.control(action_251,None,None)
scenario_context.publish_async(action_251_sim_control)

#action: 252
action_252=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor119",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_252_sim_control=scenario_context.control(action_252,None,None)
scenario_context.publish_async(action_252_sim_control)

#action: 253
action_253_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1033)
action_253_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_253=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_253_0_transform,cartesian_offset=action_253_0_cartesianOffset,entity_id=121,name="moreactor120",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_253_sim_control=scenario_context.control(action_253,None,None)
scenario_context.publish_async(action_253_sim_control)

#action: 254
action_254=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor120",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_254_sim_control=scenario_context.control(action_254,None,None)
scenario_context.publish_async(action_254_sim_control)

#action: 255
action_255_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1118)
action_255_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_255=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_255_0_transform,cartesian_offset=action_255_0_cartesianOffset,entity_id=122,name="moreactor121",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/infiniti/g37_sedan/2009/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_255_sim_control=scenario_context.control(action_255,None,None)
scenario_context.publish_async(action_255_sim_control)

#action: 256
action_256=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor121",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_256_sim_control=scenario_context.control(action_256,None,None)
scenario_context.publish_async(action_256_sim_control)

#action: 257
action_257_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1196)
action_257_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_257=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_257_0_transform,cartesian_offset=action_257_0_cartesianOffset,entity_id=123,name="moreactor122",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class_nvidia/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_257_sim_control=scenario_context.control(action_257,None,None)
scenario_context.publish_async(action_257_sim_control)

#action: 258
action_258=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor122",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_258_sim_control=scenario_context.control(action_258,None,None)
scenario_context.publish_async(action_258_sim_control)

#action: 259
action_259_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1259)
action_259_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_259=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_259_0_transform,cartesian_offset=action_259_0_cartesianOffset,entity_id=124,name="moreactor123",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_259_sim_control=scenario_context.control(action_259,None,None)
scenario_context.publish_async(action_259_sim_control)

#action: 260
action_260=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor123",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_260_sim_control=scenario_context.control(action_260,None,None)
scenario_context.publish_async(action_260_sim_control)

#action: 261
action_261_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1346)
action_261_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_261=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_261_0_transform,cartesian_offset=action_261_0_cartesianOffset,entity_id=125,name="moreactor124",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_261_sim_control=scenario_context.control(action_261,None,None)
scenario_context.publish_async(action_261_sim_control)

#action: 262
action_262=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor124",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_262_sim_control=scenario_context.control(action_262,None,None)
scenario_context.publish_async(action_262_sim_control)

#action: 263
action_263_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1393)
action_263_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_263=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_263_0_transform,cartesian_offset=action_263_0_cartesianOffset,entity_id=126,name="moreactor125",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_263_sim_control=scenario_context.control(action_263,None,None)
scenario_context.publish_async(action_263_sim_control)

#action: 264
action_264=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor125",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_264_sim_control=scenario_context.control(action_264,None,None)
scenario_context.publish_async(action_264_sim_control)

#action: 265
action_265_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1451)
action_265_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_265=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_265_0_transform,cartesian_offset=action_265_0_cartesianOffset,entity_id=127,name="moreactor126",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_265_sim_control=scenario_context.control(action_265,None,None)
scenario_context.publish_async(action_265_sim_control)

#action: 266
action_266=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor126",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_266_sim_control=scenario_context.control(action_266,None,None)
scenario_context.publish_async(action_266_sim_control)

#action: 267
action_267_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1508)
action_267_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_267=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_267_0_transform,cartesian_offset=action_267_0_cartesianOffset,entity_id=128,name="moreactor127",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_267_sim_control=scenario_context.control(action_267,None,None)
scenario_context.publish_async(action_267_sim_control)

#action: 268
action_268=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor127",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_268_sim_control=scenario_context.control(action_268,None,None)
scenario_context.publish_async(action_268_sim_control)

#action: 269
action_269_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1587)
action_269_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_269=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_269_0_transform,cartesian_offset=action_269_0_cartesianOffset,entity_id=129,name="moreactor128",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_269_sim_control=scenario_context.control(action_269,None,None)
scenario_context.publish_async(action_269_sim_control)

#action: 270
action_270=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor128",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_270_sim_control=scenario_context.control(action_270,None,None)
scenario_context.publish_async(action_270_sim_control)

#action: 271
action_271_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1639)
action_271_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_271=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_271_0_transform,cartesian_offset=action_271_0_cartesianOffset,entity_id=130,name="moreactor129",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_271_sim_control=scenario_context.control(action_271,None,None)
scenario_context.publish_async(action_271_sim_control)

#action: 272
action_272=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor129",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_272_sim_control=scenario_context.control(action_272,None,None)
scenario_context.publish_async(action_272_sim_control)

#action: 273
action_273_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1726)
action_273_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_273=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_273_0_transform,cartesian_offset=action_273_0_cartesianOffset,entity_id=131,name="moreactor130",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/s_class/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_273_sim_control=scenario_context.control(action_273,None,None)
scenario_context.publish_async(action_273_sim_control)

#action: 274
action_274=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor130",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_274_sim_control=scenario_context.control(action_274,None,None)
scenario_context.publish_async(action_274_sim_control)

#action: 275
action_275_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1797)
action_275_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_275=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_275_0_transform,cartesian_offset=action_275_0_cartesianOffset,entity_id=132,name="moreactor131",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_275_sim_control=scenario_context.control(action_275,None,None)
scenario_context.publish_async(action_275_sim_control)

#action: 276
action_276=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor131",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_276_sim_control=scenario_context.control(action_276,None,None)
scenario_context.publish_async(action_276_sim_control)

#action: 277
action_277_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1864)
action_277_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_277=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_277_0_transform,cartesian_offset=action_277_0_cartesianOffset,entity_id=133,name="moreactor132",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/accord/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_277_sim_control=scenario_context.control(action_277,None,None)
scenario_context.publish_async(action_277_sim_control)

#action: 278
action_278=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor132",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_278_sim_control=scenario_context.control(action_278,None,None)
scenario_context.publish_async(action_278_sim_control)

#action: 279
action_279_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1906)
action_279_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_279=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_279_0_transform,cartesian_offset=action_279_0_cartesianOffset,entity_id=134,name="moreactor133",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/vw/passat/2015/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_279_sim_control=scenario_context.control(action_279,None,None)
scenario_context.publish_async(action_279_sim_control)

#action: 280
action_280=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor133",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_280_sim_control=scenario_context.control(action_280,None,None)
scenario_context.publish_async(action_280_sim_control)

#action: 281
action_281_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-1947)
action_281_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_281=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_281_0_transform,cartesian_offset=action_281_0_cartesianOffset,entity_id=135,name="moreactor134",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_281_sim_control=scenario_context.control(action_281,None,None)
scenario_context.publish_async(action_281_sim_control)

#action: 282
action_282=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor134",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_282_sim_control=scenario_context.control(action_282,None,None)
scenario_context.publish_async(action_282_sim_control)

#action: 283
action_283_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2005)
action_283_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_283=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_283_0_transform,cartesian_offset=action_283_0_cartesianOffset,entity_id=136,name="moreactor135",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/lexus/is/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_283_sim_control=scenario_context.control(action_283,None,None)
scenario_context.publish_async(action_283_sim_control)

#action: 284
action_284=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor135",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_284_sim_control=scenario_context.control(action_284,None,None)
scenario_context.publish_async(action_284_sim_control)

#action: 285
action_285_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2069)
action_285_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_285=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_285_0_transform,cartesian_offset=action_285_0_cartesianOffset,entity_id=137,name="moreactor136",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/tesla/model_s/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_285_sim_control=scenario_context.control(action_285,None,None)
scenario_context.publish_async(action_285_sim_control)

#action: 286
action_286=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor136",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_286_sim_control=scenario_context.control(action_286,None,None)
scenario_context.publish_async(action_286_sim_control)

#action: 287
action_287_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2137)
action_287_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_287=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_287_0_transform,cartesian_offset=action_287_0_cartesianOffset,entity_id=138,name="moreactor137",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_287_sim_control=scenario_context.control(action_287,None,None)
scenario_context.publish_async(action_287_sim_control)

#action: 288
action_288=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor137",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_288_sim_control=scenario_context.control(action_288,None,None)
scenario_context.publish_async(action_288_sim_control)

#action: 289
action_289_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2215)
action_289_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_289=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_289_0_transform,cartesian_offset=action_289_0_cartesianOffset,entity_id=139,name="moreactor138",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2014/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_289_sim_control=scenario_context.control(action_289,None,None)
scenario_context.publish_async(action_289_sim_control)

#action: 290
action_290=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor138",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_290_sim_control=scenario_context.control(action_290,None,None)
scenario_context.publish_async(action_290_sim_control)

#action: 291
action_291_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2302)
action_291_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_291=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_291_0_transform,cartesian_offset=action_291_0_cartesianOffset,entity_id=140,name="moreactor139",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/toyota/prius/2016/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_291_sim_control=scenario_context.control(action_291,None,None)
scenario_context.publish_async(action_291_sim_control)

#action: 292
action_292=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor139",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_292_sim_control=scenario_context.control(action_292,None,None)
scenario_context.publish_async(action_292_sim_control)

#action: 293
action_293_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2390)
action_293_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_293=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_293_0_transform,cartesian_offset=action_293_0_cartesianOffset,entity_id=141,name="moreactor140",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_electric/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_293_sim_control=scenario_context.control(action_293,None,None)
scenario_context.publish_async(action_293_sim_control)

#action: 294
action_294=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor140",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_294_sim_control=scenario_context.control(action_294,None,None)
scenario_context.publish_async(action_294_sim_control)

#action: 295
action_295_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2484)
action_295_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_295=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_295_0_transform,cartesian_offset=action_295_0_cartesianOffset,entity_id=142,name="moreactor141",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_295_sim_control=scenario_context.control(action_295,None,None)
scenario_context.publish_async(action_295_sim_control)

#action: 296
action_296=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor141",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_296_sim_control=scenario_context.control(action_296,None,None)
scenario_context.publish_async(action_296_sim_control)

#action: 297
action_297_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2532)
action_297_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_297=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_297_0_transform,cartesian_offset=action_297_0_cartesianOffset,entity_id=143,name="moreactor142",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/mercedes/vision_eqs/2021/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_297_sim_control=scenario_context.control(action_297,None,None)
scenario_context.publish_async(action_297_sim_control)

#action: 298
action_298=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor142",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_298_sim_control=scenario_context.control(action_298,None,None)
scenario_context.publish_async(action_298_sim_control)

#action: 299
action_299_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2625)
action_299_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_299=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_299_0_transform,cartesian_offset=action_299_0_cartesianOffset,entity_id=144,name="moreactor143",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/generic/car_fullsize_sedan_police/2013/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_299_sim_control=scenario_context.control(action_299,None,None)
scenario_context.publish_async(action_299_sim_control)

#action: 300
action_300=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor143",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_300_sim_control=scenario_context.control(action_300,None,None)
scenario_context.publish_async(action_300_sim_control)

#action: 301
action_301_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2700)
action_301_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_301=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_301_0_transform,cartesian_offset=action_301_0_cartesianOffset,entity_id=145,name="moreactor144",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/jaguar/i_pace/2022/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_301_sim_control=scenario_context.control(action_301,None,None)
scenario_context.publish_async(action_301_sim_control)

#action: 302
action_302=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor144",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_302_sim_control=scenario_context.control(action_302,None,None)
scenario_context.publish_async(action_302_sim_control)

#action: 303
action_303_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2766)
action_303_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_303=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_303_0_transform,cartesian_offset=action_303_0_cartesianOffset,entity_id=146,name="moreactor145",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/hyundai/sonata/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_303_sim_control=scenario_context.control(action_303,None,None)
scenario_context.publish_async(action_303_sim_control)

#action: 304
action_304=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor145",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_304_sim_control=scenario_context.control(action_304,None,None)
scenario_context.publish_async(action_304_sim_control)

#action: 305
action_305_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=-3,delta_longitude=-2824)
action_305_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_305=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_305_0_transform,cartesian_offset=action_305_0_cartesianOffset,entity_id=147,name="moreactor146",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/porsche/panamera/2017/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_305_sim_control=scenario_context.control(action_305,None,None)
scenario_context.publish_async(action_305_sim_control)

#action: 306
action_306=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="moreactor146",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_306_sim_control=scenario_context.control(action_306,None,None)
scenario_context.publish_async(action_306_sim_control)

#action: 307
action_307_0_transform=py_drivesim2.scenarios.api.TransformLaneRelative(relative_entity="Ego",delta_lane=1,delta_longitude=300.0)
action_307_0_cartesianOffset=py_drivesim2.scenarios.api.TransformCartesian(translate=(0.0, 0.0, 0.0),orientation=pxr.Gf.Quatd(*(1, 0, 0, 0)))
action_307=py_drivesim2.scenarios.api.ActionAddEntity(transform=action_307_0_transform,cartesian_offset=action_307_0_cartesianOffset,entity_id=148,name="actor1",asset="{/app/drivesim/defaultNucleusRoot}/Projects/ds2_content/common_assets/vehicles/honda/civic_type_r/2018/main_with_physx.usd",entity_owners=['ReferenceTrafficModel'])
action_307_sim_control=scenario_context.control(action_307,None,None)
scenario_context.publish_async(action_307_sim_control)

#action: 308
action_308=py_drivesim2.scenarios.api.ActionMaintainSpeed(name="actor1",km_per_hour=72.405,disregard_longitudinal_safety=False)
action_308_sim_control=scenario_context.control(action_308,None,None)
scenario_context.publish_async(action_308_sim_control)

#action: 309
action_309=py_drivesim2.scenarios.api.ActionControl(control="stop_scenario")
action_309_startCondition=py_drivesim2.scenarios.api.ConditionSimulationTime(seconds=252.0,op="greater_than_or_equal_to")
action_309_sim_control=scenario_context.control(action_309,action_309_startCondition,None)
scenario_context.publish_async(action_309_sim_control)

#action: 310
action_310=py_drivesim2.scenarios.api.ActionControl(control="start_scenario")
action_310_startCondition=py_drivesim2.scenarios.api.ConditionSimulationTime(seconds=-1.0,op="greater_than_or_equal_to")
action_310_sim_control=scenario_context.control(action_310,action_310_startCondition,None)
scenario_context.publish_sync(action_310_sim_control)