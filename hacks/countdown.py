#!/usr/bin/python

from time import sleep
import datetime

import farnsworth
import constants

DTZERO = datetime.datetime( 2015, 8, 31, 19, 00 )

last_string = ""

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=60.0 )

while True:

  timedelta = DTZERO - datetime.datetime.now()
  seconds = timedelta.days * 24 * 3600 + timedelta.seconds
  
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  #days, hours = divmod(hours, 24)

  display_string = "%s:%s:%s" % (hours, minutes, seconds)
  #display_string = "%s:%s:%s:%s" % (days, hours, minutes, seconds)

  if display_string <> last_string:
    
    sign.front_layer().blank()
    sign.front_layer().render_string( 'CENTER',
                                      'CENTER',
                                      'FONT_11x15',
                                      display_string,
                                      constants.COLORS['BLUE'] )
    sign.paint()

  sleep(0.001)
