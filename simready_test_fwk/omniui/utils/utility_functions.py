# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Utilities class

    This module contains utilities for Omnidriver
"""
import importlib
import json
import os
import shutil
import socketserver
import sys
import subprocess
import random
import time
from enum import Enum
from zipfile import ZipFile
from PIL import Image

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
import pyperclip

from requests.adapters import HTTPAdapter, Retry
import requests


def get_window_model(driver, model: Enum, app: str, **kwargs):
    """Method to generate runtime window object models

    Args:
        driver (Omnidriver): Omnidriver object
        model (Enum): Model name from OmniModel enum
        app (str): Application under test
    """
    module_name = model.name
    class_name = model.value
    try:
        app_name = "_".join(app.lower().split())
        module = importlib.import_module(
            f"omniui.omni_models.{app_name}_models.{module_name}"
        )
        class_ = getattr(module, class_name)
        instance = class_(driver, **kwargs)
    except ModuleNotFoundError:
        module = importlib.import_module(
            f"omniui.omni_models.base_models.base_{module_name}"
        )
        class_ = getattr(module, f"Base{class_name}")
        instance = class_(driver, **kwargs)
    return instance


def remote_server_port_and_url(app_name: str):
    """Method to fetch remove server port and url to be used for connection.

    Args:
        app_name (str): Application under test

    Returns:
        str: Port number to connect with Kit automation server
        str: Host URL
    """
    config = os.path.join(os.getcwd(), "config", "test_config.json")
    with open(config, encoding="utf-8") as conf:
        data = json.load(conf)
        try:
            return (
                data["remote_server_host"][app_name],
                data["remote_server_port"][app_name],
            )
        except KeyError:
            return (
                data["remote_server_port"]["Default"],
                data["remote_server_host"]["Default"],
            )


def get_nucleus_server_url_and_user(server_name: str = "Default") -> tuple:
    """Method to fetch server url to be used for connection.

    Args:
        server_name (str): Nucleus server name

    Returns:
        str: Server url for connection
    """
    config = os.path.join(os.getcwd(), "config", "test_config.json")
    with open(config, encoding="utf-8") as conf:
        data = json.load(conf)
        if data["nucleus_server"][server_name]:
            return data["nucleus_server"][server_name], data["user"]
        else:
            return data["nucleus_server"]["Default"], data["user"]


def get_value_from_json(key: str, json_file: str = "test_config.json") -> str:
    """Gets a specific value from config json

    Args:
        key (str): Name of the key
        json_file (str, optional): Json file to search. Defaults to "test_config.json".

    Raises:
        Exception: When key is not found

    Returns:
        str: value for corresponging key as str
    """
    config = os.path.join(os.getcwd(), "config", json_file)

    with open(config, encoding="utf-8") as conf:
        data = json.load(conf)
        if data.get(key) is not None:
            return data.get(key)


def unzip_files(zip_file_path: str, unzip_folder_location: str):
    """
    Unzip files at given location

    Args:
        zip_file_path: File Path of Zip File
        unzip_folder_location: Folder path where Zip File contents will be unzipped
    """
    with ZipFile(zip_file_path, "r") as zip_data:
        zip_data.extractall(path=unzip_folder_location)


def write_to_file(file_path: str, file_content_to_write: list):
    """
    Writes data to file

    Args:
        file_path: File Path to write file to
        file_content_to_write: Content to write to file

    Returns:
        list: Contents of File
    """
    with open(file_path, "w") as file:
        file.writelines(file_content_to_write)
    file.close()


def read_file(file_path: str):
    """
    Reads data from file

    Args:
        file_path: File Path to read file from
        file_content_to_write: Content to write to file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.readlines()
    return file_contents


def get_text_from_current_field(omni_driver, handle_vscode: bool = False):
    """
    Fetches all the text from whichever text field the cursor is currently present,
    irrespective of active application context
    :param omni_driver: instance of OmniDriver
    :param handle_vscode: flag to handle VS code
    :return: All text from the text field
    """
    keyboard = Controller()
    if handle_vscode:
        for i in range(3):
            keyboard.tap(Key.esc.value)
        keyboard.tap(Key.enter.value)
        for i in range(3):
            keyboard.tap(Key.esc.value)
        omni_driver.wait(2)
    with keyboard.pressed(Key.ctrl.value):
        keyboard.tap("a")
        keyboard.tap("c")
    omni_driver.wait(3)
    return pyperclip.paste()


def send_text_to_text_editor_and_save(
    omni_driver, text: str, handle_vscode: bool = False
):
    """
    Sends the text to whichever text field the cursor is currently present,
    irrespective of active application context
    :param omni_driver: instance of OmniDriver
    :param text: text which is to be sent
    :param handle_vscode: flag to handle VS code
    """
    keyboard = Controller()
    if handle_vscode:
        for i in range(3):
            keyboard.tap(Key.esc.value)
        keyboard.tap(Key.enter.value)
        for i in range(3):
            keyboard.tap(Key.esc.value)
        omni_driver.wait(2)

    pyperclip.copy(text)
    with keyboard.pressed(Key.ctrl.value):
        keyboard.tap("a")
        omni_driver.wait(1)
        keyboard.tap("v")
    omni_driver.wait(3)

    with keyboard.pressed(Key.ctrl.value):
        keyboard.tap("s")


def occurrence_of_string_in_logs(string: str, log_file: str):
    """
    Returns the number of times a string has occurred in the log file
    :param string: string to search
    :param log_file: path of log file
    :return: number of times the string has appeared in the log file
    """
    count = 0
    with open(log_file, encoding="utf-8") as file:
        for log in file.readlines():
            if string in log:
                count += 1
    return count


def get_random_viewport_coordinate(x_pos: float, y_pos: float):
    """Generates random coordinate in viewport Window

    Args:
        x_pos (float): X-coordinate of Viewport Center
        y_pos (float): Y-coordinate of Viewport Center
    """
    x_pos, y_pos = int(x_pos), int(y_pos)
    quads = {}
    quads["first_quad"] = (
        random.randrange(x_pos, x_pos + 450, 10),
        random.randrange(y_pos - 300, y_pos),
    )
    quads["second_quad"] = (
        random.randrange(x_pos - 450, x_pos, 10),
        random.randrange(y_pos - 300, y_pos),
    )
    quads["third_quad"] = (
        random.randrange(x_pos - 450, x_pos, 10),
        random.randrange(y_pos, y_pos + 250),
    )
    quads["fourth_quad"] = (
        random.randrange(x_pos, x_pos + 450, 10),
        random.randrange(y_pos, y_pos + 250),
    )
    x_pos, y_pos = random.choice(list(quads.values()))
    return x_pos, y_pos


def read_contents_of_txt_file(file_loc: str):
    """Reads content of text file

    Args:
        file_loc (str): Location of file

    Returns:
        String: Contents of text file
    """
    assert os.path.isfile(file_loc), f"Provided path is not of valid file - {file_loc}"

    with open(file=file_loc, encoding="utf-8") as file:
        data = file.read()

    return data


def crop_image(image_path: str, left=0, right=0, top=0, bottom=0):
    """Crops image to given size"""
    if "/" not in image_path and "\\" not in image_path:
        image_path = os.path.join(get_images_dir(), image_path).replace("\\", "/")

    # Renaming image name
    temp = image_path.split("/")
    path, new_name = "/".join(temp[:-1]), temp[-1]
    name_split = new_name.split(".")
    name_split[0] += "_cropped"
    new_name = ".".join(name_split)
    save_path = path + "/" + new_name

    assert os.path.isfile(image_path), f"File does not exist at path: {image_path}"
    image = Image.open(image_path)
    width, height = image.size
    right = width - right
    bottom = height - bottom
    crop_image = image.crop((left, top, right, bottom))
    crop_image.save(save_path)


def connect_to_nucleus_server(
    server_url: str, user: str, endpoint: str, token="nucleus_token"
):
    """Performs nucleus authentication via API
    Args:
        server_url (str): Server URL to be added
        user (str): User for authentication
        endpoint (str): URL to use for hitting the API, base url is same as Omnidriver URL
    """
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    auth_token = get_service_account_password(user, token)

    body = {
        "serverUrl": f"omniverse://{server_url}",
        "username": "$omni-api-token",
        "token": f"{auth_token}",
    }
    response = session.post(
        url=endpoint + "/nucleus/authenticate",
        json=body,
        verify=False,
    ).json()

    assert (
        response["connectionStatus"] == "CONNECTED"
    ), "Failed to connect to nucleus server"


def search_and_extract_path(file_path: str, search_string: str, app_slug: str):
    """Searches for a specific string in file and extracts directory path
    Args:
        file_path (str): Path of file to be openend
        search_string (str): String to be searched
        app_slug (str): App Slug to be used for search_string extract
    Raises:
        Exception: When extracted path is not a valid directory
    Returns:
        None|str: Returns None if no path is found, returns path as string if found.
    """
    directory_path = None
    file_path = os.path.join(os.getcwd(), file_path)
    assert os.path.isfile(
        file_path
    ), "Omniverse Application Installer file path is missing. Either it did not run or failed intermittently."
    app_installer_log = read_file(file_path=file_path)
    app_slug_index = None
    for line_index, log_line in enumerate(app_installer_log):
        if f"Input BuildType from commandline: {app_slug}" in log_line:
            app_slug_index = line_index
            break
    if app_slug_index is None:
        raise Exception(f"Failed to find App Installed: {app_slug}")
    for log_line in app_installer_log[app_slug_index:]:
        log_line = log_line.strip()
        if search_string in log_line:
            # Split the line on the first occurrence of the search string
            line_parts = log_line.split(search_string, 1)
            # Extract the part of the line before the search string
            directory_path = line_parts[1].strip()
            break
    if directory_path:
        directory_path = os.path.abspath(directory_path)
        print("Directory Path: ", directory_path)
        if os.path.isdir(directory_path):
            return directory_path
        else:
            raise Exception(f"{directory_path} is not a valid directory")
    else:
        raise Exception("Failed to find Directory Path")


def search_and_extract_key(file_path: str, search_string: str):
    """Searches for a specific key in file and extracts it's value
    Args:
        file_path (str): Path of file to be openend
        search_string (str): Key to be searched
    Raises:
        Exception: When key not found
    Returns:
        None|str: Returns None if no key is found, returns value as string if found.
    """
    value = None
    file_path = os.path.join(os.getcwd(), file_path)
    assert os.path.isfile(file_path), f"Failed to find {file_path}"
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if search_string in line:
                # Split the line on the first occurrence of the search string
                line_parts = line.split(search_string, 1)
                # Extract the part of the line before the search string
                value = line_parts[1].strip()
    if value:
        return value
    else:
        raise Exception(f"{search_string} is not found")


def get_environ_variable(env_var: str):
    """Returns the value of given env variable

    Args:
    env_var(str): variable to return
    """
    try:
        return os.environ.get(env_var)
    except NameError:
        print(f"Unable to find {env_var} in environment variable")
        return None


def copy_and_rename_images(current_name: str, new_name: str):
    """
    Method for copy and rename Images

    Args:
       current_name (str): Current Name of image file
       new_name (str): New Name of image file
    """
    current_path = os.path.join(get_images_dir(), current_name)
    new_path = os.path.join(get_images_dir(), new_name)
    shutil.copy2(current_path, new_path)


def get_service_account_password(service_account: str = None, key="password"):
    """
    get service account password from credential service manager
    """
    account = service_account
    account = account.replace("@nvidia.com", "")
    cmd_line = f"{sys.executable} -m credential_manager -user {account} -key {key} -config vault_config.ini"
    return (
        subprocess.run(cmd_line, shell=True, stdout=subprocess.PIPE)
        .stdout.decode()
        .rstrip()
    )


def get_downloads_folder_path():
    """Get Downloads folder path on System"""
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    return download_path


def create_folder_if_not_present(folder_path: str):
    """
    Creates folder if not present
    :param folder_path: path of folder
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)


def get_images_dir():
    """
    Gets the location of image directory, defaults to results/images
    Note: This function is now mainly used for fallback cases.
    BaseModel uses the patched screenshot directory from conftest.py
    """
    try:
        from conftest import log_folder
        if log_folder:
            # Return path consistent with conftest.py structure
            return f"pytest_results/{log_folder}/images"
    except ImportError:
        # Fallback for when conftest is not available
        pass

    # Default fallback
    image_dir = get_value_from_json("images_dir")
    if not image_dir:
        create_folder_if_not_present("results/images")
        return "results/images"
    return image_dir


def get_free_local_port():
    """Returns a free port to be used for 2nd instance of the app

    Returns:
        String: Port Number
    """
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = str(s.server_address[1])
    return free_port


def handle_nucleus_browser_repeat_login(browser_web_driver):
    """
    Handles sso relogin where no userid password is added, usually this use case comes when you have already logged into another server

    """
    browser_web_driver.switch_to_and_check_window_by_title("Login", timeout=300)
    ae_button_login_with_nvidia_sso = "//button[contains(text(), 'Log in with')]"
    WebDriverWait(browser_web_driver.driver, timeout=300).until(
        EC.presence_of_element_located((By.XPATH, ae_button_login_with_nvidia_sso))
    )
    sso_btn = browser_web_driver.driver.find_element(
        By.XPATH, ae_button_login_with_nvidia_sso
    )
    sso_btn.click()

    #  TODO - Commented below lines since "Stay signed in page is not coming after entering password."
    # WebDriverWait(browser_web_driver.driver, timeout=300).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[@type='button' and @value='No']"))
    # )
    # ae_button_sso_stay_signed_in = browser_web_driver.driver.find_element(
    #     By.XPATH, "//input[@type='button' and @value='No']"
    # )
    # ae_button_sso_stay_signed_in.click()

    WebDriverWait(browser_web_driver.driver, timeout=300).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(),'You have successfully logged in. ')]")
        )
    )

    assert browser_web_driver.driver.find_element(
        By.XPATH, "//div[contains(text(),'You have successfully logged in. ')]"
    )


def read_json_data(json_file: str = "test_config.json") -> dict:
    """Gets a values from config json

    Args:
        json_file (str, optional): Json file to search. Defaults to "test_config.json".

    Raises:
        Exception: When key is not found

    Returns:
        dict: entire json data
    """
    config = os.path.join(os.getcwd(), "config", json_file)
    with open(config, encoding="utf-8") as conf:
        data = json.load(conf)
        return data


def snippet_presence_in_logs(log_file, lines_to_check):
    """
    Verifies the presence of multiple continues lines snippet in logs
    Args:
        log_file: log file path
        lines_to_check: multiple continues lines snippet
    Returns: True if the snippet is present else False
    Raises:
        FileNotFoundError: when log file does not exist
    """
    with open(log_file, 'r') as file:
        lines = file.readlines()

    continuous_lines = []
    index = 0
    for line in lines:
        if lines_to_check[index] in line:
            continuous_lines.append(line)
            index += 1
            if index == len(lines_to_check):
                return True
        else:
            index = 0
            continuous_lines = []
    return False
    
def save_folder_structure_to_json(folder_path:str):
    """ Saves the folder structure to a json format
    Args:
        folder_path : path to folder
    Returns: 
        data in json    
    """
    # Init 
    json_result = {'name': os.path.basename(folder_path), 
              'type': 'folder', 'children': []} 
  
    # Is root a directory 
    if not os.path.isdir(folder_path): 
        return json_result 
  
    # Iterate the directory 
    for elem in os.listdir(folder_path): 
        entry_path = os.path.join(folder_path, elem) 
  
        # If the entry is a directory, recursively call the function 
        if os.path.isdir(entry_path): 
            json_result['children'].append(save_folder_structure_to_json(entry_path)) 
        
        # If the entry is a file, create a dictionary with name and type 
        else: 
            json_result['children'].append({'name': elem, 'type': 'file'}) 
  
    return json_result 

def get_latest_folder_from_path(folder_path:str):
    """ Gets latest folder from path
    Args:
        folder_path : path to folder
    Returns: 
        name of latest folder
    """
    # Get all directories in the specified directory
    all_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    
    # Sort directories by modification time
    sorted_folders = sorted(all_folders, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    
    # Return the latest folder
    if sorted_folders:
        return sorted_folders[0]
    else:
        return None