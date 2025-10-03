from enum import Enum


class IrayRenderSettings(Enum):

    """Canvas Settings under Iray Render Settings"""

    beauty = 0
    diffuse = 1
    specular = 2
    glossy = 3
    emission = 4
    custom_LPE = 5
    alpha = 6
    illuminance = 7
    ray_length = 8
    depth = 9
    normal = 10
    uvw_0 = 11
    uvw_1 = 12
    material_id = 13


class ViewportMode(Enum):
    """Enum class for viewport modes in Factory Explorer

    Args:
        Enum (Enum): Enum object
    """

    PRESENT = "present"
    COMMENT = "comment"
    MODIFY = "modify"
    APPROVE = "approve"
    REVIEW = "review"
    LAYOUT = "layout"


class SectionOption(Enum):
    """Enum class for viewport modes in Factory Explorer

    Args:
        Enum (Enum): Enum object
    """

    CLONE = "Clone Section"
    RENAME = "Rename Section"
    REMOVE = "Remove Section"


class CursorType(Enum):
    """Enum class for cursor type
    
    Args:
        Enum (Enum): Enum object
    """
    ARROW = "ARROW"
    TEXT_INPUT = "TEXT_INPUT"
    RESIZE_VERTICAL = "RESIZE_NS"
    RESIZE_HORIZONTAL = "RESIZE_EW"