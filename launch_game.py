#!/usr/bin/python

import math
import os
import pygame
from pygame.locals import *
import random


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 178, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE_1 = (0, 0, 255)
BLUE_2 = (0, 30, 255)
BLUE_3 = (0, 50, 255)
BLUE_4 = (0, 90, 255)

# Styles
FPS = 10
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 400
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


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
    print "ROCKET H: %s W: %s X: %s Y: %s OTHER: %s" %(height2, width2, new_x, new_y, rotated_rocket.get_bounding_rect())
  return rotated_rocket, {'height': height2, 'width': width2, 'x': new_x, 'y': new_y, 'theta': theta}


def draw_rocket_thrust(x, y):
  # TODO: Rotate thrust through rocket rotation angle
  '''
  global screen
  thrust = pygame.Rect(x, y, 10, -20)
  pygame.draw.rect(screen, ORANGE, thrust)
  return thrust
  '''

def draw_barge(barge_offset=0):
  global screen
  barge = pygame.Rect(WINDOW_WIDTH / 2 + barge_offset, WINDOW_HEIGHT - 32, 40, 7)
  if os.environ.get('DEBUG'):
    print "BARGE L: %s R: %s" %(barge.left, barge.right)
  return barge

def draw_water():
  global screen
  shallow_water = pygame.Rect(0, WINDOW_HEIGHT - 35, WINDOW_WIDTH, 10)
  water = pygame.Rect(0, WINDOW_HEIGHT - 25, WINDOW_WIDTH, 25)
  deep_water = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
  pygame.draw.rect(screen, BLUE_2, water)
  pygame.draw.rect(screen, BLUE_3, shallow_water)
  pygame.draw.rect(screen, BLUE_1, deep_water)
  return water

def draw_metrics(fuel_reading, rocket_angle, x, y, throttle, wind):
  global screen
  if fuel_reading > 0:
    screen.blit(small_font.render('Fuel: %s' %(fuel_reading), 1, BLACK), (20, 20))
  else:
    screen.blit(small_font.render('Fuel: %s' %(fuel_reading), 1, RED), (20, 20))
  screen.blit(small_font.render('Angle: %s' %(rocket_angle), 1, BLACK), (20, 40))
  screen.blit(small_font.render('X: %s' %(x), 1, BLACK), (20, 60))
  screen.blit(small_font.render('Y: %s' %(y), 1, BLACK), (20, 80))
  screen.blit(small_font.render('Rate of Descent: %s' %(throttle), 1, BLACK), (20, 100))
  screen.blit(small_font.render('Wind: %s' %(wind), 1, BLACK), (20, 120))

def draw_arrow(direction, y, x=None):
  global screen
  if direction == 'right':
    if x is None:
      x = WINDOW_WIDTH - 50
    pygame.draw.polygon(screen, (0, 0, 0), ((x, y), (x, y + 20), (x + 20, y + 20), (x + 20, y + 30), (x + 30, y + 10), (x + 20, y - 10), (x + 20, y)))
  else:
    if x is None:
      x = 50
    pygame.draw.polygon(screen, (0, 0, 0), ((x, y), (x, y + 20), (x - 20, y + 20), (x - 20, y + 30), (x - 30, y + 10), (x - 20, y - 10), (x - 20, y)))

def quit():
  while True:
    try:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
        if event.type == KEYDOWN and event.key == K_q:
          pygame.quit()
    except:
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
  # Randomize position and angle on start, within a certain tolerance
  fuel = 1000
  done = False
  throttle = 0
  x_offset = random.randint(-200, 200)
  x_point, y_point = WINDOW_WIDTH/2 - x_offset, 0
  theta = random.randint(-20, 20)
  wind = random.randint(-2, 2)
  barge_offset = 0

  # Limits
  ANGLE_MAX = 55

  # Initialize game environment
  rocket, rocket_pos = draw_rocket(x_point, y_point, theta)
  barge = draw_barge()
  water = draw_water()
  

  while not done:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
  
    # Redraw Screen at every cycle
    screen.fill(BLUE_4)
    pressed = pygame.key.get_pressed()

    """
      Barge: sways from left to right with wind semi-randomly over small interval
    """
    #barge = draw_barge(barge_offset)
    barge_dir = random.randint(0, 1)
    
    if barge_dir == 0 and barge.left > (WINDOW_WIDTH/2) - 30:
      barge_offset -= 10
      #barge = barge.move(10, 0)
      barge = draw_barge(barge_offset)

    elif barge_dir == 1 and barge.right < (WINDOW_WIDTH/2) + 30:
      barge_offset += 10
      #barge = barge.move(-10, 0)
      barge = draw_barge(barge_offset)


    # Draw water and barge with current positions and fuel level
    water = draw_water()
    pygame.draw.rect(screen, BLACK, barge)
    

    """
      Rocket: Can steer left and right (on ascent and descent), which varies its angle between [45, -45]
    """
    # No Throttle
    if (not pressed[pygame.K_w] and not pressed[pygame.K_UP]) or fuel == 0:

      # throttle should smoothly tend towards 10 (ie., fall by 10)
      # x, y distance traveled should be the throttle components based on throttle
      throttle = min(10, throttle + 1.5)
      x_point += throttle * math.sin(math.radians(theta))
      x_point += wind
      y_point += throttle * math.cos(math.radians(theta))

      # Steer Left
      if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        theta_new = min(ANGLE_MAX, theta + 2)

      # Steer Right
      elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        theta_new = max(-ANGLE_MAX, theta - 2)

      # Angle should continue at previous angle
      else:
        theta_new = theta

      # Draw new rocket based on these parameters, and update new x and y after rotation and drift
      rocket, rocket_pos = draw_rocket(x_point, y_point, theta_new, rocket, theta)
      x_point = rocket_pos['x']
      y_point = rocket_pos['y']
      theta = theta_new
    
    # Throttle Applied
    else:

      # throttle should smoothly tend towards -4 (i.e., rise by 4*cos(angle))
      throttle = max(-4, throttle - 0.5)
      x_point += throttle * math.sin(math.radians(theta))
      x_point += wind
      y_point += throttle * math.cos(math.radians(theta))
      fuel = max(0, fuel - 10)

      # Left biased throttle
      if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        theta_new = min(ANGLE_MAX, theta + 2)
        rocket, rocket_pos = draw_rocket(x_point, y_point, theta_new, rocket, theta)
        x_point = rocket_pos['x']
        y_point = rocket_pos['y']
        theta = theta_new
        
      # Right biased throttle
      elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        theta_new = max(-ANGLE_MAX, theta - 2)
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


    # Update Metrics and screen
    if x_point > WINDOW_WIDTH:
      draw_arrow('right', y_point)
    elif x_point < 0:
      draw_arrow('left', y_point)

    draw_metrics(fuel, theta, x_point, y_point, throttle, wind)
    pygame.display.flip()


    """
      Collision Detection
    """
    # Check if rocket has collided with barge or water
    if barge.collidepoint(rocket_pos['x'] + rocket_pos['width']/2, rocket_pos['y'] + rocket_pos['height']):
      
      # Rocket is descending slowly, and within the landing angle of tolerance [-10, 10]
      if throttle < 5 and theta <= 10 and theta >= -10:
        screen.blit(small_font.render('Successful Landing!', 1, GREEN), (110, WINDOW_HEIGHT/2))
      elif throttle < 5:
        screen.blit(small_font.render('Rocket came down at bad angle!', 1, WHITE), (75, WINDOW_HEIGHT/2))
      else:
        screen.blit(small_font.render('Rocket came down too fast', 1, WHITE), (90, WINDOW_HEIGHT/2))
      done = True

    elif water.collidepoint(rocket_pos['x'], rocket_pos['y'] + rocket_pos['height']):
      screen.blit(small_font.render('Rocket missed the barge', 1, WHITE), (100, WINDOW_HEIGHT/2))
      done = True

    elif y_point > WINDOW_HEIGHT:
      screen.blit(small_font.render('Rocket missed the barge', 1, WHITE), (100, WINDOW_HEIGHT/2))
      done = True

    clock.tick(FPS)
    pygame.display.flip()


  # Wait for user keypress to quit...
  screen.blit(small_font.render('Press Q to Quit, Space to Continue', 1, WHITE), (60, 250))
  pygame.display.flip()
  quit()
