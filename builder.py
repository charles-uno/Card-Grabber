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

    url = 'http://mtg.wtf/cards/soi/215a.png'

#    url_start = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card&name='

#    card_name = 'Lambholt Pacifist'

#    card_url = url_start + card_name

    urllib.request.urlretrieve(url, 'test.jpg')

#    # Grab the image data from online, and dump it into a file. The
#    # 'wb' option means we're writing binary, not text. 
#    img = urlopen(card_url).read()

#    with open('test.jpg', 'wb') as handle:
#      handle.write(img)

    plt.figure( figsize=(5, 7) )

    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)

    # Have matplotlib read in the image as a Numpy array of pixels. 
    img = mpimg.imread('test.jpg')

    # Turn those pixels into a plot. 
    plt.imshow(img)

    plt.show()

    return

# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()

