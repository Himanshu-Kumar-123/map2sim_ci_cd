# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Message dialog class
"""

from ..base_models.base_model import BaseModel


class BaseMessageDialogModel(BaseModel):
    """Base model class for Message Dialog window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    _confirm_change_tab_btn = (
        "Message Dialog//Frame/VStack[0]/HStack[0]/Button[0].text=='Yes'"
    )

    def confirm_change_tab(self):
        """Find, confirm and select option after change of tab"""
        try:
            self.wait.element_to_be_located(
                self.omni_driver, self._confirm_change_tab_btn
            )
            self.find_and_click(self._confirm_change_tab_btn)
        except:
            print("Confirmation tab not available!")
