import os
import threading
import subprocess
import docker
from docker.errors import NotFound
from analysis_utils.ds_recorder import DSRecorder
from analysis_utils.vram_recorder_util import VramRecorder
from analysis_utils.validate_logs_util import ValidateLogsMethod, LoggerMethods
from fwk.shared.constants import FFMPEG_LOG_FILE_NAME, FFMPEG_LOG_FILE_PATH, FFMPEG_VIDEO_FILE_NAME
from fwk.shared.variables_util import varc
import time
import signal
import ctypes
import ctypes.wintypes
from fwk.fwk_logger.fwk_logging import get_logger

logger = get_logger(__name__, varc.framework_logs_path)


class PretestAnalysisCallerMethods():
    '''This class consist of all analysis methods that should be called before test'''
                    
    @staticmethod
    def find_application_window(window_title_keywords=None, process_name=None):
        '''Find application window by title keywords or process name and return its position and size'''
        
        try:
            # Windows API structures and functions
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            psapi = ctypes.windll.psapi
            
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                           ("top", ctypes.c_long),
                           ("right", ctypes.c_long),
                           ("bottom", ctypes.c_long)]
            
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long),
                           ("y", ctypes.c_long)]
            
            class WINDOWPLACEMENT(ctypes.Structure):
                _fields_ = [("length", ctypes.c_uint),
                           ("flags", ctypes.c_uint),
                           ("showCmd", ctypes.c_uint),
                           ("ptMinPosition", POINT),
                           ("ptMaxPosition", POINT),
                           ("rcNormalPosition", RECT)]
            
            def get_process_name_from_hwnd(hwnd):
                '''Get process name from window handle'''
                try:
                    # Get process ID from window handle
                    process_id = ctypes.wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
                    
                    # Open process handle
                    process_handle = kernel32.OpenProcess(0x0400 | 0x0010, False, process_id.value)  # PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
                    if not process_handle:
                        return None
                    
                    # Get process name
                    process_name_buffer = ctypes.create_unicode_buffer(260)  # MAX_PATH
                    if psapi.GetModuleBaseNameW(process_handle, None, process_name_buffer, 260):
                        kernel32.CloseHandle(process_handle)
                        return process_name_buffer.value.lower()
                    
                    kernel32.CloseHandle(process_handle)
                    return None
                except Exception as e:
                    logger.debug(f"Error getting process name from window handle {hwnd}: {e}")
                    return None
            
            # Store results in a simple list instead of using complex ctypes casting
            results = []
            
            # Function to enumerate windows
            def enum_windows_proc(hwnd, lParam):
                try:
                    # Get window title
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length == 0:
                        return True
                        
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    
                    # Check if window is visible and not minimized
                    if not user32.IsWindowVisible(hwnd):
                        return True
                    
                    # Get window placement to check if minimized
                    placement = WINDOWPLACEMENT()
                    placement.length = ctypes.sizeof(WINDOWPLACEMENT)
                    if not user32.GetWindowPlacement(hwnd, ctypes.byref(placement)):
                        # If GetWindowPlacement fails, assume window is valid
                        logger.debug(f"GetWindowPlacement failed for window {hwnd}, assuming valid")
                    elif placement.showCmd == 2:  # SW_SHOWMINIMIZED
                        return True
                    
                    # Check process name first (higher priority)
                    if process_name:
                        window_process_name = get_process_name_from_hwnd(hwnd)
                        if window_process_name:
                            # Remove .exe extension for comparison
                            clean_process_name = window_process_name.replace('.exe', '')
                            target_process_name = process_name.lower().replace('.exe', '')
                            
                            if clean_process_name == target_process_name:
                                logger.info(f"Found target window by process name: '{window_title}' (Handle: {hwnd}, Process: {window_process_name})")
                                
                                # Get window rectangle
                                rect = RECT()
                                if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                                    window_info = {
                                        'hwnd': hwnd,
                                        'title': window_title,
                                        'process_name': window_process_name,
                                        'x': rect.left,
                                        'y': rect.top,
                                        'width': rect.right - rect.left,
                                        'height': rect.bottom - rect.top
                                    }
                                    
                                    # Store in the results list directly
                                    results.append(window_info)
                                    return False  # Stop enumeration after finding first match
                                else:
                                    logger.debug(f"GetWindowRect failed for window {hwnd}")
                    
                    # Check window title keywords as fallback
                    if window_title_keywords and not process_name:  # Only check keywords if no process name specified
                        for keyword in window_title_keywords:
                            if keyword.lower() in window_title.lower():
                                logger.info(f"Found target window by title keyword: '{window_title}' (Handle: {hwnd})")
                                
                                # Get window rectangle
                                rect = RECT()
                                if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                                    window_info = {
                                        'hwnd': hwnd,
                                        'title': window_title,
                                        'process_name': get_process_name_from_hwnd(hwnd),
                                        'x': rect.left,
                                        'y': rect.top,
                                        'width': rect.right - rect.left,
                                        'height': rect.bottom - rect.top
                                    }
                                    
                                    # Store in the results list directly
                                    results.append(window_info)
                                    return False  # Stop enumeration after finding first match
                                else:
                                    logger.debug(f"GetWindowRect failed for window {hwnd}")
                    
                    return True  # Continue enumeration
                
                except Exception as e:
                    logger.debug(f"Error in enum_windows_proc for window {hwnd}: {e}")
                    return True  # Continue enumeration despite error
            
            # Prepare callback
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            callback = EnumWindowsProc(enum_windows_proc)
            
            # Enumerate all windows with a dummy lParam (we don't use it now)
            logger.debug("Starting window enumeration...")
            enum_result = user32.EnumWindows(callback, 0)
            logger.debug(f"Window enumeration completed. Result: {enum_result}, Found windows: {len(results)}")
            
            if results:
                return results[0]  # Return first match
            else:
                logger.warning("No matching windows found")
                return None
                
        except Exception as e:
            logger.error(f"Critical error in find_application_window: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return None
                    
    @staticmethod
    def _debug_list_windows_with_keyword(keyword):
        '''Debug helper: List all visible windows containing the keyword in their title'''
        try:
            import ctypes
            user32 = ctypes.windll.user32
            
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                           ("top", ctypes.c_long),
                           ("right", ctypes.c_long),
                           ("bottom", ctypes.c_long)]
            
            windows_found = []
            
            def enum_debug_windows(hwnd, lParam):
                try:
                    # Get window title
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length == 0:
                        return True
                        
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    
                    # Check if window is visible
                    if not user32.IsWindowVisible(hwnd):
                        return True
                    
                    # Check if keyword is in title (case insensitive)
                    if keyword.lower() in window_title.lower():
                        windows_found.append({
                            'title': window_title,
                            'hwnd': hwnd
                        })
                    
                    return True  # Continue enumeration
                except:
                    return True  # Continue even on error
            
            # Enumerate windows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            callback = EnumWindowsProc(enum_debug_windows)
            user32.EnumWindows(callback, 0)
            
            return windows_found
            
        except Exception as e:
            logger.error(f"Error in _debug_list_windows_with_keyword: {e}")
            return []
                    
    @staticmethod 
    def perf_recorder_caller(test_dict):
        '''This function is used to call ds recorder class for a test'''
        
        # thread_vram=None
        # def vram_recorder_function():
        #     recorder=VramRecorder(f"{test_dict['test_perf_data_path']}/{test_dict['name']}",0.5,"GPU Memory Usage for Scenario Run",test_dict)
        #     recorder.run()
        
        # if not "--no-vram-record" in test_dict["automation_flags_dict"] and not "--no-vram-record" in test_dict["automation_suite_flags_dict"]:
        #     thread_vram = threading.Thread(target=vram_recorder_function)
        #     varc.thread_list.append(thread_vram)
        #     thread_vram.start()

        upload=True if "--perf-data-upload" in test_dict['automation_flags_dict'] or "--perf-data-upload" in test_dict['automation_suite_flags_dict'] else False
        recorder = DSRecorder(f"{test_dict['test_perf_data_path']}/{test_dict['name']}",0.5,"GPU Memory Usage for Scenario Run",True,test_dict,upload)
        recorder.start()
    
    @staticmethod
    def windows_ffmpeg_recorder_caller(test_dict, video_file_name:str = FFMPEG_VIDEO_FILE_NAME, video_log_file_name:str = FFMPEG_LOG_FILE_NAME):
        '''This function is used to run ffmpeg for screen recording on Windows (capturing entire desktop).'''

        logger.info(f"Starting Windows application window recording for test: {test_dict.get('name', 'unnamed')}")

        try:
            # Use full-desktop capture by default for maximum robustness
            logger.info("Using FFmpeg full desktop capture (gdigrab)")
            ffmpeg_command_list = [
                "ffmpeg",
                "-y",
                "-f", "gdigrab",
                "-framerate", "30",
                "-thread_queue_size", "1024",
                "-i", "desktop",
                "-use_wallclock_as_timestamps", "1",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                video_file_name
            ]

            # Save the command for reference (join list for readability)
            varc.test_command_dict["ffmpeg_recorder_command"] = " ".join(ffmpeg_command_list)
            logger.info(f"Using ffmpeg command: {' '.join(ffmpeg_command_list)}")

            # Start the recording process using the command list
            try:
                # Construct the log file path dynamically
                ffmpeg_log_path = os.path.join(test_dict['test_videos_path'], video_log_file_name)
                logger.debug(f"FFmpeg log file path: {ffmpeg_log_path}")
                
                with open(ffmpeg_log_path, "w") as log_file:
                    process = subprocess.Popen(
                        ffmpeg_command_list,    # Use the list directly
                        cwd=test_dict['test_videos_path'],
                        stdout=log_file,
                        stderr=log_file,
                        stdin=subprocess.PIPE,  # Connect stdin to send 'q' later
                    )
                    logger.info(f"Windows desktop recording started with PID: {process.pid}")
                    logger.info("Recording source: full desktop (gdigrab)")
                    return process
            except FileNotFoundError as e:
                error_msg = f"'ffmpeg' command not found. Make sure ffmpeg is installed and in your system's PATH."
                logger.error(f"FileNotFoundError: {error_msg}")
                logger.error(f"Original error: {e}")
                logger.error("DEBUGGING INFO:")
                logger.error(f"  - Command attempted: {ffmpeg_command_list[0]}")
                logger.error(f"  - Working directory: {test_dict['test_videos_path']}")
                logger.error("  - Solution: Install ffmpeg and add it to your system PATH")
                return None
            except Exception as e:
                error_msg = f"Error starting Windows application recording: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Error type: {type(e)}")
                import traceback
                logger.error(f"Full traceback: {traceback.format_exc()}")
                logger.error("DEBUGGING INFO:")
                logger.error(f"  - Command: {' '.join(ffmpeg_command_list)}")
                logger.error(f"  - Working directory: {test_dict['test_videos_path']}")
                logger.error(f"  - Video output path: {video_file_name}")
                logger.error(f"  - Log file path: {os.path.join(test_dict['test_videos_path'], video_log_file_name)}")
                return None

        except Exception as e:
            error_msg = f"Critical error in windows_ffmpeg_recorder_caller: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            logger.error("DEBUGGING INFO:")
            logger.error(f"  - Test dict keys: {list(test_dict.keys()) if test_dict else 'None'}")
            logger.error(f"  - Test name: {test_dict.get('name', 'unknown') if test_dict else 'None'}")
            return None

    @staticmethod
    def _bring_window_to_foreground(hwnd):
        '''Bring a window to the foreground using Windows API'''
        try:
            import ctypes
            user32 = ctypes.windll.user32
            
            # First, check if window is minimized and restore it
            if user32.IsIconic(hwnd):  # IsIconic returns True if window is minimized
                logger.info("Window is minimized, restoring it...")
                user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9
                time.sleep(1)  # Give it time to restore
            
            # Bring window to foreground
            user32.SetForegroundWindow(hwnd)
            
            # Alternative method if SetForegroundWindow fails
            user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5
            user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_TOPMOST, SWP_NOMOVE | SWP_NOSIZE
            
            # Remove topmost flag after bringing to front
            user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)  # HWND_NOTOPMOST, SWP_NOMOVE | SWP_NOSIZE
            
            logger.info("Window bring-to-foreground completed")
            
        except Exception as e:
            logger.error(f"Error bringing window to foreground: {e}")
            raise

    @staticmethod
    def windows_stop_ffmpeg_recording(process):
        """Stop a Windows ffmpeg recording process gracefully by sending 'q'."""
        
        if not process or process.poll() is not None:
            logger.warning(f"No recording process to stop or process already finished (PID: {process.pid if process else 'N/A'}).")
            return False

        pid = process.pid
        logger.info(f"Attempting to gracefully stop ffmpeg process {pid} by sending 'q' to stdin.")
        time.sleep(30)
        try:
            # Send 'q' followed by newline to ffmpeg's stdin
            process.stdin.write(b'q\n')
            process.stdin.flush()
            process.stdin.close() # Close stdin to signal EOF

            # Wait for ffmpeg to terminate (give it time to finalize the file)
            logger.info(f"Waiting for ffmpeg process {pid} to finalize after sending 'q'...")
            process.wait(timeout=30) # Increased timeout for finalization
            logger.info(f"Process {pid} terminated gracefully after receiving 'q'.")
            return True

        except (subprocess.TimeoutExpired, OSError, BrokenPipeError, AttributeError) as e:
            logger.warning(f"Sending 'q' to ffmpeg process {pid} failed or timed out: {e}. Trying fallback methods.")
            # Ensure stdin is closed if it wasn't already
            try:
                if process.stdin and not process.stdin.closed:
                    process.stdin.close()
            except OSError:
                pass # Ignore errors closing already closed pipe

        # --- Fallback Methods ---
        if process.poll() is not None:
             logger.info(f"Process {pid} terminated during/after 'q' attempt.")
             return True # It stopped somehow

        # Fallback 1: Try taskkill without /F
        try:
            logger.warning(f"Fallback 1: Using taskkill /PID {pid} (no /F)")
            subprocess.run(["taskkill", "/PID", str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            process.wait(timeout=10)
            logger.info(f"Process {pid} terminated after taskkill (no /F).")
            return True
        except (subprocess.TimeoutExpired, Exception) as e:
            logger.warning(f"Taskkill (no /F) for {pid} failed or timed out: {e}")

        if process.poll() is not None:
             logger.info(f"Process {pid} terminated during/after taskkill (no /F) attempt.")
             return True

        # Fallback 2: Try PowerShell Stop-Process without -Force
        try:
            logger.warning(f"Fallback 2: Using PowerShell Stop-Process for {pid} (no -Force)")
            ps_command = f"Get-CimInstance Win32_Process -Filter \"ProcessId = {pid}\" | ForEach-Object {{ Stop-Process -Id $_.ProcessId }}"
            subprocess.run(["powershell", "-Command", ps_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            process.wait(timeout=10)
            logger.info(f"Process {pid} terminated after PowerShell Stop-Process (no -Force).")
            return True
        except (subprocess.TimeoutExpired, Exception) as e:
            logger.warning(f"PowerShell Stop-Process (no -Force) for {pid} failed or timed out: {e}")

        if process.poll() is not None:
             logger.info(f"Process {pid} terminated during/after PowerShell (no -Force) attempt.")
             return True

        # Fallback 3: Last resort - Force kill with PowerShell
        try:
            logger.error(f"LAST RESORT: Force killing process {pid} with PowerShell Stop-Process -Force. Video likely corrupted.")
            ps_command_force = f"Get-CimInstance Win32_Process -Filter \"ProcessId = {pid}\" | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}"
            subprocess.run(["powershell", "-Command", ps_command_force], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            process.wait(timeout=5)
            logger.info(f"Process {pid} terminated after PowerShell Stop-Process -Force.")
            return False # Indicate it was likely not graceful
        except Exception as e:
            logger.error(f"Force killing process {pid} failed: {e}")
            return False # Indicate failure
            return False

    @staticmethod
    def _debug_find_all_kit_windows():
        '''Debug helper: Find ALL windows belonging to kit processes with detailed info'''
        try:
            import ctypes
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            psapi = ctypes.windll.psapi
            
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                           ("top", ctypes.c_long),
                           ("right", ctypes.c_long),
                           ("bottom", ctypes.c_long)]
            
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long),
                           ("y", ctypes.c_long)]
            
            class WINDOWPLACEMENT(ctypes.Structure):
                _fields_ = [("length", ctypes.c_uint),
                           ("flags", ctypes.c_uint),
                           ("showCmd", ctypes.c_uint),
                           ("ptMinPosition", POINT),
                           ("ptMaxPosition", POINT),
                           ("rcNormalPosition", RECT)]
            
            def get_process_name_from_hwnd(hwnd):
                '''Get process name from window handle'''
                try:
                    # Get process ID from window handle
                    process_id = ctypes.wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
                    
                    # Open process handle
                    process_handle = kernel32.OpenProcess(0x0400 | 0x0010, False, process_id.value)
                    if not process_handle:
                        return None
                    
                    # Get process name
                    process_name_buffer = ctypes.create_unicode_buffer(260)
                    if psapi.GetModuleBaseNameW(process_handle, None, process_name_buffer, 260):
                        kernel32.CloseHandle(process_handle)
                        return process_name_buffer.value.lower()
                    
                    kernel32.CloseHandle(process_handle)
                    return None
                except Exception:
                    return None
            
            kit_windows = []
            
            def enum_kit_windows(hwnd, lParam):
                try:
                    # Get window title
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length == 0:
                        return True
                        
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    
                    # Check if this window belongs to kit process
                    process_name = get_process_name_from_hwnd(hwnd)
                    if process_name and process_name.replace('.exe', '') == 'kit':
                        # Get window rectangle
                        rect = RECT()
                        if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                            # Check visibility
                            is_visible = user32.IsWindowVisible(hwnd)
                            
                            # Check if minimized
                            placement = WINDOWPLACEMENT()
                            placement.length = ctypes.sizeof(WINDOWPLACEMENT)
                            is_minimized = False
                            if user32.GetWindowPlacement(hwnd, ctypes.byref(placement)):
                                is_minimized = (placement.showCmd == 2)  # SW_SHOWMINIMIZED
                            
                            window_info = {
                                'hwnd': hwnd,
                                'title': window_title,
                                'process_name': process_name,
                                'x': rect.left,
                                'y': rect.top,
                                'width': rect.right - rect.left,
                                'height': rect.bottom - rect.top,
                                'visible': is_visible,
                                'minimized': is_minimized
                            }
                            kit_windows.append(window_info)
                    
                    return True  # Continue enumeration
                except Exception:
                    return True  # Continue even on error
            
            # Enumerate windows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            callback = EnumWindowsProc(enum_kit_windows)
            user32.EnumWindows(callback, 0)
            
            # Filter out tiny windows and invisible windows
            filtered_windows = []
            for window in kit_windows:
                # Skip tiny windows (likely not main app windows)
                if window['width'] < 100 or window['height'] < 100:
                    continue
                # Skip invisible windows
                if not window['visible']:
                    continue
                # Skip minimized windows
                if window['minimized']:
                    continue
                    
                filtered_windows.append(window)
            
            return filtered_windows
            
        except Exception as e:
            logger.error(f"Error in _debug_find_all_kit_windows: {e}")
            return []
                    
    @staticmethod
    def _debug_list_windows_with_keyword(keyword):
        '''Debug helper: List all visible windows containing the keyword in their title'''
        try:
            import ctypes
            user32 = ctypes.windll.user32
            
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                           ("top", ctypes.c_long),
                           ("right", ctypes.c_long),
                           ("bottom", ctypes.c_long)]
            
            windows_found = []
            
            def enum_debug_windows(hwnd, lParam):
                try:
                    # Get window title
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length == 0:
                        return True
                        
                    buffer = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buffer, length + 1)
                    window_title = buffer.value
                    
                    # Check if window is visible
                    if not user32.IsWindowVisible(hwnd):
                        return True
                    
                    # Check if keyword is in title (case insensitive)
                    if keyword.lower() in window_title.lower():
                        windows_found.append({
                            'title': window_title,
                            'hwnd': hwnd
                        })
                    
                    return True  # Continue enumeration
                except:
                    return True  # Continue even on error
            
            # Enumerate windows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            callback = EnumWindowsProc(enum_debug_windows)
            user32.EnumWindows(callback, 0)
            
            return windows_found
            
        except Exception as e:
            logger.error(f"Error in _debug_list_windows_with_keyword: {e}")
            return []
                    

class PosttestAnalysisCallerMethods():
    '''This class consist of all analysis methods that should be called after test''' 
    
    @staticmethod 
    def analyze_sim_terminal_logs_caller(test_dict):
        '''Analyze simulation terminal logs and update test dictionary with results
        
        Args:
            test_dict (dict): A dictionary containing test data
        '''
        
        # Define severity mappings for cleaner code
        severity_handlers = {
            'p1': {
                'message': "p1 logs issue found",
                'skip_blocks': False,
                'set_flag': None
            },
            'p1_ignored_issue': {
                'message': "p1_ignored_issue logs issue found, no further log check was done",
                'skip_blocks': False,
                'set_flag': None
            },
            'p0_functional_iter': {
                'message': "p0_functional_iter logs issue found",
                'skip_blocks': True,
                'set_flag': 'p0_functional_iter'
            },
            'p0_functional': {
                'message': "p0_functional logs issue found",
                'skip_blocks': True,
                'set_flag': None
            },
            'p0_platform': {
                'message': "p0_platform logs issue found",
                'skip_blocks': True,
                'set_flag': 'p0_platform'
            }
        }

        result = ValidateLogsMethod.analyze_sim_terminal_logs(varc.sim_terminal_log_path, test_dict)

        if result['verdict'] == 'fail':
            severity = result['severity']
            handler = severity_handlers.get(severity)
            
            if handler:
                logger.debug(f"\n[{test_dict['name']}] : {result['reason']}")
                test_dict['detailed_analysis']['logs'] = result['reason']
                test_dict['verdicts']["logs_errors"] = handler['message']
                
                if handler['skip_blocks']:
                    varc.skip_remaining_blocks = True
                    test_dict['verdicts']['final-verdict'] = 'FAIL'
                    
                if handler['set_flag']:
                    setattr(varc, handler['set_flag'], True)

    @staticmethod 
    def threads_end_check():     
        '''This function is used to return analysis threads that are alive even after test'''
        
        #set the event to stop all analysis threads that uses it
        for threads in varc.thread_list:
            if threads is not None and threads.is_alive():
                logger.info(f"Stopping thread: {threads.name}, Target function: {threads._target.__name__}")
                varc.analysis_event.set()
                threads.join()       
