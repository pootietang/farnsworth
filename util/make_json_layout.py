#!/usr/bin/env python

import farnsworth

spacing = 0.11  # m
lines = []

horizontal_offset = -(farnsworth.PIXELS_ACROSS * spacing / 2)

for y in range(0,farnsworth.PIXELS_HIGH):
  for x in range(0,farnsworth.PIXELS_ACROSS):
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' % (x*spacing+horizontal_offset, 0, y*spacing) )

print '[\n' + ',\n'.join(lines) + '\n]'
