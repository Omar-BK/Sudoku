import pygame
from solver import check, valid, find_empty
import time
pygame.font.init()

#GUI code from https://techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
class Grid:
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

  def __init__(self, rows, cols, width, height):
    self.rows = rows
    self.cols = cols
    self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
    self.width = width
    self.height = height
    self.model = None
    self.selected = None

  def update_model(self):
    self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

  def place(self, val):
    row, col = self.selected
    self.update_model()
    if self.cubes[row][col].value == 0:
      board2 = check(self.model)
      if valid(self.model, val, {"row": row, "column": col}) and board2[row][col] == val:
        self.cubes[row][col].set(val)
        self.update_model()
        return True
      else:
        self.cubes[row][col].set(0)
        self.cubes[row][col].set_temp(0)
        self.update_model()
        return False

  def sketch(self, val):
    row, col = self.selected
    self.cubes[row][col].set_temp(val)

  def draw(self, win):
    # Draw Grid Lines
    gap = self.width / 9
    for i in range(self.rows+1):
      if i % 3 == 0 and i != 0:
        thick = 4
      else:
        thick = 1
      pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
      pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

    # Draw Cubes
    for i in range(self.rows):
      for j in range(self.cols):
        self.cubes[i][j].draw(win)

  def select(self, row, col):
      # Reset all other
      for i in range(self.rows):
          for j in range(self.cols):
              self.cubes[i][j].selected = False

      self.cubes[row][col].selected = True
      self.selected = (row, col)

  def clear(self):
    row, col = self.selected
    if self.cubes[row][col].value == 0:
      self.cubes[row][col].set_temp(0)

  def click(self, pos):
    """
    :param: pos
    :return: (row, col)
    """
    if pos[0] < self.width and pos[1] < self.height:
      gap = self.width / 9
      x = pos[0] // gap
      y = pos[1] // gap
      return (int(y),int(x))
    else:
      return None

  def is_finished(self):
    for i in range(self.rows):
        for j in range(self.cols):
            if self.cubes[i][j].value == 0:
                return False
    return True


class Cube:
  rows = 9
  cols = 9

  def __init__(self, value, row, col, width ,height):
    self.value = value
    self.temp = 0
    self.row = row
    self.col = col
    self.width = width
    self.height = height
    self.selected = False
    self.done = False

  def draw(self, win):
    fnt = pygame.font.SysFont("comicsans", 40)

    gap = self.width / 9
    x = self.col * gap
    y = self.row * gap

    if self.temp != 0 and self.value == 0:
      text = fnt.render(str(self.temp), 1, (128,128,128))
      win.blit(text, (x+5, y+5))
    elif not(self.value == 0):
      text = fnt.render(str(self.value), 1, (0, 0, 0))
      win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

    if self.selected:
      pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    if self.done:
      pygame.draw.rect(win, (0,255,0), (x,y, gap ,gap), 3)
       
  def set(self, val):
    self.value = val

  def set_temp(self, val):
    self.temp = val


def redraw_window(win, board, time, strikes):
  win.fill((255,255,255))
  # Draw time
  fnt = pygame.font.SysFont("comicsans", 40)
  text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
  win.blit(text, (540 - 160, 560))
  # Draw Strikes
  text = fnt.render("X " * strikes, 1, (255, 0, 0))
  win.blit(text, (20, 560))
  # Draw grid and board
  board.draw(win)


def format_time(secs):
  sec = secs%60
  minute = secs//60
  hour = minute//60

  mat = " " + str(minute) + ":" + str(sec)
  return mat


def main():
  win = pygame.display.set_mode((540,600))
  pygame.display.set_caption("Sudoku")
  board = Grid(9, 9, 540, 540)
  key = None
  run = True
  start = time.time()
  strikes = 0
  while run:

    play_time = round(time.time() - start)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          key = 1
        if event.key == pygame.K_2:
          key = 2
        if event.key == pygame.K_3:
          key = 3
        if event.key == pygame.K_4:
          key = 4
        if event.key == pygame.K_5:
          key = 5
        if event.key == pygame.K_6:
          key = 6
        if event.key == pygame.K_7:
          key = 7
        if event.key == pygame.K_8:
          key = 8
        if event.key == pygame.K_9:
          key = 9
        if event.key == pygame.K_DELETE:
          board.clear()
          key = None
        if event.key == pygame.K_SPACE:
          board2 = []
          row = []
          for i in range(9):
            for j in range(9):
              row.append(board.cubes[i][j].value)
            board2.append(row)
            row = []
          origin = []
          value = []
          val = 0
          board3 = check(board2)
          while find_empty(board2) != -1:
            row = find_empty(board2)["row"]
            col = find_empty(board2)["column"]
            position = {"row": row, "column": col}
            origin.append(position)
            for i in range(val+1,10):
              if (valid(board2,i,position)):
                board2[row][col] = i
                value.append(i)
                board.cubes[row][col].done = True
                board.cubes[row][col].set(i)
                count = 0
                if board2[row][col] == board3[row][col]:
                  while count < 5:
                    board.cubes[row][col].selected = True
                    count += 1
                # board.cubes[row][col].selected = False
                val = 0
                break
            if (len(value) != len(origin)):
              row_prev = origin[len(origin)-2]["row"]
              col_prev = origin[len(origin)-2]["column"]
              board2[row_prev][col_prev] = 0
              board.cubes[row_prev][col_prev].set(0)
              # board.update_model()
              val = value[len(value)-1]
              value.pop()
              origin.pop()
              origin.pop()
        if event.key == pygame.K_RETURN:
          i, j = board.selected
          if board.cubes[i][j].temp != 0:
            if board.place(board.cubes[i][j].temp):
              print("Success")
            else:
              print("Wrong")
              strikes += 1
              if strikes == 3:
                print("You Lost")
                run = False
            key = None
            if board.is_finished():
              print("Game over")
              run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          clicked = board.click(pos)
          if clicked:
              board.select(clicked[0], clicked[1])
              key = None

    if board.selected and key != None:
        board.sketch(key)

    redraw_window(win, board, play_time, strikes)
    pygame.display.update()


main()
pygame.quit()