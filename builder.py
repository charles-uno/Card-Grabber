#!/usr/bin/env python3

# Charles McEachern

# Spring 2016

# ######################################################################
# ############################################################# Synopsis
# ######################################################################

# WIP...

# ######################################################################
# ################################################## Import Dependencies
# ######################################################################

import numpy as np

import random

import urllib.request

## For conveniently parsing HTML. 
#from bs4 import BeautifulSoup

# We use Matplotlib's image library to display images. 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# For navigating between directories. 
import os

## For choosing randomly from a list. 
#from random import choice

## For grabbing HTML and images from online. 
#from urllib2 import urlopen

# #####################################################################
# ################################################################ Main
# #####################################################################

def main():

    # Grab the images, unless we have them already. 
    url_start = 'http://mtg.wtf/cards/soi/'
    names = ['203b.png', '209b.png', '215b.png']
    for name in names:
        if not os.path.exists(name):
            urllib.request.urlretrieve(url_start + name, name)

    # Fire up a plot figure in the proportions of two cards.
    plt.figure( figsize=(10, 7) )
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)

    # Read in an array of pixels. Chop off the alpha channel. 
    name = names[2]
#    name = random.choice(names)
    img = mpimg.imread(name)[:, :, :3]
    print('Dimensions of the image:', img.shape)

    # Where are the art and the text box? These are the border -- average these. 
    art_t, art_b = 35, 173
    art_l, art_r = 17, 205

    art = img[art_t:art_b+1, art_l:art_r+1]

    avg_t = np.mean(img[art_t, art_l:art_r+1], axis=0)
    avg_b = np.mean(img[art_b, art_l:art_r+1], axis=0)
    avg_l = np.mean(img[art_t:art_b+1, art_l], axis=0)
    avg_r = np.mean(img[art_t:art_b+1, art_r], axis=0)

    # Grab a copy of the image on a new canvas. This is what we'll plot.
    new_img_shape = list(img.shape)
    new_img_shape[1] *= 2
    new_img = np.zeros(new_img_shape)

    half = img.shape[1]

    new_img[:, :half, :] = img

#    # Fuzz the borders a bit. Maybe not necessary?
#    new_img[art_t, art_l:art_r+1] = avg_t
#    new_img[art_b, art_l:art_r+1] = avg_b
#    new_img[art_t:art_b+1, art_l] = avg_l
#    new_img[art_t:art_b+1, art_r] = avg_r

    red = np.array( [1, 0, 0] )

    # We'll cut the height of the art in half. 
    new_art_h = (art_b - art_t)//3
    # Set the top and bottom of the new art. 
    new_art_t = art_t + 10
    new_art_b = new_art_t + new_art_h
    # Paint the part of the art we're not using red. 
    new_img[art_t:new_art_t, art_l:art_r+1] = red
    new_img[new_art_b:art_b, art_l:art_r+1] = red
    # Cut the margins in a different place to reduce the number of seams. 
    cut = (art_b - art_t) - (new_art_b - new_art_t)
    new_img[art_t:art_t+cut, :art_l] = red
    new_img[art_t:art_t+cut, art_r:half] = red

    txt_t, txt_b = 195, 275
    # Keep half of the text box. 
    new_txt_h = (txt_b - txt_t)//2

    new_txt_t = txt_t + 12
    new_txt_b = new_txt_t + new_txt_h

    new_img[txt_t:new_txt_t, art_l:art_r+1] = red
    new_img[new_txt_b:txt_b, art_l:art_r+1] = red

    cut = (txt_b - txt_t) - (new_txt_b - new_txt_t)

    new_img[txt_t:txt_t+cut, :art_l] = red
    new_img[txt_t:txt_t+cut, art_r:half] = red


    # Chunks need to be cut out of the text box and margins in different places to preserve the curvature at the bottom. 




    # Where's the text box?
#    new_img[txt_t, art_l:art_r+1] = red
#    new_img[txt_b, art_l:art_r+1] = red

#    new_img[286, art_l:art_r+1] = red
#    new_img[290, art_l:art_r+1] = red
#    new_img[295, art_l:art_r+1] = red



#    # Left side of the art. 
#    img[:, 18] = 255

#    # Right side of the art.
#    img[:, -19] = 255

#    # Top of the art. 
#    img[36, :] = 255

#    # Bottom of the art. 
#    img[172, :] = 255

    # Turn those pixels into a plot. 
    plt.imshow(new_img)

    plt.show()

    return

# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()

