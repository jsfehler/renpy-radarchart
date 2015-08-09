![Screenshot](/screenshot0001.png?raw=true "Screenshot")

#Radar Chart for Ren'Py
Ren'Py Displayable for plotting data onto a radar chart

- radarchart.rpy: Contains the RadarChart class. Drop this file into a Ren'Py project directory
- script.rpy: Example usage situation.

###Demo
Just drop script.rpy and radarchart.rpy into a new Ren'Py project's 'game' directory and try it out.

###Getting Started
This guide assumes you have basic familiarity with Ren'Py labels and screens.

##### Necessary Files:
Place radarchart.rpy into your project's 'game' directory

##### Creating a Radar Chart:
To create a chart, first you'll need some data to plot, such as:

    COOL_VALUE = 200
    BEAUTY_VALUE = 110
    CUTE_VALUE = 90
    SMART_VALUE = 67
    TOUGH_VALUE = 100

The data can be created anytime after the start label.

Next, you'll need a RadarChart instance:

    plot_values = (COOL_VALUE, BEAUTY_VALUE, CUTE_VALUE, SMART_VALUE, TOUGH_VALUE)
    rc = RadarChart(size=200,  
                    values=plot_values, 
                    max_value=255, 
                    data_colour=(100, 200, 100, 125), 
                    line_colour=(153, 153, 153, 255), 
                    background_colour=(255, 255, 255, 255), 
                    show_lines=True, 
                    animated=True)

The RadarChart should be created inside a python block, on the screen you want to display it on.

###Documentation
- class RadarChart(size, values, max_value, data_colour, line_colour, background_colour, show_lines, animated)

    - size: int - Width and height of the chart (must be equal)
    - values: tuple - The values for each point on the cart
    - max_value: int - The maximum value any point can have
    - data_colour: tuple - (R, G, B, A) value for the data
    - line_colour: tuple - (R, G, B, A) value for the references lines
    - background_colour: tuple - (R, G, B, A) value for the chart's background
    - show_lines: bool - True for visible reference lines 
    - animated: bool - True if each point on the chart should animate from zero to the current value