#!/usr/bin/python

import farnsworth

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=5.0 )

pacman = farnsworth.sprite( sign.locate_file('pac_man_0.bmp') )
pacman.add_image( sign.locate_file('pac_man_1.bmp') )
pacman.add_image( sign.locate_file('pac_man_2.bmp') )
pacman.move_to(70,1)

ghost = farnsworth.sprite( sign.locate_file('ghost_1.bmp') )
ghost.add_image( sign.locate_file('ghost_2.bmp') )
ghost.move_to(20,0)

pellet = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet.move_to(93,7)

clock = farnsworth.clock(0.25)

new_x = 0

while True:

  sign.front_layer().blank()

  if clock.tick():
    pacman.cycle_image()
    ghost.advance_image()

    new_x = new_x - 3
    if new_x < 70:
      new_x = 93
    pellet.move_to(new_x,7)

  pellet.paint( sign.front_layer() )    
  pacman.paint( sign.front_layer(), black_xparent=True )
  ghost.paint( sign.front_layer() )
  
  sign.paint()
