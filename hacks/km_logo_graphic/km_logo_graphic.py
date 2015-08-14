#!/usr/bin/python

from time import sleep

import farnsworth

sign = farnsworth.sign( provides_logo=True,
                        is_dynamic=False,
                        preferred_duration=5.0 )
                        
logo = sign.locate_file('km_logo.bmp')
sign.front_layer().load_from_image(logo)

while True:
  sign.paint()
  sleep(0.1)
