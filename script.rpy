screen radarChart:
    # This screen displays 3 different RadarCharts.

    # Display RadarCharts using Screen Language
    add rc:
        xpos 100
        ypos 50
 
    add rc2:
        xpos 400
        ypos 50

    add rc3:
        xpos 100
        ypos 250

    # ResetChartAnimation must be called with all the RadarCharts as arguments.
    # This allows the animations to reset and replay the next time the screen containing the charts is opened.
    textbutton "Return" action [ResetChartAnimation(rc, rc2, rc3), Return()] xalign .99 yalign .99

# Game starts here
label start:
    python:
        # Create some dummy data to use in the Radar Charts
        COOL_VALUE = 200
        BEAUTY_VALUE = 110
        CUTE_VALUE = 90
        SMART_VALUE = 67
        TOUGH_VALUE = 100

        plot_values = (
            COOL_VALUE,
            BEAUTY_VALUE,
            CUTE_VALUE,
            SMART_VALUE,
            TOUGH_VALUE
        )
        
        GRAPE_VALUE = 200
        APPLE_VALUE = 110
        ORANGE_VALUE = 90
        BANANA_VALUE = 67
        LEMON_VALUE = 100
        LIME_VALUE = 82
        POTATO_VALUE = 333
        
        plot_values_2 = (
            GRAPE_VALUE,
            APPLE_VALUE,
            ORANGE_VALUE,
            BANANA_VALUE,
            LEMON_VALUE,
            LIME_VALUE,
            POTATO_VALUE
        )

        LION_VALUE = 200
        TIGER_VALUE = 110
        BEAR_VALUE = 190
        PANDA_VALUE = 67
        HORSE_VALUE = 100
        CHEETAH_VALUE = 22
        EAGLE_VALUE = 333
        FALCON_VALUE = 111
        
        plot_values_3 = (
            LION_VALUE,
            TIGER_VALUE,
            BEAR_VALUE,
            PANDA_VALUE,
            HORSE_VALUE,
            CHEETAH_VALUE,
            EAGLE_VALUE,
            FALCON_VALUE
        )

        # Create RadarChart objects
        rc = RadarChart(
            size=200,
            values=plot_values,
            max_value=255,
            data_colour=(100, 200, 100, 125),
            line_colour=(153, 153, 153, 255),
            background_colour=(255, 255, 255, 255),
            show_lines=True,
            animated=True,
            speed=2
        )
        
        # No Animation
        rc2 = RadarChart(
            size=200,
            values=plot_values_2,
            max_value=350,
            data_colour=(200, 200, 100, 255),
            line_colour=(0, 0, 0, 255),
            background_colour=(155, 55, 80, 255),
            show_lines=True,
            animated=False
        )
        
        # No lines
        rc3 = RadarChart(
            size=300,
            values=plot_values_3,
            max_value=350,
            data_colour=(50, 100, 100, 255),
            line_colour=(0, 0, 0, 255),
            background_colour=(115, 155, 80, 255),
            show_lines=False,
            animated=True,
            speed=6
        )
        
    "Let's go to the Radar Chart screen."    
    
    call screen radarChart
    
    "The values for a chart can be updated at any time. Just replace the values variable."
    python:
        COOL_VALUE = 255
        BEAUTY_VALUE = 143
        CUTE_VALUE = 110
        SMART_VALUE = 90
        TOUGH_VALUE = 245

        plot_values = (
            COOL_VALUE, 
            BEAUTY_VALUE, 
            CUTE_VALUE, 
            SMART_VALUE, 
            TOUGH_VALUE
        )
        rc.values = plot_values
        
    "Inside the script.rpy, you'll see that before this line we changed the values for one of the Radar Plots."
    
    call screen radarChart