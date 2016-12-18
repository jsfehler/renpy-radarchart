# Example Screen 1: Lines & Borders
screen radarChart_lines:

    text "Default" xpos 20 ypos 20
    add default:
        xpos 50
        ypos 50

    text "No Data Border" xpos 270 ypos 20
    add no_data_outline:
        xpos 300
        ypos 50

    text "No Borders, No Spokes" xpos 530 ypos 20
    add no_outline:
        xpos 560
        ypos 50

    text "No Spokes" xpos 100 ypos 270
    add no_spokes:
        xpos 100
        ypos 300

    text "Borders, Spokes, & Webs" xpos 400 ypos 270
    add spider_web_partial:
        xpos 400
        ypos 300

    textbutton "Return" action Return() xalign .99 yalign .99

# Example Screen 2: Labels
screen radarChart_labels:

    text "Text Labels" xpos 20 ypos 20
    add label_chart:
        xpos 120
        ypos 100

    text "Image Labels" xpos 420 ypos 20
    add label_chart_images:
        xpos 500
        ypos 100

    textbutton "Return" action Return() xalign .99 yalign .99

# Example Screen 2b: Points
screen radarChart_points:
    text "Points" xpos 20 ypos 20
    add points_chart:
        xpos 100
        ypos 100

    textbutton "Return" action Return() xalign .99 yalign .99


# Example Screen 3: ATL Transforms
screen radarChart_transforms:

    # When splitting up the pieces of a RadarChart,
    # it helps to put them inside a frame.
    text "Animated Points" xpos 20 ypos 20
    frame:
        background None
        xysize (200, 200)
        xpadding 0
        ypadding 0
        xpos 50
        ypos 50

        # The RadarChart
        add animated_points

        # The RadarChart's points, using a Transform
        add animated_points.chart_points at moving_points

    # RadarChart where all the labels are split
    text "Multiple Transforms" xpos 370 ypos 20
    frame:
        background None
        xysize (200, 200)
        xpadding 0
        ypadding 0
        xpos 400
        ypos 150
        add animated_spider_web.chart_base at spinner_base
        add animated_spider_web.chart_data at spinner_data
        add animated_spider_web.chart_lines at spinner_base
        add animated_spider_web.chart_labels at spinner_labels

    textbutton "Return" action Return() xalign .99 yalign .99
