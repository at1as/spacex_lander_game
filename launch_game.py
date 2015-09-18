#!/usr/bin/python

import math
import os
import pygame
from pygame.locals import *
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITEISH = (215, 215, 215)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 80, 255)

# Styles
FPS = 10
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 400
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
LINETHICKNESS = 10


def draw_rocket(x, y, theta1=0, prior_rocket=None, theta2=None):
  global screen

  # Redraw full size rocket and scale it at every movement (or it becomes distorted)
  rocket = pygame.image.load('falcon9.png').convert_alpha()
  rocket = pygame.transform.scale(rocket, (24, 120))

  # Draw existing rocket at new angle, but cacluate width and height based on the angle diff
  if prior_rocket is None:
    width1, height1 = rocket.get_size()
    theta = theta1
  else:
    rocket = pygame.transform.rotate(rocket, theta2)
    width1, height1 = prior_rocket.get_size()
    theta = theta1 - theta2
  
  # Rotate rocket and get bounding rectange of rotated rectange
  rotated_rocket = pygame.transform.rotate(rocket, theta)
  width2, height2 = rotated_rocket.get_size()

  new_x = round(x + ((width1 - width2)/2))
  new_y = round(y + ((height1 - height2)/2))

  screen.blit(rotated_rocket,[new_x, new_y])

  if os.environ.get('DEBUG'):
    print "H: %s W: %s X: %s Y: %s OTHER: %s" %(height2, width2, new_x, new_y, rotated_rocket.get_bounding_rect())
  return rotated_rocket, {'height': height2, 'width': width2, 'x': new_x, 'y': new_y, 'theta': theta}


def draw_rocket_thrust(x, y):
  # TODO: Rotate thrust through rocket rotation angle
  global screen
  thrust = pygame.Rect(x, y, 10, -20)
  pygame.draw.rect(screen, ORANGE, thrust)
  return thrust

def draw_barge():
  global screen
  barge = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20, 40, 5)
  pygame.draw.rect(screen, BLACK, barge)
  return barge

def draw_water():
  global screen
  water = pygame.Rect(0, WINDOW_HEIGHT - 15, WINDOW_WIDTH, 15)
  pygame.draw.rect(screen, BLUE, water)
  return water

def draw_fuel_reading(reading):
  global screen
  if reading > 0:
    screen.blit(font.render('Fuel: %s' %(reading), 1, BLACK), (20, 20))
  else:
    screen.blit(font.render('Fuel: %s' %(reading), 1, RED), (20, 20))

def wait_for(key_pressed):
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
      if event.type == KEYDOWN and event.key == K_SPACE:
        return


if __name__ == "__main__":

  pygame.init()
  screen = pygame.display.set_mode(SIZE)
  pygame.display.set_caption("SpaceX Rocket Landing")
  
  pygame.key.set_repeat
  clock = pygame.time.Clock()
  font = pygame.font.SysFont('Arial', 40)
  small_font = pygame.font.SysFont('Arial', 18)
  
  # Intialize game variables
  fuel = 1000
  done = False
  throttle = 0
  x_point, y_point, theta = WINDOW_WIDTH/2 - 100, 0, 10

  # Initialize game environment
  rocket, rocket_pos = draw_rocket(x_point, y_point, theta)
  barge = draw_barge()
  water = draw_water()
  

  while not done:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
  
    # Redraw Screen
    screen.fill(LIGHT_BLUE)
    pressed = pygame.key.get_pressed()

    
    # No Throttle
    if (not pressed[pygame.K_w] and not pressed[pygame.K_UP]) or fuel == 0:

      # throttle should smoothly tend towards 10 (ie., fall by 10)
      # x, y distance traveled should be the throttle components based on throttle
      throttle = min(10, throttle + 2)
      ##x_point -= throttle * math.sin(math.radians(theta))
      y_point += throttle * math.cos(math.radians(theta))

      # Steer Left
      if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        x_point += throttle * math.sin(math.radians(theta))
        theta = min(40, theta + 2)
        #theta = max(-40, theta - 2)
      # Steer Right
      elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        x_point += throttle * math.sin(math.radians(theta))
        theta = max(-40, theta - 2)
        #theta = min(40, theta + 2)

      # Angle should continue at previous angle
      else:
        x_point += throttle * math.sin(math.radians(theta))

      # Draw new rocket based on these parameters, and update new x and y after rotation and drift
      rocket, rocket_pos = draw_rocket(x_point, y_point, theta, rocket, theta)
      x_point = rocket_pos['x']
      y_point = rocket_pos['y']
    
    # Throttle Applied
    else:

      # throttle should smoothly tend towards -2 (i.e., rise by 2)
      throttle = max(-2, throttle -0.5)
      x_point += throttle * math.sin(math.radians(theta))
      y_point += throttle * math.cos(math.radians(theta))
      fuel = max(0, fuel - 10)

      # Left biased throttle
      if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        theta_new = min(40, theta + 2)
        rocket, rocket_pos = draw_rocket(x_point, y_point, theta_new, rocket, theta)
        x_point = rocket_pos['x']
        y_point = rocket_pos['y']
        theta = theta_new
        
      # Right biased throttle
      elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        theta_new = max(-40, theta - 2)
        rocket, rocket_pos = draw_rocket(x_point, y_point, theta_new, rocket, theta)
        x_point = rocket_pos['x']
        y_point = rocket_pos['y']
        theta = theta_new
      
      # Throttle applied at previously angle  
      else:
        rocket, rocket_pos = draw_rocket(x_point, y_point, theta, rocket, theta)
        x_point = rocket_pos['x']
        y_point = rocket_pos['y']
        
      thrust = draw_rocket_thrust(rocket_pos['x'] + rocket_pos['width']/2, rocket_pos['y'] + rocket_pos['height'])


    # Barge sways from left to right with wind semi-randomly over small interval
    barge_dir = random.randint(0, 1)
    barge = draw_barge()
    
    if barge_dir == 0 and barge.left > (WINDOW_WIDTH/2) - 100:
      barge = barge.move(10, 0)

    elif barge_dir == 1 and barge.right < (WINDOW_WIDTH/2) + 100:
      barge = barge.move(-10, 0)


    # Draw water and barge with current positions and fuel level
    draw_fuel_reading(fuel)
    water = draw_water()
    pygame.draw.rect(screen, BLACK, barge)
    pygame.display.flip()


    # Check if rocket has collided with barge or water
    if barge.collidepoint(rocket_pos['x'] + rocket_pos['width']/2, rocket_pos['y'] + rocket_pos['height']):
      
      # Rocket is descending slowly, and within the landing angle of tolerance [-10, 10]
      if throttle < 5 and theta <= 10 and theta >= -10:
        screen.blit(small_font.render('Successful Landing!', 1, WHITE), (100, WINDOW_WIDTH/2))
        print "Success!"
      else:
        screen.blit(small_font.render('Rocket came down too fast', 1, WHITE), (90, WINDOW_WIDTH/2))
        print "Too Fast!"
      done = True

    elif water.collidepoint(rocket_pos['x'], rocket_pos['y'] + rocket_pos['height']):
      screen.blit(small_font.render('Rocket missed the barge', 1, WHITE), (100, WINDOW_WIDTH/2))
      print "Rocket missed the barge!"
      done = True

    elif y_point > WINDOW_HEIGHT:
      screen.blit(small_font.render('Rocket missed the barge', 1, WHITE), (60, WINDOW_WIDTH/2))
      done = True

    clock.tick(FPS)
  
    pygame.display.flip()


  # Wait for user keypress to quit...
  screen.blit(small_font.render('Press SPACE to Quit', 1, BLACK), (90, 120))
  pygame.display.flip()
  wait_for('blah')
  
  pygame.quit()
