# farnsworth
text and graphics library for openpixelcontrol-compatible LED signage

---

###configuration

####config.py

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

set the default time allotted to hacks that don't specify a duration

```python
TIME_SLICE = 5.0
```
