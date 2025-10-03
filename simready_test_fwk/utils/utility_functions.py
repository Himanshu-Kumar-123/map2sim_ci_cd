import psutil
import time
import logging
import socket
from mss import mss
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from omniui.utils.utility_functions import (
    get_service_account_password
)
from selenium.webdriver.chrome.service import Service
import os
import platform
import subprocess
import cv2
import toml
from ov_app_installer import AppInstaller
from utils.configuration_loader import get_config

def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    return driver


def switch_to_window_with_title(driver: WebDriver, target_title, timeout=300):
    current_window = driver.current_window_handle
    available_windows = driver.window_handles
    start_time = time.time()
    while time.time() - start_time < timeout:
        for window in available_windows:
            driver.switch_to.window(window)
            if driver.title == target_title or target_title in driver.title:
                return True
        time.sleep(1)
    driver.switch_to.window(current_window)
    return False


def handle_nucleus_browser_sso_login(driver: WebDriver, userid):
    """Handles SSO logic for nucleus authentication

    Args:
        driver (WebDriver): Webdriver instance
        userid (_type_): UserId used to logging in to Nucleus
    """

    button_login_with_nvidia_sso = "//button[contains(text(), 'Log in with')]"

    switch_to_window_with_title(driver, "Login", timeout=300)
    WebDriverWait(driver, timeout=300).until(
        EC.presence_of_element_located((By.XPATH, button_login_with_nvidia_sso))
    )
    sso_btn = driver.find_element(By.XPATH, button_login_with_nvidia_sso)
    password = get_service_account_password(userid)
    sso_btn.click()
    time.sleep(5)
    WebDriverWait(driver, timeout=300).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='email' or @id='email']")
        )
    )
    email = driver.find_element(By.XPATH, "//input[@type='email' or @id='email']")
    email.send_keys(userid)

    ae_button_sso_sign_in = driver.find_element(By.XPATH, "//*[@type='submit']")
    ae_button_sso_sign_in.click()

    WebDriverWait(driver, timeout=300).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='passwd']"))
    )
    ae_input_sso_password = driver.find_element(By.XPATH, "//input[@name='passwd']")
    ae_input_sso_password.send_keys(password)
    time.sleep(2)
    submit_btn = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_btn.click()
    time.sleep(2)

def start_browser_in_normal_window():
    chrome_options = Options()
    if platform.system() == 'Windows':
        user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    else:
        user_data_dir = os.path.expanduser('~') + '/.config/google-chrome/Default'
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")   
    chrome_options.add_argument('--profile-directory=Default') 
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def verify_opened_website(url: str,driver: WebDriver, timeout=300):
    current_window = driver.current_window_handle
    available_windows = driver.window_handles
    start_time = time.time()
    while time.time() - start_time < timeout:
        for window in available_windows:
            driver.switch_to.window(window)
            if driver.title.find(url):
                return True
        time.sleep(1)
    driver.switch_to.window(current_window)
    return False


def get_process_by_port(port: int):
    """Return process running on a specified port."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    return proc
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return None


def kill_process_by_port(port: int):
    """Kill process running on a specified port."""
    logger = logging.getLogger()
    process = get_process_by_port(port)
    if process:
        logger.info(f"Process running on port {port} found. Terminating process...")
        process.terminate()
    else:
        logger.info(f"No process found running on port {port}.")


def fetch_extension_dependency(omni_driver, all_dependencies: list, ext_id: str):
    """
    Fetches dependencies of an extension identified by the given extension ID.

    Args:
        omni_driver: Omni Driver instance
        all_dependencies (list): A global list of dependencies
        ext_id (str): The ID of the extension for which dependencies are to be fetched.

    """
    logger = logging.getLogger()
    # Make the API call

    extension_detail = omni_driver.get_extension_details(ext_id)
    dependencies = extension_detail["state"].get("dependencies", {})

    # Check if all extensions from the API response are present in the global list
    if len(dependencies) == 0:
        logger.info(f"All extensions listed are already present in the global list for ext-> {ext_id}")
        return
    else:
        # Add new extensions to the global list
        dependencies = [x for x in dependencies if x not in all_dependencies]
        all_dependencies.extend(dependencies)
        logger.info(f"dependency of {ext_id} -> {dependencies}")
        # Make recursive call to get more extensions
        for ext in dependencies:
            fetch_extension_dependency(omni_driver, all_dependencies, ext)


def fetch_system_name() -> str:
    """Fetches the system name

    Returns:
        str: System name
    """
    hostname_process = subprocess.Popen(
        ["hostname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, _ = hostname_process.communicate()
    hostname = output.decode("utf-8").strip()
    return hostname

def fetch_ipv4_address() -> str:
    """Fetches the system ipv4 address

    Returns:
        str: IPv4 address
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        
    finally:
        s.close()
    
    return ip_address

def capture_screenshot(file_path: str):
    """
    Captures a screenshot of the current screen and saves it to a file.

    Args:
        file_path (str): Absolute path to destination

    Returns:
        None
    """
    with mss() as sct:
        sct.shot(output=file_path)

def encode_video(frame_path, video_name, file_format:str = ".mp4"):
    
    try:
        frame_names = sorted([os.path.join(frame_path, f) for f in os.listdir(frame_path) if f.startswith(video_name)])

        # Check if there are any frames
        if not frame_names:
            print("No frames found in the specified directory.")
            return False
        else:
            # Read the first frame to get video dimensions
            first_frame = cv2.imread(frame_names[0])
            height, width, layers = first_frame.shape

            # Define the codec and create a VideoWriter object
            video_name = video_name + file_format
            video_path = os.path.join(frame_path,video_name)
            fps = 30  # Adjust FPS as needed
            video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

            # Loop through all frames and write them to the video
            for frame_name in frame_names:
                frame = cv2.imread(frame_name)
                video_writer.write(frame)  # Write the frame to the video

            # Release the video writer object
            video_writer.release()
            logging.info(f"Video saved as {video_path}")
            # Delete all frames after video creation
            for frame_name in frame_names:
                os.remove(frame_name)
            return True
    except Exception as e:
            logging.error(f"Exception during video encoding: {e}")
            return False


def update_toml_value(file_path, section_path, key_path, new_value):
    """
    Update a value in a TOML file.

    Args:
        file_path (str): Path to the TOML file.
        section_path (str): Dot-separated path to the section.
        key_path (str): Dot-separated path to the key.
        new_value: New value for the key.
    """

    with open(file_path, 'r+', encoding='utf-8') as file:
        data = toml.load(file)

        sections = section_path.split('.')
        current_section = data

        for section in sections:
            current_section = current_section.setdefault(section, {})

        keys = key_path.split('.')
        current_key = current_section

        for key in keys[:-1]:
            current_key = current_key.setdefault(key, {})

        key = keys[-1]
        if key in current_key:
            current_key[key] = new_value
        else:
            raise KeyError(f"Key '{key}' not found in '{section_path}' section.")

        file.seek(0)
        toml.dump(data, file)
        file.truncate()


def is_app_version_compatible(min_version=107.1, app_name: str = "Kit"):
    """
    Verifies if app version meets the minimum requirement.
    
    Extracts version from installation path and performs version comparison.
    Returns the result without skipping the test, allowing flexible handling.
    
    Args:
        min_version (float): Required minimum version (default: 107.1)
        app_name (str): Target application name (default: "Kit")
        
    Returns:
        bool: True if version is sufficient, False otherwise
    """
    app_path = get_config().app.install_path

    # Fetching app install location from App Installer
    if not app_path:
        try:
            app_path = AppInstaller().get_app_install_location(app_name)
        except Exception as e:
            pass

    # Extract version number using regex
    import re
    match = re.search(r'(\d+\.\d+)', app_path)
    if match:
        version = float(match.group(1))
        return version >= min_version
