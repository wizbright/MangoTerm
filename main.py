import os
import render
import sys

manga_dir = os.path.abspath(sys.argv[1])
pics = sorted(os.listdir(manga_dir))
dp = pics[0]
r = render.Renderer()
#r.draw_image(dp)
x = 0
draw = True
r.draw_image(manga_dir + '/' + dp)
while(x != 113):
    x = r.scr.getch()
    if draw:
        draw = False
    r.scr.refresh()
r.w3m.terminate()
r.end()
