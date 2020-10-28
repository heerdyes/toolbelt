#!/usr/bin/env python
from PIL import Image,ImageDraw
import sys
import time
from random import randint

def randstr(n):
  rs=''
  for i in range(n):
    rs+=chr(randint(97,122))
  return rs

# cli params
if len(sys.argv) != 3:
  print('usage: picmerge.py <realworld.jpg> <genart.png> <r> <g> <b> <m> <n>')
  raise SystemExit
rwfn=sys.argv[1]
gafn=sys.argv[2]

irw=Image.open(rwfn)
iga=Image.open(gafn)

rww,rwh=irw.size
gaw,gah=iga.size

print('[info] iout dimensions: %d,%d'%(rww,rwh))
iout=Image.new('RGB',(rww,rwh),(0,0,0))

tr,tg,tb=int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
rgbthresh=(tr,tg,tb)
m,n=int(sys.argv[6]),int(sys.argv[7])
print('[info] rgb threshold: %s'%str(rgbthresh))
print('[info] m,n = %d,%d'%(m,n))

rwsx,rwsy=rww/2-gaw/2,rwh/2-gah/2
print('[info] rwsx,rwsy = %d,%d'%(rwsx,rwsy))

progc='-=>._'
np=len(progc)
print('[progress] ',end='',flush=True)
startts=time.time()
for i in range(rwh):
  if i%100==0:
    print('%s'%progc[randint(0,np-1)],end='',flush=True)
  for j in range(rww):
    rwpix=irw.getpixel((j,i))
    if j>=rwsx and j<rwsx+gaw and i>=rwsy and i<rwsy+gah:
      gapix=iga.getpixel((j-rwsx,i-rwsy))
      if gapix[1]>rgbthresh[1]:
        rout=round((m*gapix[0]+n*rwpix[0])/(m+n))
        gout=round((m*gapix[1]+n*rwpix[1])/(m+n))
        bout=round((m*gapix[2]+n*rwpix[2])/(m+n))
        iout.putpixel((j,i),(rout,gout,bout))
      else:
        iout.putpixel((j,i),rwpix)
    else:
      iout.putpixel((j,i),rwpix)
stopts=time.time()
print('\n[watch] operation took %f seconds'%(stopts-startts))
iout.save(randstr(8)+'.jpg')

