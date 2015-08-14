#!/usr/bin/python

import time
import opc

client = opc.Client('172.16.250.3:7890')

PIXEL_COUNT = 150
COLOR_TIME = 3

color_idx = 0
test_colors = [ (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255) ]

colorstreams = []
for color in test_colors:
  a = []
  for i in range(PIXEL_COUNT):
    a.append( color )
  colorstreams.append( a )

while True:

  client.put_pixels( colorstreams[color_idx], channel=0)
  
  color_idx += 1
  if color_idx == len(test_colors):
    color_idx = 0

  time.sleep( COLOR_TIME )
