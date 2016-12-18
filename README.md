![Screenshot](/screenshot0001.png?raw=true "Screenshot")

# Radar Chart for Ren'Py
Ren'Py Displayable for plotting data onto a radar chart

- radarchart.rpy: Contains the RadarChart classes. Drop this file into a Ren'Py project directory.
- script.rpy: Usage examples.
- example_screens.rpy: Example screens for the examples.

### Running the Demo
Just drop script.rpy, example_screens.rpy, and radarchart.rpy into a new Ren'Py project's 'game' directory and try it out.

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

The number of items in the tuple will automatically determine how many points the RadarChart has.

Next, create a RadarChart instance:

    rc = RadarChart(
        size=200,
        values=plot_values,
        max_value=255,
        labels=[Text("Coolness"), Text("Beauty"), Text("Cuteness"), Text("Intelligence"), Text("Strength")],
        lines={"webs": [2, 4, 6, 8]},
        data_colour=(100, 200, 100, 125),
        line_colour=(153, 153, 153, 255),
        background_colour=(255, 255, 255, 255)
    )

The RadarChart should be created inside a python block, inside a label.

##### Updating a Radar Chart
To update or change the values in a RadarChart object, simply assign RadarChart.values a new tuple. 

For example, if COOL_VALUE has increased:

    COOL_VALUE = 210
    rc.values = (COOL_VALUE, BEAUTY_VALUE, CUTE_VALUE, SMART_VALUE, TOUGH_VALUE)

###Documentation
- class RadarChart
    - Arguments:
        - size (int): Width & height of the chart
        - values (list[int]): All the values to chart on the plot
        - max_value (int): The largest number a value should have
        - labels(list[displayable]): All the labels for each value
        - lines(dict): Properties for which lines to draw:
            {
                "chart":True,
                "data":True                
                "spokes":True, 
                "webs":[int], # 1-9 allowed. represents 10%, 20%, etc
            }
        - break_limit(bool): If any value can exceed max_value or not
        - data_colour: RGBA tuple or HEX string
        - line_colour: RGBA tuple or HEX string
        - background_colour: RGBA tuple or HEX string
        - point (displayable): Displayable at each value's tip
        - visible (dict): Properties for which pieces of the RadarChart
            should be visible:
            {
                "base": True, 
                "data": True,
                "lines": True, 
                "points": True, 
                "labels": True
            }    

    - Attributes:
        - chart_base: Displayable for the chart's base
        - chart_data: Displayable for the chart's data
        - chart_lines: Displayable for the chart's spokes and webs
        - chart_points: Displayable for the chart's points
        - chart_labels: Displayable for the chart's labels
    
    - chart_labels.l_padding (int): Padding between the labels and chart for left-aligned labels
    - chart_labels.r_padding (int): Padding between the labels and chart for right-aligned labels
    - chart_labels.c_padding (int): Padding between the labels and chart for center-aligned labels
    
###License & Usage
The pretty icons used in the examples are from https://icons8.com/

All the code is under the MIT license, just like Ren'Py. Do whatever you want with it.

If you use this in a game, I'd appreciate getting credit for it, or at least a link back to this repo somewhere.

If you need any sort of new feature and/or enhancement, create a new issue on Github and I'll see what I can do.