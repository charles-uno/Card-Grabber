
"""
Charles McEachern

Spring 2019

Grab card images from mtg.wtf, save them as PNGs under the hood, then
return them as Matplotlib arrays.
"""

# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from PIL import Image
from urllib.request import urlretrieve

# ----------------------------------------------------------------------

def save_image(canvas, *args, **kwargs):
    print("saving", get_path(*args))
    if not os.path.isdir("flips"):
        os.mkdir("flips")
    plt.figure(**kwargs)
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
    plt.imshow(canvas)
    return plt.savefig(get_path(*args))

# ----------------------------------------------------------------------

def show_image(canvas, **kwargs):
    plt.figure(**kwargs)
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
    plt.imshow(canvas)
    return plt.show()

# ----------------------------------------------------------------------

IMAGES = {}

def get_image(*args):
    if args not in IMAGES:
        if not os.path.isdir("sides"):
            os.mkdir("sides")
        if os.path.exists(get_path(*args)):
            IMAGES[args] = get_image_local(*args)
        else:
            IMAGES[args] = get_image_remote(*args)
    return IMAGES[args]

# ----------------------------------------------------------------------

def get_image_remote(*args):
    print("downloading", get_url(*args))
    urlretrieve(get_url(*args), get_path(*args))
    # Make sure we have a PNG, not a JPG in disguise.
    try:
        return get_image_local(*args)
    except (ValueError, SystemError):
        print("converting", get_path(*args), "from JPG to PNG")
        os.rename(get_path(*args), get_path(*args, ext="jpg"))
        Image.open(get_path(*args, ext="jpg")).save(get_path(*args))
        return get_image_local(*args)

# ----------------------------------------------------------------------

def get_image_local(*args):
    print("loading", get_path(*args))
    return mpimg.imread(get_path(*args))[:, :, :3]

# ----------------------------------------------------------------------

def get_path(abbr, num, side=None, ext="png"):
    if side:
        return "sides/" + abbr + num + side + "." + ext
    else:
        return "flips/" + abbr + num + "." + ext

# ----------------------------------------------------------------------

BASE_URL = "http://mtg.wtf/cards/"

def get_url(abbr, num, side):
    return BASE_URL + abbr + "/" + num + side + ".png"
