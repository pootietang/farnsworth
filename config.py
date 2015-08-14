#!/usr/bin/env python

import constants

#=======================================================================

#IP_ADDRESS = '172.16.250.3'
IP_ADDRESS = 'localhost'
PORT = 7890

FPS = 30

PIXELS_ACROSS = 95
PIXELS_HIGH = 16
PIXEL_SPACING = 0.15

COLOR_ORDER = [ constants.COLOR_R, constants.COLOR_G, constants.COLOR_B ]

# maximum permissible post-termination hack runtime, in microseconds
#MAX_DWELL = 4000000
MAX_DWELL = 1000000

# time per screenhack, in seconds
TIME_SLICE = 5.0

#=======================================================================
