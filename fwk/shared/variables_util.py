# Standard library imports
import os
from typing import Dict, List, Optional, Any
from collections import deque

class varc:
    """A class containing all variables used across the framework.
    
    This class serves as a central storage for all variables that are used by different
    functions throughout the framework. It includes configuration settings, test data,
    execution states, and various utility paths.
    """
    
    # Command line arguments and configuration
    # args contains arg parser object from which we can extract toml name
    args: Optional[Any] = None
    # toml_path is path of test toml used in test, this path has test toml file name in it at end
    toml_path: Optional[str] = None
    # toml_dict contains dict obtained from python toml->dict conversion
    toml_dict: Dict = {}
    # dmf_config_path hold path of dmf_config.toml
    dmf_config_path: Optional[str] = None
    # tests_deque is a deque of tests, used for efficient queue operations
    tests_deque: deque = deque()
    
    # Test execution data
    # contains each valid testcase data required for test execution
    tests_list: List = []
    # test_command_dict contains command executed for each testcase, this is dumped to text file and cleared after end of each testcase execution
    test_command_dict: Dict = {}
    # header_dict contains gpu info, build, nucleus, testsuite name, timestamp
    header_dict: Dict = {}
    
    # Test results and verdicts
    # verdict_decider_list contains list of error strings which when encountered in master_dict, testcase is failed
    verdict_decider_list: List = []
    
    # Cloud storage IDs
    # share_point_ids contains sharepoint id for each testcase run
    share_point_ids: Dict = {}
    # Sharepoint Graph Endpoint
    graph_api_endpoint: Optional[str] = None
    # Sharepoint testsuite id
    testsuite_id: Optional[str] = None
    
    # Cloud storage verdicts
    # share_point_verdict contains share point failure results if any
    share_point_verdict: List = []
    
    # Path configurations
    # home contains current user ~ path
    home: str = os.path.expanduser("~")
    # cwd contains path of directory where atf_runner.sh is running
    cwd: Optional[str] = None
    # variable to hold driver dump path specified by user in ENVIRONMENT section of test toml
    dump_directory: Optional[str] = None
    # test_temp_files_path contains path of directory where all temporary files related to testsuite execution is dumped
    test_temp_files_path: Optional[str] = None
    # test_suite_name contains name of testsuite in output directory, which will be used to store test data for current run
    test_suite_name: Optional[str] = None
    # test_suite_name contains path of testsuite, which will be used to store test data for current run
    test_suite_path: Optional[str] = None
    # path of text file where slack results are to be appended
    slack_report_path: Optional[str] = None
    
    # Control flags
    # skip_remaining_blocks can be used to skip all blocks at once, starting from the block where it is invoked
    skip_remaining_blocks: bool = False
    # skip_remaining_blocks_freeze is set when any string available in check_words list is encountered and is used to skip selective blocks where it is invoked, also is used to control iterations
    skip_remaining_blocks_freeze: bool = False
    # p0_platform is set when any string available in p0_platform_list is encountered and is used to control iterations
    p0_platform: bool = False
    # p0_functional_iter is set when any string available in p0_functional_iter_list is encountered and is used to control iterations
    p0_functional_iter: bool = False
    # this is used to control atf iteration flow when exception happens during setup of docker launch and is used to control iterations
    p0_setup_iter: bool = False
    # check if log analysis block is executed
    enable_logs_analysis_runner: bool = False
    
    # Configuration dictionaries
    # control_block can be used to control execution of different blocks, this setting is loaded from dmf_config.toml
    control_block: Dict = {}
    # toml_name_dict contains randomization toml names that is assoicated with scenario in headless. it is used to identify and update period in randomization toml, when --rand-interval N flag is specified for a test in test toml
    toml_name_dict: Dict = {}
    # platform_name_dict contains nvidia-smi gpu names with simplified gpu name mapping. it is used to highlight gpu platform used in reports
    platform_name_dict: Dict = {}
    # below dict consist of ui flags that will be passed to pytest script from ATF
    ui_test_helpers: Dict = {}
    
    # Lists for configuration
    # check_words contains list of strings that can be used to kill a testcase run when encountered, this is to help come out of testcases which are freezed. this setting is loaded from dmf_config.toml
    check_words: List = []
    # When string available in this list is encountered, it asserts logs issue and the same is highlighted in report. this setting is loaded from dmf_config.toml
    p0_functional_list: List = []
    # When string available in this list is encountered, it asserts logs issue and the same is highlighted in report. this setting is loaded from dmf_config.toml
    p1_list: List = []
    # When string available in this list is encountered, no further log check is done and run is treated as normal with p1 ignored issue. this setting is loaded from dmf_config.toml
    p1_ignore_issue_list: List = []
    # When string available in this list is encountered, it asserts logs issue and the same is highlighted in report. Along with this, if --iterate flag is not used in toml, then re-run is performed. Max retry after first issue occurance is 2. Also all the data related to such testcases is made available in outputs/isolated_dump/p0_platform_issue_logs. this setting is loaded from dmf_config.toml
    p0_platform_list: List = []
    # When string available in this list is encountered, it asserts logs issue and the same is highlighted in report. Along with this, if --iterate flag is not used in toml, re-run is performed. Max retry after first issue occurance is 2. Also all the data related to such testcases is made available in outputs/isolated_dump/p0_functional_iter_issue_logs. this setting is loaded from dmf_config.toml
    p0_functional_iter_list: List = []
    # When string available in this list is encountered, it asserts pytest logs issue and the same is highlighted in report. this setting is loaded from dmf_config.toml
    pytest_p0_functional_list: List = []
    # When string available in this list is encountered, it asserts pytest logs issue and the same is highlighted in report. this setting is loaded from dmf_config.toml
    pytest_p1_list: List = []
    
    # Threading and analysis
    # list of all threads which are added in analysis functions, consisting of event. Unreturned threads event can be set at end of test to make it forecully return
    thread_list: List = []
    # use below event in all analysis parallel threads. Below event in unreturned threads can be set at end of test to make it forecully return
    analysis_event: Optional[Any] = None
    
    # Temporary storage
    # temporary data to store
    temp_data: List = []
    # to store kit file name which is required to analyze it
    kit_file_name: Optional[str] = None
    # detected kit HTTP port when running in Windows develop mode
    kit_http_port: Optional[int] = None
    # temporary data to store
    updated_toml_name: Optional[str] = None

    # Overwrite log level
    overwrite_log_level: Optional[str] = None
    # Framework logs path
    framework_logs_path: Optional[str] = None
    # Add these variables for Windows develop mode support
    skip_dsrs_process_launch: bool = False  # Similar to skip_docker_launch but for Windows processes
    skip_map2sim_process_launch: bool = False  # Similar to skip_docker_launch but for Windows processes
    map2sim_process_info: Optional[Any] = None  # Store information about the found map2sim process
    # Add CLI mode support
    cli_mode_enabled: bool = False  # Flag to indicate CLI mode is enabled
    # sim terminal log path, get updated in command runner util based on test type
    sim_terminal_log_path: Optional[str] = None

    # ffmpeg path
    test_videos_path: Optional[str] = None
