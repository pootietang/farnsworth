#!/usr/bin/python

import math

import farnsworth
import config
import constants

def blue_rings( x, y, clock ):

  period = clock * 0.01 + 0.3
  offset = 0
  seed = math.sqrt((x - config.PIXELS_ACROSS / 2.0) * (x - config.PIXELS_ACROSS / 2.0) + (y - config.PIXELS_HIGH / 2.0) * (y - config.PIXELS_HIGH / 2.0)) / 8.0
  scale = math.sin((seed/period - offset) * math.pi * 2) / 2 + 0.5
  b = int(255.0 * scale)
  r = 0
  g = 0

  return (g,r,b)

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=5.0 )

while True:

  sign.paint_from_rule(blue_rings)
  sign.front_layer().render_glyph('CENTER','CENTER','FONT_5x7','HEART',constants.COLORS['RED']);
  sign.paint()
