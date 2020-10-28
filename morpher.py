#!/usr/bin/env python
import wavio
import numpy as np
from PIL import Image,ImageDraw
from random import randint
import sys
from math import cos,sin,pi
import time

# classyfication
# image pen (invisible turtle that is!)
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
    
    def displacelr(self,delta):
        self.rt(90)
        self.fdjmp(delta)
        self.lt(90)

    def bkjmp(self,r):
        self.fd(-r)

    def lt(self,a):
        self.a+=a

    def rt(self,a):
        self.lt(-a)


# funktionality
def exprdiv(x,d):
    if '/' in x:
        lr=x.split('/')
        return round(d/float(lr[1]))
    else:
        return round(float(x))
        
# config parsing
def parseconfig(cfgfn):
    with open(cfgfn) as cfgf:
        print('[cfg] parsing config file %s'%cfgfn)
        l1=cfgf.readline().rstrip().split(' ')
        if l1[0]=='new':
            iw,ih=int(l1[1]),int(l1[2])
            x=Image.new('RGB',(iw,ih),(0,0,0))
            print('[cfg][l1] initialized new image, size: (%d,%d)'%(iw,ih))
        else:
            x=Image.open(l1[0])
            iw,ih=x.size
            print('[cfg][l1] read file %s, size: (%d,%d)'%(l1[0],iw,ih))
        l2=cfgf.readline().rstrip().split(' ')
        ix,iy=exprdiv(l2[0],iw),exprdiv(l2[1],ih)
        l3=cfgf.readline().rstrip().split(' ')
        color=(int(l3[0]),int(l3[1]),int(l3[2]))
        pm,pn=int(l3[3]),int(l3[4])
        l4=cfgf.readline().rstrip().split(' ')
        rtcoeff,rtdelta=float(l4[0]),float(l4[1])
        l5=cfgf.readline().rstrip().split(' ')
        fdcoeff,fddelta=float(l5[0]),float(l5[1])
        l6=cfgf.readline().rstrip().split(' ')
        mode,algonm=l6[0],l6[1]
        l7=cfgf.readline().rstrip().split(' ')
        print('[cfg][l7] output set to %s.'%l7[0])
        if l7[0]=='show':
            print('[cfg][l7] will not write to file')
            output=(l7[0],'')
        elif l7[0]=='save':
            outfn=l7[1]
            print('[cfg][l7] will write to file %s'%outfn)
            output=(l7[0],outfn)
        print('[cfg] configuration loaded from '+cfgfn)
        return x,iw,ih,ix,iy,color,pm,pn,rtcoeff,rtdelta,fdcoeff,fddelta,mode,algonm,output

# functions implementing different algorithms
def algo00(nsec,arate,n,mode,nmad,cnv,rtdelta,rtcoeff,fddelta,fdcoeff,ipen):
    for i in range(nsec+1):
        wa=i*arate
        wz=wa+arate
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

def algo01(nsec,arate,n,mode,nmad,cnv,rtdelta,rtcoeff,fddelta,fdcoeff,ipen):
    for i in range(nsec+1):
        wa=i*arate
        wz=wa+arate
        if wz>n:
            wz=n
        print('t=%04d [%09d-%09d]'%(i,wa,wz))
        for j in range(wz-wa):
            if mode=='cnv':
                cnvdat=cnv[wa+j]
                ipen.displacelr(cnvdat*fdcoeff)
                ipen.fdjmp(fddelta)
                ipen.lt(rtdelta)
            elif mode=='nrm':
                nmdat=nmad[wa+j,0]
                ipen.displacelr(nmdat*fdcoeff)
                ipen.fdjmp(fddelta)
                ipen.lt(rtdelta)
                
def algowave_00(nsec,arate,n,mode,nmad,cnv,rtdelta,rtcoeff,fddelta,fdcoeff,ipen):
    for i in range(nsec+1):
        wa=i*arate
        wz=wa+arate
        if wz>n:
            wz=n
        print('t=%04d [%09d-%09d]'%(i,wa,wz))
        for j in range(wz-wa):
            if mode=='cnv':
                cnvdat=cnv[wa+j]
                ipen.fdjmp(fddelta*sin(fdcoeff*j))
                ipen.lt(rtdelta*sin(rtcoeff*j))
            elif mode=='nrm':
                nmdat=nmad[wa+j,0]
                ipen.fdjmp(fddelta*sin(fdcoeff*j))
                ipen.lt(rtdelta*sin(rtcoeff*j))

def algowave_01(nsec,arate,n,mode,nmad,cnv,rtdelta,rtcoeff,fddelta,fdcoeff,ipen):
    for i in range(nsec+1):
        wa=i*arate
        wz=wa+arate
        if wz>n:
            wz=n
        print('t=%04d [%09d-%09d]'%(i,wa,wz))
        for j in range(wz-wa):
            if mode=='cnv':
                cnvdat=cnv[wa+j]
                ipen.fdjmp(fddelta*sin(cnvdat*fdcoeff*j))
                ipen.lt(rtdelta)
            elif mode=='nrm':
                nmdat=nmad[wa+j,0]
                ipen.fdjmp(fddelta*sin(nmdat*fdcoeff*j))
                ipen.lt(rtdelta)

# flow begins
# cli params
if len(sys.argv) != 3:
  print('usage: morpher.py <filename.wav> <config.cfg>')
  raise SystemExit
fn=sys.argv[1]

# soundwave reading
a=wavio.read(fn)
ad=np.array(a.data,dtype=np.float)
nmad=ad/(np.max(np.abs(ad),axis=0))
n=len(ad)
print('[wav] samples: %d'%n)
print('[wav] rate: %d'%a.rate)

# read config
cfgfn=sys.argv[2]
x,iw,ih,ix,iy,color,pm,pn,rtcoeff,rtdelta,fdcoeff,fddelta,mode,algonm,output=parseconfig(cfgfn)

cnv=None
if mode=='cnv':
    print('[cnv] performing self convolution. usually time consuming.')
    cnvt0=time.time()
    cnv=np.convolve(nmad[:,0],nmad[:,0],'same')
    cnvtN=time.time()
    print('[cnv][watch] convolution took %f seconds'%(cnvtN-cnvt0))

# algomap
algmap={'algo00':algo00,
        'algo01':algo01,
        'algo02':algowave_00,
        'algo03':algowave_01}

# image writing
ipen=IPen(iw,ih,ix,iy,x,color,pm,pn)
nsec=n//a.rate
print('[info] nsec=',nsec)

startts=time.time()
algmap[algonm](nsec,a.rate,n,mode,nmad,cnv,rtdelta,rtcoeff,fddelta,fdcoeff,ipen)
stopts=time.time()

print('[watch] operation took %f seconds'%(stopts-startts))
print('[alert] bounds exceeded %d times'%ipen.nexc)
if output[0]=='show':
    x.show()
elif output[0]=='save':
    x.save(output[1])
else:
    print('[output] unknown output mode: %s'%output[0])

