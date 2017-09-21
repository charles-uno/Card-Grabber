#!/usr/bin/env python3

"""
Charles McEachern

Spring 2016

Grab card images from www.mtg.wtf, then finagle with them. The two
halves of a transform card can be crunched into a Kamigawa-style flip
card.
"""

# ######################################################################

# Matplotlib is used to display and export images.
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
# Image library (third party) is used to convert JPG to PNG.
from PIL import Image
from urllib.request import urlretrieve

# ######################################################################




class FlipCard(dict):

    def __init__(self, abbr, num):
        """Accept the set abbreviation and the collector number. Grab
        scans for that card online if we don't have them already. Load
        those images, and construct the flip card frame.
        """
        self.abbr, self.num = abbr, str(num)
        # Make sure we have a place to store the original images.
        if not os.path.isdir('sides'):
            os.mkdir('sides')
        # Download the card images if we don't have them yet.
        [ self.load(x) for x in 'ab' ]
        # Sanity check: are the pixel arrays the same shape?
        assert self['a'].shape == self['b'].shape
        return

    # ------------------------------------------------------------------

    def frame(self, art=None, atxt=None, btxt=None):
        """Copy chunks of the front and back sides of the card over to a
        third image, where we will assemble it as a flip card. Don't
        worry about the art or text box yet.
        """
        # Start with a canvast the same size as the front and back
        # sides, the same color as the card border.
        self['c'] = np.zeros(self['a'].shape)
        self['c'][:, :] = self['a'][3, 20]

        artt, artb0, artl, artr = 69, 379, 29, 451
        artb1 = 140

        txtt0, txtb0, txtl, txtr = 431, 611, 28, 451
        txtt1 = artb1 + (txtt0 - artb0)
        txtb1 = 300

        if self.abbr in ('isd', 'dka'):
            bott0, botb0, botl, botr = txtb0, 622, txtl, 363
            boxt0, boxb0, boxl = txtb0, 665, 305
            boxt1, boxb1 = txtb1, txtb1 + (boxb0 - boxt0)
        else:
            bott0, botb0, botl, botr = txtb0, 635, txtl, 375
            boxt0, boxb0, boxl = txtb0, 665, 305
            boxt1, boxb1 = txtb1, txtb1 + (boxb0 - boxt0)

        for side in 'ab':
            arth = artb1 - artt
            self['c'][artt:artb1, artl:artr] = self[side][artt:artt + arth, artl:artr]
            self.flip_canvas()

#        for side in 'ab':
#            self[side][artt:artb0, artl:artr] = (1, 0, 1)
#            self[side][txtt0:txtb0, txtl:txtr] = (1, 0, 0)
#            self[side][bott0:botb0, botl:botr] = (0, 0, 1)
#            self[side][boxt0:boxb0, boxl:boxr] = (0, 1, 0)

        for side in 'ab':
            self['c'][:artt, :] = self[side][:artt, :]
            self['c'][artt:artb1, :artl] = self[side][artt:artb1, :artl]
            self['c'][artt:artb1, artr:] = self[side][artt:artb1, artr:]
            self['c'][artb1:txtt1, :] = self[side][artb0:txtt0, :]
            wingt = txtb0 - (txtb1 - txtt1)
            self['c'][txtt1:txtb1, :artl] = self[side][wingt:txtb0, :artl]
            # To get rid of the transform indicator cutout, let's just
            # reflect the left wing over to the right.
            dx = min(self['c'][:, artr:].shape[1], artl)
            wing = self[side][wingt:txtb0, :dx][:, ::-1]
            self['c'][txtt1:txtb1, artr:artr + dx] = wing
            # We want to stagger the power and toughness boxes a little
            # bit, which means the frames need to overlap in the middle.
            dy = 1 + self['c'].shape[0]//2 - txtb1
            self['c'][txtb1:txtb1 + dy, :] = self[side][txtb0:txtb0 + dy, :]
            # We may not want to use the entire text box. Fill in the
            # background to cover the default black.
            blank = np.mean(self[side][txtt0 + 5, txtl:txtr], axis=0)
            for i in range(txtt1, txtb1):
                self['c'][i, txtl:txtr] = blank
            self.flip_canvas()
        # Clip in the art. Allow the user to specify where the slice
        # should be taken. If they don't, take it from the middle.
        art = (art[0] + artt, art[1] + artt) if art else (None, None)
        for t0, side in zip(art, 'ab'):
            arth0, arth1 = artb0 - artt, artb1 - artt
            if t0 is None:
                t0 = artt + (arth0 - arth1)//2
            b0 = t0 + arth1
            self['c'][artt:artb1, artl:artr] = self[side][t0:b0, artl:artr]
            self.flip_canvas()

        # Clip in the text. Note that top and bottom constraints can be
        # specified. If the desired clip is too small, it'll be
        # centered; if it's too big, it'll be squished.
        txth1 = txtb1 - txtt1
        if atxt is None:
            atxt = 0
        if isinstance(atxt, int):
            atxt = (atxt, atxt + txth1)

        atxt = (atxt[0] + txtt0, atxt[1] + txtt0)

        txt = self['a'][atxt[0]:atxt[1], txtr:txtl]

        txth0 = atxt[1] - atxt[0]






        # Add the power and toughness box last, since it can overlap
        # other elements.
        for side in 'ab':
            self['c'][boxt1:boxb1, boxl:] = self[side][boxt0:boxb0, boxl:]
            self.flip_canvas()

        return

    # ------------------------------------------------------------------

    def load(self, side):
        """Check that we have an image for this side of the card. If we
        don't, grab it from the internet, and make sure it's a PNG.
        """
        # If this image doesn't exist locally, go grab it.
        if not os.path.exists( self.path(side) ):
            print( 'Downloading', self.path(side) )
            urlretrieve( self.url(side), self.path(side) )
        # The images on mtg.wtf are sometimes JPGs with the PNG file
        # extension. If that's the case, fix it.
        pngpath = self.path(side)
        jpgpath = pngpath.replace('.png', '.jpg')
        try:
            mpimg.imread(pngpath)
        except (ValueError, SystemError):
            print('Found a JPG in disguise, converting to PNG')
            os.rename(pngpath, jpgpath)
            Image.open(jpgpath).save(pngpath)
            os.remove(jpgpath)
        # Now load the converted image. Throw away the alpha channel,
        # since it does not appear consistently.
        print( 'Loading', self.path(side) )
        self[side] = mpimg.imread(pngpath)[:, :, :3]
        return

    # ------------------------------------------------------------------

    def path(self, side):
        return 'sides/hq_' + self.abbr + self.num + side + '.png'

    # ------------------------------------------------------------------

    def url(self, side):
        return 'http://mtg.wtf/cards_hq/' + self.abbr + '/' + self.num + side + '.png'

    # ------------------------------------------------------------------

    def flip_canvas(self):
        """Rotate the canvas upside-down so we can more easily apply
        back-side elements.
        """
        self['c'] = self['c'][::-1, ::-1]

    # ------------------------------------------------------------------

    def show(self, **kwargs):
        """Plot the card four ways side-by-side: front, back, flip, and
        upside-down flip.
        """
        # Sides 'a' and 'b' are the front and back. Let's have side 'c'
        # be where we assemble the flip card.
        self.frame(**kwargs)
        # Same height as a single card image, but quadruple the width.
        canvas = np.zeros( np.array(self['a'].shape)*(1, 4, 1) )
        cardwidth = self['a'].shape[1]
        # Fill in the front, back, flip, and flipped flip.
        canvas[:, :cardwidth] = self['a']
        canvas[:, cardwidth:2*cardwidth] = self['b']
        canvas[:, 2*cardwidth:3*cardwidth] = self['c']
        canvas[:, 3*cardwidth:] = self['c'][::-1, ::-1]
        # Now create a figure to show it off.
        plt.figure( figsize=(9.6, 3.4) )
        plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
        plt.imshow(canvas)
        return plt.show()





def main():

    # Startled Awake
    card = dfc('soi', 88)
    card.add_art('a', 20)
    card.add_art('b', 10)
    card.add_text('a', 0)
    card.add_text('b', 0, careful=False)
    card.save()

#    card.show( art=(50, 25) )

    return

    # Kessig Prowler
    card = dfc('emn', 163)
    card.add_art('a', 15)
    card.add_art('b', 0)
    card.add_text('a', 22)
    card.add_text('b', 10, careful=False)
    card.show()

    '''
    # Delver of Secrets.
    delver = dfc('isd', 51)
    delver.add_art('a', 20)
    delver.add_art('b', 15)
    delver.add_text('a', 15)
    delver.add_text('b', 2, kp=20)
    delver.show()

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
