import cv2, numpy as np, sys
im=cv2.imread('reference/real-mug-fact-to-file.jpg'); h,w=im.shape[:2]
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); real=((g<75)).astype(np.uint8); real[:, 262:]=0; real[:310]=0; real[730:]=0
real=cv2.morphologyEx(real,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); n,l,st,_=cv2.connectedComponentsWithStats(real); k=1+np.argmax(st[1:,4]); real=(l==k).astype(np.uint8); real=cv2.morphologyEx(real,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
a=cv2.imread(sys.argv[1],cv2.IMREAD_UNCHANGED); X0,X1,Y0,Y1=89,797,168,823; m=(a[...,3]>40).astype(np.uint8); ys,xs=np.where(m); kk=(Y1-Y0+1)/(ys.max()-ys.min()+1)
M=np.float32([[kk,0,(X0+X1)/2-kk*(xs.min()+xs.max())/2],[0,kk,(Y0+Y1)/2-kk*(ys.min()+ys.max())/2]])
c=cv2.warpAffine(a,M,(w,h)); dark=((c[...,3]>40)&(c[...,:3].max(2)<60)).astype(np.uint8); dark[:,262:]=0; dark[:310]=0; dark=cv2.morphologyEx(dark,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
inter=(real&dark).sum(); print('IoU',round(inter/((real|dark).sum()),3),'real only',int((real&~dark&1).sum()),'model only',int((dark&~real&1).sum()))
o=im.copy(); o[(real==1)&(dark==0)]=(0,0,255); o[(dark==1)&(real==0)]=(255,255,0); cv2.imwrite(sys.argv[2],o[280:740,60:340])
