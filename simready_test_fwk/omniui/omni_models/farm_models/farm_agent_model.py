# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Farm Agent UI Model class
   This module contains the base methods for Farm Agent UI modal window
"""
from omniui.omni_models.base_models.base_model import BaseModel
from omni_remote_ui_automator.common.constants import KeyboardConstants

class FarmAgentModel(BaseModel):
    """Base model class for Farm Agent UI modal

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for about modal

    _queue_address = "Omniverse Agent//Frame/**/StringField[*].name=='address'"
    _connect_btn = "Omniverse Agent//Frame/**/Button[*].text=='Connect'"
    _test_connection_btn = "Omniverse Agent//Frame/**/Button[*].text=='Test connection'"
    _configure_jobs_btn = "Omniverse Agent//Frame/**/Button[*].text=='Configure or edit job definitions   '"
    _disconnected_status = "Omniverse Agent//Frame/**/Label[*].text=='Disconnected"
    _connected_status = "Omniverse Agent//Frame/**/Label[*].text=='Connected"
    _idle_status = "Omniverse Agent//Frame/**/Label[*].text=='Idle'"
    _quit_confirmation_btn = "__exclamation_glyph__ Quit Omniverse Agent?//Frame/**/Button[*].name=='confirm_button'"
    _quit_canel_btn = "__exclamation_glyph__ Quit Omniverse Agent?//Frame/**/Button[*].name=='cancel_button'"

    def connect_to_queue(self, address="http://localhost:8222"):
        """ Connects to Queue """
        self.log.info(f"Connect Agent to Queue at {address}")
        address_bar = self.omni_driver.find_element(self._queue_address, refresh=True)
        address_bar.double_click()
        address_bar.send_keys(address)
        connect_btn = self.omni_driver.find_element(self._connect_btn)
        connect_btn.click()
        self.omni_driver.wait(5)
        
    def wait_for_idle_status(self):
        """ """
        self.wait.element_to_be_located(self.omni_driver, self._idle_status)

    def quit_agent(self, confirm = True):
        """  """
        self.omni_driver.select_menu_option("File/Exit")
        try:
            if confirm:
                self.omni_driver.emulate_key_press(KeyboardConstants.enter)
            else:
                self.omni_driver.emulate_key_press(KeyboardConstants.escape)
            connection_maintained = True
        except:
            self.log.info("Application forcibly quit")
            connection_maintained = False
        return connection_maintained