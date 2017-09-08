#!/usr/bin/python

from time import sleep
import farnsworth

sign = farnsworth.sign( provides_logo=True,
                        is_dynamic=False,
                        preferred_duration=5.0 )
                        
science = sign.locate_file('km_logo.bmp')
s = farnsworth.sprite(base_image=science)

while True:
  sign.front_layer().blank()
  s.paint( sign.front_layer() )
  sign.paint()
  sleep(0.1)
