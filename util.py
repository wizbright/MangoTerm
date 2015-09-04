#!/usr/bin/python
# util.py
#
# Defines a various utility variables, functions and classes.
#

import os
import subprocess
import struct
import sys
import fcntl
import termios
import imghdr


def get_image_dimensions(fname):
      # Determine the image type of fhandle and return its size.
      fhandle = open(fname, 'rb')
      head = fhandle.read(24)
      if len(head) != 24:
          return
      if imghdr.what(fname) == 'png':
          check = struct.unpack('>i', head[4:8])[0]
          if check != 0x0d0a1a0a:
              return
          width, height = struct.unpack('>ii', head[16:24])
      elif imghdr.what(fname) == 'gif':
          width, height = struct.unpack('<HH', head[6:10])
      elif imghdr.what(fname) == 'jpeg':
          try:
              fhandle.seek(0) # Read 0xff next
              size = 2
              ftype = 0
              while not 0xc0 <= ftype <= 0xcf:
                  fhandle.seek(size, 1)
                  byte = fhandle.read(1)
                  while ord(byte) == 0xff:
                      byte = fhandle.read(1)
                  ftype = ord(byte)
                  size = struct.unpack('>H', fhandle.read(2))[0] - 2
              # We are at a SOFn block
              fhandle.seek(1, 1)    # Skip `precision' byte.
              height, width = struct.unpack('>HH', fhandle.read(4))
          except Exception: #IGNORE:W0703
              return
      else:
          return
      return width, height

def get_font_dimensions():
      # Get the height and width of a character displayed in the terminal in
      # pixels.
      s = struct.pack("HHHH", 0, 0, 0, 0)
      fd_stdout = sys.stdout.fileno()
      x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
      rows, cols, xpixels, ypixels = struct.unpack("HHHH", x)
      return (xpixels // cols), (ypixels // rows)

