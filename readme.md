
# Transform to Flip Card

The driver `flipper.py` takes Innistrad-style double-faced cards, chops them up, and reassembles them into Kamigawa-style flip cards. This is nice if, for example, you want to put the cards in a cube and have both sides visible at once.

The slicing and dicing takes place in `flip.py`. Image access (including downloading images on the fly from `mtg.wtf`) is handled in `images.py`.

Prerequisites are wrapped up in the `Dockerfile`. To run the script in the container, use:

```
make flip
```

Note the `--debug` flag (which causes the image to pop up in a Matplotlib window) is not respected from within the container. It only saves images.

# Also

`grabber.py` shows information and images for randomly-chosen Magic cards. If something isn't present locally, it's scraped from online.
