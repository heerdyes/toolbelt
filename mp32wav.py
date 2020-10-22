#!/usr/bin/env python
from os import path
from pydub import AudioSegment
import sys

arglen=len(sys.argv)
if arglen != 3:
  print('usage: python mp32wav.py <src.mp3> <dst.wav>')
  exit(0)

src=sys.argv[1]
dst=sys.argv[2]
print('loading file: '+src)
snd=AudioSegment.from_mp3(src)
print('generating file: '+dst)
snd.export(dst,format='wav')
