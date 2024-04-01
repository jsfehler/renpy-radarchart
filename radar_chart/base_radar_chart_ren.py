from .point_2d_ren import Point2D

"""renpy
init -999 python:
"""
import math  # NOQA E402
from typing import Union  # NOQA E402


class BaseRadarChart:
    """Contains all the logical calculations for a RadarChart.

    This doesn't handle the actual drawing,
    just calculations for where to draw.

    Args:
        size (int): Width & height of the chart
        values (list[int]): All the values to chart on the plot
        max_value (int): The largest number a value should have
        labels(list[displayable]): All the labels for each value
        lines(dict): Properties for which lines to draw:
            {
                "chart":True,
                "data":True
                "spokes":True,
                "webs":[int], # 1-9 allowed. represents 10%, 20%, etc
            }
        break_limit(bool): If any value can exceed max_value or not

    Raises:
        ValueError: If labels is an empty list.
    """
    def __init__(
        self,
        size: int,
        values: list[int],
        max_value: int = 0,
        labels: Union[list, None] = None,
        lines: Union[dict[str, Union[bool, list[int]]], None] = None,
        break_limit: bool = True,
    ):

        super(BaseRadarChart, self).__init__()

        self.size = size
        self._values = values
        self.max_value = max_value

        self.labels = labels
        if labels is not None:
            if len(labels) <= 0:
                raise ValueError("Empty Label List provided.")

        self.break_limit = break_limit

        if not break_limit:
            self._values = self.__validate_values()

        # Point2D: Represents the center point of the chart.
        self.origin = size * 0.5
        self.origin_point = Point2D(self.origin, self.origin)

        self.number_of_points = len(values)

        # Dict: Default choices for drawing lines.
        lines_defaults = {
            "chart": True,
            "data": True,
            "spokes": True,
            "webs": [],
        }

        # Update defaults with args.
        if lines:
            lines_defaults.update(lines)
        self.lines = lines_defaults

        # Path for the chart's background outline and polygon.
        self._endpoints = self.__get_chart_endpoints(self.origin)
        self.max_coordinates = self.__physical_coordinates(self._endpoints)
        self.chart_polygon = self._build_path(self.max_coordinates)

        # Path for the spokes going from the origin to each max_coordinate.
        self.spokes = self._build_spokes()

        # Only build path for the spider-web if required.
        if self.lines.get("webs"):
            self.web_points = self.__build_web_points()

        # Generate the chart data from the values.
        self._generate_chart_data()

    def __build_web_points(self):
        """Create an inner outline paths at each 10th of the chart.

        Returns:
            list: List of paths for the inner web lines

        Raises:
            ValueError: If webs contain anything but integers 1-9,
                or if it has any more than once.
        """
        webs = self.lines["webs"]

        min_allowed = 1
        max_allowed = 9

        for item in webs:
            if item < min_allowed:
                raise ValueError("Lowest position possible is 1.")
            if item > max_allowed:
                raise ValueError("Can't use webs past the 9th position.")

        if len(webs) != len(set(webs)):
            raise ValueError("Can't use duplicate webs.")

        rv = []
        for item in webs:
            radius = self.origin * (float(item) * 0.1)
            endpoints = self.__get_chart_endpoints(radius)
            phys_endpoints = self.__physical_coordinates(endpoints)
            line = self._build_path(phys_endpoints)
            rv.append(line)

        return rv

    def __validate_values(self) -> list[int]:
        """Check self._values for any value being above self.max_value.

        Replace values above self.max_value with self.max_value

        Returns:
            list
        """
        for index, value in enumerate(self._values):
            if value > self.max_value:
                self._values[index] = self.max_value
        return self._values

    @property
    def values(self):
        """All the values to chart on the plot."""
        return self._values

    @values.setter
    def values(self, val: int):
        """Whenever new values are set, regenerate the chart data."""
        self._values = val
        if not self.break_limit:
            self._values = self.__validate_values()
        self.number_of_points = len(self._values)
        self._generate_chart_data()

    def __get_chart_endpoints(self, radius: int) -> list:
        """Take a circle and slice it based on the number of data points.

        Each slice is turned into a Point2D.

        Args:
            radius (int): Circle's radius

        Returns:
            list: Every Point2D created.
        """
        chart_slice = (2 * math.pi) / self.number_of_points

        rv = []
        for i in range(self.number_of_points):
            angle = chart_slice * i
            nx = round(radius * math.sin(angle))
            ny = round(radius * math.cos(angle))
            p2d = Point2D(nx, ny)

            # Correction for upside down chart display.
            p2d = p2d.rotate(180)

            rv.append(p2d)

        return rv

    def _values_to_percentage(self):
        """Convert values from integer to percentage.

        Builds new list from self.values, turning them into percentages
        based on the max_value.

        Returns:
            list: Percentage versions of the values.
        """
        max_value = float(self.max_value)

        return [(float(value) / max_value) for value in self._values]

    def __physical_coordinates(self, coords):
        """Get physical coordinates.

        Returns:
            list: Point2D coordinates relative to the origin point.
        """
        return [coord + self.origin_point for coord in coords]

    def _build_spokes(self):
        """Builds the path for the spokes inside the chart.

        A list of dict are created, one dict for each spoke's
        start and end positions:
        eg:
            {
                "a": Point2D(x, y)
                "b": Point2D(x1, y1)
            }

        Returns:
            list[dict]: Path for the spokes.
        """
        return [
            {"a":self.origin_point, "b":item} for item in self.max_coordinates
        ]

    def _build_path(self, points):
        """Creates the logical path for a set of points.

        A list of dict are created, containing the
        (x,y) and (x1, y1) Point2D for each line.

        Returns:
            list[dict]: Path for a polygon.
        """
        # Create 2nd list for (x1, y1).
        points_b = points[1:]
        points_b += [points[0]]

        return [
            {"a": a, "b": b} for a, b in zip(points, points_b)
        ]

    def _generate_chart_data(self):
        """Perform all the steps necessary to create the chart data."""
        # Convert values to percentage.
        c_values = self._values_to_percentage()

        # Data physical location.
        # endpoint * value percentage + origin = data location.
        o = self.origin
        values_length = [
            Point2D(a.x * b + o, a.y * b + o) for a, b in zip(self._endpoints, c_values)
        ]

        # Path for the data plotted.
        self.data_polygon = self._build_path(values_length)

        # Path for the origin.
        # Used to create animation effect.
        self.start_points = [
            {"a": self.origin_point} for point in self.data_polygon
        ]
