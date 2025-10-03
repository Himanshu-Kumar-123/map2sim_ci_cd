# -*- coding: utf-8 -*-
# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""
Database API Class containing all methods to transmit test data.
"""
import logging
import os
from requests.adapters import HTTPAdapter, Retry
from typing import Optional
import requests


class DatabaseAPI:
    """Database API class that allows transmission of test data."""

    def __init__(self, host: str) -> None:
        """
        Initialize the Database API.

        Args:
            host (str): IP address of the backend.
        """
        self.log = logging.getLogger()
        self.database_update_enabled = (
            os.environ.get("DATABASE_UPDATE", "false").lower() == "true"
        )
        if not self.database_update_enabled:
            self.log.info(
                "Skipping database connection. 'DATABASE_UPDATE' env variable was not set 'True'."
            )
            return
        self.host = host
        self.baseurl = f"http://{self.host}"

        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.2)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def initiate_test_record(
        self,
        Pipeline_ID: Optional[int] = None,
        Trigger_Type: Optional[str] = None,
        Project_UID: Optional[int] = None,
        System_Name: Optional[str] = None,
        System_OS: Optional[str] = None,
        System_GPU: Optional[str] = None,
        GPU_Driver_Version: Optional[str] = None,
        GPU_Driver_Branch: Optional[str] = None,
        GPU_Driver_Build_Type: Optional[str] = None,
        DevTest_Template_ID: Optional[int] = None,
        MR_Number: Optional[int] = None,
    ):
        """
        Records the data when test execution starts.

        Args:
            Pipeline_ID (int): ID of the pipeline in which tests are being executed. Defaults to None
            Trigger_Type (str): Type of trigger that started test execution - MR, Nightly, etc. Defaults to None
            Project_UID (int): Identifier UID of Gitlab project which triggered the test pipeline. Defaults to None
            System_Name (str): Name of system on which test was executed. Defaults to None
            System_OS (str): Name of OS on which test was executed. Defaults to None
            System_GPU (str): Name of GPU on which test was executed. Defaults to None
            GPU_Driver_Version (str): Version of GPU Driver. Defaults to None
            GPU_Driver_Branch (str): Branch of GPU Driver. Defaults to None
            GPU_Driver_Build_Type (str): Type of build of GPU Driver. Defaults to None
            DevTest_Template_ID (int): Template ID of the test as per Devtest. Defaults to None
            MR_Number (int): MR number in case the test is triggered by MR. Defaults to None.

        Raises:
            Exception: When API call fails.

        Returns
            int: Test Execution ID which is used to identify a test execution in the database.
        """

        if not self.database_update_enabled:
            self.log.info(
                "Skipping database API call. 'DATABASE_UPDATE' env variable was not set 'True'."
            )
            return None

        data = {
            "Trigger_Type": Trigger_Type,
            "Pipeline_ID": Pipeline_ID,
            "Project_UID": Project_UID,
            "System_Name": System_Name,
            "System_OS": System_OS,
            "System_GPU": System_GPU,
            "GPU_Driver_Version": GPU_Driver_Version,
            "GPU_Driver_Branch": GPU_Driver_Branch,
            "GPU_Driver_Build_Type": GPU_Driver_Build_Type,
            "DevTest_Template_ID": DevTest_Template_ID,
            "MR_Number": MR_Number,
        }
        try:
            resp = self.session.post(
                self.baseurl + "/initiate_test_record/",
                params=data,
                verify=False,
            )
            if not resp.status_code == 201:
                self.log.error(resp.json())
                self.log.error(f"Failed to send data to the server. Data: {data}")
            self.log.info(
                f"Successfully sent initial data to the server. Response: {resp.json()}"
            )
            return resp.json()["key"]
        except requests.RequestException as e:
            self.log.error(f"Database API call resulted in an exception: {e}")
            return None

    def update_app_details(
        self,
        TestExecutionResult_ID: int,
        App_Name: str = None,
        App_Version: Optional[str] = None,
        Release_Type: Optional[str] = None,
    ):
        """
        Updates the app details for a test execution.

        Args:
            TestExecutionResult_ID (int): Primary key of test record for which results will be updated.
            App_Name (str): Name of app on which test was executed. Defaults to None.
            App_Version (str): Version of app on which test was executed. Defaults to None
            Release_Type (str): App release type - Beta, Alpha, rc, etc. Defaults to None.

        Raises:
            Exception: When API call fails.
        """

        if not self.database_update_enabled:
            self.log.info(
                "Skipping database API call. 'DATABASE_UPDATE' env variable was not set 'True'."
            )
            return

        data = {
            "TestExecutionResult_ID": TestExecutionResult_ID,
            "App_Name": App_Name,
            "App_Version": App_Version,
            "Release_Type": Release_Type,
        }
        try:
            resp = self.session.post(
                self.baseurl + "/update_app_details/",
                params=data,
                verify=False,
            )
            if not resp.status_code == 200:
                self.log.error(resp.json())
                self.log.error(f"Failed to update app data in the server. Data: {data}")
            self.log.info(
                f"Successfully updated app data in the database at TestExecutionResult_ID={TestExecutionResult_ID}."
            )
        except requests.RequestException as e:
            self.log.error(f"Database API call resulted in an exception: {e}")

    def finalize_test_record(
        self,
        TestExecutionResult_ID: int,
        Test_Result: str,
        Test_Log_Path: str,
        Kit_Log_Path: Optional[str] = None,
    ):
        """
        Records the data when test execution ends.

        Args:
            TestExecutionResult_ID (int): Primary key of test record for which results will be updated.
            Test_Result (str): Result of test - passed/failed.
            Test_Log_Path (str): Path of log file generated by the test.
            Kit_Log_Path (str): Path of log file generated by the Kit App. Defaults to None.

        Raises:
            Exception: When API call fails.
        """

        if not self.database_update_enabled:
            self.log.info(
                "Skipping database API call. 'DATABASE_UPDATE' env variable was not set 'True'."
            )
            return

        data = {
            "TestExecutionResult_ID": TestExecutionResult_ID,
            "Test_Result": Test_Result,
            "Test_Log_Path": Test_Log_Path,
            "Kit_Log_Path": Kit_Log_Path,
        }
        try:
            resp = self.session.post(
                self.baseurl + "/finalize_test_record/",
                params=data,
                verify=False,
            )
            if not resp.status_code == 200:
                self.log.error(resp.json())
                self.log.error(f"Failed to update log data in the server. Data: {data}")
            self.log.info(
                f"Successfully updated log data in the database at TestExecutionResult_ID={TestExecutionResult_ID}."
            )
        except requests.RequestException as e:
            self.log.error(f"Database API call resulted in an exception: {e}")
            return None
