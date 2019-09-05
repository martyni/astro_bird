from sense_hat import SenseHat
from random import choice
import time

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255,255,255)
NOTHING = (0,0,0)
PINK = (255,105, 180)

class Screen(object):
  def __init__(self, width=8, height=8):
    self.s = SenseHat()
    self.s.low_light = True
    self.width = width
    self.height = height

    START_GRID = [
      # When the program is running, we only use the values True and False
      # We only write 0 and 1 here because they look shorter in code and
      # are the same length as each other
      0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 0, 0, 0, 1, 0,
      0, 0, 0, 0, 0, 0, 0, 0,
      0, 1, 1, 1, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0
    ]

    self.cells = map(lambda x: True if x == 1 else False, START_GRID)
    self.cells_new = list(self.cells)
    self.buffer = [WHITE if pixel else NOTHING for pixel in self.cells]
    self.buffer_original = list(self.buffer)
    self.button_presses = {}

  def count_neighbours(self, x, y):
    neighbours = 0
    start_x = max(0, x-1)
    end_x = min(7, x+1)

    start_y = max(0, y-1)
    end_y = min(7, y+1)
    print "boundary for cell {x},{y} is x:{sx}-{ex} and y:{sy}-{ey}".format(x=x,y=y,sx=start_x, ex=end_x,ey=end_y,sy=start_y)

    for i in range(start_x, end_x +1 ):
      for j in range(start_y, end_y + 1):
        if i == x and j == y:
            print "skipping a cell because we're on ourself"
            continue
        print "for cell {x},{y} I am checking {i},{j} - it is {val}".format(x=x,y=y,i=i,j=j, val=self.cells[i*8+j])
        neighbours += 1 if self.cells[i*8+j] else 0

    print "cell {X},{Y} has {neighbours} neighbours".format(X=x, Y=y, neighbours=neighbours)
    print "\n"
    return neighbours

  def calculate_next(self):
    for x in range(8):
      for y in range(8):
        n_count = self.count_neighbours(x,y)
        if n_count < 2:
          self.cells_new[x*8 + y] = False
        elif n_count < 4 and self.cells[x*8 + y]:
          self.cells_new[x*8 + y] = self.cells[x*8 + y]
        elif n_count == 3 and not self.cells[x*8 + y]:
          self.cells_new[x*8 + y] = True
        else:
          self.cells_new[x*8 +y] = False

  def draw_frame(self):
    for x in range(8):
      for y in range(8):
        self.buffer[x*8+y] = WHITE if self.cells_new[x*8 +y] else NOTHING

    self.s.set_pixels(self.buffer)
    for row in range(8):
        print map(lambda x: 1 if x else 0, self.cells_new[row*8:row*8+8])
    print

  def reset_buffer(self):
    self.buffer = list(self.buffer_original)
    self.cells = list(self.cells_new)

  def get_button_presses(self):
    button_presses_now = {event.direction : event.action for event in self.s.stick.get_events()}
    self.button_presses.update(button_presses_now)

  def update(self):
    self.calculate_next()
    self.draw_frame()
    self.reset_buffer()
    self.get_button_presses()
    return self.button_presses


def main():
   the_screen = Screen()
   speed = 0.2
   game = True
   while game:
      #if the_screen.button_presses.get('up') == 'pressed':
      the_screen.update()
      time.sleep(speed)


if __name__ == "__main__":
  main()


