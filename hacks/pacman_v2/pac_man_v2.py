#!/usr/bin/python

import farnsworth

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=9 )

pacman = farnsworth.sprite( sign.locate_file('pacman_1.bmp') )
pacman.add_image( sign.locate_file('pacman_2.bmp') )
pacman.add_image( sign.locate_file('pacman_3.bmp') )
pacman.move_to(-16,0)
pacman.tween_to(95,0,95)

blinky = farnsworth.sprite( sign.locate_file('blinky_1.bmp') )
blinky.add_image( sign.locate_file('blinky_2.bmp') )
blinky.move_to(-50,0)
blinky.tween_to(96,0,107)

pellet1 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet1.move_to(4,7)

pellet2 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet2.move_to(12,7)

pellet3 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet3.move_to(20,7)

pellet4 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet4.move_to(28,7)

pellet5 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet5.move_to(36,7)

pellet6 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet6.move_to(44,7)

pellet7 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet7.move_to(52,7)

pellet8 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet8.move_to(60,7)

pellet9 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet9.move_to(68,7)

pellet10 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet10.move_to(76,7)

pellet11 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet11.move_to(84,7)

pellet12 = farnsworth.sprite( sign.locate_file('pellet.bmp') )
pellet12.move_to(92,7)

clock = farnsworth.clock(.075)
#clock = farnsworth.clock(1.5)
frame_count = 0

while True:

  sign.front_layer().blank()

  if clock.tick():
    pacman.cycle_image()
    pacman.tween()
    blinky.cycle_image()
    blinky.tween() 
    print "Blinky = ", blinky._x, blinky._x_inc, blinky._x_float
    print "Pacman = ", pacman._x , pacman._x_inc, pacman._x_float
    #print frame_count
    if frame_count <= 5:
        p1=True
    else:
        p1=False
  
    if frame_count <= 9:
        p2=True
    else:
        p2=False
     
    if frame_count <= 17:
        p3=True
    else:
        p3=False
  
    if frame_count <= 25:
        p4=True
    else:
        p4=False
  
    if frame_count <= 33:
        p5=True
    else:
        p5=False
  
    if frame_count <= 41:
        p6=True
    else:
        p6=False
  
    if frame_count <= 49:
        p7=True
    else:
        p7=False
  
    if frame_count <= 57:
        p8=True
    else:
        p8=False
  
    if frame_count <= 65:
        p9=True
    else:
        p9=False
  
    if frame_count <= 73:
        p10=True
    else:
        p10=False
  
    if frame_count <= 81:
        p11=True
    else:
        p11=False
  
    if frame_count <= 89:
        p12=True
    else:
        p12=False
  
    frame_count+=1
  
  if p1:
      pellet1.paint( sign.front_layer() )
  if p2:
      pellet2.paint( sign.front_layer() )
  if p3:
      pellet3.paint( sign.front_layer() )
  if p4:
      pellet4.paint( sign.front_layer() )
  if p5:
      pellet5.paint( sign.front_layer() )
  if p6:
      pellet6.paint( sign.front_layer() )
  if p7:
      pellet7.paint( sign.front_layer() )
  if p8:
      pellet8.paint( sign.front_layer() )
  if p9:
      pellet9.paint( sign.front_layer() )
  if p10:
      pellet10.paint( sign.front_layer() )
  if p11:
      pellet11.paint( sign.front_layer() )
  if p12:
      pellet12.paint( sign.front_layer() )

  pacman.paint( sign.front_layer(), black_xparent=True )
  blinky.paint( sign.front_layer(), black_xparent=True )
  
  sign.paint()
