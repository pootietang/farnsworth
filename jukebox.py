#!/usr/bin/python

import sys
import signal
from os import getcwd, listdir, walk, kill
from os.path import isfile, join, split
import fnmatch
from subprocess import Popen, PIPE
from time import time, sleep
import random
import curses

import constants
import config

########################################################################

MAX_X = 79
MAX_Y = 23

STATUS_LINE_Y = 1
STATUS_LINE_X = 1

HACK_WINDOW_LINE_CT = 8
HACK_WINDOW_X = 1
HACK_WINDOW_Y = 3

MSG_WINDOW_LINE_CT = 10
MSG_WINDOW_X = 1
MSG_WINDOW_Y = 12

########################################################################

stdscr = None
hacks_dir = join( getcwd(), 'hacks')

screenhacks = []
found_logos = False
found_dynamic = False

hack_index = 0

########################################################################

def setup_screen():
  global stdscr, msg_win
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.keypad(1)
  msg_win = stdscr.subwin(MAX_Y, MAX_X, 0, 0)
  msg_win.box()
  msg_win.hline(2, 1, curses.ACS_HLINE, 77)
  msg_win.hline(HACK_WINDOW_LINE_CT+3, 1, curses.ACS_HLINE, 77)
  
########################################################################

hack_list_idx = 0
def paint_hack_list():
  global stdscr

  for i in range(HACK_WINDOW_LINE_CT):
    cursor = i + hack_list_idx
    if cursor >= len(screenhacks):
      cursor -= len(screenhacks)

    if i == selected_hack:
      stdscr.addstr(HACK_WINDOW_Y + i, HACK_WINDOW_X, screenhacks[cursor]["name"], curses.A_REVERSE)
    else:
      stdscr.addstr(HACK_WINDOW_Y + i, HACK_WINDOW_X, screenhacks[cursor]["name"])

  stdscr.refresh()

########################################################################

msg_buffer = [" "] * MSG_WINDOW_LINE_CT
msg_idx = 0
def log_msg(msg):
  global msg_buffer, msg_idx, stdscr
  msg_buffer[msg_idx] = msg
  msg_idx += 1
  if msg_idx == len(msg_buffer):
    msg_idx = 0

  for i in range(MSG_WINDOW_LINE_CT):
    cursor = i + msg_idx
    if cursor >= len(msg_buffer):
      cursor -= len(msg_buffer)
    pstr = msg_buffer[cursor] + " " * ( MAX_X - (len(msg_buffer[cursor])+2) )
    stdscr.addstr(MSG_WINDOW_Y + i, MSG_WINDOW_X, pstr, curses.A_REVERSE)

  stdscr.refresh()
  
########################################################################

def set_status(msg):
  global stdscr
  stdscr.addstr(STATUS_LINE_Y, STATUS_LINE_X, msg, curses.A_REVERSE)
  stdscr.refresh()

########################################################################

def bail():
  global stdscr
  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()
  curses.curs_set(1)

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

  log_msg( "  %s: %s" % (len(screenhacks), hack["name"]) )
  log_msg( "	provides_logo: %s	is_dynamic: %s" % (settings[0] == "True", settings[1] == "True") )

  if hack["preferred_duration"] > config.MAX_RUN:
    hack["preferred_duration"] = config.MAX_RUN
    log_msg( "	requested time of %s seconds abbreviated to %s seconds" % (settings[2],config.MAX_RUN) )

  screenhacks.append( hack )
  
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
      
  return screenhacks[hack_index]

########################################################################

selected_hack = 0

def hack_up():
  global selected_hack
  if selected_hack > 0:
    selected_hack -= 1
    paint_hack_list()

def hack_down():
  global selected_hack, hack_list_idx
  if selected_hack < len(screenhacks) - 1:
    selected_hack += 1
    if selected_hack >= HACK_WINDOW_LINE_CT + hack_list_idx:
      hack_list_idx += 1
    paint_hack_list()

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
  set_status("finding hacks...")
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
  set_status(" RUNNING %s " % hack["name"])
  log_msg( "starting %s; will run for %s secs" % (hack["name"],hack["preferred_duration"]) )
  runs = ""
  wt = ""
  for h in screenhacks:
    runs = runs + "%s	" % h["run_count"]
    wt = wt + "%s	" % h["weight"]
#  print "[%s]" % runs
#  print "<%s>" % wt
  return hack

########################################################################

setup_screen()

load_hacks()

paint_hack_list()

hack = start_next_hack()

while True:

  ch = stdscr.getch()
  if ch == ord('q'):
    break
  elif ch == curses.KEY_ENTER:
    pass
  elif ch == curses.KEY_DOWN:
    hack_down()
  elif ch == curses.KEY_UP:
    hack_up()

  elapsed = time() - hack["start_time"]
  if elapsed > hack["preferred_duration"]:
    # the currently running screenhack has run out of time
    if hack["state"] == constants.ST_RUNNING:
      # request exit
      log_msg("requesting exit of %s" % hack["name"])
      hack["proc"].terminate()
      hack["state"] = constants.ST_TERMINATING
    elif hack["state"] == constants.ST_TERMINATING:
      if hack["proc"].poll() is not None:
        # the screenhack that was running has terminated
        log_msg("exited; starting next hack...")
        hack = start_next_hack()
      else:
        hack["termination_clock"] += 1
        if hack["termination_clock"] > config.MAX_DWELL:
          # the screenhack is taking too long to terminate
          # shoot it in the head
          log_msg("%s taking too long to exit; killing" % hack["name"])
          hack["proc"].kill()

  sleep(0.001)

bail()

########################################################################
