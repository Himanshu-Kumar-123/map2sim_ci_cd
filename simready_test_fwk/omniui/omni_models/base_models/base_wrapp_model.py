"""Base Welcome to Omniverse model class
   This module contains the base methods for Welcome to Omniverse Model for actions to perform as soon as app opens
"""
import time
from ..base_models.base_model import BaseModel
import time
import sys
import os
import platform

class BaseWrappModel(BaseModel):
    """BaseWrappModel class for apps like Code containing common methods"""


    def execute_commands(self,commands,log_file: str,wrapp_exe_path:str):
        """Method to take to check presence of elements at given path

        Args:
            path (str):nuclues server path
            elements (list)): Elements which need to verify.

        """
        time.sleep(2)
        try:
            for command in commands:
                if sys.platform == "win32":
                    command_with_output_redirection = f'{wrapp_exe_path}\\wrapp {command} >> {log_file} 2>&1'
                else: 
                    command_with_output_redirection = f'{wrapp_exe_path}/wrapp {command} >> {log_file} 2>&1'
                self.log.info(f"command {command_with_output_redirection}")
                os.system(command_with_output_redirection)

        except IndexError:
            self.log.error(f"Error: No window found with process name")

        except Exception as e:
            self.log.error(f"Error interacting with the window: {e}")

    
    def verify_elements_for_given_path(self,path: str,elements:[]):
        """Method to take to check presence of elements at given path

        Args:
            path (str):nuclues server path
            elements (list)): Elements which need to verify.

        """
        if len(elements)==0:
            self.omni_driver.wait(2)
            response = self.omni_driver.list(path)
            self.log.info(f"Response Elements: {len(response)}")
            self.log.info(f"No Elements for verify Fetching Elements:{response} for path: {path}")
            if len(response)==0:
                return True
            return False
        else:
            self.omni_driver.wait(2)
            response = self.omni_driver.list(path)
            self.log.info(f"Fetched Elements:{response} for path: {path}")
            for item in elements:
                if item in response:
                    continue
                else:
                    self.log.info(f"Files are not present at given location")
                    return False

            self.log.info("all files are there at given location verfication successfull!!")
            return True
    
    def delete_file(self,folder_path: str,file_name:str):
        """Method to delete file at given path

        Args:
            folder_path (str): nuclues server path
            file_name (str): file name
        """
     
        self.omni_driver.wait(2)
        self.omni_driver.delete_file_or_folder(folder_path+file_name,raise_error_if_path_not_present=False)
        self.log.info(f"file : {file_name} deleted from path: {folder_path}")

    def delete_folder(self,folder_path: str):
        """Method to delete folder at given server location

        Args:
            folder_path (str): nuclues server path
        """
        self.omni_driver.wait(2)
        self.omni_driver.delete_file_or_folder(folder_path,raise_error_if_path_not_present=False)
        self.log.info(f"deleted from path: {folder_path}")

    
    def extract_path_from_logfile(self,file_path: str):
        """Method to get path and version of package from given file location

        Args:
            file_path (str): log file path
        """
        path = ""
        with open(file_path, 'r') as file:
            read_lines = file.readlines()
            line = read_lines[0]
            self.log.info(f"list path from log file = {line}")
            split_result = line.split(': ')

            # Extract path and version
            path = split_result[0].strip()
            version = split_result[1].strip() if len(split_result) > 1 else None
            self.log.info(f"The path of package = {path} and its version = {version}")


            path = f"{path}/{version}"
            self.log.info(f"Extracted path from the log string: {path}")
        return path
    
    def verify_log_data(self,search_string: str,file_path: str):
        """Method to verify given search string from given file

        Args:
            search_string (str): string that needs to be searched
            file_path (str): file path
        """
        assert os.path.isfile(
            file_path
        ), "Wrapp log file is not present"
        log_line = "".join(open(file_path).read().splitlines())
        if search_string in log_line:
            self.log.info(f"Found search string:{search_string} in line: {log_line}")
            return True
        self.log.info(f"Search string:{search_string} not found")
        return False
    
    def delete_exported_wrapp_file(self,file_name:str):
        """Deletes the exported given .tar file
    
        Args:
        file_name (string) : File name that need to be deleted
        """
        if platform.system() == 'Windows':
            file_path = os.getcwd() + f"\\{file_name}"
        else:
            file_path = os.getcwd() + f"/{file_name}"

        self.log.info(f"Export .tar file: {file_path}")
        self.log.info(os.path.isfile(file_path))

        if os.path.isfile(file_path):
            self.log.info(f"Inside if file exist")
            try:
                os.remove(file_path)
                self.log.info(f"File {file_path} deleted successfully.")
                return True
            except FileNotFoundError:
                self.log.info(f"File {file_path} not found.")
            except PermissionError:
                self.log.info(f"Permission error: Unable to delete {file_path}.")
            except Exception as e:
                self.log.info(f"An error occurred: {e}")
            return False
        
        return True
        
    def verify_exported_wrapp_file(self,file_name:str):
        """Checks if the exported file is present or not

        Args:
            file_name (str): name of file that needs to checked
        """
        os.path.join(os.path.expanduser('~'))
        if platform.system() == 'Windows':
            file_path = os.getcwd() + f"\\{file_name}"
        else:
            file_path = os.getcwd() + f"/{file_name}"
    
        self.log.info(f"Exported file path: {file_path}")

        if os.path.isfile(file_path):
            self.log.info(f"Exported file is present at: {file_path}")
            return True
        self.log.info(f"Exported file is not present at: {file_path}")
        return False

    def run_command_in_thread(self,commands,log_file,wrapp_exe_path):
        """Method to add new nucleus server connection

        Args:
            commands (list): list of commands
            log_file (str): Log file path
            wrapp_exe_path (str): wrapp.exe path
        """
        for command in commands:
            import threading
            self.log.info("Starting executing command another thread.")
            thread = threading.Thread(target=self.execute_commands, args=([command],log_file,wrapp_exe_path))
            self.log.info("Started execution in another thread.")
            thread.start()
            thread.join()