init -1500 python:
    import math

    class Point2D(object):
        """Stores x and y coordinates.

        Args:
            x (int): x-axis coordinate
            y (int): y-axis coordinate

        """
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __str__(self):
            return "x:{}, y:{}".format(self.x, self.y)

        def __add__(self, other):
            return Point2D(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
            return Point2D(self.x - other.x, self.y - other.y)

        def rotate(self, angle):
            """
            Rotates the point around the x and y axis by 
            the given angle in degrees.

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


    class BaseRadarChart(object):
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
        def __init__(self, size, values=None, max_value=0, labels=None,
                lines={}, break_limit=True):

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
            """
            For every spider-web, create an outline path that's a 
            fraction of the total size of the chart.

            Returns:
                list: List of paths for the inner web lines

            Raises:
                ValueError: If webs contain anything but integers 1-9, 
                    or if it has any more than once.
            """
            webs = self.lines["webs"]

            for item in webs:
                if item < 1:
                    raise ValueError("Lowest position possible is 1.")
                if item > 9:
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

        def __validate_values(self):
            """
            Checks self._values for any value being above self.max_value,
            and replaces it with self.max_value

            Returns:
                list
            """
            for index, value in enumerate(self._values):
                if value > self.max_value:
                    self._values[index] = self.max_value
            return self._values

        @property
        def values(self):
            return self._values

        @values.setter
        def values(self, val):
            """Whenever new values are set, regenerate the chart data.
            """
            self._values = val
            if not self.break_limit:
                self._values = self.__validate_values()
            self.number_of_points = len(self._values)
            self._generate_chart_data()    

        def __get_chart_endpoints(self, radius):
            """
            Take a circle and slice it based on the number of data points.
            Each slice is turned into a Point2D.

            Args:
                radius (int): Circle's radius

            Returns:
                list: Every Point2D created.
            """
            slice = (2 * math.pi) / self.number_of_points

            rv = []
            for i in range(self.number_of_points):
                angle = slice * i
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
            """
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
            """Perform all the steps necessary to create the chart data.
            """
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


    class _RadarChartPolygon(renpy.Displayable):
        """Displayable to draw a polygon for the RadarChart.

        Args:
            radar_chart(displayable): The RadarChart using this displayable.
            border(displayable): The border associated with this displayable.
        """
        def __init__(self, radar_chart, colour, border=None, **kwargs):
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


    class _RadarChartData(_RadarChartPolygon):
        """Draws the polygon that represents the chart data.
        """
        @property
        def points(self):
            """Rebuild the points list.
            """
            return [
                (point['a'].x, point['a'].y) for point in self.radar_chart.data_polygon
            ]


    class AALineDisplayable(renpy.Displayable):
        """Displayable to draw an aaline.
        """
        def __init__(self, radar_chart, colour, lines, **kwargs):
            super(AALineDisplayable, self).__init__(**kwargs)

            self.radar_chart = radar_chart
            self.size = radar_chart.size
            self.colour = colour
            self._lines = lines

        @property
        def lines(self):
            return self._lines

        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)

            shape = render.canvas()
            for line in self.lines:
                shape.aaline(
                    self.colour,
                    (line['a'].x, line['a'].y),
                    (line['b'].x, line['b'].y)
                )

            return render

        def per_interact(self):
            renpy.redraw(self, 0)


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

            self.chart_base = _RadarChartPolygon(self, self.background_colour, border=chart_line)

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
