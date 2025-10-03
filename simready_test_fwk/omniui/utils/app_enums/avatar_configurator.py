# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Enums for Avatar Studio
   This module contains the Enums for Avatar Studio window
"""

from enum import Enum

from omniui.utils.utility_functions import get_value_from_json


class BackgroundImages(Enum):
    """Enum class for all Background Images"""

    UI_LABEL = "Background Image"
    DEFAULT_VALUE = "."
    IMAGE_1 = get_value_from_json("BackgroundImages", "avatar_configurator_data.json")[
        "IMAGE_1"
    ]


class OutFitLogo(Enum):
    """Enum class for all Outfit Logo"""

    UI_LABEL = "Outfit Logo"
    DEFAULT_VALUE = "."
    LOGO_1 = get_value_from_json("OutFitLogo", "avatar_configurator_data.json")[
        "LOGO_1"
    ]


class Buttons(Enum):
    """Enum class for all Buttons"""

    PLAY = "Play"
    PAUSE = "Pause"
    SAVE_SCREENSHOT = "Save Screenshot"
    SAVE_SCENE = "Save Scene"


class AvatarModels(Enum):
    """Enum class for all Avatar Models"""

    UI_LABEL = "Avatar Model"
    TED = "Ted"
    VIOLET = "Violet"
    EMMA = "Emma"
    BENJAMIN = "Benjamin"
    FERRET = "Ferret"
    DEFAULT_VALUE = TED


class SceneModels(Enum):
    """Enum class for all Scene Models"""

    UI_LABEL = "Scene Model"
    IMAGE_BACKGROUND = "Image Background"
    QUICK_SERVICE_RESTAURANT = "Quick Service Restaurant"
    DATA_CENTER = "Data Center"
    DESK = "Desk"
    SKYSCRAPER = "Skyscraper"
    STORE = "Store"
    DEFAULT_VALUE = IMAGE_BACKGROUND


class SceneMoods(Enum):
    """Enum class for all Scene Moods"""

    UI_LABEL = "Scene Mood"
    MOOD_1 = "Mood 1"
    MOOD_2 = "Mood 2"
    DEFAULT_VALUE = MOOD_1


class OutfitModels(Enum):
    """Enum class for all Outfit Model"""

    UI_LABEL = "Outfit Model"
    T_SHIRT = "T-Shirt"
    FORMAL_OUTFIT = "Formal Outfit"
    HOODIE = "Hoodie"
    COAT = "Coat"
    APRON = "Apron"
    DEFAULT_VALUE = T_SHIRT


class GlassesModels(Enum):
    """Enum class for all Glasses Model"""

    UI_LABEL = "Glasses Model"
    NO_GLASSES = "No Glasses"
    GLASSES_1 = "Glasses 1"
    GLASSES_2 = "Glasses 2"
    DEFAULT_VALUE = GLASSES_1


class HeadgearModels(Enum):
    """Enum class for all Headgear Model"""

    UI_LABEL = "Headgear Model"
    NO_HEADGEAR = "No Headgear"
    BASEBALL_CAP = "Baseball Cap"
    DRIVER_HAT = "Driver Hat"
    TOQUE = "Toque"
    HARD_HAT = "Hard Hat"
    COWBOY_HAT = "Cowboy Hat"
    ALTERNATIVE_HEARSTYLE = "Alternative Hairstyle"
    DEFAULT_VALUE = NO_HEADGEAR


class EyeColors(Enum):
    """Enum class for all Eye Color"""

    UI_LABEL = "Eye Color"
    BLUE = "Blue"
    BROWN = "Brown"
    DARK_BROWN = "Dark Brown"
    GRAY = "Gray"
    GREEN = "Green"
    DEFAULT_VALUE = GREEN


class SkinColors(Enum):
    """Enum class for all Skin Color"""

    UI_LABEL = "Skin Color"
    DARK = "Dark"
    MEDIUM = "Medium"
    LIGHT = "Light"
    DEFAULT_VALUE = MEDIUM


class ScenePrimaryColors(Enum):
    """Class for Scene Primary Color"""

    UI_LABEL = "Scene Primary Color"
    DEFAULT_VALUE = "#343636"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class SceneSecondaryColors(Enum):
    """Class for Scene Secondary Color"""

    UI_LABEL = "Scene Secondary Color"
    DEFAULT_VALUE = "#6E5B40"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class SceneTertiaryColors(Enum):
    """Class for Scene Tertiary Color"""

    UI_LABEL = "Scene Tertiary Color"
    DEFAULT_VALUE = "#698556"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class OutfitPrimaryColors(Enum):
    """Class for Outfit Primary Color"""

    UI_LABEL = "Outfit Primary Color"
    DEFAULT_VALUE = "#CCCBCC"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class OutfitSecondaryColors(Enum):
    """Class for Outfit Secondary Color"""

    UI_LABEL = "Outfit Secondary Color"
    DEFAULT_VALUE = "#323C47"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class GlassesColors(Enum):
    """Class for Glasses Color"""

    UI_LABEL = "Glasses Color"
    DEFAULT_VALUE = "#B7BEC4"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class HeadgearColors(Enum):
    """Class for Headgear Color"""

    UI_LABEL = "Headgear Color"
    DEFAULT_VALUE = "#588524"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"


class HairColors(Enum):
    """Class for Hair Color"""

    UI_LABEL = "Hair Color"
    DEFAULT_VALUE = "#332E2B"
    RED = "#FF0000"
    BLUE = "#0000FF"
    GREEN = "#00FF00"
