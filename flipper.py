#!/usr/bin/env python3

"""
Charles McEachern

Spring 2019

Finagle with the offsets to get some double-faced card to look like nice
flip cards.
"""

# ----------------------------------------------------------------------

import flip

# ----------------------------------------------------------------------

def main():

    # Reckless Waif
    flip.dfc("isd", 159, txt_a=(15, 50), txt_b=(15, 50), art_ab=(10, 10))





    return

    # Kessig Prowler
    flip.dfc("emn", 163, txt_a=(25, 40), txt_b=(15, 45), art_ab=(10, 10))

    # Timber Shredder
    flip.dfc("soi", 210, txt_a=(5, 39), txt_b=(0, 52), art_ab=(0, 5))

    # Delver of Secrets
    flip.dfc("isd", 51, txt_a=(14, 71), txt_b=(6, 20), art_ab=(10, 10))

    # Aberrant Researcher
    flip.dfc("soi", 49, txt_a=(0, 68), txt_b=(8, 22), art_ab=(10, 10))

    return






    # Villagers of Estwald
    card = dfc('isd', 209)
    card.add_art('a', 15)
    card.add_art('b', 35)
    card.add_text('a', 8)
    card.add_text('b', 11)
    card.save()

    # Solitary Hunter
    card = dfc('soi', 229)
    card.add_art('a', 15)
    card.add_art('b', 30)
    card.add_text('a', 8)
    card.add_text('b', 11)
    card.save()

    # Startled Awake
    card = dfc('soi', 88)
    card.add_art('a', 20)
    card.add_art('b', 10)
    card.add_text('a', 0)
    card.add_text('b', 0, careful=False)
    card.save()


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

#    # Breakneck Rider... five lines of text is just too much!
#    card = dfc('soi', 147)
#    card.add_art('a', 25)
#    card.add_art('b', 25)
#    card.add_text('a', 8)
#    card.add_text('b', 9)
#    card.show()

    return

# ----------------------------------------------------------------------

if __name__=='__main__':
  main()
