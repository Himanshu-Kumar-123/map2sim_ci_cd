# -*- coding: utf-8 -*-
# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

# """
# VS Code installation script
# """
import logging
import os
import subprocess
import sys
import platform
import shutil
import psutil


log = logging.getLogger()  # auto added class log instance


def get_installer_directory():
    """Returns Directory for VS Code Installer"""
    location = ""
    if sys.platform == "win32":
        location = "C:/Gitlab_Runner/locked"
    else:
        location = f"{os.path.expanduser('~')}/Gitlab_Runner/locked"
    if not os.path.exists(location):
        raise RuntimeError(
            f"VS Code installer not present at given location: {location}"
        )
    return location

def kill_vscode():
        # Define the process name for VS Code
        process_name = "code"
        if platform.system() == 'Windows':
            process_name = "Code.exe"

        # Iterate over all running processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check if process name matches VS Code process
                if process_name.lower() in proc.info['name'].lower():
                    log.info(f"Killing process {proc.info['name']} with PID {proc.info['pid']}")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                log.info(f"Error killing process: {e}")

def install_vscode_windows(version):
    try:
        url = f"https://update.code.visualstudio.com/{version}/win32-x64/stable"
        filename = f"VSCodeSetup-{version}.exe"
        installer_path = os.path.join(get_installer_directory(), filename)

        # Download the installer
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Invoke-WebRequest -Uri '{url}' -OutFile '{installer_path}'",
            ],
            check=True,
        )

        install_path = os.path.join(get_installer_directory(), "VSCode")

        # Install silently without launching VS Code
        subprocess.run([installer_path, "/VERYSILENT", "/NORESTART", f"/DIR={install_path}", "/mergetasks=!runcode"], check=True)

        # Remove the installer file after installation
        os.remove(installer_path)
        log.info(f"VS Code {version} installed successfully on Windows.")

    except subprocess.CalledProcessError as e:
        log.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
    except Exception as e:
        log.error(f"An error occurred: {str(e)}")


def install_vscode_linux(version):
    try:
        url = f"https://update.code.visualstudio.com/{version}/linux-deb-x64/stable"
        filename = f"code_{version}-1_amd64.deb"
        installer_path = os.path.join(get_installer_directory(), filename)
        install_path = os.path.join(get_installer_directory(), "VSCode")

        # Download the installer
        subprocess.run(["wget", url, "-O", installer_path], check=True)

        # Install the .deb package
        subprocess.run(["dpkg-deb", "-x", installer_path, install_path], check=True)

        # Remove the installer file after installation
        os.remove(installer_path)
        log.info(f"VS Code {version} installed successfully on Linux.")

    except subprocess.CalledProcessError as e:
        log.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
    except Exception as e:
        log.error(f"An error occurred: {str(e)}")


def uninstall_all_vscode_windows():
    possible_paths = [
        os.path.join(os.environ["ProgramFiles"], "Microsoft VS Code"),
        os.path.join(os.environ["ProgramFiles(x86)"], "Microsoft VS Code"),
        os.path.join(os.environ["LocalAppData"], "Programs", "Microsoft VS Code"),
        os.path.join(os.environ["LocalAppData"], "Programs", "Microsoft VS Code Insiders")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            log.info(f"Uninstalling VS Code from {path}...")
            uninstaller = os.path.join(path, "unins000.exe")
            if os.path.exists(uninstaller):
                subprocess.run([uninstaller, "/silent"], check=True)
                log.info(f"VS Code uninstalled successfully from {path}.")
            else:
                log.info(f"Uninstaller not found in {path}, removing folder directly.")
                shutil.rmtree(path)


def uninstall_all_vscode_linux():
    # Remove installations done via package managers
    log.info("Uninstalling VS Code installations via apt...")
    subprocess.run(["sudo", "apt-get", "remove", "-y", "code"], check=True)

    # Also check for VS Code installations in common directories
    possible_paths = [
        "/usr/share/code",
        "/usr/local/share/code",
        os.path.expanduser("~/.vscode"),
        os.path.expanduser("~/.vscode-insiders"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            log.info(f"Removing VS Code files from {path}...")
            shutil.rmtree(path)


def install_vscode(version):
    system = platform.system()
    kill_vscode()
    if system == "Windows":
        # uninstall_all_vscode_windows()
        install_vscode_windows(version)
    elif system == "Linux":
        # uninstall_all_vscode_linux()
        install_vscode_linux(version)
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def install_python_debug_extension():
    if platform.system() == "Windows":
        pip_command = "pip"
    else: 
        pip_command = os.path.join(os.sys.prefix, 'bin', 'pip')
    try:
        log.info(pip_command)
        subprocess.check_call([pip_command, "install", "debugpy"])
        log.info("debugpy installed successfully.")
    except subprocess.CalledProcessError:
        log.info("Failed to install debugpy.")
    try:
        os.system("code --install-extension ms-python.debugpy")
        log.info("VS Code Python extension installed successfully.")
    except Exception as e:
        log.info(f"Exception occured {e}")
    
if __name__ == "__main__":
    vscode_version = "1.92.2"
    install_vscode(vscode_version)
