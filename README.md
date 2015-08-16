# farnsworth
the central jukebox script schedules and transitions between the
individual "hack" scripts that are responsible for actually painting
the display.

the farnsworth library provides the individual hack scripts with common
functionality such as character generation, bitmap loading, and sprites
with animation and tweening.

##configuration
general, systemwide configuration is accomplished by editing the
config.py file

set the ip address to "localhost" if you're running a local opengl
simulator; otherwise, set the ip address of the openpixelcontrol target

```python
IP_ADDRESS = 'localhost'
PORT = 7890
```
set the global framerate

```python
FPS = 30
```

set the resolution of the target display

```python
PIXELS_ACROSS = 95
PIXELS_HIGH = 16
```

set the spacing between pixels on the target display. this setting is
used to generate the layout file for the opengl simulator. it does
nothing in production use.

```python
PIXEL_SPACING = 0.15
```

the sequence in which color channel data should be sent to the target
display. probably doesn't need changing.

```python
COLOR_ORDER = [ constants.COLOR_R, constants.COLOR_G, constants.COLOR_B ]
```

set the maximum time a hack will be allowed to run beyond its allotted
time before having its process forcibly killed, in microseconds

```python
MAX_DWELL = 1000000
```

set the maximum runtime a hack will be allowed to schedule. hacks
requesting longer time slices will be run this long, in decimal seconds

```python
MAX_RUN = 30.0
```

set the default time allotted to hacks that don't specify a duration, in
decimal seconds

```python
TIME_SLICE = 5.0
```

##invocation
run the start_jukebox.sh script to initialize farnsworth. by default,
farnsworth's jukebox provides an interactive curses interface. if your
terminal is too small, you'll be limited to non-interactive silent mode.

###interactive mode
interactive mode exposes the jukebox's internal state and allows you to
control it manually as desired.

key | function
----|---------
q | shutdown the farnsworth system
r | rescan hacks folder so as to make newly-added hacks available
m | toggle manual mode, in which each hack runs until a new one is selected
[enter] | stop the current hack and (re)load the highlighted one
[down arrow] | move the hack selection downwards
[up arrow] | move the hack selection upwards
