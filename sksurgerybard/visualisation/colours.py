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
    "50": [255, 255, 255],
    "100": [250, 250, 0],
    "200": [236, 236, 0],
    "300": [220, 220, 0],
    "400": [203, 203, 0],
    "500": [184, 184, 0],
    "600": [162, 162, 0],
    "700": [134, 134, 0],
    "800": [97, 97, 0],
    "900": [0, 0, 0]
}

green =  {
    "50": [255, 255, 255],
    "100": [205, 255, 205],
    "200": [129, 255, 129],
    "300": [0, 247, 0],
    "400": [0, 228, 0],
    "500": [0, 207, 0],
    "600": [0, 182, 0],
    "700": [0, 151, 0],
    "800": [0, 110, 0],
    "900": [0, 0, 0]
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
    return integer_colour_to_float(green.get(y_pos_to_luminance(y_pos)))

def get_yellow(y_pos):
    """Gets a yellow shade with luminace set by y_pos"""
    return integer_colour_to_float(yellow.get(y_pos_to_luminance(y_pos)))
