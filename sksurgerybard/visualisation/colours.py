"""
Preset colours for Athena's luminance study
"""

# from here
# Grayscale Design palette: https://grayscale.design/app

#lets create dictionaries we can use of pre set colours
grayscale = {
    "50": [255, 255, 255],
    "100": [242, 242, 242],
    "200": [228, 228, 228],
    "300": [213, 213, 213],
    "400": [197, 197, 197],
    "500": [178, 178, 178],
    "600": [156, 156, 156],
    "700": [130, 130, 130],
    "800": [94, 94, 94],
    "900": [0, 0, 0]
}

yellow = {
    "50": [255, 255, 142],
    "100": [245, 245, 0],
    "200": [232, 232, 0],
    "300": [217, 217, 0],
    "400": [203, 203, 0],
    "500": [184, 184, 0],
    "600": [164, 164, 0],
    "700": [141, 141, 0],
    "800": [111, 111, 0],
    "900": [63, 63, 0]
}

green =  {
    "50": [233, 255, 233],
    "100": [181, 255, 181],
    "200": [92, 255, 92],
    "300": [0, 244, 0],
    "400": [0, 227, 0],
    "500": [0, 207, 0],
    "600": [0, 185, 0],
    "700": [0, 159, 0],
    "800": [0, 125, 0],
    "900": [0, 72, 0]
}

def y_pos_to_luminance(y_pos):
    """
    y_pos is a float between 0 and 1 representing the position of the
    mouse on the screen. High y_pos corresponds to high luminance (50)
    low y_pos to low luminance (900)
    """
    luminances = ["50", "100", "200", "300", "400", "500", "600",
            "700", "800", "900"]
    index = 0
    threshold = 0.9
    while index < len(luminances):
        if y_pos > threshold:
            return luminances[index]
        index += 1
        threshold -= 0.1

    return luminances[index-1]


def integer_colour_to_float(colour):
    """
    converts an integer colour to a float colour
    """
    out=[]
    for value in colour:
        out.append((value)/255.0)

    return out


def get_green(y_pos):
    """Gets a green shade with luminace set by y_pos"""
    luminance = y_pos_to_luminance(y_pos)
    return luminance, integer_colour_to_float(green.get(luminance))

def get_yellow(y_pos):
    """Gets a yellow shade with luminace set by y_pos"""
    luminance = y_pos_to_luminance(y_pos)
    return luminance, integer_colour_to_float(yellow.get(luminance))
