import time


#GUI code from https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
board = [
  [0, 2, 0, 5, 0, 1, 0, 9, 0],
  [8, 0, 0, 2, 0, 3, 0, 0, 6],
  [0, 3, 0, 0, 6, 0, 0, 7, 0],
  [0, 0, 1, 0, 0, 0, 6, 0, 0],
  [5, 4, 0, 0, 0, 0, 0, 1, 9],
  [0, 0, 2, 0, 0, 0, 7, 0, 0],
  [0, 9, 0, 0, 3, 0, 0, 8, 0],
  [2, 0, 0, 8, 0, 4, 0, 0, 7],
  [0, 1, 0, 9, 0, 7, 0, 6, 0]
]

# board2 = [
#   [0,0,0,2,6,0,7,0,1],
#   [6,8,0,0,7,0,0,9,0],
#   [1,9,0,0,0,4,5,0,0],
#   [8,2,0,1,0,0,0,4,0],
#   [0,0,4,6,0,2,9,0,0],
#   [0,5,0,0,0,3,0,2,8],
#   [0,0,9,3,0,0,0,7,4],
#   [0,4,0,0,5,0,0,3,6],
#   [7,0,3,0,1,8,0,0,0]
# ]

# board3 = [
#   [1,0,0,4,8,9,0,0,6],
#   [7,3,0,0,0,0,0,4,0],
#   [0,0,0,0,0,1,2,9,5],
#   [0,0,7,1,2,0,6,0,0],
#   [5,0,0,7,0,3,0,0,8],
#   [0,0,6,0,9,5,7,0,0],
#   [9,1,4,6,0,0,0,0,0],
#   [0,2,0,0,0,0,0,3,7],
#   [8,0,0,5,1,2,0,0,4]
# ]

def draw(board):
  for i in range(len(board)):
    if(i % 3 == 0 and i != 0):
      print("\n" + "- - - - - - - - - - - -" + "\n")
    for j in range(len(board)):
      if(j%3 == 0 and j != 0):
        print(" | " + str(board[i][j]) + " ",end = "")
      elif (j%8 == 0 and j != 0):
        print(str(board[i][j]) + "\n")
      else:
        print(str(board[i][j]) + " ", end = "")

def find_empty(board):
  for i in range(len(board)):
    for j in range(len(board)):
      if board[i][j] == 0:
        return {"row": i,"column": j}
  return -1      

def valid(board, number, position):
  # Position is a dictionary {"row", "column"}
  #####################################
  # Checking validity of number in row
  for i in board[position["row"]]:
    if i == number:
      return False
  #####################################
  # Checking validity of number in column
  for i in board:
    if i[position["column"]] == number:
      return False
  #####################################
  # Checking for validity of number in box
  if (position["row"]%3 == 0):
    if (position["column"]%3 == 0):
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"]+i][position["column"] + j]):
            return False
    elif (position["column"]%3 == 1):
      for i in range(1,3):
        for k in range(1,3):
          if (number == board[position["row"]+i][position["column"] + (-1)**k]):
            return False
    else:
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"]+i][position["column"] - j]):
            return False
  elif (position["row"]%3 == 1):
    if (position["column"]%3 == 0):
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"] + (-1)**i][position["column"]+j]):
            return False
    elif (position["column"]%3 == 1):
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"] + (-1)**i][position["column"] + (-1)**j]):
            return False
    else:
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"] + (-1)**i][position["column"] - j]):
            return False
  else:
    if(position["column"]%3 == 0):
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"] - i][position["column"] + j]):
            return False
    elif (position["column"]%3 == 1):
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"]-i][position["column"] + (-1)**j]):
            return False
    else:
      for i in range(1,3):
        for j in range(1,3):
          if (number == board[position["row"] - i ][position["column"] - j]):
            return False
  return True

def check(board):
  origin = []
  value = []
  val = 0
  board2 = []
  row = []
  for i in range(len(board)):
    for j in range(len(board)):
      row.append(board[i][j])
    board2.append(row)
    row = []
  while find_empty(board2) != -1:
    # draw(board2)
    row = find_empty(board2)["row"]
    col = find_empty(board2)["column"]
    position = {"row": row, "column": col}
    origin.append(position)
    for i in range(val+1,10):
      if (valid(board2,i,position)):
        board2[row][col] = i
        value.append(i)
        val = 0
        break
    if (len(value) != len(origin)):
        row_prev = origin[len(origin)-2]["row"]
        col_prev = origin[len(origin)-2]["column"]
        board2[row_prev][col_prev] = 0
        val = value[len(value)-1]
        value.pop()
        origin.pop()
        origin.pop()
  return board2


# print("Before solving:" + "\n" )
# draw(board)
# print("After solving: " + "\n")
# check(board)
