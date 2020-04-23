import os
from os import path
import shutil

src = "/home/rupen/Desktop/cahss courses"
dst = "/home/rupen/Desktop/cahss short courses"

f = open('01shortlist.txt', 'r')
x = f.read().splitlines()
f.close()

for i in os.listdir(src):
    if i in x:
        shutil.copy(path.join(src, i), dst)
