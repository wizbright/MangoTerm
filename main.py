import os
import render 
import sys
import curses

manga_dir = os.path.abspath(sys.argv[1])
pics = sorted(os.listdir(manga_dir))
pos = 0
r = render.Renderer()
#r.draw_image(dp)
x = 0
draw = True

r.draw_image(manga_dir + '/' +  pics[pos])
while(x != 113):
    x = r.scr.getch()
    if (x == curses.KEY_RESIZE):
        r.scr.refresh()
        r.update()
        r.draw_image(manga_dir + '/' +  pics[pos])
    if (x == 260):
      if (pos > 0):
         pos-=1 
         r.clear_image()
         r.draw_image(manga_dir + '/' +  pics[pos])
    if (x == 261):
      if (pos < len(pics) - 1):
        pos+=1
        r.clear_image()
        r.draw_image(manga_dir + '/' +  pics[pos])
    if(x == 99):
      r.clear_image()
    if (x == 100):
      r.draw_image(manga_dir + '/' +  pics[pos])
r.w3m.terminate()
r.end()
