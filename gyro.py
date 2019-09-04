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
    self.buffer = [NOTHING if pixel < self.width * self.height /2 else NOTHING for pixel in range(self.width * self.height)]
    self.buffer_original = list(self.buffer)
    self.score = 0
    self.button_presses = {}
    
  def colour_pixel(self, x, y, colour):
    try:
       self.buffer[ y * self.width + x ] = colour
    except:
       pass
    
  def draw_frame(self):
    self.s.set_pixels(self.buffer)
    
  def reset_buffer(self):
    self.buffer = list(self.buffer_original)
    
  def get_button_presses(self):
    button_presses_now = {event.direction : event.action for event in self.s.stick.get_events()}
    self.button_presses.update(button_presses_now)



class Sprite(object):
  def __init__(self,screen, position=[0,4], height=1, width=1, colour=YELLOW):
    self.screen = screen
    self.position = list(position)
    self.colour = colour
    self.height = height
    self.width =  width
    
  def draw_sprite(self, custom_size=None, custom_position=None):
    if custom_size is not None:
       width,height = custom_size
    else:
       width,height = self.width, self.height
    
    if custom_position is not None:
       position = custom_position
    else:
       position = self.position
    for i in range(width):
       for j in range(height):
          x = position[0] + i
          y = position[1] + j
          self.screen.colour_pixel(x, y, self.colour)
    print('drew {}, {}'.format(self.position, self.colour))
          
  def update(self):
    pass


class Ball(Sprite):
  def update(self):
    acceleration = self.screen.s.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)
    self.position[0] += int(x)
    self.position[1] += int(y)
    overflow_array = [self.width, self.height]
    for pos, value in enumerate(self.position):
        max_value = 8 - overflow_array[pos]
        if self.position[pos] > max_value:
            self.position[pos] = max_value
        if self.position[pos] < 0:
            self.position[pos] = 0

    print("x={0}, y={1}, z={2}".format(x, y, z))
    print("x={0}, y={1}, z={2}".format( self.position[0],  self.position[1], z))
  


def main():
   the_screen = Screen()
   ball = Ball(the_screen, width=2, height=2,position=[4,4])
   sprites = [ ball ]
   speed = 0
   game = True
   while game: 
       for sprite in sprites:
         sprite.update()
         sprite.draw_sprite()
       the_screen.draw_frame()
       the_screen.reset_buffer()
       time.sleep(speed)



if __name__ == "__main__":
  main()
