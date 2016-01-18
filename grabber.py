#!/usr/bin/env python

# Charles McEachern

# Spring 2016

# This document wraps at line 72. 

# #####################################################################
# ############################################################ Synopsis
# #####################################################################

# This routine does a little parsing on magiccards.info, grabs some
# card images, then shows them off. 

# #####################################################################
# ############################################### Import Python Modules
# #####################################################################

# For checking that websites exist, then grabbing data from them. 
from urllib2 import urlopen, HTTPError

# For parsing HTML pages. 
from bs4 import BeautifulSoup

# For converting images from jpg to png. 
import Image

# For displaying images. 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# For creating and navigating directories. 
import os

# For making random choices. 
from random import randrange

# #####################################################################
# ################################################################ Main
# #####################################################################

def main():

  # Grab set names and abbreviations from our local record. If no
  # local record exists (that is, if this is the first time the script
  # has run) then we instead grab this information from the
  # magiccards.info sitemap. 
  sets = getSets()

  # Once we have a list of sets, we go for a list of card images. 
  getCards('isd')

  return

# Gaea's Cradle: us, 321
# Nezumi Graverobber: chk, 129a
# Garruk Relentless: isd, 181a
# Evermind: sok, 37
# Pact of the Titan: fut, 103

#  imgdata = urlopen(imgpath).read()
#  with open('test.jpg', 'wb') as imgfile:
#    imgfile.write(imgdata)
#  Image.open('test.jpg').save('test.png')
#  img = mpimg.imread('test.png')
#  plt.imshow(img)
#  plt.show()

# #####################################################################
# ############################################################# Helpers
# #####################################################################

# Print something out in a nice column. Justify or trim to fit the
# desired width. 
def col(x, width=10):
  return str(x).ljust(width-1)[:width-1] + ' '

# Read in a file with two tab-delimited columns and return it as a
# dictionary. 
def readDict(filename):
  # Dictionary to be returned. 
  d = {}
  # Grab the file contents as a string of lines. 
  with open(filename, 'r') as dictfile:
    dictlines = dictfile.readlines()
  # Split each line into a key and a value. 
  for line in dictlines:
    key, val = [ x.strip() for x in line.split('\t') ]
    d[key] = val
  # Store those values in the dictionary, then return it. 
  return d

# Write a dictionary to a file with two tab-delimited columns. 
def writeDict(d, filename):
  with open(filename, 'w') as dictfile:
    for key, val in sorted( d.items() ):
      dictfile.write(key + '\t' + val + '\n')
  return

# #####################################################################
# ############################################### BeautifulSoup Helpers
# #####################################################################

# As we go, the sanity check is the prettify() method. Any
# BeautifulSoup object (page, table, list, link, whatever) can be
# displayed using:
# print whatever.prettify()
# This will add indentation and spacing to make the HTML legible, even
# if it's a jumbled mess on the website. Note that these expressions
# can be quite long, so it's often better to just look at the first
# chunk of the pretty expression, for example:
# print whatever.prettify()[:100]
# slices off the first 100 characters to print. 

# =====================================================================
# ========================================================== Soup Maker
# =====================================================================

# Given the URL of an HTML page, return a BeautifulSoup object. 
def getSoup(URL):
  return BeautifulSoup( urlopen(URL).read() )

# Safely try to grab the contents of a URL that may not exist. 
def getURL(URL):
  try:
    page = urlopen(URL)
    return page.read()
  except HTTPError, e:
    return False



# =====================================================================
# ==================================== Grab Set Names and Abbreviations
# =====================================================================

# We want a list of set titles and their corresponding abbreviations.
# If no local record of that data exists, we create a record from the
# site map on magiccards.info. Data will be returned as a dictionary with entries of the form {abbr:title}.
def getSets():
  # Move to the output folder, after creating it if necesary. 
  if 'output' not in os.listdir('.'):
    print 'Creating output directory'
    os.mkdir('output')
  print 'Moving to output directory'
  os.chdir('output')
  # If sets.txt exists, read it. 
  if 'sets.txt' in os.listdir('.'):
    print 'Reading sets.txt'
    sets = readDict('sets.txt')
  # If the file doesn't exist, parse the sitemap of magiccards.info
  # and dump it into the file. 
  else:
    print 'Parsing magiccards.info sitemap'
    # Grab a soup object of the sitemap HTML. 
    soup = getSoup('http://magiccards.info/sitemap.html')
    # The links to expansion pages are all in the second table. 
    table = soup.find_all('table')[1]
    # The table contains a list (ul, for unordered list, since the
    # bullets are not numbered) of blocks. Each block has a list of
    # sets. We scroll through the set lists to get a list of set names
    # and abbreviations. 
    sets = {}
    for block in table.find('ul').find_all('ul'):
      # Within a block, each list item (li) corresponds to a single
      # expansion. 
      for expansion in block.find_all('li'):
        # From there we can grab the set name (the text in the link to
        # that set's name) and its abbreviation (the small text next to
        # the link). 
        title = expansion.find('a').string
        abbr = expansion.find('small').string
        # Add this set to the dictionary. 
        sets[abbr] = title
    # Write the set names and abbreviations out to a text file so we
    # don't have to parse the website all over again next time. 
    print 'Creating sets.txt'
    writeDict(sets, 'sets.txt')
  # Return the dictionary of set titles and abbreviations. 
  return sets

# =====================================================================
# ====================================================== Grab Card Data
# =====================================================================








# Grab the card data. It comes from magiccards.info the first time,
# then we just look for our local copy. 
def getCards(abbr):
  # We have a directory for each set. 
  if abbr not in os.listdir('.'):
    print 'Creating ' + abbr + ' directory'
    os.mkdir(abbr)
  print 'Moving to ' + abbr + ' directory'
  os.chdir(abbr)

  for n in range(1, 500):

#    print 'card number: ', n

    start = 'http://magiccards.info/scans/en/' + abbr + '/' + str(n)

    URL = start + '.jpg'
    URLa = start + 'a.jpg'
    URLb = start + 'b.jpg'

    imgdata = getURL(URL)

    if imgdata:

      print 'found ', str(n) + '.jpg'

      with open(str(n) + '.jpg', 'wb') as imgfile:
        imgfile.write(imgdata)

    else:

#      print 'didn\'t find ', str(n) + '.jpg'
      imgdataa = getURL(URLa)
      imgdatab = getURL(URLb)

      if imgdataa and imgdatab:

        print 'found ' + str(n) + 'a and ' + str(n) + 'b'

        with open(str(n) + 'a.jpg', 'wb') as imgfile:
          imgfile.write(imgdataa)

        with open(str(n) + 'b.jpg', 'wb') as imgfile:
          imgfile.write(imgdatab)

      else:

        print 'found nothing'
        break




#    imgdata = urlopen(URL).read()
#    imgdata = getURL(URL)

#    with open(str(n) + '.jpg', 'wb') as imgfile:
#      imgfile.write(imgdata)

#  Image.open('test.jpg').save('test.png')
#  img = mpimg.imread('test.png')
#  plt.imshow(img)

  print 'Moving back to output directory'
  os.chdir('..')


  return







#  # If cards.txt exists, read it. 
#  if 'cards.txt' in os.listdir('.'):
#    print 'Reading cards.txt'
#    cards = readDict('cards.txt')
  # Otherwise, we need to scrape the card data ourselves. 
#  else:
#    for n in range(1, 11):
#      print 'trying to grab ', n
#      URL = ('http://magiccards.info/' + abbr + '/en/' + str(n) +
#             '.html')
#      page = getURL(URL)
#    return


















  # We set the URL of the card page based on the set abbreviation and
  # the card's collector number. 
  soup = getSoup('http://magiccards.info/' + abbr + '/en/' +
                 str(num) + '.html')
  # The data we care about -- card name, card text, etc -- is in the
  # fourth table on the page. 
  table = soup.find_all('table')[3]
  # The card name is in the first link. 
  print 'card name: ', table.find('a').string
  # Everything else we care about is in a paragraph tag. 
  paragraphs = table.find_all('p')
  # The first paragraph has the type line, power/toughness, loyalty,
  # mana cost, cmc, and color indicator all mashed up together. A
  # little bit of string parsing is necessary to disentangle that
  # information... which is left as an exercise to the reader. 






  print 'rules text: ', paragraphs[1]

  print 'number of paragraphs: ', len(paragraphs)

  for i, p in enumerate(paragraphs):
    # On its own, get_text cuts out line breaks. We want those to be
    # newlines instead... but never double newlines. 

    print 'Paragraph ', i

#    [ br.replace_with('\n') for br in p.find_all('br') ]
#    print p.get_text().replace('\n\n', '\n')
    print p.prettify()



  return {}



  # A few chunks of data are squished together, so we need to split them up. Specifically, the first paragraph contains the card's types, its size (if a creature or planeswalker), and its cost and CMC (


  # A few chunks of data are squished together, so we need to split
  # them up. 
  typeSize, costCmc = paragraphs[0].string.split(',')

  # Cost and converted mana cost. 
  cost, cmc = costCmc.replace('(', '').replace(')', '').split()

  print 'cost = ', cost
  print 'cmc = ', cmc

  # If we're looking at a creature or planeswalker, there last "word"
  # is its size. We isolate that by finding the last space. 
  if 'Planeswalker' in typeSize or 'Creature' in typeSize:
    lastSpace = typeSize.rfind(' ')
    types, size = typeSize[:lastSpace], typeSize[lastSpace+1:]
  else:
    types, size = typeSize, None

  print 'types = ', types
  print 'size = ', size

  print table.find_all('p')[1].prettify()
  print table.find_all('p')[1].get_text()

  print table.find_all('p')[2].prettify()


  return {'card name':'test'}


# =====================================================================
# ===================================================== Grab Card Image
# =====================================================================

# Card data and images on magiccards.info are indexed by set
# abbreviation and collector number. 

def imgURL(abbr, num):
  return ( 'http://magiccards.info/scans/en/' + abbr + '/' + str(num) +
           '.jpg' )



# #####################################################################
# ################################################## Matplotlib Helpers
# #####################################################################











# #####################################################################
# ################################################### For Importability
# #####################################################################

if __name__=='__main__':
  main()
