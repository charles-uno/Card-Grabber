
import matplotlib.pyplot as plt
import numpy as np
import sys

from . import scryfall


def flip(cardname, **kwargs):

    fig, axes = plt.subplots(1, 4, figsize=(12, 4))
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
    axes = axes.flatten()
    for ax in axes:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.axis("off")

    front, back = scryfall.get_card_images(cardname)

    combined = combine_sides(front, back, **kwargs)

    upside_down = combined[::-1, ::-1, :]

    axes[0].imshow(front)
    axes[1].imshow(back)
    axes[2].imshow(combined)
    axes[3].imshow(upside_down)
    plt.tight_layout()
    plt.show()





def combine_sides(*sides, **kwargs):

    assert sides[0].shape == sides[1].shape

    canvas = np.zeros(sides[0].shape)
    # Red background so we can see what we haven't done yet
#    canvas[:, :] = [1, 0, 0]
    border_sample = sides[0][10, 100:-100, :]
    border_color = np.mean(border_sample, axis=0)
    canvas[:, :] = border_color

    for i, side in enumerate(sides):

        title_top = 0
        title_bot = 118

        art_height_new = 175
        art_height_old = 460
        art_offset_default = (art_height_old - art_height_new)//2
        art_offset = kwargs.get(f"art_offset_{i}", art_offset_default)

        art_top_new = title_bot
        art_bot_new = art_top_new + art_height_new

        art_top_old = title_bot + art_offset
        art_bot_old = art_top_old + art_height_new

        type_height = 80

        type_top_new = art_bot_new
        type_bot_new = type_top_new + type_height

        type_top_old = title_bot + art_height_old
        type_bot_old = type_top_old + type_height

        flank_width = 65
        flank_height_old = 310
        flank_height_new = 130

        flank_bot_old = type_bot_old + flank_height_old
        flank_top_old = flank_bot_old - flank_height_new

        flank_top_new = type_bot_new
        flank_bot_new = flank_top_new + flank_height_new

        foot_height = 10
        foot_bot_new = flank_bot_new
        foot_top_new = foot_bot_new - foot_height

        foot_bot_old = flank_bot_old
        foot_top_old = foot_bot_old - foot_height

        box_hang = 20
        box_height = 65
        box_width = 170

        box_bot_new = foot_bot_new + box_hang
        box_top_new = box_bot_new - box_height

        box_bot_old = foot_bot_old + box_hang
        box_top_old = box_bot_old - box_height

        text_height_max = foot_top_new - type_bot_new
        text_offset_old = kwargs.get(f"text_offset_{i}", 0)
        text_height = kwargs.get(f"text_height_{i}", text_height_max)

        text_offset_new = (text_height_max - text_height)//2

        text_top_new = type_bot_new + text_offset_new
        text_bot_new = text_top_new + text_height

        text_top_old = type_bot_old + text_offset_old
        text_bot_old = text_top_old + text_height

        # Old is where it comes from on the old canvas. New is where it goes on
        # the new canvas.

        canvas[:title_bot, :] = side[:title_bot, :]

        canvas[art_top_new:art_bot_new, :] = side[art_top_old:art_bot_old, :]

        canvas[type_top_new:type_bot_new, :] = side[type_top_old:type_bot_old, :]

        canvas[flank_top_new:flank_bot_new, :flank_width] = side[flank_top_old:flank_bot_old, :flank_width]
        canvas[flank_top_new:flank_bot_new, -flank_width:] = side[flank_top_old:flank_bot_old, :flank_width][:, ::-1]

        background_sample = side[foot_top_old-1, flank_width:-flank_width]
        background_color = np.mean(background_sample, axis=0)
        canvas[type_bot_new:foot_top_new, flank_width:-flank_width] = background_color

        canvas[text_top_new:text_bot_new, flank_width:-flank_width] = side[text_top_old:text_bot_old, flank_width:-flank_width]
        canvas[foot_top_new:foot_bot_new, :] = side[foot_top_old:foot_bot_old, :]
        canvas[box_top_new:box_bot_new, -box_width:] = side[box_top_old:box_bot_old, -box_width:]

        canvas = canvas[::-1, ::-1]

    return canvas





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
