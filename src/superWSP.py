#! /usr/bin/python

"""superWSP.py: SuperWordSearchPuzzle class for Super Word Search Puzzle Game."""

__author__ = ['Hong Wu<xunzhangthu@gmail.com>']

from load import LoadInput

class SuperWordSearchPuzzle(Exception):
  '''SuperWordSearchPuzzle class.'''  
  
  def __init__(self, grid, swords, is_wrap):
    '''Initialize the SuperWordSearch's data.'''
    self.rows = len(grid)
    self.cols = len(grid[0])
    self.num_swords = len(swords)
    
    self.grid = grid
    self.swords = swords
    self.is_wrap = is_wrap
    
    # generate the ghost_grid 
    self.ghost_grid = self.init_ghost_grid()
    
    self.ghost_rows = len(self.ghost_grid)
    self.ghost_cols = len(self.ghost_grid[0])
     
    # generate the hash_map 
    self.hash_map = self.init_hash_map()
    # generate the ghost_grid_flag
    self.ghost_grid_flag = self.init_ghost_grid_flag()
    

  def init_ghost_grid(self):
    '''Initializes the ghost_grid.'''
    part1 = [row[1:] for row in self.grid[1:]]
    part2 = self.grid[1:]
    part3 = [row[:-1] for row in self.grid[1:]]

    part4 = [row[1:] for row in self.grid]
    part5 = self.grid
    part6 = [row[:-1] for row in self.grid]

    part7 = [row[1:] for row in self.grid[:-1]]
    part8 = self.grid[:-1]
    part9 = [row[:-1] for row in self.grid[:-1]]  
    
    ghost_grid = [part1[i] + part2[i] + part3[i] for i in range(self.rows - 1)] + \
                 [part4[i] + part5[i] + part6[i] for i in range(self.rows)] + \
                 [part7[i] + part8[i] + part9[i] for i in range(self.rows - 1)] 
  
    return ghost_grid
       
  
  def init_ghost_grid_flag(self):
    '''set is_ghost flag of ghost_grid, to distinguish grid from ghost_grid'''
    ghost_grid_flag = [[True for j in range(self.ghost_cols)] for i in range(self.ghost_rows)]
    for i in range(self.ghost_rows):
      for j in range(self.ghost_cols):
        origin_i = i + 1 - self.rows
        origin_j = j + 1 - self.cols
        if origin_i + 1 and self.rows - origin_i and origin_j + 1 and self.cols - origin_j:
          ghost_grid_flag[i][j] = False
    return ghost_grid_flag 
  
   
  def init_hash_map(self):
    '''Initialize hash_map for every word in ghost_grid: (Key, Value) <=> (coord, list of coord pairs in at most 8 directions)'''
    hash_map = {}
    for i in range(self.ghost_rows):
      for j in range(self.ghost_cols):
        tmp = []
        if i and j:
          tmp.append((i - 1, j - 1)) # left up point
          tmp.append((i - 1, j)) # top point
          if self.ghost_cols - j - 1:
            tmp.append((i - 1, j + 1)) # right up point
        if j:
          tmp.append((i, j - 1)) # left point
        if self.ghost_cols - j - 1:
          tmp.append((i, j + 1)) # right point
        if self.ghost_rows - i - 1 and j: 
          tmp.append((i + 1, j - 1)) # left bottom point
          tmp.append((i + 1, j)) # bottom point
          if self.ghost_cols - j - 1:
            tmp.append((i + 1, j + 1)) # bottom right point
        hash_map[(i,j)] = tmp 
    return hash_map
  
  
  def mapping(self, ghost_grid_point):
    '''
    Mapping relation between ghost_grid and grid. 
    Input a coord index and return a coord in original word grid.
    This function helps to save the space.
    '''
    i = ghost_grid_point[0]
    j = ghost_grid_point[1]
    
    if i >= 0 and i <= self.rows - 2:
      if j >= 0 and j <= self.cols - 2: # part1
        return (i + self.rows, j + self.cols)
      if j >= self.cols - 1 and j <= 2 * self.cols - 2: # part2
        return (i + self.rows, j)
      if j >= 2 * self.cols - 1 and j <= 3 * self.cols - 3: # part3
        return (i + self.rows, j - self.cols)
    
    if i >= self.rows - 1 and i <= 2 * self.rows - 2:
      if j >= 0 and j <= self.cols - 2: # part4
        return (i, j + self.cols)
      if j >= self.cols - 1 and j <= 2 * self.cols - 2: # part5
        return (i, j)
      if j >= 2 * self.cols - 1 and j <= 3 * self.cols - 3: # part6
        return (i, j - self.cols)
    
    if i >= 2 * self.rows - 1 and i <= 3 * self.rows - 3: 
      if j >= 0 and j <= self.cols - 2: # part7
        return (i - self.rows, j + self.cols)
      if j >= self.cols - 1 and j <= 2 * self.cols - 2: # part8
        return (i - self.rows, j)
      if j >= 2 * self.cols - 1 and j <= 3 * self.cols - 3: # part9
        return (i - self.rows, j - self.cols)
 
  
  def restore_path(self, path):  
    '''
    Restore the path in original grid using mapping function.
    Input a path in ghost_grid and return a path in original grid.
    '''
    original_path = []
    for indx in path:
      temp = self.mapping(indx)
      original_path.append((temp[0] - self.rows + 1, temp[1] - self.cols + 1))
    return original_path

        
  def find_paths(self):
    '''Find paths of input pesudo super words.'''
    return [self.find_path(word) for word in self.swords]


  def find_path(self, word):
    '''Find the path of a word in original grid.'''
    flag = False # use var flag to sign if exists a start point
     
    # for-loops for every same starting_point in ghost_grid
    # flag to make sure point in original grid.
    for i in range(self.ghost_rows):
      for j in range(self.ghost_cols):
        if self.ghost_grid[i][j] == word[0] and self.ghost_grid_flag[i][j] == False: # find starting point in original grid(flag of them are False)
          starting_point = (i, j)
          path = self.search_word(starting_point, word) # Submodule of find_path
          if path: # if there exists a path, set flag True, link the path with starting_point, the path will be checked below
            path = [starting_point] + path
            flag = True
          else:
            continue
          # path checking
          # restore the path in original grid
          path_coord = self.restore_path(path)
          tmp_dict = {} 
          # tmp_dict make sure that each point in the original grid must be used only once
          for key in path_coord:
            if key in tmp_dict.keys():
              flag = False
              break
            tmp_dict[key] = 1
          # pass the checking and print the start and end point here
          if flag == True:
            print path_coord[0], path_coord[-1]
            return path_coord
       
    # search failed and print 'NOT FOUND'
    if flag == False:
      print 'NOT FOUND'
      return None
   
  
  def search_word(self, start_point, word):
    '''Submodule of find_path.'''
    path = []
    # var cross to sign if go through a ghost point which means wrap
    cross = False
    flag = False
    for indx in self.hash_map[start_point]:
      if self.ghost_grid[indx[0]][indx[1]] == word[1] and indx not in path:
        if self.ghost_grid_flag[indx[0]][indx[1]] == True:
          cross = True
        # boundary condition of recursively the function
        if len(word) == 2:
          if not (self.is_wrap == False and cross == True):
            return [indx]
          else:
            break
        flag = True
        path.append(indx)
        # call search_word recursively
        # stack may not overflow because the depth is really small in this function
        # believe me
        path_after = self.search_word(indx, word[1:])
        if not path_after:
          flag = False
          cross = False
          path.pop()
          continue
        path += path_after
        break
    
    if flag == False:
      return None
    if self.is_wrap == False and cross == True: 
      return None
    
    return path    
    
    
if __name__ == '__main__':
  r = LoadInput('test.txt')
  grid, is_wrap, swords = r.getData()
  a = SuperWordSearchPuzzle(grid, swords, is_wrap)
  a.find_paths()
  # write more test code here!!
