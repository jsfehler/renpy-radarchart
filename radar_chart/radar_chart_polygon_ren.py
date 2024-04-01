"""renpy
init -999 python:
"""


class _RadarChartPolygon(renpy.Displayable):
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
        **kwargs,
    ):
        super(_RadarChartPolygon, self).__init__(**kwargs)

        self.radar_chart = radar_chart

        self.size = radar_chart.size
        self.colour = colour

        self.border = border

        # Collect coordinates for a polygon into a list.
        self._points = [
            (point['a'].x, point['a'].y) for point in radar_chart.chart_polygon
        ]

    @property
    def points(self):
        rv = self._points
        return rv

    def render(self, width, height, st, at):
        render = renpy.Render(self.size, self.size)

        shape = render.canvas()
        shape.polygon(self.colour, self.points)

        if self.border is not None:
            render.place(self.border, x=0, y=0)

        return render

    def per_interact(self):
        renpy.redraw(self, 0)

    def visit(self):
        return [self.border]
