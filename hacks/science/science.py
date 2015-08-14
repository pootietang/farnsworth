#!/usr/bin/python

from time import sleep
import farnsworth

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=False,
                        preferred_duration=5.0 )
                        
science = sign.locate_file('science.bmp')
sign.front_layer().load_from_image(science)

while True:
  sign.paint()
  sleep(0.1)
