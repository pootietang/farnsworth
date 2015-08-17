#!/usr/bin/python

import farnsworth
import config

gifs = [
              { "file": "alarm.gif",
                "fps": 10,
                "x": 0 },
              { "file": "banana.gif",
                "fps": 8,
                "x": 20 },
              { "file": "fire.gif",
                "fps": 3,
                "x": 40 },
              { "file": "goomba.gif",
                "fps": 1,
                "x": 60 },
              { "file": "qblock.gif",
                "fps": 5,
                "x": 80 }
            ]

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=5.0 )

for gif in gifs:
  gif["file"] = sign.locate_file(gif["file"])
  gif["sprite"] = farnsworth.sprite(gif_source=gif["file"], scale_y_to=config.PIXELS_HIGH)
  gif["sprite"].move_to( gif["x"], 0 )
  gif["clock"] = farnsworth.clock( 1.0 / gif["fps"] )

while True:

  sign.front_layer().blank()

  for gif in gifs:
    if gif["clock"].tick():
      gif["sprite"].advance_image()
    gif["sprite"].paint( sign.front_layer() )    

  sign.paint()
