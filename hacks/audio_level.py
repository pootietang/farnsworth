#!/usr/bin/env python

import audioop
import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np

import farnsworth
import config
import constants

#=======================================================================

SAMPLE_RATE = 44100
CHANNEL_COUNT = 2
CHUNK_SIZE = 512

BAR_COUNT = 16
BAR_GUTTER = 2
BAR_WIDTH = (config.PIXELS_ACROSS / BAR_COUNT) - BAR_GUTTER
BAR_X_OFF = (config.PIXELS_ACROSS - ((BAR_COUNT * BAR_WIDTH) + ((BAR_COUNT - 1) * BAR_GUTTER))) / 2

#=======================================================================

sign = farnsworth.sign( provides_logo=False,
                        is_dynamic=True,
                        preferred_duration=15.0 )

audio = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
audio.setchannels(CHANNEL_COUNT)
audio.setrate(SAMPLE_RATE)
audio.setformat(aa.PCM_FORMAT_S16_LE)
audio.setperiodsize(CHUNK_SIZE)

#=======================================================================

def calculate_levels(data):
   # Convert raw data to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
   fourier = np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier = np.delete( fourier, len(fourier)-1 )
   # Find amplitude
   power = np.log10( np.abs(fourier) ) ** 2
   # Araange array into columns
   power = np.reshape( power, ( BAR_COUNT, CHUNK_SIZE/BAR_COUNT) )
   matrix = np.int_( np.average(power,axis=1) )
   return matrix

#=======================================================================

while True:

  sign.front_layer().blank()

  l,data = audio.read()
  audio.pause(1)
   
  if l:
    try:
      matrix = calculate_levels(data)
      for i in range(BAR_COUNT):
        this_bar_left = BAR_X_OFF + i * (BAR_WIDTH + BAR_GUTTER)
        sign.front_layer().paint_box( this_bar_left, matrix[i], this_bar_left + BAR_WIDTH, 0, constants.COLORS['GREEN'] )

    except audioop.error, e:
      if e.message !="not a whole number of frames":
        raise e

  sign.paint()
  
  audio.pause(0)

#=======================================================================
