#!/usr/bin/python

from time import sleep

import farnsworth
import config

x = int( (config.PIXELS_ACROSS - 72) / 2 )
y = int( (config.PIXELS_HIGH - 9) / 2 )

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=False,
                        preferred_duration=3.0 )

game_over = sign.locate_file('game_over.bmp')

while True:
  sign.front_layer().blank()
  sign.front_layer().blit_image( game_over, x, y )
  sign.paint()
  sleep(0.1)
