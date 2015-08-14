#!/usr/bin/python

from time import sleep

import farnsworth
import constants

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=5.0 )

clock = farnsworth.clock(0.5)

index = -1
lyrics = [ 'WORK IT',
           'MAKE IT',
           'DO IT',
           'BREAK IT',
           'TRY IT',
           'TEST IT',
           'HACK IT',
           'PRESS IT',
           'OUR WORK IS',
           'NEVER OVER' ]

while True:

  if clock.tick():

    index += 1
    if index >= len(lyrics):
      index = 0

    sign.front_layer().blank()
    sign.front_layer().render_string( 'CENTER',
                                      'CENTER',
                                      'FONT_5x7',
                                      lyrics[index],
                                      constants.COLORS['BLUE'] )
    sign.paint()
  sleep(0.001)
