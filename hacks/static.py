#!/usr/bin/python

import random

import farnsworth
import config

#=======================================================================

MAX_RUN = 4

#=======================================================================

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=3.0 )

#=======================================================================

while True:

  pixel_run = 0
  pixel_color = (0,0,0)
  
  if sign.paint():
    for y in range(config.PIXELS_HIGH):
      for x in range(config.PIXELS_ACROSS):
        if pixel_run == 0:
          pixel_run = int( random.random() * MAX_RUN )
          pixel = int( random.random() * 255 )
          pixel_color = (pixel,pixel,pixel)
          sign.front_layer().set_pixel(x,y,pixel_color)
        else:
          pixel_run -= 1
          sign.front_layer().set_pixel(x,y,pixel_color)

#=======================================================================
