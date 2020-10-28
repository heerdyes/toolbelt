#!/usr/bin/env python
import pydub
from pydub import AudioSegment
import sys

# cli params
if len(sys.argv) != 4:
  print('usage: chopper.py <filename.mp3> <startms> <stopms>')
  raise SystemExit
fn=sys.argv[1]

t1,t2=int(sys.argv[2]),int(sys.argv[3])
x=AudioSegment.from_mp3(fn)
n=len(x)
if t1<0 or t1>(n-1) or t2<0 or t2>(n-1):
  print('[ERR] bounds exceeded. either %d or %d is outside [0,%d]'%(t1,t2,n))
  raise SystemExit
fx=x[t1:t2]
fout=fn.split('.')[0]+'.wav'
fx.export(fout,format='wav')

