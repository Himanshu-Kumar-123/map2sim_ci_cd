# This file contains constants that are used in the project

import os
from fwk.shared.variables_util import varc

# UI Automator version
AUTOMATOR_VERSION = "0.1.31"

# Timeout for map2sim and dsrs app launch and scenario launch
# NOTE: Custom --timeout flag in TOML only affects scenario launch timeout
# App launch timeout always uses the default values below
MAP2SIM_LAUNCH_TIMEOUT = 7200
DSRS_LAUNCH_TIMEOUT = 150
MAP2SIM_SCENARIO_LAUNCH_TIMEOUT = 7200
DSRS_SCENARIO_LAUNCH_TIMEOUT = 150

# Log level for main runner
MAIN_RUNNER_LOG_LEVEL = 'DEBUG'

# App launch log file name for dsrs and map2sim
KIT_PROCESS_NAME = 'kit.exe'
DSRS_LAUNCH_LOG_FILE_NAME = 'dsrs_sim_launch_logs.txt'
MAP2SIM_LAUNCH_LOG_FILE_NAME = 'map2sim_launch_logs.txt'

# Scenario launch log file name for dsrs and map2sim
DSRS_SCENARIO_LAUNCH_LOG_FILE_NAME = 'dsrs_scenario_launch_logs.txt'
MAP2SIM_SCENARIO_LAUNCH_LOG_FILE_NAME = 'map2sim_scenario_launch_logs.txt'

# Scenario type for dsrs and map2sim
# We can update this to add more scenario types in future
DSRS_SCENARIO_TYPE = 'DSRS'
MAP2SIM_SCENARIO_TYPE = 'MAP2SIM'

# pytest root directory
PYTEST_ROOT_DIR = os.path.join(varc.cwd, "simready_test_fwk") if varc.cwd else None

# ffmpeg files
FFMPEG_VIDEO_FILE_NAME = "test_video.mp4"
FFMPEG_LOG_FILE_NAME = "ffmpeg_log.txt"
FFMPEG_LOG_FILE_PATH = os.path.join(varc.test_videos_path, FFMPEG_LOG_FILE_NAME) if varc.test_videos_path else None

# Scenario success message list (legacy, no longer used for verdicts)
SCENARIO_SUCCESS_MESSAGE_LIST = ["scenario is successful"]
