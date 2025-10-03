# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Assets Model class
   This module contains the base methods for Assets window
"""
from ..base_models.base_model import BaseModel


from bs4 import BeautifulSoup
from omni_remote_ui_automator.driver.exceptions import ElementNotFound
import re
from omniui.utils.utility_functions import get_value_from_json


class BaseSimpleShareModel(BaseModel):
    """Base model class for Simple Share related methods

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _cloudshare = "Viewport//Frame/**/Button[0].name=='CloudShare'"
    _share_window = "Share: Kitchen_set.usd//Frame/VStack[0]"
    _loading_info_label = "Share: Kitchen_set.usd//Frame/**/Label[0].text=='Loading share info ...'"
    _email_field = "Share: Kitchen_set.usd//Frame/**/StringField[0]"
    _share_button = "Share: Kitchen_set.usd//Frame/**/OneClickButton[0]"
    _overwrite_share = "Share: Kitchen_set.usd//Frame/**/OneClickButton[1].text=='Overwrite existing and upload again'"
    _share_finish_label = "Share: Kitchen_set.usd//Frame/**/Label[0].text=='File has been shared with'"
    _close_button = "Share: Kitchen_set.usd//Frame/**/Button[0].text=='Close'"

    def _click_share_button(self):
        """Clicks on share button and waits for share window to open"""
        self.find_and_click(self._cloudshare)
        self.wait.element_to_be_located(self.omni_driver, self._share_window)
        self.omni_driver.wait(10)

    def _enter_recipient_emails(self):
        """Enters the emails of the recipients"""
        emails = get_value_from_json("test_simple_share_e2e", "create_test_data.json")["recipient_emails"]
        email_field = self.omni_driver.find_element(self._email_field)
        email_field.send_keys(emails)
        self.omni_driver.wait(2)

    def _handle_overwrite_share(self):
        """Handles the pop up of overwrite share if it occurs"""
        try:
            self.wait.element_to_be_located(self.omni_driver, self._overwrite_share)
            overwrite_share = self.omni_driver.find_element(self._overwrite_share)
            overwrite_share.click()
        except ElementNotFound:
            pass

    
    def get_invite_link(self, emails: list):
        """Returns invite link from required email

        Args:
            emails (list): List of all e-mails

        Returns:
            str: invite link
        """
        email_index = -1
        for i in range(len(emails)):
            if (
                emails[i]["sender"]
                == get_value_from_json("test_simple_share_e2e", "create_test_data.json")["invite_email_sender"]
            ):
                email_index = i
                break
        invite_message = emails[email_index]["message"]
        soup = BeautifulSoup(invite_message, "html.parser")
        invite_link = soup.find_all("a")[1].get("href")
        return invite_link

    
    def share_scene(self):
        """Shares the current scene to emails provided

        Args:
            emails (str): string of recipient emails separated by a comma
        """
        self._click_share_button()
        self._enter_recipient_emails()
        self.find_and_click(self._share_button)
        self._handle_overwrite_share()
        self.wait.element_to_be_located(self.omni_driver, self._share_finish_label)
        self.find_and_click(self._close_button)

    def get_security_check_link(self, emails):
        """Returns security check link from the specific email

        Args:
            emails (_type_): List of all the e-mails

        Returns:
            security_link(str): security url link
        """
        email_index = -1
        for i in range(len(emails)):
            if (
                emails[i]["sender"]
                == get_value_from_json("test_simple_share_e2e", "create_test_data.json")["security_email_sender"]
            ):
                email_index = i
                break
        security_message = emails[email_index]["message"]
        security_link = re.findall(r"\<.*?\>", str(security_message))[1][1:-1]
        return security_link
