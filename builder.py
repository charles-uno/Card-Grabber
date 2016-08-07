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

    flip = None

    h_ttl = 35
    h_art = 138
    h_typ = 22
    h_txt = 90
    h_div = 5
    h_lip = 5
    h_pow = 20

    h_art_new = 45
    h_txt_new = 45

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
            self.draw_flip(side)
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

    def draw_flip(self, side, careful=False):

        art_top = self.h_ttl
        art_bot = art_top + self.h_art
        txt_top = art_bot + self.h_typ
        txt_bot = txt_top + self.h_txt
        txt_mid = txt_bot - self.h_txt_new
        div_bot = txt_bot + self.h_div
        pow_bot = div_bot + self.h_lip
        pow_top = pow_bot - self.h_pow
        art_bot_new = art_top + self.h_art_new
        txt_top_new = art_bot_new + self.h_typ
        txt_bot_new = txt_top_new + self.h_txt_new
        div_bot_new = txt_bot_new + self.h_div
        pow_bot_new = div_bot_new + self.h_lip
        pow_top_new = pow_bot_new - self.h_pow

        # Title line. 
        self.flip[:art_top, :] = self[side][:art_top, :]
        # Type line.
        self.flip[art_bot_new:txt_top_new, :] = self[side][art_bot:txt_top, :]
        # Text box framing. Note that we don't use the right side. We
        # reflect the left over instead, to get rid of the divot. 
        temp = self[side][txt_mid:pow_top, :self.w_pad]
        self.flip[txt_top_new:pow_top_new, :self.w_pad] = temp
        self.flip[txt_top_new:pow_top_new, -self.w_pad:] = temp[:, ::-1]
        # Bottom of the text box, including the divider line. This risks
        # overwriting part of the text box. 
        if not careful:
            self.flip[pow_top_new:div_bot_new, :] = self[side][pow_top:div_bot, :]
        # Power toughness box. Constrain the width so the front and back
        # boxes can be staggered. 
        temp = self[side][pow_top:pow_bot, -self.w_pow:]
        self.flip[pow_top_new:pow_bot_new, -self.w_pow:] = temp

        return

    # ==================================================================
    # ================================================== Add Art to Flip
    # ==================================================================

    def add_art(self, side, offset=None):
        # If the position isn't given, go for the middle. 
        if offset is None:
            offset = (self.h_art - self.h_art_new)//2
            print('automatic art offset:', offset)
        # Grab the art slice. 
        top_old = self.h_ttl + offset
        bot_old = top_old + self.h_art_new
        temp = self[side][top_old:bot_old, :]
        # Flip the canvas, if necessary. 
        if side == 'b':
            self.flip_flip()
        # Paste in the art slice. Note that we go all the way to the
        # edges because Eldrazi flip cards have transparent borders. 
        top_new = self.h_ttl
        bot_new = top_new + self.h_art_new
        self.flip[top_new:bot_new, :] = temp
        # Flip the canvas back. 
        if side == 'b':
            self.flip_flip()
        return

    # ==================================================================
    # ================================================= Add Text to Flip
    # ==================================================================

    def add_text(self, side, offset=None, careful=True):

        # If the position isn't given, go for the middle. 
        if offset is None:
            offset = (self.h_txt - self.h_txt_new)//2
            print('automatic text offset:', offset)
        # Grab the text slice. 
        top_old = self.h_ttl + self.h_art + self.h_typ + offset
        bot_old = top_old + self.h_txt_new
        temp = self[side][top_old:bot_old, self.w_pad:-self.w_pad]
        # Flip the canvas, if necessary. 
        if side == 'b':
            self.flip_flip()
        # Paste in the text slice. Note that we have already handled the
        # borders, to preserve the curvature. 
        top_new = self.h_ttl + self.h_art_new + self.h_typ
        bot_new = top_new + self.h_txt_new
        self.flip[top_new:bot_new, self.w_pad:-self.w_pad] = temp
        # Redraw the power toughness box. Optionally, also redraw the
        # bottom of the text box -- this can be used to wipe out
        # truncated flavor text. 
        self.draw_flip(side, careful=careful)
        # Flip the canvas back. 
        if side == 'b':
            self.flip_flip()


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

    # ------------------------------------------------------------------

    @property
    def pilf(self):
        return self.flip[::-1, ::-1]

    @pilf.setter
    def pilf(self, *args):
        raise TypeError('dfc.pilf is read-only')

    # ------------------------------------------------------------------

    def debug(self):
        shape = np.array(self.shape)*(1, 4, 1)
        arr = np.zeros(shape)
        width = self.shape[1]

        arr[:, :width] = self['a']
        arr[:, width:2*width] = self['b']
        arr[:, 2*width:3*width] = self.flip
        arr[:, 3*width:] = self.pilf

        return arr        









class dfc_old(dfc):
    # In SOI, cards have the new new frame, which is black at the
    # bottom. That's very convenient. In the original Innistrad block,
    # cards used the 8th Edition frame. The bottom requires better
    # matching, and the proportions are a bit different. 
    h_ttl = 35
    h_art = 138
    h_typ = 21
    h_txt = 83
    h_div = 7
    h_lip = 12
    h_pow = 22

    h_art_new = 43
    h_txt_new = 43

    w_pad = 17
    w_pow = 112




# ######################################################################
# ################################################################# Main
# ######################################################################

def main():

    prowler = dfc('emn', 163)
    prowler.add_art('a', 15)
    prowler.add_art('b', 0)
    prowler.add_text('a', 22)
    prowler.add_text('b', 10, careful=False)

    waif = dfc_old('isd', 159)
    waif.add_art('a', 10)
    waif.add_art('b')
    waif.add_text('a', 11)
    waif.add_text('b', 8)

    # Fire up a plot figure in the proportions of three cards.
    plt.figure( figsize=(20, 7) )
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)

    # Plot the front, back, flip, and flipped flip. 
    img = waif.debug()

    blue = np.array( [0, 0, 1] )

#    img[50, :] = blue
#    img[100, :] = blue
#    img[150, :] = blue
#    img[200, :] = blue
#    img[250, :] = blue
#    img[300, :] = blue



    plt.imshow(img)

    return plt.show()

# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()

