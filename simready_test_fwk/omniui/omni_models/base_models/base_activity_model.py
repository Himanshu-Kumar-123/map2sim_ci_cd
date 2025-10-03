# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Activity class
   This module contains the base methods for Activity window
"""

import os
import re
from ..base_models.base_model import BaseModel
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
from pynput.keyboard import Key, Controller
from omni_remote_ui_automator.driver.omnielement import OmniElement
from omni_remote_ui_automator.common.constants import KeyboardConstants
from typing import List, Dict
from omniui.utils.utility_functions import (
    get_downloads_folder_path,
)


class BaseActivityModel(BaseModel):
    """Base model class for Activity window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Activity window
    _window_name = "Activity Progress"
    _activity_window = "Activity Progress//Frame/Frame[0]/VStack[0]"
    
    # Progress Bar Window
    _progress_bar_option = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[0]/RadioButton[0]"
    _progress_bar_usd_count = "Activity Progress//Frame/**/ScrollingFrame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[1]/Label[0]"
    _progress_bar_material_count = "Activity Progress//Frame/**/ScrollingFrame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[3]/Label[0]"
    _progress_bar_texture_count = "Activity Progress//Frame/**/ScrollingFrame[0]/ZStack[0]/VStack[0]/HStack[0]/VStack[0]/HStack[5]/Label[0]"
    
    # Activity Window
    _activity_option = "Activity Progress//Frame/**/RadioButton[1].text=='Activity'"
    _activity_hamburger = "Activity Progress//Frame/**/Button[0].name=='options'"

    # Locators related to Main Progress Bar
    #_progress_bar = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[2]/VStack[1]/ZStack[0]/HStack[0]/Label[0]"
    _total_files = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[2]/VStack[1]/HStack[0]/Label[0]"
    _load_time = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[2]/VStack[1]/HStack[0]/Label[1]"
    #_progress_status = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[2]/VStack[1]/ZStack[0]/HStack[0]/Label[0]"
    #_progress_percentage = "Activity Progress//Frame/Frame[0]/VStack[0]/HStack[2]/VStack[1]/ZStack[0]/HStack[0]/Label[1]"
 
    # Activity Timeline
    _activity_timeline = "Activity Timeline//Frame/Frame[0]/VStack[0]"
    _activity_timeline_hamburger = "Activity Timeline//Frame/**/Button[0].name=='options'"
    _timeline_activities = "Activity Timeline//Frame/**/RadioButton[1].text=='Activities'"
    _timeline_texture_expand = "Activity Timeline//Frame/**/ScrollingFrame[0]/TreeView[0]/HStack[11]/ImageWithProvider[0]"

    # Save/Open Log
    _directory_path_picker = "Save As...//Frame/**/StringField[*].identifier=='filepicker_directory_path'"
    _test_folder = "apollo-prod.ov.nvidia.com/Library/test/ActivityTest/"
    _save_dialog = "Save As...//Frame/VStack[0]"
    _file_name_textbox = "Save As...//Frame/VStack[0]/HStack[2]/ZStack[0]/HStack[0]/Placer[0]/StringField[0]"

    # Timeline Activities TreeView
    _timeline_activities_TreeView = "Activity Timeline//Frame/Frame[0]/VStack[0]/VStack[0]/ZStack[0]/VStack[1]/ScrollingFrame[0]/TreeView[0]"
    _timeline_activities_plus_icon = "Activity Timeline//Frame/**/ScrollingFrame[0]/TreeView[0]/HStack[*]/ImageWithProvider[0]"
    
    
    def load_activity_window(self):
        """Loads activity window
        
        """
        self.omni_driver.select_menu_option("Window/Utilities/Activity Progress")
        self.omni_driver.wait(2)
    
    def is_activity_window_enabled(self):
        """Checks if activity window is enabled
        
        Returns:
            True/False
        """

        found = False
        try:
            activity_window = self.omni_driver.find_element(self._activity_window, True)
            found = True
        except Exception:
            pass 
        
        return found

    def get_activity_tree(self) -> Dict:
        """Get all the elements from the activity tree(file and size)

        Returns:
            dict: Dictionary of all elements
        """
        # Click on Activity tab
        activity_element=self.omni_driver.find_element(self._activity_option, True)
        activity_element.click()

        main_tree=self.omni_driver.find_element("Activity Progress//Frame/**/TreeView[0]", True)
        file_names=main_tree.find_elements("**/HStack[0]/Label[0]")
        files_count = len(file_names) * 3 # since there are 3 columns name, durataion and size, files_count is row count of tree
        tree_details = {}

        for counter in range(0, files_count, 3):
            main_path = f"Activity Progress//Frame/Frame[0]/VStack[0]/HStack[1]/ScrollingFrame[0]/ZStack[0]/VStack[1]/TreeView[0]"
            
            name_path = main_path + f"/VStack[{counter}]/HStack[0]/Label[0]"
            file_name = self.omni_driver.find_element(name_path, True)
            file_data = file_name.get_text()

            # Duration may change and not feasible to compare, hence ignoring it and fetching size
            size_data = 0
            size_path = main_path + f"/VStack[{counter+2}]/Label[0]"

            # Exception ignored when ther is no Label[0] in tree for a particular row
            try:
                size_name = self.omni_driver.find_element(size_path, True)
                size_data = size_name.get_text()
            except Exception:
                pass 
                
            tree_details[file_data] = size_data
            
        return tree_details

    def get_total_files(self):
        """Get all the elements from the activity progress bar

        Returns:
            total files (int)
        """
        # Fetched value is like 'Total:624/624' split it accordingly
        element = self.omni_driver.find_element(self._total_files, True)
        element_label = element.get_text().split(':')[1]
        return int(element_label.split('/')[1])

    def get_count_details(self, prim: str):
        """Get the current loaded count and total count

        Args:
            Prim name (str) :  Count of prim USD or Material or Texture
        Return:
            Current Loaded, Total Count (int)
        """
        element = self.omni_driver.find_element(prim, True).get_text()
        tokens = element.split("/")
        return int(tokens[0]), int(tokens[1])
    
    def select_hamburger_menu_option(self, setting: str):
        """Selects option from setting menu

        Args:
            setting (str) : Hamburger of Timeline or Activity
        """
        menu_path = setting.split("/")
        menu = self.omni_driver.find_element(self._activity_hamburger,True)
        menu.click()
        self.omni_driver.wait(2)
        if len(menu_path) > 0:
            self.omni_driver.select_context_menu_option(menu_path[0])
        if len(menu_path) > 1:
            for i in range(1,len(menu_path)): 
                setting_label = "**/Label[*].text=='" + menu_path[i] +"'"
                option = self.omni_driver.find_context_menu_elements(menu_path[i-1],setting_label)
                if option:
                    option[0].click(False)
    
    def is_activity_timeline_active(self):
        """Verify if activity timeline is enabled

        Returns:
            True/False
        """
        timeline_found = False
        try:
            timeline_elem = self.omni_driver.find_element(self._activity_timeline, True)
            timeline_found = True
        except Exception:
            pass

        return timeline_found
    
    def is_save_dialog_active(self):
        """Verify if save as dialog is enabled

        Returns:
            True/False
        """
        dialog_found = False
        try:
            dialog_elem = self.omni_driver.find_element(self._save_dialog, True)
            dialog_found = True
        except Exception:
            pass

        return dialog_found
    
    def save_activity_file(self, hamburger:str, file_name:str):
        """Save file to download folder
        
        Args:
            hamgurger(str) :  Timeline or Activity
            FileName(str) : Filename to save with without extension, default is .acivity
       
        """
        menu_elem = self.omni_driver.find_element(hamburger, True)
        menu_elem.click()
        self.omni_driver.wait(1)
        self.omni_driver.select_context_menu_option("Save...")
        self.omni_driver.wait(1)

        search_bar: OmniElement = self.omni_driver.find_element(self._directory_path_picker)
        search_bar.click(bring_to_front=True)
        self.omni_driver.wait(3)
        #search_bar.send_keys("omniverse://" + self._test_folder)
        search_bar.send_keys("file://"+ get_downloads_folder_path())
        self.omni_driver.wait(5)

        text_box_elem = self.omni_driver.find_element(self._file_name_textbox, True)
        try:
            text_box_elem.send_keys(file_name)
        except Exception:
            pass
        self.omni_driver.wait(2)       

    def enable_timeline_activities(self):
        """Enable activities from Timeline
        
        """
        elem = self.omni_driver.find_element(self._timeline_activities, True)
        elem.click()

    def get_treeview_columns_label(self):
        """Get all 5 colums Name, Dur, Start, End and Size are visible
        
        Return:
            all_labels(list) : List of labels
        """
        all_labels = []
        for counter in range(0, 5):
            xpath = self._timeline_activities_TreeView + f"/Label[{counter}]"
            get_label_element = self.omni_driver.find_element(xpath)
            all_labels.append(get_label_element.get_text().strip())
        return all_labels
    
    def get_element_count_loaded(self):
        """Get the count of element loaded
        
        Returns:
            USD_count(int) : Count of USD in timeline
            Material_count(int) : Count of Material in timeline
        """

        # Expand material, usd and texture group
        # TODO: Workaround till we have API
        
        # Resize the activity timeline window to fetch all tree elements
        self.set_window_position("Activity Timeline", 0, 0)
        self.omni_driver.find_element("Activity Timeline").resize_window(1363, 900)        
        
        # Expand all nodes
        all_labels = []
        expand_list = self.omni_driver.find_elements(self._timeline_activities_plus_icon)
        for expand in reversed(expand_list):           
            expand.click()
            # First level open, get tree details
            main_treeview_elements = self.omni_driver.find_element(self._timeline_activities_TreeView, True)
            get_label_elements = main_treeview_elements.find_elements("**/Label[0]")       
            for lbl in get_label_elements:
                lab = lbl.get_text()
                all_labels.append(lab)

        # Look for USD->Read, Material and Texture->Load
        usd_count = None
        material_count = None
        texture_count = None
        try:
            for label in all_labels:
                if 'Read (' in label:
                    usd_count = int(label[label.find("(")+1:label.find(")")])
                if 'Materials (' in label:
                    material_count = int(label[label.find("(")+1:label.find(")")])
                if 'Load (' in label:
                    texture_count = int(label[label.find("(")+1:label.find(")")])
        except Exception:
            pass
        self.log.info(f"Counts fetched, USD : {usd_count}, Materials : {material_count}, Texture : {texture_count}")
        return usd_count, material_count, texture_count
