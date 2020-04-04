#!/usr/bin/env python3

import json
import os
from PIL import Image
import requests
import time

import numpy as np

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def main():
    cardname = "Kessig Prowler"
    images = list(get_card_images(cardname))


IMAGE_DIR = "card-images/"


def get_card_images(cardname):
    card_data = get_card(cardname)
    slug = get_slug(cardname)
    if "image_uris" in card_data:
        filename = f"{IMAGE_DIR}/{slug}.png"
        url = card_data["image_uris"]["png"]
        download_image(url, filename)
        yield load_image(filename)
    else:
        for i, face in enumerate(card_data["card_faces"]):
            filename = f"{IMAGE_DIR}/{slug}-{i}.png"
            url = face["image_uris"]["png"]
            download_image(url, filename)
            yield load_image(filename)


def load_image(filename):
    return mpimg.imread(filename)[:, :, :3]


def download_image(url, filename):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    if os.path.exists(filename):
        print("already have:", filename)
        return
    print("saving:", filename)
    with open(filename, 'wb') as handle:
        handle.write(get_url(url).content)


def get_slug(cardname):
    tmp = cardname.lower()
    for c in "',":
        tmp = tmp.replace(c, "")
    for c in " ":
        tmp = tmp.replace(c, "-")
    return tmp


def get_card(cardname):
    return get_url(
        "https://api.scryfall.com/cards/search?",
        q=f"!'{cardname}'",
    ).json()["data"][0]


def get_url(url, **kwargs):
    time.sleep(0.2)
    return requests.get(
        url=url,
        params=kwargs,
    )


if __name__ == '__main__':
    main()
