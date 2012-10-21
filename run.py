#! /usr/bin/python

"""run.py: entry of the game!"""

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
from load import LoadInput
from superWSP import SuperWordSearchPuzzle

if __name__ == '__main__':
  
  if len(sys.argv) != 2:
    print 'Illegal input!!'
    sys.exit()
  
  input_obj = LoadInput(sys.argv[1])
  grid, is_wrap, swords = input_obj.getData()
  search_obj = SuperWordSearchPuzzle(grid, swords, is_wrap)
  search_obj.find_paths()
