# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Base Textures Model class
   This module contains the base methods for Textures window
"""
import random
from ..base_models.base_model import BaseModel



class BaseTexturesModel(BaseModel):
    """Base model class for Textures window

    Args:
        BaseModel (BaseModel): BaseModel class parent to all window classes.
    """

    # Locators related to Textures window
    _window_title = "Textures"
    _textures_window = "Textures//Frame/VStack[0]"
    _all_textures = "Textures//Frame/**/ThumbnailView[0]/Frame[*]/HStack[0]"
    _textures_slider = "Textures//Frame/**/IntSlider[0]"

    
    def navigate_to_textures(self):
        """Navigates to textures window"""

        self.omni_driver.select_menu_option(f"Window/Browsers/{self._window_title}")
        self.omni_driver.wait(2)
        assert (
            "Textures" in self.omni_driver.get_windows()["visible_windows"]
        ), f"Cannot find window for '{self._window_title}'."
        self.log.info("Navigated to Textures window successfully.")
        textures_window = self.omni_driver.find_element(self._textures_window)
        textures_window.click()
        self.screenshot("navigated_to_textures")

    
    def select_texture_and_drop_to_position(self, position, normal_map: bool):
        """Applies texture to prim properties

        Args:
            position (_type_): Position to drag texture to
            normal_map (bool): If material is for normal map.
        """
        self.omni_driver.find_element(self._textures_slider).send_keys(200)

        textures = self.omni_driver.find_elements(self._all_textures)
        rand_value = random.randrange(0, len(textures))

        for _ in range(0, 100):
            texture_name = textures[rand_value].find_element("**/Label[0]").get_text()
            if normal_map:
                if "normal" in texture_name.lower():
                    texture = textures[rand_value]
                    break
            else:
                if "normal" not in texture_name.lower():
                    texture = textures[rand_value]
                    break

            rand_value = random.randrange(0, len(textures))

        self.omni_driver.find_element(self._textures_slider).send_keys(10)

        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
        self.omni_driver.wait_frames(5)

        texture.drag_and_drop(position[0], position[1])
        self.screenshot("applied_material")
        self.omni_driver.wait(2)
        self.omni_driver.wait_for_stage_load()
