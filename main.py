import os
import render
import sys
import curses
import shutil
import tempfile

#Opening the zip file
#shutil.register_archive_format(".rar")
#shutil.register_unpack_format(RAR, .rar, function)
tempdir = tempfile.mkdtemp()
shutil.unpack_archive(sys.argv[1], tempdir)

pics = sorted(os.listdir(tempdir))
pos = 0
r = render.Renderer()
#r.draw_image(dp)
x = 0
draw = True

r.draw_image(tempdir + '/' +  pics[pos]) # Draws first image
while(x != 113): # As long as q is not pressed
    x = r.scr.getch()
    if (x == curses.KEY_RESIZE): # Allows the image to resize and redraws
        r.scr.refresh()
        r.update()
        r.draw_image(tempdir + '/' +  pics[pos])
    if (x == 260): # Pressing left arrow key goes to the previous image
      if (pos > 0):
         pos-=1
         r.clear_image()
         r.draw_image(tempdir + '/' +  pics[pos])
    if (x == 261): # Pressing right arrow key advances the image forward
      if (pos < len(pics) - 1):
        pos+=1
        r.clear_image()
        r.draw_image(tempdir + '/' +  pics[pos])
    if(x == 99): # Pressing c clears the image
      r.clear_image()
    if (x == 100): # Pressing d redraws the image
      r.draw_image(tempdir + '/' +  pics[pos])
r.w3m.terminate()
r.end()
