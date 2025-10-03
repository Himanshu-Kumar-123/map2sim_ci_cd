__copyright__ = "Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved."
__license__ = """
NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""

import os
import sys

import omni.drivesim.runtime_autotests as rat

obj = rat.RuntimeAutoTestsWrapper()

scenario = ""
if len(sys.argv) > 1:
    scenario = sys.argv[1]
elif os.getenv("DS_AUTOTEST_SCENARIO") is not None:
    scenario = os.getenv("DS_AUTOTEST_SCENARIO")
else:
    obj.printStringImmediate(
        "Unable to run " + sys.argv[0] + " missing scenario argument or DS_AUTOTEST_SCENARIO envrionment variable"
    )
    exit()

scenario_stops_itself = False
if "--scenario_stops_itself" in sys.argv:
    scenario_stops_itself = True

# immediate output to log
obj.printStringImmediate("Queuing autotest using script " + sys.argv[0] + " for map " + scenario)

# queued steps will run once sim is initialized
obj.startTest()
obj.printString("Loading")
obj.scenarioLoad(str(scenario))
# wait a few seconds after the load before starting the init.
obj.waitRealTimeMs(3000)
obj.printString("Init")
obj.scenarioInit()
# obj.printString("Enabling Pertracker Logging")
# obj.enablePerfTrackerLogging(True)
if scenario_stops_itself:
    obj.printString("Play")
    obj.scenarioPlay()
    obj.waitOnScenarioState("eRunning", 800000)
    # We need to wait until success or test timeout. Since it is unclear how to do
    # that, give it a day to stop itself and return to loading state. Test timeout
    # should occur before then assuming we don't run multiday tests with this script.
    obj.waitOnScenarioState("eLoading", 24 * 3600 * 1000)
else:
    obj.printString("Play")
    obj.waitOnScenarioState("eLoading", 800000)
    obj.scenarioPlay()
    obj.waitOnScenarioState("eRunning", 800000)
    stop_time_s = 100
    stop_time_ms = stop_time_s * 1000
    obj.waitRealTimeMs(stop_time_ms)
    obj.printString("Stop")
    obj.scenarioStop()
    obj.waitRealTimeMs(1000)
obj.endTest()
obj.waitRealTimeMs(3000)
obj.printString("Shutdown")
obj.waitOnScenarioState("eLoading", 800000)
obj.shutdown()