#!/usr/bin/python

from time import sleep

import farnsworth
import constants

#=======================================================================

STRIPE_WIDTH = 10

#=======================================================================

def hazard(x,y,clock):
  
  if int((x + y + clock) / STRIPE_WIDTH) % 2 == 0:
    return constants.COLORS['YELLOW']
  else:
    return constants.COLORS['BLACK']

#=======================================================================

sign = farnsworth.sign( provides_logo=True,
                        is_dynamic=True,
                        preferred_duration=5.0 )

sign.rule_clock().set_maximum_count( STRIPE_WIDTH*2 )
sign.rule_clock().set_count_latency( 0.1 )

while True:

  sign.paint_from_rule(hazard)
  sign.front_layer().render_string( 'CENTER',
                                    'CENTER',
                                    'FONT_5x7',
                                    'KNOX MAKERS',
                                    constants.COLORS['WHITE'],
                                    constants.COLORS['BLACK'] )
  sign.paint()
  sleep(0.001)
  
#=======================================================================
