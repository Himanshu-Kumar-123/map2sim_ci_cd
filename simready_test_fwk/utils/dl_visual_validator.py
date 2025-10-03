
import logging
# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import json
import requests
import logging
import os
import time
import subprocess
import sys



class DL_Solution():
    """
    DL Solution class for utilization of DL Algorithm for image validation.
    """
    log = logging.getLogger()
    host = "dlsolutions.nvidia.com"
    predict_url = "http://dlsolutions.nvidia.com:80/predict/v3"
    reply_url = "http://dlsolutions.nvidia.com:80/reply"

    payload = {}
    headers = {}
    files = []
    request_id = ""
    # folder_path = os.path.join(
    #     os.getcwd(),
    #     ATPTaskResult.DEFAULT_TASK_RESULT_DIR_NAME,
    #     ATPTaskResult.TASK_IMAGES_DIR_NAME,
    # )
    
    timeout_seconds = 300
    def __init__(self) -> None:
        from tests.conftest import log_folder
        self.ss_dir = os.path.join(
            os.getcwd(),
            "results",
            log_folder,
            "images"
        )
        
    def dl_visual_validation(self,file_name):
        file_path = os.path.join(self.ss_dir, file_name)
        self.log.info(file_path)
        if not os.path.exists(file_path):
            logging.error(f"Unable to find {file_path}")
            raise Exception(f"Unable to find {file_path}")
        #check file size
        if os.path.getsize(file_path) == 0:
            logging.error(f"File {file_name} is empty")
            raise Exception(f"File {file_name} is empty")
        self.config_file = "dl_config.json"
        self.config_path = os.path.join(
            os.getcwd(),
            "config", self.config_file
        )
    
        self.files=[('input_file',(file_name,open(file_path,'rb'))),
                    ('config_file',(self.config_file,open(self.config_path,'rb')))]
        self.headers = {}
        self.payload = {}
        self.dl_predict()
        result = self.get_result()
        logging.info(f"Visual validation result for {file_name}:\n{result}")
        defects = self.extract_defects(result)
        return defects

    def dl_predict(self):
        """This method calls the predict API"""
        try:
            #ping dlsolutions
            if sys.platform == "win32":
                output = subprocess.run(["ping", "-n", "4", self.host], capture_output=True, text=True)
            else:
                output = subprocess.run(["ping", "-c", "4", self.host], capture_output=True, text=True)

            # Check the return code to see if the ping was successful
            if output.returncode == 0:
                self.log.info(f"{self.host} is reachable.") 
            else:
                self.log.error(f"{self.host} is not reachable.Error code {output.returncode}")
                self.log.error(f"Response : {output.stdout}")
                self.log.error(f"error : {output.stderr}")
                
                raise Exception(f"{self.host} is not reachable.")

            response = requests.request(
                "POST",
                url=self.predict_url,
                headers=self.headers,
                data=self.payload,
                files=self.files,
            )
            if response.status_code == 200:
                self.log.info(response.text)
                response = response.json()
                self.request_id = response["request_id"]

        except Exception as exp:
            self.log.error(f"Exception found while requesting : {self.predict_url}")
            self.log.error(exp)
            time.sleep(5)
            self.log.info("Trying again")
            try:
                response = requests.request(
                    "POST",
                    url=self.predict_url,
                    headers=self.headers,
                    data=self.payload,
                    files=self.files,
                )
                if response.status_code == 200:
                    self.log.info(response.text)
                    response = response.json()
                    self.request_id = response["request_id"]
            except Exception as e:
                self.log.error(f"Exception found while requesting second time : {self.predict_url}")
                self.log.error(e)
                raise Exception(e)

    def get_result(self):
        """get result method"""
        if self.request_id:
            self.payload = json.dumps({"request_id": self.request_id})
            self.headers = {"Content-Type": "application/json"}
            start_time = time.time()
            while True:
                if time.time() - start_time > self.timeout_seconds:
                    # Break the loop if the timeout is reached
                    raise TimeoutError(
                        "Timeout reached while waiting for success status"
                    )
                response = requests.request(
                    "POST", url=self.reply_url, headers=self.headers, data=self.payload
                )
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                    except ValueError as e:
                        self.log.error(f"Error decoding JSON: {e}")
                        self.log.info(f"Response content: {response.content}")
                        return None
                    status = response_json.get("status")

                    if status == "SUCCESS":
                        # Break out of the loop if status is SUCCESS
                        break
                    elif status == "PENDING":
                        # Optionally, you can introduce a delay before making the next request
                        time.sleep(1)
                    else:
                        # Handle other statuses if needed
                        break
                else:
                    try:
                        self.log.error(response.status_code, response.json())
                        break
                    except ValueError as e:
                        self.log.error(f"Error decoding JSON: {e}")
                        self.log.info(f"Response content: {response.content}")
                        return None

            return response_json

        else:
             self.log.error("Unable to extract the request_id")

    def extract_defects(self,data):
        result_list = []
        if data is None:
            logging.info(f"Result Data is Empty")
            return result_list
        media_type = data["result"]["media_type"]
        defects = data["result"]["defects"]
        result_list = []
        logging.info(f"All defects in {media_type}: {defects}")
        if media_type == "VIDEO":
            if "flicker" in defects and defects["flicker"] is not None:
                result_list.append({"flicker": defects["flicker"]})
        elif media_type == "IMAGE":
            for defect_type in ["blackframe", "blockcorruption", "colorcorruption"]:
                if defect_type in defects and defects[defect_type] is not None:
                    result_list.append({defect_type: defects[defect_type]})

        logging.info(f"Desired defects: {result_list}")
        return result_list
