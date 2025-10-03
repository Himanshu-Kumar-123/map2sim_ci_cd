# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""
This module contains image comparison helper based on SSIM and FSIM algorithms

"""
import logging
import os
import shutil
import sys
import cv2
from skimage.metrics import structural_similarity
from omniui.framework_lib.softassert import SoftAssert
from omniui.utils.utility_functions import get_service_account_password, get_value_from_json
from omniui.utils.swiftstack_helper import SwiftStackHelper


class ImageComparisonHelper:
    log = logging.getLogger()

    def __init__(self, test_case: str, is_capture_mode: bool = False, app: str = "", result_folder: str = r"results/images"):
        self.test_case = test_case
        self.is_capture_mode = is_capture_mode
        self.assertion = SoftAssert()
        self.is_foreign_assertion_obj = False
        self.all_comparisons = []
        self.captured_img_paths = []
        self.is_golden_image_absent = False
        self.image_dir = result_folder
        self.app = app
        swiftstack_secret_key = get_service_account_password(get_value_from_json("swiftstack_user"), "swiftstack_token")
        config = get_value_from_json("swiftstack")
        self.swiftstack = SwiftStackHelper(
            config["endpoint_url"], config["aws_access_key_id"], swiftstack_secret_key, config["region_name"]
        )

    def finalize(self):
        if self.is_golden_image_absent:
            self.sync_golden_images()
        self.log.info("===============================IMAGE COMPARISON RESULTS BELOW================================")
        for line in self.all_comparisons:
            self.log.info(line)
            self.log.info("--------------------------------------------------------------")
        self.log.info("===============================IMAGE COMPARISON RESULTS ABOVE================================")
        if not self.is_foreign_assertion_obj:
            self.assertion.assert_all()

    def ssim(
        self,
        golden_img_path: str,
        captured_img_path: str,
        threshold=0.90,
        assertion_msg: str = None,
        negative_assert: bool = False,
        is_local_comparison: bool = False,
        multichannel: bool = False,
        **kwargs,
    ):
        """Returns the Structural Similarity Index Metric score for two images.
        Args:
            golden_img_path (str): path of golden image or first image
            captured_img_path (str): path of captured image or second image
            threshold (float): threshold value
            assertion_msg (str, Optional): message that is to be logged on failed assertion
            negative_assert (bool, Optional): flag to evaluate negative assertion
            is_local_comparison (bool, Optional): flag to determine whether comparison is with local
            image or with remote image
        Returns:
            similarity score (float)
        """
        img1, img2 = self._load_images(golden_img_path, captured_img_path, is_local_comparison=is_local_comparison)
        if self.is_capture_mode and not is_local_comparison:
            self.log.info("[SSIM] Running in Capture Mode. No comparison will be performed.")
            return 0
        if img1 is None or img2 is None:
            return 0

        if multichannel:
            score, full = structural_similarity(img1, img2, channel_axis=2, full=True, **kwargs)

            diff = (full * 255).astype("uint8")

            thresh_b = cv2.threshold(diff[:, :, 0], 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            thresh_g = cv2.threshold(diff[:, :, 1], 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            thresh_r = cv2.threshold(diff[:, :, 2], 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            thresh = cv2.merge((thresh_b, thresh_g, thresh_r))

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                area = cv2.contourArea(c)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
        else:
            img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            score, full = structural_similarity(img1_gray, img2_gray, channel_axis=None, full=True, **kwargs)

            diff = (full * 255).astype("uint8")

            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            for c in contours:
                area = cv2.contourArea(c)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
                    cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
        self.assertion.expect(
            negative_assert ^ (score >= threshold),
            (assertion_msg + "\n" if assertion_msg else "")
            + f"SSIM score {score} is less than threshold {threshold} "
            f"for images at paths {golden_img_path} and {captured_img_path}",
        )
        self.all_comparisons.append(
            f"Image 1: {golden_img_path} \nImage 2: {captured_img_path} \nSSIM Score = {score}, Threshold = {threshold}"
        )
        imgconcat = cv2.hconcat([img1, img2])
        imgconcat = cv2.cvtColor(imgconcat, cv2.COLOR_BGR2RGB)
        cv2.imwrite(self.image_dir + "/result_diff.png", diff)
        cv2.imwrite(self.image_dir + "/result_anno.png", imgconcat)
        return score

    def set_assertion_obj(self, assertion_obj: SoftAssert):
        """User can use their own SoftAssert object according to test requirement
        Args:
            assertion_obj (SoftAssert): SoftAssert object from a test script.
        """
        self.assertion = assertion_obj
        self.is_foreign_assertion_obj = True

    def sync_golden_images(self):
        """sync golden images from swiftstack"""

        if self.is_capture_mode or self.is_golden_image_absent:
            self.log.info("[Sync Golden Images] Uploading to server")
        else:
            self.log.info("[Sync Golden Images] Downloading from server")
        container = get_value_from_json("golden_images")[self.app]["container"]
        base_dir = get_value_from_json("golden_images")[self.app]["base_path"]
        if sys.platform == "win32":
            remote_golden_root = os.path.join(base_dir, "windows")
        else:
            remote_golden_root = os.path.join(base_dir, "linux")
        local_golden_root = os.path.join(self.image_dir)
        local_golden_dir = os.path.join(local_golden_root, "golden_images")
        remote_golden_dir = os.path.join(remote_golden_root, self.test_case)

        if self.is_capture_mode or self.is_golden_image_absent:
            try:
                for path in self.captured_img_paths:
                    key = os.path.join(remote_golden_dir, os.path.basename(path)).replace("\\", "/")
                    self.swiftstack.upload_file(file_name=path, container=container, object_name=key)
                return os.path.join(remote_golden_dir).replace("\\", "/")
            except:
                self.log.info(f"[Sync Golden Images] Image upload failed")
                raise
        else:
            try:
                shutil.rmtree(local_golden_dir)
            except:
                self.log.info(f"[Sync Golden Images] failed to remove {local_golden_dir}")
            try:
                key = remote_golden_dir.replace("\\", "/")
                self.swiftstack.download_folder(container=container, src_path=key, dest_path=local_golden_dir)
                self.log.info("[Sync Golden Images] Sync complete.")
                return os.path.join(local_golden_dir).replace("\\", "/")
            except:
                self.log.info("[Sync Golden Images] Image upload failed")
                raise

    def _load_images(self, golden_img_path: str, captured_img_path: str, is_local_comparison: bool = False):
        if "/" not in golden_img_path and "\\" not in golden_img_path:
            golden_img_path = os.path.join(self.image_dir, golden_img_path).replace("\\", "/")
        if "/" not in captured_img_path and "\\" not in captured_img_path:
            captured_img_path = os.path.join(self.image_dir, captured_img_path).replace("\\", "/")
        assert os.path.isfile(
            captured_img_path
        ), f"[ImageComparisonHelper] File does not exist at path: {captured_img_path}"
        if not is_local_comparison:
            if self.is_capture_mode:
                self.captured_img_paths.append(captured_img_path)
                return None, None
            if not os.path.isfile(golden_img_path):
                self.is_golden_image_absent = True
                self.captured_img_paths.append(captured_img_path)
                self.assertion.expect(
                    False,
                    f"[ImageComparisonHelper] Could not find golden image: {golden_img_path}. Captured new image.",
                )
                return None, None

        assert os.path.isfile(
            golden_img_path
        ), f"[ImageComparisonHelper] File does not exist at path: {golden_img_path}"

        img1 = cv2.imread(golden_img_path)
        img2 = cv2.imread(captured_img_path)
        assert not (img1 is None), f"[ImageComparisonHelper] Could not read image at path: {golden_img_path}"
        assert not (img2 is None), f"[ImageComparisonHelper] Could not read image at path: {captured_img_path}"
        self.log.info("[ImageComparisonHelper] Found valid images at given paths")
        return img1, img2
