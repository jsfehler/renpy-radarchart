"""renpy
init -999 python:
"""
class AALineDisplayable(renpy.Displayable):
    """Displayable to draw an aaline."""
    def __init__(
        self,
        radar_chart,
        colour: tuple[int, int, int, int],
        lines,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.radar_chart = radar_chart
        self.size = radar_chart.size
        self.colour = colour
        self._lines = lines

    @property
    def lines(self):
        """Coordinates for the lines."""
        return self._lines

    def render(self, width, height, st, at):  # NOQA: D102
        render = renpy.Render(self.size, self.size)

        shape = render.canvas()
        for line in self.lines:
            shape.aaline(
                self.colour,
                (line['a'].x, line['a'].y),
                (line['b'].x, line['b'].y),
            )

        return render

    def per_interact(self):  # NOQA: D102
        renpy.redraw(self, 0)
