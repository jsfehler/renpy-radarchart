"""renpy
init -999 python:
"""
from typing import Union


class PolygonDisplayable(renpy.Displayable):
    """Displayable to draw a polygon for the RadarChart.

    Args:
        radar_chart(displayable): The RadarChart using this displayable.
        border(displayable): The border associated with this displayable.
    """
    def __init__(
        self,
        radar_chart,
        colour: tuple[int, int, int, int],
        border=None,
        points: Union[list[tuple[int, int]], None] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.radar_chart = radar_chart

        self.size = radar_chart.size
        self.colour = colour

        self.border = border

        self._points = points

    @property
    def points(self):
        """Coordinates for the polygon."""
        rv = self._points
        return rv

    def render(self, width, height, st, at):  # NOQA: D102
        render = renpy.Render(self.size, self.size)

        shape = render.canvas()
        shape.polygon(self.colour, self.points)

        if self.border is not None:
            render.place(self.border, x=0, y=0)

        return render

    def per_interact(self):  # NOQA: D102
        renpy.redraw(self, 0)

    def visit(self):  # NOQA: D102
        return [self.border]
