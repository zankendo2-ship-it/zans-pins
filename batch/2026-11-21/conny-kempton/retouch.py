"""Local fixes on the FLUX pictures (864x1536): hide faces in natural shadow, remove number-cloth text, bandages and blazes.
Constitution Hill = bay, small white star, no sourced leg markings. python3 retouch.py"""
import cv2, numpy as np, os
D=os.path.dirname(os.path.abspath(__file__))
def soft(shape,box,blur):
    m=np.zeros(shape[:2],np.float32); x0,y0,x1,y1=box; m[y0:y1,x0:x1]=1; return cv2.GaussianBlur(m,(0,0),blur)[...,None]
def shade(im,box,k,blur=6):                      # darken (shadow) inside a soft box
    m=soft(im.shape,box,blur); return (im*(1-m*(1-k))).astype(np.float32)
def kill_white(im,box,to=(28,40,62),thr=120,blur=3):   # pale, unsaturated pixels in the box -> a dark/bay colour, keeping shading
    x0,y0,x1,y1=box; roi=im[y0:y1,x0:x1]; hsv=cv2.cvtColor(np.clip(roi,0,255).astype(np.uint8),cv2.COLOR_BGR2HSV)
    w=((hsv[...,2]>thr)&(hsv[...,1]<90)).astype(np.float32); w=cv2.GaussianBlur(cv2.dilate(w,np.ones((3,3))),(0,0),blur)[...,None]
    lum=(roi.mean(2,keepdims=True)/255.0); col=np.array(to,np.float32)*(0.55+0.9*lum)
    im[y0:y1,x0:x1]=roi*(1-w)+col*w; return im
def clean_cloth(im,box,k=15,thr=165):       # dark marks (numbers, lettering) on a pale cloth -> filled from the cloth round them
    x0,y0,x1,y1=box; roi=np.clip(im[y0:y1,x0:x1],0,255).astype(np.uint8); g=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    pale=(g>thr).astype(np.uint8); closed=cv2.morphologyEx(pale,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
    mark=cv2.dilate(((closed==1)&(pale==0)).astype(np.uint8),np.ones((3,3),np.uint8))
    im[y0:y1,x0:x1]=cv2.inpaint(roi,mark*255,4,cv2.INPAINT_TELEA); return im
def run(name,ops):
    im=cv2.imread(f'{D}/raw/{name}.png').astype(np.float32)
    for f,a in ops: im=f(im,*a)
    cv2.imwrite(f'{D}/pics/{name}.png',np.clip(im,0,255).astype(np.uint8))
run('1-hook',[(shade,((398,512,472,588),0.10,7)),                      # face under the helmet peak, in the backlight's shadow
              (clean_cloth,((336,580,376,645),13,150)),(clean_cloth,((508,580,552,645),13,150)),   # numbers on the sleeves
              (kill_white,((362,700,452,742),(30,42,66)))])               # sheepskin noseband -> plain bay nose (bandaged lower legs sit behind the card)
run('2-news',[(shade,((350,592,402,640),0.18,6)),
              (clean_cloth,((455,735,635,885),19,160)),
              (kill_white,((95,668,175,790),(34,48,76),105))])            # blaze -> bay (the star above y668 stays)
def blurbox(im,b,s=7):
    im[b[1]:b[3],b[0]:b[2]]=cv2.GaussianBlur(im[b[1]:b[3],b[0]:b[2]],(0,0),s); return im
run('3-legend',[(clean_cloth,((275,760,345,900),15,150)),(blurbox,((60,770,140,870),))])
run('4-flat',[])
run('5-last',[(kill_white,((385,405,440,530),(26,34,52),110)),           # long stripe -> bay; the top of it stays as a small star
              (clean_cloth,((585,770,660,840),13,150)),
              (blurbox,((388,356,446,414),2.2)),
              (shade,((392,262,480,322),0.25,6))])
