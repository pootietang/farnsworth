#!/usr/bin/env python

#=======================================================================

from __future__ import division
import argparse
import time
import math
import random
import os
import sys
import signal
import opc
from PIL import Image
  
import constants
import config

#=======================================================================

class layer():

  def __init__(self, width=0, height=0, filename=None):

    self._data = []
    self._dirty = True

    if filename:
      self.load_from_image(filename)
    else:
      self._width = width
      self._height = height
      for y in range(0,self._height):
        row = []
        for x in range(0,self._width):
          row.append( (0,0,0) )
        self._data.append(row)
      
    self._scroll_cursor = self._width

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def is_dirty(self):
    return self._dirty

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def blank( self, rgb_color=(0,0,0) ):

    for y in range(0,self._height):
      for x in range(0,self._width):
        self._data[y][x] = rgb_color

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def get_pixel( self, x, y ):

    if self.in_bounds(x,y):
      return self._data[y][x]
    else:
      return None

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def set_pixel( self, x, y, rgb_color ):
    if self.in_bounds(x,y):
      real_color = self.translate_color( rgb_color )
      if self._data[y][x] <> real_color:
        self._data[y][x] = real_color
        self._dirty = True

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def read_pixel( self, x, y ):

    if self.in_bounds( x, y):
      return self._data[y][x]
    else:
      return None

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def in_bounds( self, x, y ):

    if x < 0:
      return False
    elif y < 0:
      return False
    elif x >= self._width:
      return False
    elif y >= self._height:
      return False
    else:
      return True

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def paint_box( self, tlx, tly, brx, bry, rgb_color ):

    for x in range(tlx,brx+1):
      for y in range(bry,tly+1):
        self.set_pixel( x, y, rgb_color )

    self._dirty = True

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def translate_color( self, color ):

    return ( color[config.COLOR_ORDER[0]],
             color[config.COLOR_ORDER[1]],
             color[config.COLOR_ORDER[2]] )

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def load_from_image( self, filename ):

    im = Image.open(filename)
    pixels = im.load()
    self._width, self._height = im.size
    
    for y in range(0,self._height):
      row = []
      for x in range(0,self._width):
        row.append( (0,0,0) )
      self._data.append(row)

    for y in range(0,self._height):
      for x in range(0,self._width):
        self.set_pixel(x, self._height - (y+1), pixels[(x,y)])

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def blit_image( self, filename, x, y ):

    im = Image.open(filename)
    pixels = im.load()
    w, h = im.size

    for by in range(0,h):
      for bx in range(0,w):
        self.set_pixel(bx + x, y + h - (by+1), pixels[(bx,by)])

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  def serialize_data(self):

    flat = []
    for y in range(0,self._height):
      for x in range(0,self._width):
        flat.append( self._data[y][x] )
    self._dirty = False
    return flat

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def blit(self, destination_layer, dx=0, dy=0, black_xparent=False ):

    for x in range(self._width):
      for y in range(self._height):
        if (not black_xparent) or ( self._data[y][x] <> constants.COLORS['BLACK'] ):
          destination_layer.set_pixel( dx + x, dy + y, self._data[y][x] )

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def glyph_width(self, font_name, glyph):

    font = constants.FONTS[font_name]
    if glyph not in font:
      width = font['METRICS']['WIDTH']
    else:
      width = 0
      for pixel in font[glyph]:
        if pixel[0] + 1 > width:
          width = pixel[0] + 1

    return width

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def render_glyph(self, x, y, font_name, glyph, rgb_color):

    font = constants.FONTS[font_name]

    if glyph <> ' ':
	  
      if x == 'CENTER':
        width = self.glyph_width(font_name, glyph)
        x = int((self._width - width) / 2)
  
      if y == 'CENTER':
        height = font['METRICS']['HEIGHT']
        y = int((self._height - height) / 2)
  
      if glyph not in font:
        pixels = font['BLOCK']
      else:
        pixels = font[glyph]

      for pixel in pixels:
        self.set_pixel( pixel[0]+x,
                        pixel[1]+y,
                        rgb_color )

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def measure_string(self, font_name, string, char_space=1):

    width = 0
    for char in string:
      width += self.glyph_width(font_name,char) + char_space
    width -= char_space

    return width
    
  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def render_string(self, x, y, font, string, rgb_color, rgb_bgcolor=None, char_space=1):

    cursor = 0
  
    if x == 'CENTER':
      string_width = self.measure_string(font,string)
      x = int((self._width - string_width) / 2)
  
    if y == 'CENTER':
      string_height = constants.FONTS[font]['METRICS']['HEIGHT']
      y = int((self._height - string_height) / 2)
  
    if rgb_bgcolor:
      self.paint_box( x-1, y+string_height, x+string_width, y-1, rgb_bgcolor )

    for char in string:
      self.render_glyph(x + cursor,y,font,char,rgb_color)
      cursor += self.glyph_width(font,char) + char_space

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def scroll_string(font_name, string, rgb_color, y=0, scroll_rate=0.3):

    self.render_string( self._scroll_cursor, y, font_name, string, rgb_color )

    if time.time() - self._last_scroll >= scroll_rate:
      self._scroll_cursor -= 1		
      if self._scroll_cursor < -self.measure_string(font_name,string):
        self._scroll_cursor = self._width

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def render_twoline_string( self,
                             string1, string1_font_name, string1_rgb_color,
                             string2, string2_font_name, string2_rgb_color ):

    string1_height = constants.FONTS[string1_font_name]['METRICS']['HEIGHT']
    string2_height = constants.FONTS[string2_font_name]['METRICS']['HEIGHT']

    sm_buffer = int( (self._height - (string1_height + string2_height)) / 3 )
    bg_buffer = int( self._height - (string1_height + string2_height + sm_buffer * 2) )

    self.render_string( 'CENTER',
                        string2_height + sm_buffer + bg_buffer,
                        string1_font_name,
                        string1,
                        string1_rgb_color )
                        
    self.render_string( 'CENTER',
                        sm_buffer,
                        string2_font_name,
                        string2,
                        string2_rgb_color)

#=======================================================================

class scroller(layer):

  def __init__(self):
    super(scroller,self).__init__()
    
  def paint(self):
    pass

#=======================================================================

class sign():

  def __init__( self, provides_logo=False, is_dynamic=False,
                preferred_duration=10.0 ):

    self._provides_logo = provides_logo
    self._is_dynamic = is_dynamic
    self._preferred_duration = preferred_duration

    self.setup_properties()
    self.handle_command_line()

    signal.signal(signal.SIGTERM,self.clean_shutdown)
    signal.signal(signal.SIGINT,self.clean_shutdown)

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def clean_shutdown(self,signum,dataframe):
    # free resources, etc. also catch "error" of sudden exit
    sys.exit()

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def handle_command_line(self):

    parser = argparse.ArgumentParser()
    parser.add_argument("--register", action="store_true", default=False)
    parser.add_argument("--time",type=float)
    args = parser.parse_args()

    if args.time:
      self._remaining_time = args.time

    if args.register:
      self.register()
      sys.exit()

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def setup_properties(self):

    self._remaining_time = self._preferred_duration
    self._currently_glitching = False
    self._glitching_up = False
    self._glitch_cursor = 0
    self._glitch_dwell = 3
    self._last_glitch = 0

    self._front_layer = layer( width=config.PIXELS_ACROSS, height=config.PIXELS_HIGH )
    self._back_layer = layer( width=config.PIXELS_ACROSS, height=config.PIXELS_HIGH )

    self._paint_clock = clock( tick_every = 1 / config.FPS )
    self._rule_clock =  clock( tick_every = 1 / config.FPS,
                               maximum_count = 30 )
                               
    self._opc_client = opc.Client("%s:%s" % (config.IP_ADDRESS,config.PORT))

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def register(self):

    for setting in [self._provides_logo, self._is_dynamic, self._preferred_duration]:
      print setting
    sys.exit()

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  def locate_file(self,fname):
    #cwd = os.path.dirname(os.path.realpath(__file__))
    fp = os.path.join(sys.path[0],fname)
    return fp

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def front_layer(self):
    return self._front_layer

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def back_layer(self):
    return self._back_layer

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def rule_clock(self):
    return self._rule_clock

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def flip(self):

    temp_layer = self._front_layer
    self._front_layer = self._back_layer
    self._back_layer = temp_layer

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def paint(self):

    if self._paint_clock.tick() and self._front_layer.is_dirty():
      serialized = self._front_layer.serialize_data()
      self._opc_client.put_pixels(serialized)
      return True
    return False

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def paint_once(self):

    serialized = self._front_layer.serialize_data()
    self._opc_client.put_pixels(serialized)
    return True

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def paint_from_rule( self, paint_rule ):

    if self._rule_clock.tick():
	  
      for y in range(0,config.PIXELS_HIGH):
        for x in range(0,config.PIXELS_ACROSS):
          self._back_layer.set_pixel( x,
                                      y,
                                      paint_rule( x, y, self._rule_clock.get_count() )
                                    )
      self.flip()

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  def fx_glitch_band(self):

    if not self._currently_glitching:

      if time.time() - self._last_glitch > 1/config.FPS:
        self._currently_glitching = (random.random() > 0.9)
        if self._currently_glitching:
          self._glitching_up = (random.random() > 0.5)
          self._glitch_cursor = 0
          self._glitch_dwell = random.random() / 5
        self._last_glitch = time.time()

    if self._currently_glitching:

      for y in range(0,config.PIXELS_HIGH):
        for x in range(0,config.PIXELS_ACROSS):
          if ((self._glitching_up and (y in range(self._glitch_cursor,self._glitch_cursor+1))) or
             (not self._glitching_up and (y in range(self._glitch_cursor-1,self._glitch_cursor)))):
            if random.random() > 0.5:
              pixel = random.random() * 255
              self._back_layer.set_pixel(x, y, (pixel,pixel,pixel))
            else:
              self._back_layer.set_pixel(x, y, self._front_layer.get_pixel(x, y))
          else:
            self._back_layer.set_pixel(x, y, self._front_layer.get_pixel(x, y))

      self.flip()
        
      if time.time() - self._last_glitch > self._glitch_dwell:

        if self._glitching_up:
          self._glitch_cursor += 1
          if self._glitch_cursor >= config.PIXELS_HIGH:
            self._glitch_cursor = 0
            self._currently_glitching = (random.random() > 0.9)
        else:
          self._glitch_cursor -= 1
          if self._glitch_cursor + config.PIXELS_HIGH <= 0:
            self._glitch_cursor = 0
            self._currently_glitching = (random.random() > 0.9)

        self._last_glitch = time.time()

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def fx_glitch_vsync(self):
  
    if not self._currently_glitching:
    
      if time.time() - self._last_glitch > 1/config.FPS:
        self._currently_glitching = (random.random() > 0.95)
        if self._currently_glitching:
          self._glitching_up = (random.random() > 0.5)
          self._glitch_cursor = 0
          self._glitch_dwell = random.random() / config.FPS
        self._last_glitch = time.time()

    if self._currently_glitching:

      for y in range(0,config.PIXELS_HIGH):

        skewed_y = y + self._glitch_cursor
        if skewed_y < 0:
          skewed_y += config.PIXELS_HIGH
        if skewed_y >= config.PIXELS_HIGH:
          skewed_y -= config.PIXELS_HIGH
      
        for x in range(0,config.PIXELS_ACROSS):
          self._back_layer.set_pixel(x, skewed_y, self._front_layer.get_pixel(x, y))

      self.flip()
        
      if time.time() - self._last_glitch > self._glitch_dwell:

        if self._glitching_up:
          self._glitch_cursor += 1
          if self._glitch_cursor >= config.PIXELS_HIGH:
            self._glitch_cursor = 0
            self._currently_glitching = (random.random() > 0.9)
        else:
          self._glitch_cursor -= 1
          if self._glitch_cursor + config.PIXELS_HIGH <= 0:
            self._glitch_cursor = 0
            self._currently_glitching = (random.random() > 0.9)

        self._last_glitch = time.time()

#=======================================================================

class clock():

  def __init__(self, tick_every=1.0, maximum_count=1, count_every=1/config.FPS):

    self._tick_every = tick_every
    self._last_tick = 0

    self._last_count = 0    
    self._count = 0
    self._count_every = count_every
    self._maximum_count = maximum_count

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def tick(self):

    elapsed_time = time.time() - self._last_tick
    if elapsed_time > self._tick_every:

      elapsed_time = time.time() - self._last_count
      if elapsed_time > self._count_every:
        self._count += 1
        if self._count > self._maximum_count:
          self._count = 0
        self._last_count = time.time()
        
      self._last_tick = time.time()
      return True
    else:
      return False

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def set_maximum_count(self,maximum_count):

    self._maximum_count = maximum_count
    if self._count > self._maximum_count:
      self._count = 0

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def set_tick_latency(self,tick_every):

    self._tick_every = tick_every

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def set_count_latency(self,count_every):

    self._count_every = count_every

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  def get_count(self):

    return self._count

#=======================================================================

class sprite(layer):

  def __init__(self, base_image):

    self._x = 0
    self._y = 0
    self._dest_x = 0
    self._dest_y = 0
    self._x_inc = 0
    self._y_inc = 0
    self._images = []
    self._image_cursor = 0
    self._cursor_increment = 1
    self.add_image(base_image)

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def add_image(self, filename):

    self._images.append( layer(filename=filename) )

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def paint(self, dest_layer, black_xparent=False):

    current_image = self._images[self._image_cursor]
    current_image.blit( dest_layer, self._x, self._y, black_xparent )

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def move_to(self, x, y):

    self._x = x
    self._y = y

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def tween_to(self, x, y, framecount):

    self._dest_x = x
    self._dest_y = y
    
    if self._dest_x <> self._x:
      self._x_inc = (self._dest_x - self._x) / framecount
      if self._x_inc > 0 and self._x_inc < 1:
        self._x_inc = 1
      elif self._x_inc < 0 and self._x_inc > -1:
        self._x_inc = -1
    
    if self._dest_y <> self._y:
      self._y_inc = (self._dest_y - self._y) / framecount
      if self._y_inc > 0 and self._y_inc < 1:
        self._y_inc = 1
      elif self._y_inc < 0 and self._y_inc > -1:
        self._y_inc = -1

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def advance_image(self):

    self._image_cursor += 1
    if self._image_cursor >= len(self._images):
      self._image_cursor = 0

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def cycle_image(self):

    self._image_cursor += self._cursor_increment

    if self._image_cursor >= len(self._images):
      self._cursor_increment = -1
      self._image_cursor -= 2
    if self._image_cursor < 0:
      self._cursor_increment = 1
      self._image_cursor = 1

  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  def tween(self):

    self._x = int(self._x + self._x_inc)
    if ((self._x_inc > 0) and (self._x >= self._dest_x)) or ((self._x_inc < 0) and (self._x <= self._dest_x)):
      #done animating x
      self._x_inc = 0
      self._dest_x = self._x
      
    self._y = int(self._y + self._y_inc)
    if ((self._y_inc > 0) and (self._y >= self._dest_y)) or ((self._y_inc < 0) and (self._y <= self._dest_y)):
      #done animating y
      self._y_inc = 0
      self._dest_y = self._y  

#=======================================================================
