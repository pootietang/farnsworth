#!/usr/bin/python

import math
import farnsworth

def red_dots( x, y, count ):
  scale = 0.5 + 0.1 * count
  color = int( (128.0 * math.sin(x * scale)) + (128.0 * math.sin(y * scale)) )

  return (color,0,0)

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=3.0 )

while True:

  sign.paint_from_rule(red_dots)
  sign.paint()
