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

SEARCHBAR_OFFSET = 2
SEARCHLEFT_OFFSET = 8

class Renderer(object):
    def __init__(self, w3m_binary='/usr/lib/w3m/w3mimgdisplay'):
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

        if os.path.exists(w3m_binary):
          self.w3m = w3m.W3MImage_display(w3m_binary)
          self.w3m_enabled = True
         
        # Create a search box

        # Create result box delimiter
        for i in range(curses.COLS - 1):
          self.scr.insch(1, i, curses.ACS_HLINE)
        self.scr.refresh()

        # Set selection index to search
        self.index = -1
        
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
        y_m = (bh - ih) / 2

        # Get x, y coordinates
        x = x * fw + x_m
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
        x = x * fw + x_m
        y = y * fh + y_m
        #self.w3m.clear(x, y, w=iw, h=ih)
        self.w3m.clear(x, y, iw, ih)

    def draw_image(self, image):
          if (self.w3m_enabled):
            try:
                self._draw_image(image, curses.COLS - curses.COLS/2, SEARCHBAR_OFFSET, curses.COLS/2, curses.LINES - SEARCHBAR_OFFSET)
                self.current_image = image
            except Exception as e:
                # Who cares? it's just a picture.
                self.end()
                print(str(e))
                pass
        #self.results.noutrefresh(0, 0, SEARCHBAR_OFFSET, 0, curses.LINES-1, curses.COLS-1)

    # View for user to select a package from a list of options

    def end(self):
        self._clear_image(self.current_image,curses.COLS - curses.COLS/2, SEARCHBAR_OFFSET, curses.COLS/2, curses.LINES - SEARCHBAR_OFFSET)
        self.scr.clear()
        curses.nocbreak()
        self.scr.keypad(False)
        curses.echo()
        curses.endwin()

