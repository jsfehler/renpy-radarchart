init -998 python:
    import math


    class _RadarChartData(PolygonDisplayable):
        """Draws the polygon that represents the chart data."""
        @property
        def points(self):
            """Rebuild the points list.
            """
            return [
                (point['a'].x, point['a'].y) for point in self.radar_chart.data_polygon
            ]


    class _RadarChartDataBorder(AALineDisplayable):
        @property
        def lines(self):
            return self.radar_chart.data_polygon


    class _RadarChartLines(renpy.Displayable):
        """Collection of AALineDisplayable.

        All the lines that can be drawn inside a chart.
        """
        def __init__(self, children, **kwargs):
            super(_RadarChartLines, self).__init__(**kwargs)

            self.children = children
            self.size = children[0].size

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)

            for child in self.children:
                render.place(child, x=0, y=0)

            return render

        def visit(self):
            return self.children


    class _RadarChartLabels(renpy.Displayable):
        """Collection of labels for each data point.

        For every data point,
        take any displayable and place it as a label for the data.

        Args:
            radar_chart(displayable): The RadarChart using this displayable.

        Attributes:
            l_padding (int): Padding between the labels and chart for left-aligned labels
            r_padding (int): Padding between the labels and chart for right-aligned labels
            c_padding (int): Padding between the labels and chart for center-aligned labels

        Raises:
            ValueError: If the number of labels and data points are not the same.
        """
        def __init__(self, radar_chart, **kwargs):
            super(_RadarChartLabels, self).__init__(**kwargs)

            self.radar_chart = radar_chart
            self.size = radar_chart.size
            self.labels = radar_chart.labels

            self.l_padding = 20
            self.r_padding = 20
            self.c_padding = 20

            if len(self.radar_chart.chart_polygon) != len(self.labels):
                raise ValueError("Amount of labels given does not match amount of data points.")

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)

            origin = round(self.radar_chart.origin)

            for x, item in enumerate(self.labels):
                chart = self.radar_chart.chart_polygon[x]

                # Only Text Displayables have a size attribute
                try:
                    w, h = item.size()

                except AttributeError:
                    child_render = renpy.render(item, width, height, st, at)
                    w, h = child_render.get_size()

                xa = round(chart["a"].x)
                ya = round(chart["a"].y)

                x_center = xa - (w * 0.5)
                y_center = ya - (h * 0.5)

                # Left.
                if xa < origin:
                    px = xa - w - self.l_padding
                    py = y_center

                # Center Top.
                elif xa == origin and ya == 0:
                    px = x_center
                    py = ya - h - self.c_padding

                # Center Bottom.
                elif xa == origin and ya == round(self.size):
                    px = x_center
                    py = ya + self.c_padding

                # Right.
                else:
                    px = xa + self.r_padding
                    py = y_center

                render.place(item, x=px, y=py)

            return render

        def visit(self):
            return self.labels


    class _RadarChartPoints(renpy.Displayable):
        """Handles display for all point displayables in a RadarChart.

        Args:
            radar_chart(displayable): The RadarChart using this displayable.
        """
        def __init__(self, radar_chart, **kwargs):
            super(_RadarChartPoints, self).__init__(**kwargs)

            self.radar_chart = radar_chart
            self.size = radar_chart.size

            # Displayable at each point.
            self.points = []
            for item in radar_chart.data_polygon:
                self.points.append(radar_chart.point)

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)

            # Get width and height of point.
            child_render = renpy.render(self.points[0], width, height, st, at)
            w, h = child_render.get_size()

            data = self.radar_chart.data_polygon
            for n in range(len(self.points)):
                render.place(self.points[n], x=data[n]["a"].x - w / 2, y=data[n]["a"].y - h / 2)

            return render

        def visit(self):
            return self.points


    class RadarChart(BaseRadarChart, renpy.Displayable):
        """
        Displayable that uses BaseRadarChart for the path calculations.
        Collects all the displayables that make up the pieces of the RadarChart.

        Args:
            data_colour: RGBA tuple or HEX string
            line_colour: RGBA tuple or HEX string
            background_colour: RGBA tuple or HEX string
            point (displayable): Displayable at each value's tip
            visible (dict): Properties for which pieces of the RadarChart
                should be visible:
                {
                    "base": True,
                    "data": True,
                    "lines": True,
                    "points": True,
                    "labels": True
                }
        """
        def __init__(self,
            data_colour=(100, 200, 100, 125),
            line_colour=(153, 153, 153, 255),
            background_colour=(255, 255, 255, 255),
            point=None, visible = {}, **kwargs):

            super(RadarChart, self).__init__(**kwargs)

            # Colours.
            self.data_colour = color(data_colour)
            self.line_colour = color(line_colour)
            self.background_colour = color(background_colour)

            visible_defaults = {
                "base": True,
                "data": True,
                "lines": True,
                "points": True,
                "labels": True
            }

            visible_defaults.update(visible)
            self.visible = visible_defaults

            # Displayable for the points.
            self.point = point

            # Group of point displayables, one for each point on the chart.
            if point is not None:
                self.chart_points = _RadarChartPoints(self)
            else:
                self.chart_points = None

            # Lines
            chart_lines = []
            chart_line = None

            if self.lines["chart"]:
                chart_line = AALineDisplayable(self, line_colour, self.chart_polygon)

            _points = [
                (point['a'].x, point['a'].y) for point in self.chart_polygon
            ]

            self.chart_base = PolygonDisplayable(
                self,
                self.background_colour,
                border=chart_line,
                points=_points,
            )

            if self.lines["spokes"]:
                line = AALineDisplayable(self, line_colour, self.spokes)
                chart_lines.append(line)

            self.data_line = None
            if self.lines["data"]:
                self.data_line = _RadarChartDataBorder(self, line_colour, self.data_polygon)

            if self.lines["webs"]:
                for item in self.web_points:
                    line = AALineDisplayable(self, line_colour, item)
                    chart_lines.append(line)

            self.chart_lines = None
            if len(chart_lines) > 0:
                self.chart_lines = _RadarChartLines(chart_lines)

            self.chart_labels = None
            if self.labels:
                self.chart_labels = _RadarChartLabels(self)

        @property
        def chart_data(self):
            """Chart Data must be rebuilt every time it's called.
            """
            return _RadarChartData(self, self.data_colour, border=self.data_line)

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)

            if self.visible["base"]:
                render.place(self.chart_base, x=0, y=0)

            if self.visible["data"]:
                render.place(self.chart_data, x=0, y=0)

            if self.chart_lines is not None and self.visible["lines"]:
                render.place(self.chart_lines, x=0, y=0)

            if self.point is not None and self.visible["points"]:
                render.place(self.chart_points, x=0, y=0)

            if self.labels is not None and self.visible["labels"]:
                render.place(self.chart_labels, x=0, y=0)

            return render

        def per_interact(self):
            renpy.redraw(self, 0)

        def visit(self):
            return [
                self.chart_base,
                self.chart_data,
                self.chart_lines,
                self.chart_points,
                self.chart_labels
            ]
