#!/usr/bin/env python

import farnsworth
import config
import constants
import datetime
import time

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=15.0 )



octgif=sign.locate_file('october.gif')
octsprite=farnsworth.sprite(gif_source=octgif,scale_y_to=config.PIXELS_HIGH)

decgif=sign.locate_file('december.gif')
decsprite=farnsworth.sprite(gif_source=decgif)

tvegif=sign.locate_file('tvegif.gif')
tvesprite=farnsworth.sprite(gif_source=tvegif)

clock = farnsworth.clock(0.1)

t=datetime.datetime.now()
m=t.strftime("%B")
d=t.strftime("%d")

while True:


    sign.front_layer().blank(constants.COLORS["WHITE"])

    if m =="October" and int(d)>15:
        if clock.tick():
            time.sleep(1)
            octsprite.advance_image()
        octsprite.paint(sign.front_layer())
    elif m == "December" and int(d)>15:
        if clock.tick():
            time.sleep(1)
            decsprite.advance_image()
        decsprite.paint(sign.front_layer())
    else:
        if clock.tick():
            tvesprite.advance_image()
        tvesprite.paint(sign.front_layer())

    sign.paint()
