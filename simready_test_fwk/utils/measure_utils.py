"""
Module: measure_utils.py

This module provides utility functions and classes for working with 3D measurements.
"""

from dataclasses import dataclass

@dataclass
class Cube:
    """
    A dataclass representing a 3D cube with x, y, and z dimensions.

    Attributes:
        x (float): The length of the cube along the x-axis.
        y (float): The length of the cube along the y-axis.
        z (float): The length of the cube along the z-axis.
    """
    x: float = None
    y: float = None
    z: float = None

@dataclass
class MeasureData:
    """
    A dataclass representing various types of measurements that can be made on a 3D object.

    Attributes:
        default (str): The default measurement type.
        surface (str): The measurement type for surface area.
        edge (str): The measurement type for edge length.
        midpoint (str): The measurement type for midpoint.
        pivot (str): The measurement type for pivot point.
        center (str): The measurement type for center point.
        perpendicular (str): The measurement type for perpendicular distance.
    """
    default: str = None
    surface: str = None
    edge: str = None
    midpoint: str = None
    pivot: str = None
    center: str = None
    perpendicular: str = None
    min: str = None
    max: str = None
    center: str = None

@dataclass
class MeasureConfig:
    """
    A dataclass representing a test data for measurement

    Attributes:
        cube (Cube): The cube object being tested.
        cube_01 (Cube): The first reference cube object.
        cube_02 (Cube): The second reference cube object.
        measure (Measure): The measurement type being used for the test.
    """
    measure: MeasureData
    cube: Cube = None
    cube_01: Cube = None
    cube_02: Cube = None
