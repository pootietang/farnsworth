#!/usr/bin/python

from time import sleep
import farnsworth

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=False,
                        preferred_duration=5.0 )
                        
science = sign.locate_file('science.bmp')
s = farnsworth.sprite(base_image=science)

while True:
  sign.front_layer().blank()
  s.paint( sign.front_layer() )
  sign.paint()
  sleep(0.1)
