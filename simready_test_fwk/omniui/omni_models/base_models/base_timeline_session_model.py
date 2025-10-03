# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Timeline Session class
   This module contains the base methods for Measure Window
"""
from ..base_models.base_model import BaseModel


class BaseTimelineSessionModel(BaseModel):
    """Base Timeline Session model class for Timeline Session Window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # svcovqa04@nvidia.com (Factory Explorer) [Owner][Presenter][Current user]

    _session_users_list = "Timeline Session//Frame/**/ScrollingFrame[0]/**/Label[*]"
    _presenter_request_list = "Timeline Session//Frame/**/ScrollingFrame[1]/**/Label[*]"

    # Button locators
    _set_presenter_btn = "Timeline Session//Frame/**/Button[0].text=='Set as Timeline Presenter'"
    _revoke_request_btn = "Timeline Session//Frame/**/Button[0].text=='Revoke Request'"
    _request_presenter_btn = "Timeline Session//Frame/**/Button[0].text=='Request Timeline Control'"

    def get_user_from_session_users(self, username: str):
        """Returns Session user label

        Args:
        username(str): Name of the user
        """
        users = self.omni_driver.find_elements(self._session_users_list)
        for user in users:
            if username in user.get_text():
                return user
        raise ValueError(f"Can't find user with username {username} in session")

    def get_user_from_request_list(self, username: str):
        """Returns user label from requests

        Args:
        username(str): Name of the user
        """
        users = self.omni_driver.find_elements(self._presenter_request_list)
        for user in users:
            if username in user.get_text():
                return user
        raise ValueError(f"Can't find request of user {username}")

    def set_user_as_presenter(self, username: str):
        """Set given user as Timeline Presenter

        Args:
        username(str): Name of the user
        """
        user_tile = self.get_user_from_session_users(username)
        user_tile.click()
        self.find_and_click(self._set_presenter_btn)

    def approve_presenter_request(self, username: str):
        """Approve request for Timeline Presenter

        Args:
        username(str): Name of the user
        """
        user_tile = self.get_user_from_request_list(username)
        user_tile.click()
        self.find_and_click(self._set_presenter_btn)
        self.omni_driver.wait(1)

    def request_for_presenter(self):
        """Request for Timeline Presenter"""
        self.find_and_click(self._request_presenter_btn)
        self.omni_driver.wait(1)

    def revoke_request_for_presenter(self):
        """Revoke the request for presenter"""
        self.find_and_click(self._revoke_request_btn)
        self.omni_driver.wait(1)

    def is_user_owner(self, user_detail: str):
        """Returns whether user has owner tag attached to it

        Args:
        user_detail(str): User Detail string
        """
        return "[Owner]" in user_detail

    def is_user_presenter(self, user_detail: str):
        """Returns whether user has presenter tag attached to it

        Args:
        user_detail(str): User Detail string
        """
        return "[Presenter]" in user_detail

    def has_current_user_tag(self, user_detail: str):
        """Returns whether user has current user tag attached to it

        Args:
        user_detail(str): User Detail string
        """
        return "[Current user]" in user_detail

    def get_app_of_user(self, user_detail: str):
        """Returns app name of connected user

        Args:
        user_detail(str): User Detail string
        """
        return user_detail[user_detail.find("(") + 1 : user_detail.find(")")]
