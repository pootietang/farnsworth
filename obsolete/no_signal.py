#!/usr/bin/python

import time

import farnsworth
import constants

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=False,
                        preferred_duration=3.0 )


while True:

  sign.front_layer().blank( rgb_color=constants.COLORS['BLUE'] )
  sign.front_layer().render_string( 51, 1, 'FONT_5x5', 'NO SIGNAL', constants.COLORS['WHITE'] )
  sign.paint()
