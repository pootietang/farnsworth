#!/usr/bin/python

from time import sleep

import farnsworth
import config

x = (config.PIXELS_ACROSS - 72) / 2
y = (config.PIXELS_HIGH - 9) / 2

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=False,
                        preferred_duration=3.0 )

sign.front_layer().blank()

game_over = sign.locate_file('game_over.bmp')
sign.front_layer().blit_image( game_over, x, y )

while True:
  sign.paint()
  sleep(0.1)
