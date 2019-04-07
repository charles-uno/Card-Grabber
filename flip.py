
"""
Charles McEachern

Spring 2019

Assemble the front and back of a double-faced card into a Kamigawa-style
flip card.
"""

# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import sys

import images

DEBUG = "--debug" in sys.argv

# ----------------------------------------------------------------------

def dfc(abbr, num, **kwargs):
    # Card frames have changed since the original Innistrad block.
    if abbr in ("isd", "dka"):
        return dfc_old(abbr, num, **kwargs)
    else:
        return dfc_new(abbr, num, **kwargs)

# ----------------------------------------------------------------------

class dfc_new(dict):

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
    art_offset = {"a": 0, "b": 0}
    # Where are we trimming text from the old text box?
    txt_top = {"a": 0, "b": 0}
    txt_bot = {"a": 45, "b": 45}
    # What's the size of the new text box?
    h_txt_new = {"a": 45, "b": 45}
    w_pad = 18
    w_pow = 53

    # ------------------------------------------------------------------

    def __init__(self, abbr, num, **kwargs):
        self.abbr, self.num = abbr, str(num)
        for side in "ab":
            self[side] = images.get_image(self.abbr, self.num, side)
        assert self["a"].shape == self["b"].shape
        # Create a third array. Fill it with the border color.
        self.flip = np.zeros(self["a"].shape)
        self.flip[:, :] = self["a"][3, 20]
        # Figure out what text will go where.
        if "txt_a" in kwargs:
            self.txt_top["a"], self.txt_bot["a"] = kwargs.pop("txt_a")
        if "txt_b" in kwargs:
            self.txt_top["b"], self.txt_bot["b"] = kwargs.pop("txt_b")
        # Optionally also say where to slice the art.
        if "art_ab" in kwargs:
            self.art_offset["a"], self.art_offset["b"] = kwargs.pop("art_ab")
        # Figure out if we need to resize the text boxes.
        h_txt = {
            "a": self.txt_bot["a"] - self.txt_top["a"],
            "b": self.txt_bot["b"] - self.txt_top["b"],
        }
        h_txt_total = self.h_txt_new["a"] + self.h_txt_new["b"]
        # Sanity check: does all the text fit?
        if h_txt["a"] + h_txt["b"] > h_txt_total:
            raise ValueError("can't fit %d + %d in %d pixels" % (h_txt["a"], h_txt["b"], h_txt_total))
        # If one side wants 60 pixels of text, shrink the other to fit.
        for side in "ab":
            if h_txt[side] > self.h_txt_new[side]:
                other_side = "a" if side == "b" else "b"
                self.h_txt_new[side] = h_txt[side]
                self.h_txt_new[other_side] = h_txt_total - h_txt[side]
        return self.debug() if DEBUG else self.save()

    # ------------------------------------------------------------------

    def __del__(self):
        # When the object goes out of scope, clean up the plot.
        return plt.close()

    # ------------------------------------------------------------------

    def draw(self):
        for side in ('a', 'b'):
            self.draw_art(side)
            # Frame includes text background.
            self.draw_frame(side)
            self.draw_text(side)
            self.draw_power(side)
            self.flip_flip()
        return

    # ------------------------------------------------------------------

    def save(self):
        self.draw()
        return images.save_image(self.flip, self.abbr, self.num, figsize=(4.46, 6.20))

    # ------------------------------------------------------------------

    def show(self, side):
        self.draw()
        return images.show_image(self[side], figsize=(4.46, 6.20))

    # ------------------------------------------------------------------

    def debug(self):
        self.draw()
        shape = np.array(self["a"].shape)*(1, 4, 1)
        arr = np.zeros(shape)
        width = self["a"].shape[1]
        arr[:, :width] = self['a']
        arr[:, width:2*width] = self['b']
        arr[:, 2*width:3*width] = self.flip
        arr[:, 3*width:] = self.flip[::-1, ::-1]
        images.show_image(arr, figsize=(19.84, 6.20))
        # Debug one thing at a time.
        return sys.exit()

    # ------------------------------------------------------------------

    def flip_flip(self):
        self.flip = self.flip[::-1, ::-1]

    # ------------------------------------------------------------------

    def draw_power(self, side):
        art_top = self.h_ttl
        art_bot = art_top + self.h_art
        txt_top = art_bot + self.h_typ
        txt_bot = txt_top + self.h_txt
        div_bot = txt_bot + self.h_div
        pow_bot = div_bot + self.h_lip
        pow_top = pow_bot - self.h_pow
        art_bot_new = art_top + self.h_art_new
        txt_top_new = art_bot_new + self.h_typ
        txt_bot_new = txt_top_new + self.h_txt_new[side]
        div_bot_new = txt_bot_new + self.h_div
        pow_bot_new = div_bot_new + self.h_lip
        pow_top_new = pow_bot_new - self.h_pow
        self.flip[pow_top_new:pow_bot_new, -self.w_pow:] = self[side][pow_top:pow_bot, -self.w_pow:]
        return

    # ------------------------------------------------------------------

    def draw_frame(self, side):
        art_top = self.h_ttl
        art_bot = art_top + self.h_art
        txt_top = art_bot + self.h_typ
        txt_bot = txt_top + self.h_txt
        txt_mid = txt_bot - self.h_txt_new[side]
        div_bot = txt_bot + self.h_div
        pow_bot = div_bot + self.h_lip
        pow_top = pow_bot - self.h_pow
        art_bot_new = art_top + self.h_art_new
        txt_top_new = art_bot_new + self.h_typ
        txt_bot_new = txt_top_new + self.h_txt_new[side]
        div_bot_new = txt_bot_new + self.h_div
        pow_bot_new = div_bot_new + self.h_lip
        pow_top_new = pow_bot_new - self.h_pow
        # Title line.
        self.flip[:art_top, :] = self[side][:art_top, :]
        # Type line.
        self.flip[art_bot_new:txt_top_new, :] = self[side][art_bot:txt_top, :]
        # Text box framing. Reflect the left over to lose the divot.
        temp = self[side][txt_mid:pow_top, :self.w_pad]
        self.flip[txt_top_new:pow_top_new, :self.w_pad] = temp
        self.flip[txt_top_new:pow_top_new, -self.w_pad:] = temp[:, ::-1]
        # Right and bottom borders of the text box.
        self.flip[pow_top_new:div_bot_new, :self.w_pad] = self[side][pow_top:div_bot, :self.w_pad]
        self.flip[txt_bot_new:div_bot_new, self.w_pad:] = self[side][txt_bot:div_bot, self.w_pad + 1:self.w_pad + 2, :]
        # Empty background for the text box.
        text_box_bg = [1, 0, 0] if DEBUG else self[side][txt_bot - 2, self.w_pad + 1]
        self.flip[txt_top_new:txt_bot_new, self.w_pad:-self.w_pad] = text_box_bg
        return

    # ------------------------------------------------------------------

    def draw_art(self, side):
        offset = self.art_offset[side]
        top_old = self.h_ttl + offset
        bot_old = top_old + self.h_art_new
        temp = self[side][top_old:bot_old, :]
        # Handle full-width art so transparent borders look good.
        top_new = self.h_ttl
        bot_new = top_new + self.h_art_new
        self.flip[top_new:bot_new, :] = temp
        return

    # ------------------------------------------------------------------

    def draw_text(self, side):
        # Grab the chunk of text. Top and bottom are configurable.
        top_old = self.h_ttl + self.h_art + self.h_typ + self.txt_top[side]
        bot_old = top_old - self.txt_top[side] + self.txt_bot[side]
        # Figure out where it's going to go.
        pad = (self.h_txt_new[side] - bot_old + top_old)//2
        if pad < 0:
            raise ValueError("calculated negative padding for the textbox!")
        top_new = self.h_ttl + self.h_art_new + self.h_typ + pad
        bot_new = top_new + (bot_old - top_old)
        self.flip[top_new:bot_new, self.w_pad:-self.w_pad] = self[side][top_old:bot_old, self.w_pad:-self.w_pad]
        return

# ----------------------------------------------------------------------

class dfc_old(dfc_new):

    h_ttl = 37
    h_art = 136
    h_typ = 21
    h_txt = 83
    h_div = 7
    h_lip = 12
    h_pow = 22
    h_art_new = 41
    w_pad = 20
    w_pow = 60
    art_offset = {"a": 0, "b": 0}
    # Where are we trimming text from the old text box?
    txt_top = {"a": 0, "b": 0}
    txt_bot = {"a": 45, "b": 45}
    # What's the size of the new text box?
    h_txt_new = {"a": 43, "b": 43}
