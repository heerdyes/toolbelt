#!/user/bin/env python
from os import path
from pydub import AudioSegment
import sys

arglen=len(sys.argv)
if arglen != 3:
  print('usage: python wav2mp3.py <src.wav> <dst.mp3>')
  exit(0)

src=sys.argv[1]
dst=sys.argv[2]
print('loading file: '+src)
snd=AudioSegment.from_wav(src)
print('generating file: '+dst)
snd.export(dst,format='mp3')
