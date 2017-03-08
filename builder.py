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

from urllib.request import urlretrieve

from PIL import Image

# We use Matplotlib's image library to display images.
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# For navigating between directories.
import os





# ######################################################################
# ################################################################# Main
# ######################################################################

def main():


    # Delver of Secrets.
    delver = dfc('isd', 51)
    delver.add_art('a', 20)
    delver.add_art('b', 15)
    delver.add_text('a', 15)
    delver.add_text('b', 2, kp=20)
    delver.show()

    '''
    # Kessig Prowler
    card = dfc('emn', 163)
    card.add_art('a', 15)
    card.add_art('b', 0)
    card.add_text('a', 22)
    card.add_text('b', 10, careful=False)
    card.save()

    waif = dfc('isd', 159)
    waif.add_art('a', 10)
    waif.add_art('b')
    waif.add_text('a', 11)
    waif.add_text('b', 8)
    waif.save()

    angler = dfc('emn', 63)
    angler.add_art('a', 20)
    angler.add_art('b')
    angler.add_text('a', 5)
    angler.add_text('b', 10, careful=False)
    angler.save()

    chalice = dfc('dka', 146)
    chalice.add_art('a', 20)
    chalice.add_art('b')
    chalice.add_text('a', 10)
    chalice.add_text('b')
    chalice.save()

    rider = dfc('emn', 33)
    rider.add_art('a', 10)
    rider.add_art('b', 10)
    rider.add_text('a', 3)
    rider.add_text('b', 3, careful=False)
    rider.save()

    stranger = dfc('soi', 119)
    stranger.add_art('a', 12)
    stranger.add_art('b', 3)
    stranger.add_text('a', 10)
    stranger.add_text('b', 8)
    stranger.save()

    # Town Gossipmonger
    card = dfc('soi', 46)
    card.add_art('a')
    card.add_art('b')
    card.add_text('a', 15)
    card.add_text('b', 7)
    card.save()

    # Heir of Falkenrath
    card = dfc('soi', 116)
    card.add_art('a', 25)
    card.add_art('b', 55)
    card.add_text('a', 2)
    card.add_text('b', 2, careful=False)
    card.save()

    # Conduit of Storms
    card = dfc('emn', 124)
    card.add_art('a', 60)
    card.add_art('b', 40)
    card.add_text('a', 15)
    card.add_text('b', 15)
    card.save()

    # Smoldering Werewolf
    card = dfc('emn', 142)
    card.add_art('a', 20)
    card.add_art('b', 5)
    card.add_text('a', 5)
    card.add_text('b', 4)
    card.save()

    # Tangleclaw Werewolf
    card = dfc('emn', 174)
    card.add_art('a', 20)
    card.add_art('b', 20)
    card.add_text('a', 5)
    card.add_text('b', 10)
    card.save()

    # Village Messenger... doctored the reminder text out of Menace.
    card = dfc('soi', 190)
    card.add_art('a', 25)
    card.add_art('b', 40)
    card.add_text('a', 14)
    card.add_text('b', 28)
    card.save()
    '''

#    # Breakneck Rider... five lines of text is just too much!
#    card = dfc('soi', 147)
#    card.add_art('a', 25)
#    card.add_art('b', 25)
#    card.add_text('a', 8)
#    card.add_text('b', 9)
#    card.show()

    return


# ######################################################################
# ############################################## Double Faced Card Class
# ######################################################################

def dfc(abbr, num):
    # Card frames have changed since the original Innistrad block.
    if abbr in ('isd', 'dka'):
        return dfc_old(abbr, num)
    else:
        return dfc_new(abbr, num)



class dfc_new(dict):

    url_root = 'http://mtg.wtf/cards/'

    abbr, num = None, None

    flip = None

    h_ttl = 35
    h_art = 138
    h_typ = 22
    h_txt = 91
    h_div = 4
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
        # Store the input files in their own directory.
        if not os.path.isdir('sides'):
            os.mkdir('sides')
        # Check if we already have images for this card. If not,
        # download them.
        for side in ('a', 'b'):
            if os.path.exists( self.path(side) ):
                print( 'already have ', self.path(side) )
            else:
                print( 'getting ', self.path(side) )
                urlretrieve( self.url(side), self.path(side) )

        # Make sure our image is actually a PNG! Some of the scans on
        # mtg.wtf have PNG extensions, but are actually in JPG format.
        for side in 'ab':
            pngpath = self.path(side)
            jpgpath = pngpath.replace('.png', '.jpg')
            try:
                mpimg.imread(pngpath)
            except (ValueError, SystemError):
                print('WARNING:', pngpath, 'is actually a JPG')
                # Rename the JPG to be accurate.
                os.rename(pngpath, jpgpath)
                # Conver it to a PNG.
                Image.open(jpgpath).save(pngpath)

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
        return 'sides/' + self.abbr + self.num + side + '.png'

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

    def add_text(self, side, offset=None, careful=True, kp=None):
        # If the position isn't given, go for the middle.
        if offset is None:
            offset = (self.h_txt - self.h_txt_new)//2
            print('automatic text offset:', offset)
        # Grab the text slice.
        top_old = self.h_ttl + self.h_art + self.h_typ + offset
        bot_old = top_old + self.h_txt_new

#        if kp is not None:
#            self[side][top_old + offset:top_old + kp] = (1, 0, 0)

        temp = self[side][top_old:bot_old, self.w_pad:-self.w_pad]

        if kp is not None:

            h_template = bot_old - top_old
            h_actual = kp - offset
            text = np.array( self[side][top_old:top_old + h_actual, self.w_pad:-self.w_pad] )

            buff = self[side][top_old+2:top_old+3, self.w_pad:-self.w_pad]

            print('offset', offset)
            print('kp', kp)

            print('text height', h_actual)

            print('template height', h_template)

            buf_top = (h_template - h_actual)//2
            buf_bot = h_template - h_actual - buf_top

            print('buffer lines at the top', buf_top)
            print('buffer lines at the bottom', buf_bot)

            for i in range(h_template):
                temp[i, :] = buff

            temp[buf_top:buf_top + h_actual, :] = text


#            # Where is the top of the text box?
#            box_top = self.h_ttl + self.h_art + self.h_typ + 1
#            # Replace the stuff under the rules text (likely flavor
#            # text) with blank space from the top of the text box.
#            dy1 = kp - offset
#            dy2 = self.h_txt_new - dy1
#            temp[dy1:, :] = self[side][box_top:box_top + dy2, self.w_pad:-self.w_pad]

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

    # ==================================================================
    # ================================================== Save Card Image
    # ==================================================================

    def save(self):
        plt.figure( figsize=(2.23, 3.10) )
        plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
        plt.imshow(self.flip)
        # Make sure we have a directory to save the output.
        if not os.path.isdir('flips'):
            os.mkdir('flips')
        savepath = 'flips/' + self.abbr + self.num + '.png'
        print('saving', savepath)
        return plt.savefig(savepath)

    # ==================================================================
    # ================================================== Show Card Image
    # ==================================================================

    def show(self):
        plt.figure( figsize=(9.92, 3.10) )
        plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
        plt.imshow( self.debug() )
        return plt.show()





class dfc_old(dfc_new):
    # In SOI, cards have the new new frame, which is black at the
    # bottom. That's very convenient. In the original Innistrad block,
    # cards used the 8th Edition frame. The bottom requires better
    # matching, and the proportions are a bit different.
    h_ttl = 37
    h_art = 136
    h_typ = 21
    h_txt = 83
    h_div = 7
    h_lip = 12
    h_pow = 22

    h_art_new = 41
    h_txt_new = 43

    w_pad = 17
    w_pow = 112


# ######################################################################
# #################################################### For Importability
# ######################################################################

if __name__=='__main__':
  main()
