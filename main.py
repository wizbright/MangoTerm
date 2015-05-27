import os
import sys

manga_dir = sys.argv[1]
pics = sorted(os.listdir(manga_dir))
print(pics)
