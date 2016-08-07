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

from urllib.request import urlretrieve

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

# ######################################################################
# ############################################## Double Faced Card Class
# ######################################################################

class dfc(dict):

    url_root = 'http://mtg.wtf/cards/'

    abbr, num = None, None

    flip = None, None, None

    h_ttl = 35
    h_art = 138
    h_typ = 22
    h_txt = 80
    h_div = 15
    h_pow = 6

    h_art_new = 45
    h_txt_new = 34

    w_pad = 17
    w_pow = 53

    # ==================================================================
    # ========================================== Initialize Pixel Arrays
    # ==================================================================

    def __init__(self, abbr, num):

        self.abbr, self.num = abbr, str(num)

        # Check if we already have images for this card. If not,
        # download them. 
        for side in ('a', 'b'):
            if os.path.exists( self.path(side) ):
                print( 'already have ', self.path(side) )
            else:
                print( 'getting ', self.path(side) )
                urlretrieve( self.url(side), self.path(side) )
        # Load the front and back images into arrays.
        for side in ('a', 'b'):
            self[side] = mpimg.imread( self.path(side) )[:, :, :3]
        # Sanity check: are the pixel arrays the same shape?
        assert self['a'].shape == self['b'].shape
        # Create a third array. Fill it with the border color. 
        self.flip = np.zeros(self['a'].shape)
        self.flip[:, :] = self['a'][3, 20]
        # Combine the front and back like a flip card. 
        for side in ('a', 'b'):
            self.frame_flip(side)
            # Flipping the canvas is easier than rearranging the pieces.
            self.flip_flip()
        return

    # ------------------------------------------------------------------

    def path(self, side):
        return self.abbr + self.num + side + '.png'

    # ------------------------------------------------------------------

    def url(self, side):
        return self.url_root + self.abbr + '/' + self.num + side + '.png'

    # ==================================================================
    # ================================================== Flip the Canvas
    # ==================================================================

    def flip_flip(self):
        self.flip = self.flip[::-1, ::-1]

    # ==================================================================
    # ============================================= Map Card Frames Over
    # ==================================================================

    def frame_flip(self, side):
        # Title line. 
        self.flip[:self.h_ttl, :] = self[side][:self.h_ttl, :]
        # Left and right art framing. 
        bot_old = self.h_ttl + self.h_art
        top_old = bot_old - self.h_art_new
        left = self[side][top_old:bot_old, :self.w_pad]
        right = self[side][top_old:bot_old, -self.w_pad:]
        bot_new = self.h_ttl + self.h_art_new
        top_new = self.h_ttl
        self.flip[top_new:bot_new, :self.w_pad] = left
        self.flip[top_new:bot_new, -self.w_pad:] = right
        # Type line.
        top_old = self.h_ttl + self.h_art
        bot_old = top_old + self.h_typ
        top_new = self.h_ttl + self.h_art_new
        bot_new = top_new + self.h_typ
        self.flip[top_new:bot_new, :] = self[side][top_old:bot_old, :]
        # Text box framing. Note that we don't use the right side. We
        # reflect the left over instead, to get rid of the divot. 
        bot_old = self.h_ttl + self.h_art + self.h_typ + self.h_txt
        top_old = bot_old - self.h_txt_new
        left = self[side][top_old:bot_old, :self.w_pad]
        top_new = self.h_ttl + self.h_art_new + self.h_typ
        bot_new = top_new + self.h_txt_new
        self.flip[top_new:bot_new, :self.w_pad] = left
        self.flip[top_new:bot_new, -self.w_pad:] = left[:, ::-1]
        # Divider at the bottom of the text box. 
        top_old = self.h_ttl + self.h_art + self.h_typ + self.h_txt
        bot_old = top_old + self.h_div
        top_new = self.h_ttl + self.h_art_new + self.h_typ + self.h_txt_new
        bot_new = top_new + self.h_div
        self.flip[top_new:bot_new, :] = self[side][top_old:bot_old, :]
        # Get the bottom of the power toughness box. Constrain the width
        # so the front and back boxes can be staggered. 
        top_old = self.h_ttl + self.h_art + self.h_typ + self.h_txt + self.h_div
        bot_old = top_old + self.h_pow
        temp = self[side][top_old:bot_old, -self.w_pow:]
        top_new = self.h_ttl + self.h_art_new + self.h_typ + self.h_txt_new + self.h_div
        bot_new = top_new + self.h_pow
        self.flip[top_new:bot_new, -self.w_pow:] = temp
        return


    # ==================================================================
    # ================================================= Helper Functions
    # ==================================================================

    @property
    def shape(self):
        return self['a'].shape

    @shape.setter
    def shape(self, *args):
        raise TypeError('dfc.shape is read-only')




# ######################################################################
# ################################################################# Main
# ######################################################################

def main():

    prowler = dfc('emn', 163)

    # We'll plot a triple-wide image: front, back, and flip. 
    new_img_shape = np.array(prowler.shape)*(1, 3, 1)
    new_img = np.zeros(new_img_shape)

    # Put the front in the first slot and the back in the second slot.
    # We'll stitch them together in the third slot. 
    card_width = prowler.shape[1]
    new_img[:, :card_width] = prowler['a']
    new_img[:, card_width:2*card_width] = prowler['b']
    new_img[:, 2*card_width:] = prowler.flip

    # Fire up a plot figure in the proportions of three cards.
    plt.figure( figsize=(15, 7) )
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)

    # Turn those pixels into a plot. 
    plt.imshow(new_img)

    return plt.show()

# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()

