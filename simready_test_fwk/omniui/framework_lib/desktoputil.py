# -*- coding: utf-8 -*-
# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

""" Desktop helper class

This is a helper class to handle all desktop operations

"""
import logging
import multiprocessing
import subprocess
import sys
import time
import os

from omniui.framework_lib.commonutil import CommonUtilityClass

if sys.platform == "win32":
    import pyautogui


class DesktopUtil:
    """
    Common helper class for desktop operations
    """

    log = logging.getLogger()

    def is_window_title_present(self, title):
        """Method to check title present in window or not"""
        flag = False
        if sys.platform == "win32":
            time.sleep(2)
            for window in pyautogui.getAllWindows():
                if window.title == title or title in window.title or window.title == title.split(os.sep)[-1]:
                    flag = True
                    self.log.info("title is present in window.")
                    window.close()
                    break
        else:
            if title == "Select Folder":
                time.sleep(2)
                cmd_line = "wmctrl -l | awk '{$1=$2=$3=\"\"; print}'"
                window_names = subprocess.check_output(cmd_line, shell=True).decode().splitlines()
                for name in window_names:
                    temp = name.split()
                    if "" in name and len(temp) == 0:
                        flag = True
                        self.log.info("title is present in window.")
                        break
            else:
                cmd_line = r"wmctrl -lxp"
                window_names = subprocess.check_output(cmd_line, shell=True).decode().splitlines()
                for name in window_names:
                    if title in name or title.split("/")[-1] in name:
                        flag = True
                        self.log.info("title is present in window.")
        assert flag, f"{title} is not present"

    def click_and_verify_window_title(self, folder, window_title, get_path=False):
        """
        Clicks path/ folder and verifies title
        useful when path is expected in window title

        :param get_path: retrieves actual path opened for linux
        :param folder: folder to be clicked
        :param window_title: title to be verified
        """
        self.log.info("[DesktopUtil] Adding Process 1 & 2 ")
        proc1 = multiprocessing.Process(target=CommonUtilityClass.click, args=(folder,))
        proc2 = multiprocessing.Process(target=self.is_window_title_present, args=(window_title,))
        self.log.info("[DesktopUtil] Starting Process 1")
        proc1.start()
        time.sleep(2)
        self.log.info("[DesktopUtil] Starting Process 2")
        proc2.start()
        path = ""
        if not sys.platform == "win32":
            cmd_line = "ps -eaf  | grep 'nautilus' | grep 'new-window' | awk '{print $2, $3, $10}'"
            time.sleep(2)
            [pid, ppid, path] = subprocess.check_output(cmd_line, shell=True).decode().splitlines()[0].split()
            subprocess.Popen(f"kill {ppid}", shell=True, stdout=subprocess.PIPE)
            subprocess.Popen(f"kill {pid}", shell=True, stdout=subprocess.PIPE)
        if get_path:
            return path
        return
