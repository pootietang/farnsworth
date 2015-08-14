#!/usr/bin/python

from time import sleep
import datetime

import farnsworth
import constants

sign = farnsworth.sign( provides_logo=True,
                        is_dynamic=True,
                        preferred_duration=10.0 )

while True:

  sign.front_layer().blank()
  t = datetime.datetime.now()
  s = t.strftime("%b %e %I:%M:%S")
  sign.front_layer().render_twoline_string( 'KNOX MAKERS',
                                            'FONT_5x7',
                                            constants.COLORS['RED'],
                                            s,
                                            'FONT_5x5',
                                            constants.COLORS['WHITE'] )
  sign.fx_glitch_band()
  sign.paint()
  sleep(0.001)
