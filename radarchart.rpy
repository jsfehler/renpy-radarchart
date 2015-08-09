# Copyright (c) 2015 Joshua Fehler <jsfehler@gmail.com>

#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation files
#(the "Software"), to deal in the Software without restriction,
#including without limitation the rights to use, copy, modify, merge,
#publish, distribute, sublicense, and/or sell copies of the Software,
#and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:

#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init -1500 python:
    import copy
    import math

    
    class Point2D(object):
        """
        Every point in a RadarChart is stored as a Point2D object.
        """
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __add__(self, other):
            return Point2D(self.x + other.x, self.y + other.y) 
        
        def __sub__(self, other):
            return Point2D(self.x - other.x, self.y - other.y) 
        
        def magnitude(self):
            u = self.x * self.x
            v = self.y * self.y
            return math.sqrt(u + v)
 
        def normalize(self, factor):
            vmag = self.magnitude()
            return Point2D((self.x / vmag) * factor, (self.y / vmag) * factor)
  
        def rotate(self, angle):
            """Rotates the point around the X and Y axis by the given angle in degrees."""         
            rad = angle * math.pi / 180
            cos_angle = math.cos(rad)
            sin_angle = math.sin(rad)
            
            x = self.y * sin_angle + self.x * cos_angle
            y = self.y * cos_angle - self.x * sin_angle
            return Point2D(x, y)


    class RadarChart(renpy.Displayable):        
        def __init__(self, 
                     size=0,  
                     values=None,
                     max_value=0,
                     data_colour=(100, 200, 100, 125), 
                     line_colour=(153, 153, 153, 255), 
                     background_colour=(255, 255, 255, 255), 
                     show_lines=False, 
                     animated=True,
                     speed=1):
            super(renpy.Displayable, self).__init__()
            
            # Width and Height of the RadarChart must be equal.
            self.size = size
            
            # Origin point is the dead center of the chart.
            origin = size * 0.5, size * 0.5
            
            # Number of points in the chart is determined by the number of values.
            self.number_of_points = len(values)  
   
            # Set colour of the chart's data polygon
            try:
                self.data_colour = color(data_color)
            except:
                self.data_colour = data_colour

            self.show_lines = show_lines
                
            # Set colour for the chart's lines
            try:
                self.line_colour = color(line_colour)
            except:
                self.line_colour = line_colour
 
            # Set colour for the chart's background
            try:
                self.background_colour = color(background_colour)
            except:
                self.background_colour = background_colour
 
            # Is the chart animated?
            self.animated = animated
            self.speed = speed
      
            # Convert values into percentage
            c_values = []
            max_value = max_value
            for value in values:
                c_values.append(float(value)/float(max_value))
   
            # Calculate endpoints
            endpoints = self.get_chart_endpoints()

            # Endpoints with offset for the origin point. The physical length of each line in the chart
            max_coordinates = [Point2D(t.x + origin[0], t.y + origin[1]) for t in endpoints]

            # Centre point of the chart
            origin_point = Point2D(origin[0], origin[1])

            # Data values
            values_length = [Point2D(endpoints[x].x * c_values[x] + origin[0], endpoints[x].y * c_values[x] + origin[1]) for x in range(len(endpoints))]

            # Path for the chart's border
            self.chart = []
            for x in range(self.number_of_points-1):
                self.chart.append({"a":max_coordinates[x], "b":max_coordinates[x+1]})
            self.chart.append({"a":max_coordinates[self.number_of_points-1], "b":max_coordinates[0]})

            # Path for the chart's background polygon
            self.chart_polygon = copy.copy(self.chart)

            # Path for the reference lines inside the chart
            for item in max_coordinates:
                self.chart.append({"a":origin_point, "b":item})
                
            # Path for the data plotted
            self.data_polygon = []
            for x in range(self.number_of_points-1):
                self.data_polygon.append({"a":values_length[x], "b":values_length[x+1]})  
            self.data_polygon.append ({"a":values_length[self.number_of_points-1], "b":values_length[0]})
 
            # Path for the origin
            # Used to create animation effect
            self.start_points = [{"a": origin_point} for point in self.data_polygon]

        def get_chart_endpoints(self):
            """
            Calculate the endpoint for each piece of data on the chart.
            
            Returns:
                List containing all the endpoints
            """
            rotation_amount = 360 / self.number_of_points
            radius = self.size * 0.5
            slice = (2 * math.pi) / self.number_of_points
            
            endpoints = []
            for i in range(self.number_of_points):
                angle = slice * i
                nx = radius * math.sin(angle)
                ny = radius * math.cos(angle) 
                p2d = Point2D(nx, ny)

                # Correction for upside down chart display
                correction = float(self.number_of_points) * 0.5
                p2d = p2d.rotate(rotation_amount * correction)
                
                endpoints.append(p2d)  
            
            return endpoints
                
        def draw_lines(self, render, at, st):      
            # Draw to create the Radar Chart's grid.
            shape = render.canvas()
            for line in self.chart:
                shape.aaline(self.line_colour, (line['a'].x, line['a'].y), (line['b'].x, line['b'].y))
            
        def draw_polygon(self, render, at, st, polygon, color):
            # Collect coordinates for a polygon
            points = [(point['a'].x, point['a'].y) for point in polygon]
         
            # Draw
            shape = render.canvas()
            shape.polygon(color, points)
    
        def render(self, width, height, st, at):
            render = renpy.Render(self.size, self.size)
            
            # Draws the background
            self.draw_polygon(render, at, st, self.chart_polygon, self.background_colour) 
            
            # Draws the data   
            if not self.animated:
                self.draw_polygon(render, at, st, self.data_polygon, self.data_colour)
            
            else:
                acceleration = self.speed * st
                for x in range(len(self.start_points)):
                    # Only keep moving if we haven't reached the endpoint
                    if float(self.start_points[x]['a'].x) < float(self.data_polygon[x]['a'].x):
                        # Calculates movement of animated data
                        target_vector = []
                        for x in range (len(self.start_points)):
                            p2d = self.data_polygon[x]['a'] - self.start_points[x]['a']
                            target_vector.append(p2d)
                          
                        # Update start points to new position  
                        for x in range (len(target_vector)):
                            move_vector = target_vector[x].normalize(acceleration)
                            p2d = self.start_points[x]['a'] + move_vector
                            
                            # Replace start points with new start points
                            self.start_points[x]['a'] = p2d
                        
                self.draw_polygon(render, at, st, self.start_points, self.data_colour)  

                # Only need to redraw if chart is animated
                renpy.redraw(self, 0)
        
            # Draws the outline shape and the lines    
            if self.show_lines:
                self.draw_lines(render, at, st)
        
            return render