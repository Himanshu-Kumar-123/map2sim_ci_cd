# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Farm Queue UI Model class
   This module contains the base methods for Farm Queue UI modal window
"""
from omniui.omni_models.base_models.base_model import BaseModel


class FarmQueueModel(BaseModel):
    """Base model class for Farm Queue UI modal

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators for about modal

    _quit_queue_btn = "Omniverse Farm Queue//Frame/**/Button[*].text=='Quit Queue'"
    _quit_confirmation_btn = "__exclamation_glyph__ Quit Omniverse Farm Queue?//Frame/**/Button[*].name=='confirm_button'"
    _quit_canel_btn = "__exclamation_glyph__ Quit Omniverse Farm Queue?//Frame/**/Button[*].name=='cancel_button'"

    def click_quit_btn(self, confirm = True):
        """  """
        quit_btn = self.wait.element_to_be_located(self.omni_driver, self._quit_queue_btn)
        quit_btn.click()
        if confirm:
            action_btn = self.wait.element_to_be_located(self.omni_driver, 
                                                         self._quit_confirmation_btn.replace(
                                                             "__exclamation_glyph__", self.get_glyph_code("exclamation.svg"))
                                                        )
        else:
            action_btn = self.wait.element_to_be_located(self.omni_driver, 
                                                         self._quit_canel_btn.replace(
                                                             "__exclamation_glyph__", self.get_glyph_code("exclamation.svg"))
                                                        )
        try:
            action_btn.click()
            connection_maintained = True
        except:
            self.log.info("Application forcibly quit")
            connection_maintained = False
        return connection_maintained
    
            