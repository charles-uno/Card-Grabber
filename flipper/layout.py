
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

        text_skew = kwargs.get("text_skew", 0)*(-1)**i

        flank_width = 65
        flank_height_old = 310
        flank_height_new = 135 + text_skew

        flank_bot_old = type_bot_old + flank_height_old
        flank_top_old = flank_bot_old - flank_height_new

        flank_top_new = type_bot_new
        flank_bot_new = flank_top_new + flank_height_new

        foot_height = 15
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

        if text_height > text_height_max:
            print("WARNING: text height max is", text_height_max)

        text_offset_new = (text_height_max - text_height)//2

        text_top_new = type_bot_new + text_offset_new
        text_bot_new = text_top_new + text_height

        text_top_old = type_bot_old + text_offset_old
        text_bot_old = text_top_old + text_height

        print("text goes from", type_bot_old, "to", foot_top_old, ":", foot_top_old - type_bot_old)


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
