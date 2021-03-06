# render.py
#
# Defines the Render class.
#

import curses
import curses.textpad
import os
import w3m
import util
import ast
from subprocess import Popen, PIPE
import re

SEARCHBAR_OFFSET = 2
SEARCHLEFT_OFFSET = 8
W3MIMGDISPLAY_PATH = '/usr/lib/w3m/w3mimgdisplay'
W3MIMGDISPLAY_OPTIONS = []


class Renderer(object):
    def __init__(self, w3m_binary='/usr/lib/w3m/w3mimgdisplay'):
        p = Popen(["tput cols"], stdout=PIPE,shell=True)
        out = p.communicate()
        self.COLS = int(re.search('[0-9]+',str(out)).group(0))
        p = Popen(["tput lines"], stdout=PIPE,shell=True)
        out = p.communicate()
        self.LINES = int(re.search('[0-9]+',str(out)).group(0))
        self.current_image = None 
        self.scr = curses.initscr()
        curses.noecho()         # don't echo characters
        curses.cbreak()         # no key buffering
        self.scr.keypad(True) # let curses handle keys
        self.scr.clear()
        curses.curs_set(0) 
        self.results = None
        self.first_pic = True
        self.w3m_enabled = False
        self.process = Popen([w3m_binary] + W3MIMGDISPLAY_OPTIONS,
          stdin=PIPE, stdout=PIPE, universal_newlines=True)
        if os.path.exists(w3m_binary):
          self.w3m = w3m.W3MImage_display(w3m_binary)
          self.w3m_enabled = True
         
        # Create result box delimiter
       # for i in range(self.COLS - 1):
       #   self.scr.insch(1, i, curses.ACS_HLINE)
        self.scr.refresh()

        # Set selection index to search
        self.index = -1

    def update(self):
        p = Popen(["tput cols"], stdout=PIPE,shell=True)
        out = p.communicate()
        self.COLS = int(re.search('[0-9]+',str(out)).group(0))
        p = Popen(["tput lines"], stdout=PIPE,shell=True)
        out = p.communicate()
        self.LINES = int(re.search('[0-9]+',str(out)).group(0))
        
    def handle_scroll(self):
        k = self.scr.getkey()
        self.end()
        print(k)
        exit()

    def loop(self):
        self.handle_scroll()
        return 0

    # This will draw into a box defined by the passed in parameters
    def _draw_image(self, temp_file, x, y, w, h, re=False):
        # Font dimensions
        fw, fh = util.get_font_dimensions()
        # Image dimensions
        iw, ih = util.get_image_dimensions(temp_file)
        # Box dimensions
        bw, bh = w * fw, h *fh
        
        # Scale the image to the box
        if iw > ih:
          scale = 1.0 * bw / iw
        else:
          scale = 1.0 * bh / ih
        iw = scale * iw
        ih = scale * ih

        # Get margin
        x_m = (bw - iw) / 2
        #x_m = 0
        y_m = (bh - ih) / 2
        #y_m = 0

        # Get x, y coordinates
        x = x * fw - iw/2
        y = y * fh + y_m
        #self.w3m.clear(x, y, w=iw, h=ih)
        self.w3m.draw(temp_file, 1, x, y, w=iw, h=ih)

    # This will clear an image defined by the passed in parameters
    def _clear_image(self, temp_file, x, y, w, h, re=False):
        # Font dimensions
        fw, fh = util.get_font_dimensions()
        # Image dimensions
        iw, ih = util.get_image_dimensions(temp_file)
        # Box dimensions
        bw, bh = w * fw, h *fh
        
        # Scale the image to the box
        if iw > ih:
          scale = 1.0 * bw / iw
        else:
          scale = 1.0 * bh / ih
        iw = scale * iw
        ih = scale * ih

        # Get margin
        x_m = (bw - iw) / 2
        y_m = (bh - ih) / 2

        # Get x, y coordinates
        #x = x * fw + x_m
        x = x * fw - iw/2
        y = y * fh + y_m
        #self.w3m.clear(x, y, w=iw, h=ih)
        #self.w3m.clear(x, y, iw, ih)
        cmd = "6;{x1};{y1};{w1};{h1}\n4;\n3;\n".format(
            x1 = x,
            y1 = y,
            w1 = iw,
            h1 = ih)
        self.process.stdin.write(cmd)
        self.process.stdin.flush()
        self.process.stdout.readline()
        print("cleared")



    def draw_image(self, image):
          if (self.w3m_enabled):
            try:
                self._draw_image(image, self.COLS - self.COLS/2, SEARCHBAR_OFFSET, self.COLS/2, self.LINES - SEARCHBAR_OFFSET)
                self.current_image = image
            except Exception as e:
                # Who cares? it's just a picture.
                self.end()
                print(str(e))
                pass
        #self.results.noutrefresh(0, 0, SEARCHBAR_OFFSET, 0, self.LINES-1, self.COLS-1)

    def clear_image(self):
          if (self.w3m_enabled):
            try:
                self.scr.clear()
                # Create result box delimiter
                self.scr.refresh()
            except Exception as e:
                # Who cares? it's just a picture.
                self.end()
                print(str(e))
                pass
        #self.results.noutrefresh(0, 0, SEARCHBAR_OFFSET, 0, self.LINES-1, self.COLS-1)

    # View for user to select a package from a list of options

    def end(self):
        self.clear_image()
        self._clear_image(self.current_image,self.COLS - self.COLS/2, SEARCHBAR_OFFSET, self.COLS/2, self.LINES - SEARCHBAR_OFFSET)
        self.process.kill()
        self.scr.clear()
        curses.nocbreak()
        self.scr.keypad(False)
        curses.echo()
        curses.endwin()

