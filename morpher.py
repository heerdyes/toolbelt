#!/usr/bin/env python
import wavio
import numpy as np
from PIL import Image,ImageDraw
from random import randint
import sys
from math import cos,sin,pi

# image pen
class IPen:
    def __init__(self,bx,by,x,y,img,color,m,n):
        self.x,self.y=x,y
        self.a=0
        self.img=img
        self.color=color
        self.bx,self.by=bx,by
        self.m,self.n=m,n
        self.nexc=0

    def fdjmp(self,r):
        x2=round(self.x+r*cos(self.a*pi/180))
        y2=round(self.y-r*sin(self.a*pi/180))
        # boundary checking
        if x2>=self.bx or y2>=self.by or x2<0 or y2<0:
            self.nexc+=1
            return
        oldpix=self.img.getpixel((x2,y2))
        rv=round((self.m*oldpix[0]+self.n*self.color[0])/(self.m+self.n))
        gv=round((self.m*oldpix[1]+self.n*self.color[1])/(self.m+self.n))
        bv=round((self.m*oldpix[2]+self.n*self.color[2])/(self.m+self.n))
        self.img.putpixel((x2,y2),(rv,gv,bv))
        self.x=x2
        self.y=y2

    def bkjmp(self,r):
        self.fd(-r)

    def lt(self,a):
        self.a+=a

    def rt(self,a):
        self.lt(-a)


# cli params
if len(sys.argv) != 3:
  print('usage: morpher.py <filename.wav> <config.cfg>')
  raise SystemExit
fn=sys.argv[1]

# sound reading
a=wavio.read(fn)
ad=np.array(a.data,dtype=np.float)
nmad=ad/(np.max(np.abs(ad),axis=0))
n=len(ad)
print(n)
print(a.rate)

# read config
cfgfn=sys.argv[2]
print('[cfg] reading '+cfgfn)
with open(cfgfn) as cfgf:
    l1=cfgf.readline().rstrip().split(' ')
    iw,ih=int(l1[0]),int(l1[1])
    l2=cfgf.readline().rstrip().split(' ')
    ix,iy=int(l2[0]),int(l2[1])
    l3=cfgf.readline().rstrip().split(' ')
    color=(int(l3[0]),int(l3[1]),int(l3[2]))
    pm,pn=int(l3[3]),int(l3[4])
    l4=cfgf.readline().rstrip().split(' ')
    rtcoeff,rtdelta=float(l4[0]),float(l4[1])
    l5=cfgf.readline().rstrip().split(' ')
    fdcoeff,fddelta=float(l5[0]),float(l5[1])
    l6=cfgf.readline().rstrip()
    mode=l6
    print('configuration loaded from '+cfgfn)

if mode=='cnv':
    cnv=np.convolve(nmad[:,0],nmad[:,0],'same')

# image writing
x=Image.new('RGB',(iw,ih),(0,0,0))
ipen=IPen(iw,ih,ix,iy,x,color,pm,pn)
nsec=n//a.rate
print('nsec=',nsec)
for i in range(nsec+1):
    wa=i*a.rate
    wz=wa+a.rate
    if wz>n:
        wz=n
    print('t=%04d [%09d-%09d]'%(i,wa,wz))
    for j in range(wz-wa):
        if mode=='cnv':
            cnvdat=cnv[wa+j]
            ipen.fdjmp(fddelta+cnvdat*fdcoeff)
            ipen.lt(rtdelta+cnvdat*rtcoeff)
        elif mode=='nrm':
            nmdat=nmad[wa+j,0]
            ipen.fdjmp(fddelta+nmdat*fdcoeff)
            ipen.lt(rtdelta+nmdat*rtcoeff)

print('bounds exceeded %d times'%ipen.nexc)
x.show()
