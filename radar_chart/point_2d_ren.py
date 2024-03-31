"""renpy
init -999 python:
"""
import math

class Point2D:
    """Stores x and y coordinates.

    Args:
        x (int): x-axis coordinate
        y (int): y-axis coordinate

    """
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def rotate(self, angle: int):
        """Rotate around the x and y axis by the given angle in degrees.

        Args:
            angle (int): Degrees to rotate the point

        Returns:
            Point2D
        """
        rad = angle * math.pi / 180
        cos_angle = math.cos(rad)
        sin_angle = math.sin(rad)

        x = self.y * sin_angle + self.x * cos_angle
        y = self.y * cos_angle - self.x * sin_angle

        return Point2D(x, y)
