#!/usr/bin/python

from time import sleep

import farnsworth
import constants

sign = farnsworth.sign( provides_logo=True,
                        is_dynamic=True,
                        preferred_duration=5.0 )

while True:

  sign.front_layer().blank()
  sign.front_layer().render_twoline_string( 'KNOX MAKERS', 'FONT_5x7', constants.COLORS['RED'],
                                            'community/workshop', 'FONT_5x5', constants.COLORS['WHITE'] )
  sign.fx_glitch_vsync()
  sign.paint()
  sleep(0.001)
