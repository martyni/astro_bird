from sense_hat import SenseHat
from random import choice
from math import pow
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
    self.buffer = [YELLOW if pixel < self.width * self.height /2 else YELLOW for pixel in range(self.width * self.height)]
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
  def __init__(self,screen, position=[0,4], height=1, width=1, colour=BLUE):
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
          
  def update(self):
    pass


class Bird(Sprite):
  direction = 1
  
  # def get_direction(self)
  
  def update(self):
    if self.screen.button_presses.get("up") == "pressed" or self.screen.button_presses.get("up") == "held":
      self.direction = 1
      
    if self.screen.button_presses.get("down") == "pressed" or self.screen.button_presses.get("down") == "held":
      self.direction = -1
      
    self.position[1] += self.direction
    if self.position[1] < 0:
      self.position[1] = 0
    if self.position[1] > 7:
      self.position[1] = 7
  

class Cloud(Sprite):
   def update(self):
      overflow = self.width -1
      if self.position[0] >= 0 + overflow:
        self.position[0] -= 1
      else:
        self.position[0] = 7 - overflow
        self.position[1] = choice([_ for _ in range(4)])
        

class Pipe(Sprite):
  def update(self):
      overflow = self.width -1
      if self.position[0] >= 0 + overflow:
        self.position[0] -= 1
      else:
        self.position[0] = 7 - overflow
        new_height = choice([_ for _ in range(7)])
        self.height = new_height
        self.position[1] = 8 - new_height
      self.draw_sprite(custom_size=[1, 6 - self.height], custom_position=[self.position[0],0])  

# class Tommy(Sprite):
#   def update(self):
    

def check_if_lossed(bird, pipe):
   acceptable_height = [ pipe.position[1] - _ for _ in range(3)]
   if bird.position[1]  not in acceptable_height:
       print('lossed as bird is {} and acceptable heights are {}'.format(bird.position[1], acceptable_height))
       return True
   return False

def main():
   the_screen = Screen()
   bird = Bird(the_screen)
  # cloud = Cloud(the_screen, colour=WHITE, width=2, height=1, position=[2,1])
   pipe = Pipe(the_screen,  colour=RED,   width=1,  height=2, position=[7,6])
   sprites = [ pipe, bird ]
   speed = 0
   game = True
   while game: 
       the_screen.get_button_presses()
       for sprite in sprites:
         sprite.update()
         sprite.draw_sprite()
       the_screen.draw_frame()
       if pipe.position[0] == bird.position[0]:
           if check_if_lossed(bird,pipe):
               the_screen.s.show_message('{}'.format(the_screen.score))
               the_screen.score = 0
               speed = 0.2
               bird.position[1] = 4
           else:
               the_screen.score += 1
               if speed > 0.01:
                 speed -= 0.01
       the_screen.reset_buffer()
       time.sleep(speed)



if __name__ == "__main__":
  main()