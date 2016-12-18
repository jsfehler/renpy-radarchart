# Example Selection Menu
screen example_select:
    window:
        xalign 0.5
        yalign 0.0
        vbox:
            text "Example Select"
            textbutton "Lines & Borders" xfill True action Jump("example_one")
            textbutton "Labels & Points" xfill True action Jump("example_two")
            textbutton "ATL Transforms" xfill True action Jump("example_three")
            textbutton "Updating Values" xfill True action Jump("example_four")


label example_select:
    call screen example_select


label start:

    # Data Setup
    python:
        # Create some dummy data to use in the Radar Charts        
        GRAPE_VALUE = 200
        APPLE_VALUE = 110
        ORANGE_VALUE = 90
        BANANA_VALUE = 67
        LEMON_VALUE = 100
        LIME_VALUE = 82
        POTATO_VALUE = 333
        
        plot_values_2 = [
            GRAPE_VALUE,
            APPLE_VALUE,
            ORANGE_VALUE,
            BANANA_VALUE,
            LEMON_VALUE,
            LIME_VALUE,
            POTATO_VALUE
        ]

        LION_VALUE = 200
        TIGER_VALUE = 110
        BEAR_VALUE = 190
        PANDA_VALUE = 67
        HORSE_VALUE = 100
        CHEETAH_VALUE = 22
        EAGLE_VALUE = 333
        FALCON_VALUE = 111
        
        plot_values_3 = [
            LION_VALUE,
            TIGER_VALUE,
            BEAR_VALUE,
            PANDA_VALUE,
            HORSE_VALUE,
            CHEETAH_VALUE,
            EAGLE_VALUE,
            FALCON_VALUE
        ]

        # Create RadarChart objects

        # Example Screen 1 Charts: 

        # Default
        default = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(255, 238, 136, 255),
            line_colour=(136, 0, 68, 255),
            background_colour=(221, 17, 85, 255)
        )
        
        # Outline, spokes, and no data outline
        no_data_outline = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(81, 214, 85, 255),
            line_colour=(82, 43, 41, 255),
            background_colour=(160, 107, 154, 255),
            lines={"data": False},
        )
        
        # Outline, no spokes
        no_spokes = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(198, 192, 19, 255),
            line_colour=(66, 62, 55, 255),
            background_colour=(110, 103, 95, 255),
            lines={"spokes": False},
        )
       
        # No outline
        no_outline = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(108, 207, 246, 255),
            background_colour=(0, 16, 17, 255),
            lines={"chart":False, "data":False, "spokes":False},
        )
       
        # Spider-web
        spider_web_partial = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(254, 220, 151, 255),
            line_colour=(3, 63, 99, 255),
            background_colour=(40, 102, 110, 255),
            lines={"webs": [2, 4, 6, 8]},
        )     

        # Example Screen 2 Charts

        example_labels_text = [
            Text('Attack'), 
            Text('Defense'), 
            Text('Evasion'), 
            Text('Magic'), 
            Text('M. Defense'), 
            Text('M.Evade'), 
            Text('Speed'), 
            Text('Stamina')
        ]

        example_labels_images = [
            Image('icons/Sword-48.png'),
            Image('icons/Knight Shield-48.png'),
            Image('icons/Dashboard-48.png'),
            Image('icons/Cards-48.png'),
        ]

        label_chart = RadarChart(
            size=200,
            values=plot_values_3,
            max_value=350,
            data_colour=(213, 71, 130, 255),
            line_colour=(0, 0, 0, 255),
            background_colour=(20, 21, 17, 170),
            labels = example_labels_text
        )

        label_chart_images = RadarChart(
            size=200,
            values=[300, 246, 765, 444],
            max_value=1000,
            data_colour=(254, 185, 95, 255),
            line_colour=(9, 4, 70, 255),
            background_colour=(120, 111, 82, 255),
            labels = example_labels_images
        )

        basic_point = Image("icons/square.png")

        points_chart = RadarChart(
            size=200,
            values=[300, 246, 765, 444, 676],
            max_value=1000,
            data_colour=(237, 155, 64, 255),
            line_colour=(170, 43, 102, 255),
            background_colour=(186, 59, 70, 255),
            point=basic_point,
            lines={'data':False}
        )    

        # Example Screen 3 Charts
        animated_points = RadarChart(
            size=200,
            values=[100, 134, 222, 122, 77, 99, 101],
            max_value=350,
            data_colour=(229, 99, 153, 255),
            line_colour=(80, 81, 79, 255),
            background_colour=(135, 145, 158, 255),
            point=basic_point,
            visible={
                "base": True, 
                "data": True, 
                "lines": True, 
                "points": False, 
                "labels": True
            }
        )

        animated_spider_web = RadarChart(
            size=200,
            values=[50, 50, 30, 50, 50, 50],
            max_value=50,
            labels = [
                Text("Strength"),
                Text("Speed"),
                Text("Range"),
                Text("Durability"),
                Text("Precision"),
                Text("Potential")
            ],
            data_colour=(165, 190, 0, 255),
            line_colour=(103, 148, 54, 255),
            background_colour=(88, 82, 74, 255),
            lines={"webs": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            visible={"base":False}
        )

    transform moving_points:
        zoom 0.0
        align (0.5, 0.5)
        alpha 0.0
        parallel:
            linear 0.5 zoom 1.0
            linear 0.5 zoom 0.9
            repeat
        parallel:
            linear 1.0 alpha 1.0
        
    transform spinner_base:
        zoom 0.0
        align (0.5, 0.5)
        rotate 0.0
        alpha 0.0
        parallel:
            linear 1.0 rotate 360
        parallel:
            linear 1.0 zoom 1.0
        parallel:
            linear 1.0 alpha 1.0
    
    transform spinner_data:
        zoom 0.0
        align (0.5, 0.5)
        rotate 0.0
        alpha 0.0
        parallel:
            linear 1.0 rotate 360
        parallel:
            pause 1.0
            linear 0.5 zoom 1.0
        parallel:
            linear 2.0 alpha 1.0
                
    transform spinner_labels:
        zoom 0.0
        align (0.5, 0.5)
        alpha 0.0
        parallel:
            linear 1.0 zoom 1.0
        parallel:
            linear 1.0 alpha 1.0

    jump example_select

# Example One: Lines & Borders    
label example_one:
    call screen radarChart_lines
    jump example_select

# Example Two: Labels & Points
label example_two:
    "Example Two: Labels & Points"
    "Each value in a RadarChart can have a label assigned to it."
    "Each label must be a Displayable. Text or pictures, it doesn't matter."
    call screen radarChart_labels
    "Look at label example_two in the script to see how they're created."
    "You can also assign a Displayable to be shown at each value point."

    call screen radarChart_points
    "Like the labels, this can be any Displayable, but unlike the labels, one Displayable is used for every value."

    jump example_select

label example_three:
    
    "Example Three: ATL Transforms"
    "The RadarChart is a Displayable. As such it can be used with Ren'Py Transforms and ATL."
    "However, you may only want to Transform one part of the RadarChart."
    "Each RadarChart can be split into 5 pieces: Base, Lines, Data, Labels, and Points."
    "These are all Displayables as well, and can all be called separately after creating the RadarChart."
    
    call screen radarChart_transforms
    "By switching off the default visibility of each piece, they won't appear until you explicitly call them."
    "This allows you to apply Transforms to each piece."
    "Look at label example_three in the script to see how this is done."
    
    jump example_select

# Example Four: Updating Values    
label example_four:    
    python:
        # Dummy data
        COOL_VALUE = 200
        BEAUTY_VALUE = 110
        CUTE_VALUE = 90
        SMART_VALUE = 67
        TOUGH_VALUE = 100

        # Stick them into a tuple.
        plot_values = (
            COOL_VALUE,
            BEAUTY_VALUE,
            CUTE_VALUE,
            SMART_VALUE,
            TOUGH_VALUE
        )
        
        # Create a basic RadarChart
        example_four_chart = RadarChart(
            size=200,
            values=plot_values,
            max_value=255,
            data_colour=(100, 200, 100, 255),
            line_colour=(153, 153, 153, 255),
            background_colour=(255, 255, 255, 255),
        )
    
    show image example_four_chart at topright
    "The values for a RadarChart can be updated by setting RadarChart.values."
    "The chart on display's current values are [example_four_chart.values]."
    "Take a peek at label example_four in script.rpy."
    "We're going to update the values for the chart currently on display."

    python:
        # Update the variables.
        COOL_VALUE = 255
        BEAUTY_VALUE = 143
        CUTE_VALUE = 110
        SMART_VALUE = 90
        TOUGH_VALUE = 245

        # Stick them into a tuple.
        new_plot_values = (
            COOL_VALUE, 
            BEAUTY_VALUE, 
            CUTE_VALUE, 
            SMART_VALUE, 
            TOUGH_VALUE
        )

        # Update values.
        example_four_chart.values = new_plot_values

    "Now the values are [example_four_chart.values]."

    "Of course, this can also be done with a chart that uses ATL."
    hide image example_four_chart

    python:
        # Create RadarChart, but hide the data and lines.
        # We'll show them separately.
        example_four_animated_chart = RadarChart(
            size=200,
            values=plot_values,
            max_value=255,
            data_colour=(100, 200, 100, 255),
            line_colour=(153, 153, 153, 255),
            background_colour=(255, 255, 255, 255),
            visible={
                "data": False,
                "lines": False
            }
        )

    # Create transform for the data
    transform atl_data:
        alpha 0.0
        align (1.0, 0.0)
        linear 1.0 alpha 1.0

    show image example_four_animated_chart at topright
    show image example_four_animated_chart.chart_data at atl_data
    show image example_four_animated_chart.chart_lines at topright
    
    "This RadarChart starts off with the values [example_four_animated_chart.values]."

    python:
        example_four_animated_chart.values = new_plot_values
    
    show image example_four_animated_chart.chart_data at atl_data
    "Now, let's update them."
    "Like the previous chart, the values are updated to [example_four_animated_chart.values]."
    
    hide image example_four_animated_chart
    hide image example_four_animated_chart.chart_data
    hide image example_four_animated_chart.chart_lines
    
    jump example_select
