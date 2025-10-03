import datetime
import logging
import os
import re
import subprocess
import sys
import time
from typing import Optional, Dict, List, Any
from threading import Thread, Event

class TDRDetector:
    """
    Utility class to detect TDR (Timeout Detection and Recovery) events on Windows and Linux systems.
    """
    
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self._setup_logging()
        self._stop_event = Event()
        self._tdr_thread = None
        self._tdr_results = {
            "detected": False,
            "details": "",
            "timestamp": None,
            "recovery_time": None
        }

    def _setup_logging(self):
        """Configure logging if not already configured"""
        if not self.log.handlers:
            logging.basicConfig(
                format='[%(asctime)s] : [%(levelname)s] : %(message)s',
                level=logging.INFO,
                filename="tdr_identifier.log"
            )

    def start_monitoring(self):
        """Start monitoring for TDR events in a separate thread"""
        if self._tdr_thread is not None and self._tdr_thread.is_alive():
            self.log.warning("TDR monitoring is already running")
            return
            
        self._stop_event.clear()
        self._tdr_results = {
            "detected": False,
            "details": "",
            "timestamp": None,
            "recovery_time": None
        }
        
        if sys.platform == "win32":
            self._tdr_thread = Thread(target=self._check_windows_tdr)
        elif sys.platform.startswith("linux"):
            self._tdr_thread = Thread(target=self._check_linux_tdr)
        else:
            self.log.error(f"Unsupported platform: {sys.platform}")
            return
            
        self._tdr_thread.daemon = True
        self._tdr_thread.start()
        
    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring for TDR events and return results"""
        if self._tdr_thread is None or not self._tdr_thread.is_alive():
            self.log.warning("No active TDR monitoring to stop")
            return self._tdr_results
            
        self._stop_event.set()
        self._tdr_thread.join()
        self._tdr_thread = None
        return self._tdr_results

    def _check_windows_tdr(self):
        """Check for TDR events on Windows systems"""
        if sys.platform != "win32":
            self.log.error("Windows TDR check attempted on non-Windows platform")
            return

        try:
            while not self._stop_event.is_set():
                cmd = 'powershell "Get-WinEvent -FilterHashTable @{LogName=\'System\'; ' \
                      'ProviderName=\'Display\'; StartTime=(Get-Date).AddSeconds(-10)}" -ErrorAction SilentlyContinue'
                
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = proc.communicate()
                
                if output:
                    events = output.decode('utf-8')
                    if "nvlddmkm" in events:
                        detection_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        self._tdr_results.update({
                            "detected": True,
                            "details": {
                                "message": "Display driver TDR detected in Windows Event Log",
                                "event_log": events.strip(),
                                "detection_time": detection_timestamp,
                                "driver": "nvlddmkm", 
                                "source": "Windows Event Log - System/Display"
                            }
                        })
                        # Wait for recovery
                        recovery_start = time.time()
                        while time.time() - recovery_start < 30 and not self._stop_event.is_set():  # Wait up to 30 seconds for recovery
                            if self._check_gpu_active():
                                self._tdr_results["recovery_time"] = time.time() - recovery_start
                                break
                            time.sleep(1)
                            
                time.sleep(2)
                
        except Exception as e:
            self.log.error(f"Error checking for Windows TDR: {str(e)}")
            self._tdr_results["details"] = f"Error during TDR detection: {str(e)}"

    def _check_linux_tdr(self):
        """Check for TDR events on Linux systems"""
        if not sys.platform.startswith("linux"):
            self.log.error("Linux TDR check attempted on non-Linux platform")
            return

        try:
            while not self._stop_event.is_set():
                # Check dmesg for NVIDIA driver timeout messages
                cmd = "dmesg | grep -i 'nvidia.*timeout\\|nvidia.*failed\\|nvidia.*error' | tail -n 5"
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, _ = proc.communicate()
                
                if output:
                    messages = output.decode('utf-8')
                    if any(x in messages.lower() for x in ['timeout', 'gpu hang', 'gpu reset']):
                        detection_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        self._tdr_results.update({
                            "detected": True,
                            "details": {
                                "message": "GPU timeout detected in dmesg",
                                "event_log": messages.strip(),
                                "detection_time": detection_timestamp,
                                "driver": "nvidia",
                                "source": "Linux dmesg"
                            }
                        })
                        # Wait for recovery
                        recovery_start = time.time()
                        while time.time() - recovery_start < 30 and not self._stop_event.is_set():  # Wait up to 30 seconds for recovery
                            if self._check_gpu_active():
                                self._tdr_results["recovery_time"] = time.time() - recovery_start
                                break
                            time.sleep(1)
                            
                time.sleep(2)
                
        except Exception as e:
            self.log.error(f"Error checking for Linux TDR: {str(e)}")
            self._tdr_results["details"] = f"Error during TDR detection: {str(e)}"

    def _check_gpu_active(self) -> bool:
        """Check if GPU is responsive"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return len(gpus) > 0 and all(gpu.load > 0 for gpu in gpus)
        except:
            return False

    def get_tdr_settings(self) -> Dict[str, Any]:
        """Get current TDR settings from the system"""
        if sys.platform == "win32":
            return self._get_windows_tdr_settings()
        elif sys.platform.startswith("linux"):
            return self._get_linux_tdr_settings()
        else:
            self.log.error(f"Unsupported platform: {sys.platform}")
            return {"error": f"Unsupported platform: {sys.platform}"}

    def _get_windows_tdr_settings(self) -> Dict[str, Any]:
        """Get TDR settings from Windows registry"""
        if sys.platform != "win32":
            self.log.error("Windows TDR settings check attempted on non-Windows platform")
            return {"error": "Not a Windows platform"}

        try:
            import winreg
            settings = {}
            
            reg_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
                try:
                    settings["TdrDelay"] = winreg.QueryValueEx(key, "TdrDelay")[0]
                except:
                    settings["TdrDelay"] = "Not Set"
                try:
                    settings["TdrDdiDelay"] = winreg.QueryValueEx(key, "TdrDdiDelay")[0]
                except:
                    settings["TdrDdiDelay"] = "Not Set"
                    
            return settings
        except Exception as e:
            self.log.error(f"Error reading Windows TDR settings: {str(e)}")
            return {"error": str(e)}

    def _get_linux_tdr_settings(self) -> Dict[str, Any]:
        """Get TDR-related settings from Linux system"""
        if not sys.platform.startswith("linux"):
            self.log.error("Linux TDR settings check attempted on non-Linux platform")
            return {"error": "Not a Linux platform"}

        try:
            settings = {}
            
            # Check for nvidia-smi timeout settings
            cmd = "nvidia-smi --query-gpu=gpu_reset_timeout --format=csv,noheader"
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = proc.communicate()
            
            if output:
                settings["gpu_reset_timeout"] = output.decode('utf-8').strip()
            
            return settings
        except Exception as e:
            self.log.error(f"Error reading Linux TDR settings: {str(e)}")
            return {"error": str(e)}