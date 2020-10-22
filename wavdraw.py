#!/usr/bin/env python
import wavio
import numpy as np
from PIL import Image
from random import randint
import sys

# cli params
if len(sys.argv) != 2:
  print('usage: python wavdraw.py <filename.wav>')
  raise SystemExit
fn=sys.argv[1]

# sound reading
a=wavio.read(fn)
maxspike=np.amax(a.data,axis=0)
minspike=np.amin(a.data,axis=0)
ad=a.data
alen=len(ad)
maxspikeint=int(maxspike[0])
minspikeint=int(minspike[0])
sqspikeint=max(maxspikeint*maxspikeint,minspikeint*minspikeint)
print('maxspike: ',maxspikeint)
print('minspike: ',minspikeint)
print('sqspike: ',sqspikeint)

# image writing
iw=1400
ih=200
atoi_ratio=alen//iw
print('atoi_ratio -> %d/%d = %d'%(alen,iw,atoi_ratio))

# visualization
ctr=0
x=Image.new('RGB',(iw,ih),(0,0,0))
for i in range(iw):
  limA=ctr
  limZ=limA+atoi_ratio
  rndloc=randint(limA,limZ)
  lr=ad[rndloc]
  lrint=int(lr[0])
  #print('ad[%d] = %s'%(rndloc,lr))
  ampfrac=(lrint*lrint)/sqspikeint
  r=0
  g=0
  if ampfrac<=0.333333:
    r=0
    g=round((ampfrac/0.3333334)*255)
  elif ampfrac>0.333333 and ampfrac<=0.666666:
    r=round(((ampfrac-0.333333)/0.3333334)*255)
    g=255
  else:
    r=255
    g=255-round(((ampfrac-0.666666)/0.3333334)*255)
  color=(r,g,0,255)
  for j in range(ih):
    x.putpixel((i,j),color)
  ctr+=atoi_ratio

x.show()

