#! /usr/bin/python

"""run.py: entry of the game!"""

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import sys
import src.packages as namespace
#from load import LoadInput
#from superWSP import SuperWordSearchPuzzle

if __name__ == '__main__':
  
  if len(sys.argv) != 2:
    print 'Illegal input, see README please!'
    sys.exit()
  
  input_obj = namespace.LoadInput(sys.argv[1])
  grid, is_wrap, swords = input_obj.getData()
  search_obj = namespace.SuperWordSearchPuzzle(grid, swords, is_wrap)
  search_obj.find_paths()
