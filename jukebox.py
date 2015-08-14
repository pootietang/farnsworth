#!/usr/bin/python

import sys
import signal
from os import getcwd, listdir, walk, kill
from os.path import isfile, join, split
import fnmatch
from subprocess import Popen, PIPE
from time import time, sleep
import random

import constants
import config

########################################################################

hacks_dir = join( getcwd(), 'one_hack')

screenhacks = []
found_logos = False
found_dynamic = False

hack_index = 0

########################################################################

def register_hack( path ):
  global screenhacks, found_logos, found_dynamic

  settings = []
  proc = Popen( [path,"--register"], stdout=PIPE )
  for setting in proc.stdout:
    settings.append(setting.strip())

  hack = {}
  hack["provides_logo"] = settings[0] == "True"
  hack["is_dynamic"] = settings[1] == "True"
  hack["preferred_duration"] = float(settings[2])  
  hack["run_count"] = 0
  hack["path"] = path
  hack["name"] = split(path)[1]
  hack["weight"] = 5
  
  if hack["provides_logo"]:
    found_logos = True
  if hack["is_dynamic"]:
    found_dynamic = True

  screenhacks.append( hack )

  print "  %s: %s" % (len(screenhacks), hack["name"])
  
########################################################################

def random_hack():
  global hack_index

  totals = []
  running_total = 0

  for h in screenhacks:
    running_total += h["weight"]
    totals.append(running_total)
    h["weight"] += 1

  rnd = random.random() * running_total
  for i, total in enumerate(totals):
    if rnd < total:
      hack_index = i
      break
    else:
      print "rnd: %s	total: %s" % (rnd,total)

  return screenhacks[hack_index]

########################################################################

def next_hack():
  global hack_index

  last_hack = screenhacks[hack_index]

  logo_required = False
  dynamic_required = False

  if found_logos and not last_hack["provides_logo"]:
    logo_required = True
  if found_dynamic and not last_hack["is_dynamic"]:
    dynamic_required = True
  
  hack = random_hack()
  while ((not hack["provides_logo"]) and logo_required) or ((not hack["is_dynamic"]) and dynamic_required):
    hack = random_hack()

  hack["run_count"] += 1
  hack["weight"] -= 5

  return hack
  
########################################################################
def load_hacks():
  print "finding hacks..."
  for root, dirnames, filenames in walk(hacks_dir):
    for filename in fnmatch.filter(filenames, '*.py'):
      register_hack(join(root, filename))

########################################################################

def start_next_hack():
  hack = next_hack()
  hack["start_time"] = time()
  hack["termination_clock"] = 0
  hack["state"] = constants.ST_RUNNING
  hack["proc"] = Popen( [hack["path"],"--time",str(config.TIME_SLICE)] )
  print "starting %s; will run for %s secs" % (hack["name"],hack["preferred_duration"])
  runs = ""
  wt = ""
  for h in screenhacks:
    runs = runs + "%s	" % h["run_count"]
    wt = wt + "%s	" % h["weight"]
  print "[%s]" % runs
  print "<%s>" % wt
  return hack

########################################################################

load_hacks()

hack = start_next_hack()

while True:

  elapsed = time() - hack["start_time"]
  if elapsed > hack["preferred_duration"]:
    # the currently running screenhack has run out of time
    if hack["state"] == constants.ST_RUNNING:
      # request exit
      hack["proc"].terminate()
      hack["state"] = constants.ST_TERMINATING
    elif hack["state"] == constants.ST_TERMINATING:
      if hack["proc"].poll() is not None:
        # the screenhack that was running has terminated
        hack = start_next_hack()
      else:
        hack["termination_clock"] += 1
        if hack["termination_clock"] > config.MAX_DWELL:
          # the screenhack is taking too long to terminate
          # shoot it in the head
          hack["proc"].kill()

  sleep(0.001)

########################################################################
