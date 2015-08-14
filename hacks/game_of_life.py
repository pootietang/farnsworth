#!/usr/bin/python

import random
from time import sleep

import farnsworth
import config
import constants

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=15.0 )

sign.rule_clock().set_tick_latency( 0.1 )

for x in range(config.PIXELS_ACROSS):
  for y in range(config.PIXELS_HIGH):
    if random.random() > 0.8:
      sign.front_layer().set_pixel(x,y,constants.COLORS['GREEN'])

def generate(x,y,clock):

  live_neighbors = 0
  for xo in range(3):
    for yo in range(3):
      if (xo == 1) and (yo == 1):
        continue	
      xt = x + xo - 1
      yt = y + yo - 1
      if xt >= config.PIXELS_ACROSS:
        xt -= config.PIXELS_ACROSS
      if xt < 0:
        xt += config.PIXELS_ACROSS
      if yt >= config.PIXELS_HIGH:
        yt -= config.PIXELS_HIGH
      if yt < 0:
        yt += config.PIXELS_HIGH
      if sign.front_layer().read_pixel(xt,yt) <> constants.COLORS['BLACK']:
		live_neighbors += 1

  if live_neighbors in (0,1,4,5,6,7,8):
    color = 0
  elif live_neighbors == 3:
    color = 255
  else:
    if sign.front_layer().read_pixel(x,y) <> constants.COLORS['BLACK']:
      color = 255
    else:
      color = 0

  return (0, color, 0)

while True:

  sign.paint_from_rule(generate)
  sign.paint()
  sleep(0.001)
