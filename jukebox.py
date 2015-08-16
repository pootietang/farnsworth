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

PAINT_INTERVAL = 0.1

MAX_X = 79
MAX_Y = 23

STATUS_WINDOW_Y = 1
STATUS_WINDOW_X = 2
STATUS_WINDOW_W = 75

HACK_WINDOW_LINE_CT = 8
HACK_WINDOW_X = 2
HACK_WINDOW_Y = 3
HACK_WINDOW_W = 75

MSG_WINDOW_LINE_CT = 10
MSG_WINDOW_X = 2
MSG_WINDOW_Y = 12
MSG_WINDOW_W = 75

########################################################################

stdscr = None
hacks_dir = join( getcwd(), 'hacks')

screenhacks = []
found_logos = False
found_dynamic = False

hack_run_count = 0
hack_index = 0
manual = False
total_odds = 1

########################################################################

def setup_screen():
  global CURSES_ENABLED, stdscr, msg_win
  
  stdscr = curses.initscr()
  term_y,term_x = stdscr.getmaxyx()
  
  if (term_x < MAX_X) or (term_y < MAX_Y):
    curses.endwin()
    print "Terminal must be at least %sx%s for interactive mode; running in silent mode instead." % (MAX_X,MAX_Y)
    print "Press Ctrl+C to terminate script."
    CURSES_ENABLED = False
    return

  CURSES_ENABLED = True

  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.keypad(1)
  
  win_title = "[ farnsworth ]"
  msg_win = stdscr.subwin(MAX_Y, MAX_X, 0, 0)
  msg_win.box()
  msg_win.hline(2, 1, curses.ACS_HLINE, 77)
  msg_win.hline(HACK_WINDOW_LINE_CT+3, 1, curses.ACS_HLINE, 77)
  stdscr.addstr(0, int((MAX_X - len(win_title)) / 2), win_title)  
  stdscr.refresh()

########################################################################

hack_list_idx = 0
def paint_hack_list():
  global stdscr
  
  if not CURSES_ENABLED:
    return

  actual_lines = min(HACK_WINDOW_LINE_CT,len(screenhacks))
  for i in range(actual_lines):
    cursor = i + hack_list_idx
    if cursor >= len(screenhacks):
      cursor -= len(screenhacks)

    m = " "
    if cursor == hack_index:
      if manual:
        m = "="
      else:
		m = ">"

    this_hack = screenhacks[cursor]
    odds = this_hack["odds"] * 1.0 / total_odds
    t = "%s[R:%s O:%.2f] %s" % ( m, this_hack["run_count"], odds, this_hack["name"] )
    w = MAX_X - (len(t)+HACK_WINDOW_X*2)
    t = t + " " * w
    t = t[:HACK_WINDOW_W]

    if cursor == selected_hack:
      stdscr.addstr(HACK_WINDOW_Y + i, HACK_WINDOW_X, t, curses.A_REVERSE)
    else:
      stdscr.addstr(HACK_WINDOW_Y + i, HACK_WINDOW_X, t)

  stdscr.refresh()

########################################################################

msg_buffer = [" "] * MSG_WINDOW_LINE_CT
msg_idx = 0

def log_msg(msg):
  global msg_buffer, msg_idx, stdscr
  
  if not CURSES_ENABLED:
    return
  
  msg_buffer[msg_idx] = msg
  
  cursor_offset = msg_idx - MSG_WINDOW_LINE_CT + 1
  for i in range(MSG_WINDOW_LINE_CT):
    cursor = cursor_offset + i
    if cursor >= len(msg_buffer):
      cursor -= len(msg_buffer)
    msg_w = MAX_X - (len(msg_buffer[cursor])+MSG_WINDOW_X*2)
    pstr = msg_buffer[cursor] + " " * msg_w
    stdscr.addstr(MSG_WINDOW_Y + i, MSG_WINDOW_X, pstr[:HACK_WINDOW_W])

  stdscr.refresh()

  msg_idx += 1
  if msg_idx == len(msg_buffer):
    msg_idx = 0

########################################################################

status = ""
cached_status = ""

def set_status(new_status):
  global status

  status = new_status
  paint_status()

def cache_status():
  global cached_status
  cached_status = status

def restore_status():
  global status
  status = cached_status

########################################################################

def paint_status():
  global stdscr

  if not CURSES_ENABLED:
    return

  if len(screenhacks) > 0:
    h = screenhacks[hack_index]
    if manual:
      s = "%s | %.1fs" % (status, h["elapsed"])
    else:
      s = "%s | %.1f / %.1fs" % (status, h["elapsed"], h["preferred_duration"])
  else:
	s = status

  if manual:
    s = "MANUAL | %s" % s
  else:
    s = "AUTO | %s"  % s
  w = MAX_X - (len(s)+STATUS_WINDOW_X*2)
  s = s + " " * w
  s = s[:STATUS_WINDOW_W]

  stdscr.addstr(STATUS_WINDOW_Y, STATUS_WINDOW_X, s)
  stdscr.refresh()

########################################################################

def bail(signum=None,dataframe=None):
  global stdscr

  if CURSES_ENABLED:
    # undo all the curses stuff to restore normalcy to the terminal
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    curses.curs_set(1)

  # kill the hack currently running before exiting
  screenhacks[hack_index]["proc"].kill()
  
  print " "
  print "Clean exit."
  
  sys.exit()

########################################################################

def register_hack( path ):
  global screenhacks, found_logos, found_dynamic

  for hack in screenhacks:
    if path == hack["path"]:
      return False

  settings = []
  proc = Popen( [path,"--register"], stdout=PIPE )
  for setting in proc.stdout:
    settings.append(setting.strip())

  hack = {}
  hack["provides_logo"] = settings[0] == "True"
  hack["is_dynamic"] = settings[1] == "True"
  hack["preferred_duration"] = float(settings[2])
  hack["elapsed"] = 0
  hack["run_count"] = 0
  hack["odds"] = 100
  hack["path"] = path
  hack["name"] = split(path)[1]
  
  if hack["provides_logo"]:
    found_logos = True
  if hack["is_dynamic"]:
    found_dynamic = True

  if hack["preferred_duration"] > config.MAX_RUN:
    hack["preferred_duration"] = config.MAX_RUN

  log_msg("found new hack: %s" % hack["name"])

  screenhacks.append( hack )
  paint_hack_list()
  
########################################################################

def random_hack_id():
  global total_odds

  hack_id = 0
  totals = []
  running_total = 0

  total_odds = 0
  for i in range( len(screenhacks) ):
    h = screenhacks[i]
    if hack_run_count == 0 or h["run_count"] == 0:
      h["odds"] = 100
    elif i == hack_index:
      h["odds"] = 0
    else:
      h["odds"] = int(((hack_run_count - h["run_count"]) * 100) / hack_run_count)
    total_odds += h["odds"]

    running_total += h["odds"]
    totals.append(running_total)

  rnd = random.random() * running_total
  for i, total in enumerate(totals):
    if rnd < total:
      hack_id = i
      break
      
  return hack_id

########################################################################

selected_hack = 0

def hack_up():
  global selected_hack, hack_list_idx

  if selected_hack > 0:
    selected_hack -= 1
    if selected_hack < hack_list_idx:
      hack_list_idx -= 1
    paint_hack_list()

########################################################################

def hack_down():
  global selected_hack, hack_list_idx

  if selected_hack < len(screenhacks) - 1:
    selected_hack += 1
    if selected_hack >= HACK_WINDOW_LINE_CT + hack_list_idx:
      hack_list_idx += 1
    paint_hack_list()

########################################################################

def set_hack():
  while not stop_hack(hack_index):
    sleep(0.001)
  start_hack( selected_hack )

########################################################################

def next_hack_id():

  last_hack_rec = screenhacks[hack_index]

  logo_required = False
  dynamic_required = False

  if found_logos and not last_hack_rec["provides_logo"]:
    logo_required = True
  if found_dynamic and not last_hack_rec["is_dynamic"]:
    dynamic_required = True
  
  new_hack_id = random_hack_id()
  new_hack_rec = screenhacks[new_hack_id]
  while ((not new_hack_rec["provides_logo"]) and logo_required) or ((not new_hack_rec["is_dynamic"]) and dynamic_required):
    new_hack_id = random_hack_id()
    new_hack_rec = screenhacks[new_hack_id]

  return new_hack_id

########################################################################

def load_hacks(reloading=False):

  cache_status()
  log_msg("reloading hack list...")
  
  if reloading:
    set_status("LOOKING FOR NEW HACKS...")
  else:
    set_status("LOADING HACKS...")

  for root, dirnames, filenames in walk(hacks_dir):
    for filename in fnmatch.filter(filenames, '*.py'):
      register_hack(join(root, filename))

  restore_status()

########################################################################

def start_hack(new_hack_id):
  global hack_run_count, hack_index, screenhacks
  
  hack_run_count += 1
  hack_index = new_hack_id
  hack_rec = screenhacks[new_hack_id]
  hack_rec["start_time"] = time()
  hack_rec["termination_clock"] = 0
  hack_rec["state"] = constants.ST_RUNNING
  hack_rec["proc"] = Popen( [ hack_rec["path"],
                                 "--time",
                                 str(hack_rec["preferred_duration"]) ] )
  hack_rec["run_count"] += 1
  set_status( "RUNNING %s " % hack_rec["name"] )
  log_msg( "starting %s; will run for %s secs" % ( hack_rec["name"], hack_rec["preferred_duration"] ))
  paint_hack_list()

########################################################################

def stop_hack(hack_id):

  hack_rec = screenhacks[hack_id]
  if hack_rec["state"] == constants.ST_RUNNING:
    # request exit
    hack_rec["proc"].terminate()
    hack_rec["state"] = constants.ST_TERMINATING
    return False
  elif hack_rec["state"] == constants.ST_TERMINATING:
    if hack_rec["proc"].poll() is not None:
      # the screenhack that was running has terminated
      hack_rec["state"] = constants.ST_STOPPED
      return True
    else:
      hack_rec["termination_clock"] += 1
      if hack_rec["termination_clock"] > config.MAX_DWELL:
        # the screenhack is taking too long to terminate
        # shoot it in the head
        hack_rec["proc"].kill()
        return False

########################################################################
# the global "manual" variable determines whether hacks are
# automatically advancing or under manual control

def toggle_manual_control():
  global manual

  if manual:
    manual = False
    log_msg("manual control released; auto-advance resumed")
  else:
    manual = True
    log_msg("manual control set")
      
  paint_status()
  paint_hack_list()

########################################################################

last_update = time()

def update_screen():
  global last_update
  
  if CURSES_ENABLED and (time() - last_update > PAINT_INTERVAL):
    paint_status()
    last_update = time()

########################################################################

signal.signal(signal.SIGINT,bail)

setup_screen()
load_hacks()
hack_index = next_hack_id()
start_hack(hack_index)

paint_hack_list()

while True:

  if CURSES_ENABLED:
    key = stdscr.getch()
    if key == ord('q'):
      break
    elif key == ord('r'):
      load_hacks(reloading=True)
    elif key == ord('m'):
      toggle_manual_control()
    elif key == ord("\n"):
      set_hack()
    elif key == curses.KEY_DOWN:
      hack_down()
    elif key == curses.KEY_UP:
      hack_up()   

  hack_rec = screenhacks[hack_index]
  hack_rec["elapsed"] = time() - hack_rec["start_time"]
  if not manual and (hack_rec["elapsed"] > hack_rec["preferred_duration"]):
    # the currently running screenhack has run out of time
    set_status("REQUESTING EXIT of %s" % hack_rec["name"])
    while not stop_hack(hack_index):
      sleep(0.001)

    hack_index = next_hack_id()
    start_hack(hack_index)

  update_screen()

  sleep(0.001)

bail()

########################################################################
