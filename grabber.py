#!/usr/bin/env python

# Charles McEachern

# Spring 2016

# This document wraps at line 72. 

# #####################################################################
# ############################################################ Synopsis
# #####################################################################

# This script presents random card data and images. If the necessary
# files aren't present locally, it scrapes them from the internet. 

# #####################################################################
# ############################################# Import Python Libraries
# #####################################################################

# For conveniently parsing HTML. 
from bs4 import BeautifulSoup
# We use Matplotlib's image library to display images. 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# For navigating between directories. 
import os
# For choosing randomly from a list. 
from random import choice
# For grabbing HTML and images from online. 
from urllib2 import urlopen

# #####################################################################
# ################################################################ Main
# #####################################################################

def main():

  print 'LOADING SET LISTING'
  sets = getSets()
  abbr, title = choice(sets)

  print 'LOADING CARD LISTING FOR ' + title
  cards = getCards(abbr)
  num, name = choice(cards)

  print 'LOADING CARD DATA FOR ' + name

  getData(abbr, num)

  return

  print 'SHOWING CARD IMAGE FOR ' + name

  getImage(abbr, num)
  showImage(abbr, num)


#  print num, name



  return



# #####################################################################
# #################################################### Get Set Listings
# #####################################################################

# Get a dictionary of set titles, keyed by their abbreviations (which
# are also used in URLs). 
def getSets():
  # Let's try to keep the output organized. 
  if 'output' not in os.listdir('.'):
    print '\tCreating directory: output'
    os.mkdir('output')
  # If we already have a record of the sets, read it. 
  if 'sets.txt' in os.listdir('output'):
    print '\tReading output/sets.txt '
    return readTuples('output/sets.txt')
  # Otherwise, scrape this data from mtg.wtf and store it. 
  else:
    print '\tScraping set information from mtg.wtf '
    sets = []
    # We grab the set listing page from mtg.wtf, which lists set
    # titles and abbreviations in an unordered list. 
    setList = getSoup('http://mtg.wtf/set').find('ul')
    # Each list item is a set. 
    for setItem in setList.find_all('li'):
      # Watch out for em dashes. 
      setText = setItem.get_text().strip().replace(u'\u2014', '--')
      # Some set titles have parentheses in them, awkwardly. To get
      # the abbreviation, we split on the last one. 
      lastParen = setText.rfind('(')
      setTitle = setText[:lastParen].strip()
      setAbbr = setText[lastParen+1:-1].strip()
      # Keep track of this information in a list of tuples. 
      sets.append( (setAbbr, setTitle) )
    print '\tCreating output/sets.txt'
    return writeTuples(sets, 'output/sets.txt')

# #####################################################################
# ################################## Get Card Listings for a Single Set
# #####################################################################

def getCards(abbr):
  # Give each set its own subdirectory. 
  if abbr not in os.listdir('output'):
    print '\tCreating subdirectory: output/' + abbr
    os.mkdir('output/' + abbr)
  # If this data already exists, grab it. 
  if 'cards.txt' in os.listdir('output/' + abbr):
    print '\tReading output/' + abbr + '/cards.txt '
    return readTuples('output/' + abbr + '/cards.txt')
  # Otherwise, parse it from mtg.wtf. 
  else:
    print '\tScraping ' + abbr + ' card information from mtg.wtf '
    cards = []
    # Awkwardly, this site breaks up their set into pages of 25. We
    # keep grabbing pages until we find an empty one (or get to page 
    # 100, which means something is wrong). 
    for page in range(1, 100):
      URL = 'http://mtg.wtf/set/' + abbr + '?page=' + str(page)
      # The cards are all in the first table on the page. 
      cardTable = getSoup(URL).find('table')
      # If no table exists, we have run out of pages. 
      if cardTable is None:
        break
      # Otherwise, grab the cards. 
      else:
        print '\t\tPage ' + str(page)
        # Split the table into rows, then grab the first link in each
        # row. The link text is the card name, and its destination
        # gives the collector number. Note that split cards, etc, are
        # numbered a and b. 
        for tr in cardTable.find_all('tr')[:3]:
          link = tr.find('a')
          cardNum = link.get('href').split('/')[-1]
          cardName = link.get_text().strip()
          # Keep track of this information in a list of tuples. 
          cards.append( (cardNum, cardName) )
    print '\tCreating output/' + abbr + '/cards.txt'
    return writeTuples(cards, 'output/' + abbr + '/cards.txt')

# #####################################################################
# ########################################## Get Data for a Single Card
# #####################################################################

def getData(abbr, num):

  soup = getSoup('http://www.mtg.wtf/card/' + abbr + '/' + num)

  dataTable = soup.find('table')

  print dataTable.prettify()[:300]

  print dataTable.find( **{'class':'card_title'} ).prettify()


  return



# #####################################################################
# ######################################### Get Image for a Single Card
# #####################################################################

def getImage(abbr, num):
  # Give each set its own subdirectory. 
  if abbr not in os.listdir('output'):
    print '\tCreating subdirectory: output/' + abbr
    os.mkdir('output/' + abbr)
  # If we already have this image, where do we keep it? 
  path = cardImagePath(abbr, num)
  # If we already have this card image, we're done. 
  if os.path.exists(path):
    print '\tReading ' + path
  # Otherwise, download it from mtg.wtf. 
  else:
    # Where is this image? 
    URL = cardImageURL(abbr, num)
    print '\tScraping ' + URL
    # Grab the image data from online, and dump it into a file. The
    # 'wb' option means we're writing binary, not text. 
    img = urlopen(URL).read()
    with open(path, 'wb') as imgfile:
      imgfile.write(img)
    print '\tCreating ' + path
  return

# #####################################################################
# ################################################### Show a Card Image
# #####################################################################

def showImage(abbr, num):
  # Where is this image? 
  path = cardImagePath(abbr, num)
  # Sanity check: does it exist? 
  if not os.path.exists(path):
    print '\tNo image found at ' + path
  # Show the image using Matplotlib. 
  else:
    # Set up the Matplotlib window. Proportion it like a card, and tell
    # the plot axes to go all the way to the edge. 
    plt.figure( figsize=(5, 7) )
    plt.subplots_adjust(bottom=0., left=0., right=1., top=1.)
    # Have matplotlib read in the image as a Numpy array of pixels. 
    img = mpimg.imread(path)
    # Turn those pixels into a plot. 
    plt.imshow(img)
    # Display the plot window. 
    plt.show()
  return

# #####################################################################
# #################################################### Helper Functions
# #####################################################################

# How are images organized locally? 
def cardImagePath(abbr, num):
  return 'output/' + abbr + '/' + str(num) + '.jpg'

# How are images organized online? 
def cardImageURL(abbr, num):
  # Oddly, images scraped from mtg.wtf don't seem to show up right.
  # Maybe they store them compressed or something? We use
  # magiccards.info instead, which uses a similar URL for card images.
  # This isn't ideal... it looks like Python can natively read in
  # PNGs, but JPG handling has more tenuous dependencies. 
#    URL = 'http://mtg.wtf/cards/' + abbr + '/' + num + '.png'
  return 'http://magiccards.info/scans/en/' + abbr + '/' + num + '.jpg'

# Given a URL, return a BeautifulSoup object. 
def getSoup(URL):
  return BeautifulSoup( urlopen(URL).read() )

# Read in two tab-delimited columns as a list of tuples.  
def readTuples(filename):
  with open(filename, 'r') as infile:
    return [ x.strip().split('\t') for x in infile.readlines() ]

# Write a list of tuples to file as tab-delimited columns. 
def writeTuples(tlist, filename):
  with open(filename, 'w') as outfile:
    [ outfile.write('\t'.join(x) + '\n') for x in tlist ]
  return tlist

# #####################################################################
# ################################################### For Importability
# #####################################################################

if __name__=='__main__':
  main()

