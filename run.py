#! /usr/bin/python

"""run.py: entry of the game!"""

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

from load import LoadInput
from superWSP import SuperWordSearchPuzzle

if __name__ == '__main__':
  input_obj = LoadInput('input.txt')
  grid, is_wrap, swords = input_obj.getData()
  search_obj = SuperWordSearchPuzzle(grid, swords, is_wrap)
  search_obj.find_paths()
