#! /usr/bin/python
# Filename: load.py

"""load.py: class LoadInput helps to load input data."""

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

import re

class LoadInput(Exception):
  
  def __init__(self, input_file):
    '''Initializes the LoadInput class.'''
    f = file(input_file, 'r')
    self.content = f.read()
    f.close()
        
  def getData(self):
    '''Load input to memory.'''
    pattern = re.compile(r'''
      (?P<rows>\d+)            # number of rows
      [ ]                      # a space
      (?P<cols>\d+)            # number of cols
      \s
      (?P<grid>.*)             # every before NO_WRAP|WRAP
      \s
      (?P<mode>WRAP|NO_WRAP)   # mode between WRAP and NO_WRAP
      \s
      (?P<num_swords>\d+)  # number of pseudo-super words
      \s
      (?P<swords>.*)       # pseudo-super words
      \s
      ''', re.VERBOSE|re.DOTALL) 

    data_dict = re.search(pattern, self.content).groupdict()

    grid = data_dict['grid'].split('\n')
    swords = data_dict['swords'].split('\n')
    mode = data_dict['mode']
    if mode == 'WRAP':
      is_wrap = True
    else:
      is_wrap = False
    
    # rows = int(data_dict['rows'])
    # cols = int(data_dict['cols'])
    # num_swords = int(data_dict['num_swords'])
    # here rows|cols|num_swords can be get by using len(grid)|len(grid[0])|len(swords), so no need to return them
    return grid, is_wrap, swords

if __name__ == '__main__':  
  test_obj = LoadInput('test.txt')
  grid, is_wrap, swords = test_obj.getData()
  print len(grid) 
  print len(grid[0])
  print grid
  print is_wrap
  print len(swords)
  print swords  
  
