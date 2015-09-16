#!/usr/bin/python

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
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 400
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
LINETHICKNESS = 10


def draw_rocket(x, y):
  global screen
  rocket = pygame.Rect(x, y, 10, 80)
  pygame.draw.rect(screen, WHITEISH, rocket)
  return rocket

def draw_rocket_thrust(x, y):
  global screen
  thrust = pygame.Rect(x, y, 10, 10)
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


if __name__ == "__main__":

  pygame.init()
  screen = pygame.display.set_mode(SIZE)
  pygame.display.set_caption("SpaceX Rocket Landing")
  
  pygame.key.set_repeat
  clock = pygame.time.Clock()
  
  # Intialize game
  done = False
  throttle = 0
  y_delta = 10
  rocket = draw_rocket(WINDOW_WIDTH/2, 0)
  barge = draw_barge()
  
  
  while not done:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
    
    # Redraw Screen
    screen.fill(LIGHT_BLUE)
    
    pressed = pygame.key.get_pressed()

    if not pressed[pygame.K_w]:
      throttle = 0
      y_delta = min(10, y_delta + 2)
      rocket = rocket.move(0, y_delta)
    else:
      y_delta = max(-1, y_delta - 1)
      rocket = rocket.move(0, y_delta)
      thrust = draw_rocket_thrust(rocket.left, rocket.bottom)

    if pressed[pygame.K_q]:
      r_new = pygame.transform.rotate(screen, 30)


    # Barge sways from left to right with wind
    barge_dir = random.randint(0, 1)
    barge = draw_barge()
    
    if barge_dir == 0 and barge.left > (WINDOW_WIDTH/2) - 100:
      barge = barge.move(10, 0)

    elif barge_dir == 1 and barge.right < (WINDOW_WIDTH/2) + 100:
      barge = barge.move(-10, 0)


    # Draw water and barge with current positions
    water = draw_water()
    pygame.draw.rect(screen, BLACK, barge)
    
    # Print rocket with lettering
    pygame.draw.rect(screen, WHITEISH, rocket)
    font = pygame.font.SysFont('Arial', 12)
    text = [font.render("S", 1, RED), 
            font.render("p", 1, RED), 
            font.render("a", 1, RED),
            font.render("c", 1, RED),
            font.render("e", 1, RED),
            font.render("X", 1, RED)]

    for idx, letter in enumerate(text):
      screen.blit(letter, (rocket.left, rocket.top + 10*idx))

    pygame.display.flip()
    
    if barge.colliderect(rocket):
      # Rocket is descending slowly, and within the barge bounds
      if y_delta < 5 and barge.left < rocket.left and barge.right > rocket.right:
        screen.blit(font.render('You Win', 1, WHITE), (40, WINDOW_WIDTH/2))
        pygame.font.Font(None, 36).render("YOU WIN", True, (10, 10, 10))
        pygame.display.flip()
      else:
        screen.blit(font.render('You Lose. Rocket came down too fast', 1, WHITE), (40, WINDOW_WIDTH/2))
      
      done = True

    elif water.colliderect(rocket):
      screen.blit(font.render('You Lose. Rocket missed the barge', 1, WHITE), (40, WINDOW_WIDTH/2))
      done = True

    clock.tick(FPS)


  # Exit game on next key press
  pressed = pygame.key.get_pressed()
  while len(pressed) == 0:
    pass
  
  pygame.quit()
