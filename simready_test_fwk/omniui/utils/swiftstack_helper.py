# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""
This module contains SwiftStack helper based on AWS Boto3 SDK
"""
import os
import logging
import boto3
from boto3.exceptions import S3UploadFailedError, S3TransferFailedError
from botocore.config import Config
from botocore.exceptions import ClientError


class SwiftStackHelper:
    log = logging.getLogger()

    def __init__(self, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        try:
            self.s3 = boto3.client(
                      "s3",
                      endpoint_url=endpoint_url,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name,
                      config=Config(connect_timeout=5))
            bucket_list = self.s3.list_buckets()
            self.log.info("[SwiftStackHelper] Connection successful.")
        except ClientError:
            self.log.info("[SwiftStackHelper] Connection failed.")
            raise

    def upload_file(self, file_name: str, container: str, object_name: str = None, overwrite: bool = True):
        """Upload a file to an S3 bucket (SwiftStack container)
        :param file_name: File to upload (complete path)
        :param container: Container to upload to (S3 bucket)
        :param object_name: S3 object name. Path relative to the container can be used.
        If not specified then file_name is used.
        :param overwrite: Defaults to True. If False and if object_name already exists on the
        container, upload will be aborted.
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        self.log.info(f"[SwiftStackHelper] Overwrite flag is set to: {overwrite}")
        if not overwrite:
            if self._file_exists(container, object_name):
                self.log.info(f"[SwiftStackHelper] File/object already exists. Will not be overwritten. container: {container}, object_name: {object_name}")
                return False

        # Upload the file
        try:
            response = self.s3.upload_file(file_name, container, object_name)
            self.log.error(
                f"[SwiftStackHelper] File uploaded file_name: {file_name}, container: {container}, object_name: {object_name}")
        except (ClientError, S3UploadFailedError):
            self.log.error(f"[SwiftStackHelper] File upload failed. file_name: {file_name}, container: {container}, object_name: {object_name}")
            raise
        return True

    def download_file(self, container: str, object_name: str, file_name: str):
        """Download a file from an S3 bucket (SwiftStack container)
        :param container: Container to download from (S3 bucket)
        :param object_name: S3 object name. Path relative to the container can be used
        :param file_name: Local filename/path
        :return: True if file was downloaded, else False
        """
        # Download the file
        try:
            response = self.s3.download_file(container, object_name, file_name)
            self.log.info(
                f"[SwiftStackHelper] File downloaded. container: {container}, object_name: {object_name}, file_name: {file_name}")
        except (ClientError, S3TransferFailedError):
            self.log.info(f"[SwiftStackHelper] File download failed. container: {container}, object_name: {object_name}, file_name: {file_name}")
            raise
        return True

    def download_folder(self, container: str, src_path: str, dest_path: str):
        """Downloads a complete virtual folder from specified container
        :param container: Container to download from (S3 bucket)
        :param src_path: Path of the virtual folder relative to container
        :param dest_path: Local path where the folder is to be saved
        """
        all_objects = self._fetch_all_objects(container=container, prefix=src_path)
        for obj in all_objects:
            file_dir = os.path.join(dest_path, os.path.dirname(obj["Key"]).lstrip(src_path))
            os.makedirs(file_dir, exist_ok=True)

            self.download_file(container=container, object_name=obj["Key"],
                               file_name=os.path.join(file_dir, os.path.basename(obj["Key"])))

    def _file_exists(self, container: str, object_name: str):
        """Checks whether a file/object exists in the container
        :param container: Name of container to check
        :param object_name: S3 object name. Path relative to the container can be used
        :return: True if the file/object exits, else False
        """
        try:
            res = self.s3.list_objects_v2(Bucket=container)

            for key in res['Contents']:
                if object_name == key:
                    self.log.info(
                        f"[SwiftStackHelper] Found object with key {object_name} in container {container}")
                    return True

            while res['IsTruncated']:
                continuation_token = res['NextContinuationToken']
                res = self.s3.list_objects_v2(Bucket=container, ContinuationToken=continuation_token)
                for key in res['Contents']:
                    if object_name == key:
                        self.log.info(
                            f"[SwiftStackHelper] Found object with key {object_name} in container {container}")
                        return True
            self.log.info(
                f"[SwiftStackHelper] Object does not exist with key {object_name} in container {container}")
            return False
        except ClientError as e:
            self.log.info(
                f"[SwiftStackHelper] Failed to find object with key {object_name} in container {container}")
            raise

    def _fetch_all_objects(self, container: str, prefix: str = ""):
        """Checks whether a file/object exists in the container
        :param container: Name of container to check
        :param prefix: Fetch objects whose keys begin with specified prefix
        :return: List of all object keys
        """
        try:
            res = self.s3.list_objects_v2(Bucket=container, Prefix=prefix)

            object_list = []
            if res['KeyCount'] == 0:
                return object_list
            else:
                object_list.extend(res['Contents'])

            while res['IsTruncated']:
                continuation_token = res['NextContinuationToken']
                res = self.s3.list_objects_v2(Bucket=container,
                                              ContinuationToken=continuation_token,
                                              Prefix=prefix)
                for key in res['Contents']:
                    object_list.append(key)
            self.log.info(
                f"[SwiftStackHelper] Search complete for objects with prefix '{prefix}' in container '{container}'")
            return object_list
        except ClientError as e:
            self.log.info(
                f"[SwiftStackHelper] Failed to find objects with prefix '{prefix}' in container '{container}'")
            raise
