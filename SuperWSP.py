#! /usr/bin/python
# Filename: SuperWSP.py

from load import LoadInput

class SuperWordSearchPuzzle(Exception):
  
  def __init__(self, grid, swords, is_wrap):
    self.rows = len(grid)
    self.cols = len(grid[0])
    self.num_swords = len(swords)
    self.grid = grid
    self.swords = swords
    self.is_wrap = is_wrap
    
    # Generate ghost_grid
    part1 = [row[1:] for row in grid[1:]]
    part2 = grid[1:]
    part3 = [row[:-1] for row in grid[1:]]

    part4 = [row[1:] for row in grid]
    part5 = grid
    part6 = [row[:-1] for row in grid]

    part7 = [row[1:] for row in grid[:-1]]
    part8 = grid[:-1]
    part9 = [row[:-1] for row in grid[:-1]]  
    
    self.ghost_grid = [part1[i] + part2[i] + part3[i] for i in range(self.rows - 1)] + \
                      [part4[i] + part5[i] + part6[i] for i in range(self.rows)] + \
                      [part7[i] + part8[i] + part9[i] for i in range(self.rows - 1)] 
    
    ghost_rows = len(self.ghost_grid)
    ghost_cols = len(self.ghost_grid[0])
    
    # set is_ghost flag of ghost_grid
    self.ghost_grid_flag = [[True for j in range(ghost_cols)] for i in range(ghost_rows)]
    for i in range(ghost_rows):
      for j in range(ghost_cols):
        origin_i = i + 1 - self.rows
        origin_j = j + 1 - self.cols
        if origin_i >= 0 and origin_i <= self.rows - 1 and origin_j >= 0 and origin_j <= self.cols - 1:
          self.ghost_grid_flag[i][j] = False

    # Generate hash_map for every word in ghost_grid
    # Key: coord
    # Value: list of coord pairs in 8 directions
    self.hash_map = {}
    for i in range(ghost_rows):
      for j in range(ghost_cols):
        tmp = []
        if i - 1 >= 0 and j - 1 >= 0:
          tmp.append((i - 1, j - 1)) # left up point
          tmp.append((i - 1, j)) # top point
          if j + 1 <= ghost_cols - 1:
            tmp.append((i - 1, j + 1)) # right up point
        if j - 1 >= 0:
          tmp.append((i, j - 1)) # left point
        if j + 1 <= ghost_cols - 1:
          tmp.append((i, j + 1)) # right point
        if i + 1 <= ghost_rows - 1 and j - 1 >= 0: 
          tmp.append((i + 1, j - 1)) # left bottom point
          tmp.append((i + 1, j)) # bottom point
          if j + 1 <= ghost_cols - 1:
            tmp.append((i + 1, j + 1)) # bottom right point
        self.hash_map[(i,j)] = tmp 
     
  
  def mapping(self, ghost_grid_point):

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
    original_path = []
    for indx in path:
      temp = self.mapping(indx)
      original_path.append((temp[0] - self.rows + 1, temp[1] - self.cols + 1))
    return original_path

        
  def find_paths(self):
    return [self.find_path(word) for word in self.swords]


  def find_path(self, word):
    flag = False # use flag to sign if exists a start point
    for i in range(len(self.ghost_grid)):
      for j in range(len(self.ghost_grid[0])):
        if self.ghost_grid[i][j] == word[0] and self.ghost_grid_flag[i][j] == False: 
          starting_point = (i, j)
          path = self.search_word(starting_point, word)
          flag = True
          if not path:
            flag = False
            continue
          path_coord = self.restore_path(path)

          tmp_dict = {} 
          for key in path_coord:
            if key in tmp_dict.keys():
              flag = False
              break
            tmp_dict[key] = 1
          if flag == True:
            print path_coord[0], path_coord[-1]
            return path_coord
    if flag == False:
      print 'NOT FOUND'
      return None

      
  def search_word(self, start_point, word):
    path = [start_point]
    cross = False
    for w in word[1:]:
      flag = False
      queue = []
      for indx in self.hash_map[start_point]:
        if self.ghost_grid[indx[0]][indx[1]] == w and indx not in path:
          if self.ghost_grid_flag[indx[0]][indx[1]] == True:
            cross = True
          flag = True
          path.append(indx)
          start_point = indx
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
