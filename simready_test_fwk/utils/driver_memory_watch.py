# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import logging
import subprocess
import re
import os
import platform
import time


class DriverVerifier():
    """
    DriverVerifier class for monitoring and detecting memory leaks in GPU and DirectX (Windows) or Kernel (Linux) drivers.
    """

    log = logging.getLogger()
    
    # Regex patterns for extracting driver statistics (Windows)
    NVLDDMKM_PATTERN = (
        r"MODULE: nvlddmkm.sys.*?"
        r"Current Pool Allocations:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\).*?"
        r"Peak Pool Allocations:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\).*?"
        r"Current Pool Bytes:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\).*?"
        r"Peak Pool Bytes:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\)"
    )

    DXGKRNL_PATTERN = (
        r"MODULE: dxgkrnl.sys.*?"
        r"Current Pool Allocations:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\).*?"
        r"Peak Pool Allocations:\s+\(\s*(\d+)\s*/\s*(\d+)\s*\)"
    )

    def __init__(self, log_dir: str = r"results/driver-mem-logs") -> None:
        """
        Initialize the DriverVerifier class.
        """
        self.os_type = platform.system()
        self.log_dir= log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log.info(f"Operating System: {self.os_type}")
        self.log.info(f"Log directory: {self.log_dir}")
        
        if self.os_type == "Windows":
            self.log_file_1 = os.path.join(self.log_dir, "DriverVerifierLog1.txt")
            self.log_file_2 = os.path.join(self.log_dir, "DriverVerifierLog2.txt")
        else:
            self.dmesg_log = os.path.join(self.log_dir, "dmesg_driver_check.log")

    def run_admin_command(self, command: str) -> None:
        """
        Executes a command with Administrator privileges.

        :param command: The command to execute.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            if result.returncode != 0:
                self.log.error(f"Command failed with return code {result.returncode}: {command}")
                return None
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.log.error(f"Error running command: {command}\n{e}")
            return None

    def parse_module(self, log_data: str, pattern: str) -> dict:
        """
        Parses driver statistics from log data.

        :param log_data: The log file content.
        :param pattern: The regex pattern for extracting relevant data.
        :return: Dictionary containing parsed values.
        """
        match = re.search(pattern, log_data, re.DOTALL)
        if match:
            return {
                "current_allocations": int(match.group(1)),
                "peak_allocations": int(match.group(3)),
                "current_nonpaged_bytes": int(match.group(5)) if len(match.groups()) > 4 else None,
                "peak_nonpaged_bytes": int(match.group(7)) if len(match.groups()) > 6 else None,
            }
        return None

    def extract_values(self, log_file: str) -> dict:
        """
        Extracts values from a given log file (Windows).

        :param log_file: Path to the log file.
        :return: Dictionary containing extracted values.
        """
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                log_data = f.read()

            return {
                "nvlddmkm": self.parse_module(log_data, self.NVLDDMKM_PATTERN),
                "dxgkrnl": self.parse_module(log_data, self.DXGKRNL_PATTERN),
            }

        except FileNotFoundError:
            self.log.error(f"Error: Log file {log_file} not found!")
            return {}

    def get_slab_stats(self, driver_name):
        """Extracts current and peak allocations for a given driver from /proc/slabinfo"""
        self.log.info(f"Checking slab allocation for driver: {driver_name}...")

        slab_output = self.run_admin_command(f'sudo cat /proc/slabinfo | grep -i {driver_name} || true')
        if not slab_output:
            self.log.warning(f"No slab data found for {driver_name}!")
            return None

        columns = slab_output.split()
        if len(columns) < 6:
            self.log.warning(f"Unexpected slabinfo format: {slab_output}")
            return None

        return {
            "current_allocations": int(columns[2]),
            "peak_allocations": int(columns[3])
        }

    def check_dmesg(self):
        """Scans dmesg logs for memory leaks"""
        self.log.info("Scanning dmesg logs for memory issues...")
        mem_logs = self.run_admin_command('dmesg | grep -i "memory\\|leak\\|alloc\\|slab\\|oom"')

        if mem_logs:
            self.log.warning(f"Potential memory issue detected in dmesg logs:\n{mem_logs}")
            return True
        return False

    def check_kmemleak(self):
        """Runs kmemleak scan and checks for unreferenced allocations"""
        self.log.info("Checking kmemleak for unreferenced allocations...")
        self.run_admin_command('sudo sh -c "echo scan > /sys/kernel/debug/kmemleak"')
        kmemleak_output = self.run_admin_command("cat /sys/kernel/debug/kmemleak")

        if kmemleak_output:
            self.log.warning(f"Memory leak detected by kmemleak:\n{kmemleak_output}")
            return True
        return False

    def check_memory_leak_windows(self, log_file: str) -> None:
        """
        Checks for memory leaks in Windows drivers.

        :param log_file: Path to the log file to analyze.
        """
        self.log.info(f"Running Driver Verifier Query and saving to {log_file}...")
        self.run_admin_command(f'cmd.exe /c verifier /query > "{log_file}"')

        values = self.extract_values(log_file)
        nv = values.get("nvlddmkm")
        dx = values.get("dxgkrnl")

        if not nv:
            raise ValueError("NVIDIA driver statistics not found in log file!")
        if not dx:
            raise ValueError("DirectX Kernel statistics not found in log file!")

        # Assertions for memory stability
        assert nv["current_nonpaged_bytes"] < nv["peak_nonpaged_bytes"], "Potential memory leak in NVIDIA driver!"
        assert nv["current_allocations"] <= nv["peak_allocations"], "Potential memory leak in NVIDIA GPU Driver!"
        assert dx["current_allocations"] <= dx["peak_allocations"], "Potential memory leak in DirectX Kernel!"

        self.log.info("No memory leaks detected!")

    def check_memory_leak_linux(self, driver) -> None:
        """
        Checks dmesg logs for potential driver errors on Linux.
        """
        self.log.info("Checking dmesg logs for driver-related errors...")
        leak_detected = False

        stats = self.get_slab_stats(driver)
        if stats:
            if stats["current_allocations"] > stats["peak_allocations"]:
                self.log.error(f"Potential memory leak in {driver}! Current: {stats['current_allocations']}, Peak: {stats['peak_allocations']}")
                leak_detected = True

        if self.check_dmesg():
            leak_detected = True

        if self.check_kmemleak():
            leak_detected = True

        if not leak_detected:
            self.log.info("No memory leaks detected!")
        else:
            self.log.error("Memory leak detected!")

    def check_memory_leak(self) -> None:
        """
        Runs the appropriate memory leak check based on the OS.
        """
        if self.os_type == "Windows":
            self.check_memory_leak_windows(self.log_file_1)
            time.sleep(30)
            self.check_memory_leak_windows(self.log_file_2)
        else:
            self.check_memory_leak_linux('nvidia')
