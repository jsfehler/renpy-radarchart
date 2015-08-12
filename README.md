![Screenshot](/screenshot0001.png?raw=true "Screenshot")

# Radar Chart for Ren'Py
Ren'Py Displayable for plotting data onto a radar chart

- radarchart.rpy: Contains the RadarChart class. Drop this file into a Ren'Py project directory
- script.rpy: Example usage situation.

### Demo
Just drop script.rpy and radarchart.rpy into a new Ren'Py project's 'game' directory and try it out.

### Getting Started
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

The data should be created inside a label.

A chart's data should then be gathered in a tuple:

    plot_values = (COOL_VALUE, BEAUTY_VALUE, CUTE_VALUE, SMART_VALUE, TOUGH_VALUE)

The number of items in the tuple will determine how many points the RadarChart has.

Next, you'll need a RadarChart instance:

    rc = RadarChart(size=200,  
                    values=plot_values, 
                    max_value=255, 
                    data_colour=(100, 200, 100, 125), 
                    line_colour=(153, 153, 153, 255), 
                    background_colour=(255, 255, 255, 255), 
                    show_lines=True, 
                    animated=True,
                    speed=1)

The RadarChart should be created inside a python block, inside a label.

##### Updating a Radar Chart

To update or change the values in a RadarChart object, simply assign RadarChart.values a new tuple. 

For example, if COOL_VALUE has increased:

    COOL_VALUE = 210
    rc.values = (COOL_VALUE, BEAUTY_VALUE, CUTE_VALUE, SMART_VALUE, TOUGH_VALUE)

If the chart needs a new point:

    SEXY_VALUE = 66
    rc.values = (COOL_VALUE, BEAUTY_VALUE, CUTE_VALUE, SMART_VALUE, TOUGH_VALUE, SEXY_VALUE) 

##### Resetting chart animations

After a chart's animations have played, they won't replay until the data has changed. If you want the animation to play whenever the screen is opened, an Action called ResetChartAnimation can be attached to a button. As arguments, it takes whichever charts need their animations reset. Using this action causes the charts to replay the next time the screen is displayed. 

This Action can be attached to a "Close" button, for example:

    textbutton "Close Menu" action [ResetChartAnimation(rc, rc2, rc3), Return()] xalign .99 yalign .99

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
    - speed: int - The rate at which an animated chart's values should expand out
    
- class ResetChartAnimation(*args)

    - *args: RadarChart instances
    
###License & Usage
Everything here is under the MIT license, just like Ren'Py. Do whatever you want with it.

If you use this in a commercial game, I'd appreciate getting credit for it.

If you need any sort of new feature and/or enhancement, create a new issue and I'll see what I can do.