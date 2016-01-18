#!/usr/bin/env python

# Charles McEachern

# Spring 2016

# This document wraps at line 72. 

# #####################################################################
# ############################################################ Synopsis
# #####################################################################

# This routine grabs card data and images from magiccards.info, then
# displays the images. 

# #####################################################################
# ############################################### Import Python Modules
# #####################################################################

# For grabbing data from websites. 
from urllib2 import urlopen

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

  # Grab the set names and abbreviations from the sitemap of
  # magiccards.info. The site isn't perfect for this purpose, but (to
  # me at least) it seems a lot more convenient than Gatherer or
  # TCGPlayer. 
  sets = getSets()

  for abbr, name in sorted( sets.items() )[:10]:
    print abbr.ljust(4) + ' : ' + name

  # Let's just grab an abbreviation from the set dictionary and
  # grab the first card from that set. 

  abbrs = sorted( sets.keys() )

  abbr = abbrs[ randrange( 0, len(abbrs) ) ]

  abbr = 'm11'

  print 'abbr = ', abbr

  num = randrange(1, 100)

  num = 175

  print 'num = ', num

  for key, val in getCardData(abbr, num).items():
    print col(key) + col(val)








  return




  lists = tables[1].find_all('ul')

  print 'number of lists in the second table: ', len(lists)

  print 'first list'

#  print lists[0].prettify()

#  print tables[1].find('ul').prettify()

  setlist = tables[1].find('ul')

  blocks = setlist.find_all('ul')

  print 'first block: '

  print blocks[0].prettify()

  b = blocks[0]

  setname = b.find('a').string
  print 'set name = ', setname

  setabbr = b.find('small')

  print 'set abbr = ', setabbr


  return


  abbr = 'bfz/'

  lang = 'en/'

  indx = '1'

  pageurl = mcdi + abbr + lang + indx + '.html'

  page = urlopen(pageurl).read()

  soup = BeautifulSoup(page)

  paragraphs = soup.find_all('p')

  print 'number of paragraphs: ', len(paragraphs)

  for p in paragraphs:
    print p

  print '\ncard text\n'

  print soup.find( **{'class':'ctext'} )

  imgpath = mcdi + 'scans/' + lang + abbr + indx + '.jpg'

  print 'path to the image is: ', imgpath

  imgdata = urlopen(imgpath).read()

  with open('test.jpg', 'wb') as imgfile:
    imgfile.write(imgdata)

  Image.open('test.jpg').save('test.png')

  img = mpimg.imread('test.png')

  plt.imshow(img)

  plt.show()

# #####################################################################
# ############################################################# Helpers
# #####################################################################

# Print something out in a nice column. Justify or trim to fit the
# desired width. 
def col(x, width=10):
  return str(x).ljust(width-1)[:width-1] + ' '






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

# =====================================================================
# ==================================== Grab Set Names and Abbreviations
# =====================================================================

# Parse the sitemap on magiccards.info to get a dictionary of set
# names and their abbreviations. 
def getSets():
  # We'll return a dictionary with entries of the form {abbr:name}. 
  sets = {}
  # Start at the site map. It lists all of the sets, and also gives
  # their three-letter abbreviations. We grab the raw HTML, then run
  # it through BeautifulSoup to allow easy parsing. 
  soup = getSoup('http://magiccards.info/sitemap.html')
  # By looking at the page source, we see that the links to expansion
  # pages are in the second table on the sitemap page. 
  table = soup.find_all('table')[1]
  # The table contains a list (ul, for unordered list, since the
  # bullets are not numbered) of blocks. Each block has a list of
  # sets. We scroll through the set lists to get a list of set names
  # and abbreviations. 
  for block in table.find('ul').find_all('ul'):
    # Within a block, each list item (li) corresponds to a single
    # expansion. 
    for expansion in block.find_all('li'):
      # From there we can grab the set name (the text in the link to
      # that set's name) and its abbreviation (the small text next to
      # the link). 
      name = expansion.find('a').string
      abbr = expansion.find('small').string
      # Add this set to the dictionary. 
      sets[abbr] = name
  # Return the dictionary of set names and abbreviations. 
  return sets

# =====================================================================
# ====================================================== Grab Card Data
# =====================================================================

# The page for each card lists off the card's name, text, etc. 
def getCardData(abbr, num):
  # We set the URL of the card page based on the set abbreviation and
  # the card's collector number. 
  soup = getSoup('http://magiccards.info/' + abbr + '/en/' +
                 str(num) + '.html')
  # The data we care about -- card name, card text, etc -- is in the
  # fourth table on the page. 
  table = soup.find_all('table')[3]
  # The card name is in the first link. Everything else we care about
  # is in a paragraph. 
  print 'card name: ', table.find('a').string
  paragraphs = table.find_all('p')
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
