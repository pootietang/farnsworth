#!/usr/bin/python

from time import sleep

import farnsworth
import config

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=9.0 )

walker = farnsworth.sprite( sign.locate_file('01.bmp') )
walker.add_image( sign.locate_file('02.bmp') )
walker.add_image( sign.locate_file('03.bmp') )
walker.add_image( sign.locate_file('04.bmp') )
walker.add_image( sign.locate_file('05.bmp') )
walker.add_image( sign.locate_file('06.bmp') )
walker.add_image( sign.locate_file('07.bmp') )
walker.add_image( sign.locate_file('08.bmp') )
walker.add_image( sign.locate_file('09.bmp') )
walker.add_image( sign.locate_file('10.bmp') )
walker.add_image( sign.locate_file('11.bmp') )
walker.add_image( sign.locate_file('12.bmp') )
walker.add_image( sign.locate_file('13.bmp') )
walker.add_image( sign.locate_file('14.bmp') )
walker.add_image( sign.locate_file('15.bmp') )
walker.add_image( sign.locate_file('16.bmp') )

walker.move_to(-10,0)
walker.tween_to(95,0,150)

clock = farnsworth.clock(0.08)

while True:

  sign.front_layer().blank()

  if clock.tick():
    walker.advance_image()
    walker.tween()

  walker.paint( sign.front_layer() )    
  
  sign.paint()

  sleep(0.001)
