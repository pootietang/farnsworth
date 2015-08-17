#!/usr/bin/python

import farnsworth
import config

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=5.0 )

gif = sign.locate_file('nyan_cat.gif')
cat = farnsworth.sprite(gif_source=gif, scale_y_to=config.PIXELS_HIGH)

clock = farnsworth.clock(0.1)

while True:

  sign.front_layer().blank()

  if clock.tick():
    #cat.cycle_image()
    cat.advance_image()

  cat.paint( sign.front_layer() )    
  
  sign.paint()
