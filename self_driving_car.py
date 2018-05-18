import numpy as np
from PIL import ImageGrab
import cv2
import time
from direct_keys import ReleaseKey,PressKey, W,A,S,D

def roi(img,vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255)
    masked = cv2.bitwise_and(img,mask)
    return masked



def get_coords(slopes):
    sx1=sy1=sx2=sy2=0
    for line in slopes:
        sx1+=line[0][0]
        sy1+=line[0][1]
        sx2+=line[0][2]
        sy2+=line[0][3]
    sx1//=len(slopes)
    sy1//=len(slopes)
    sx2//=len(slopes)
    sy2//=len(slopes)
    
    return [sx1,sy1,sx2,sy2]
    
def get_lane(lines):
    s1= 0.5
    s2= -0.5
    slopes1=slopes2=[]
    try:
        for line in lines:
            coords = line[0]
            x1 = coords[0]
            y1 = coords[1]
            x2 = coords[2]
            y2 = coords[3]
            slope = (y2-y1)/((x2-x1)+0.0000001)
            if abs(slope-s1)<abs(slope-s2):
                slopes1.append(line)
            else:
                slopes2.append(line)
        
        coords1=get_coords(slopes1)
        coords2=get_coords(slopes2)
        
        return [coords1,coords2]
    except:
        pass

def draw_lane(img,coords):
    print('here')
    try:
        print(coords)
        cv2.line(img,(coords[0][0],coords[0][1]),(coords[0][2],coords[0][3]),[0,255,0],10)
        cv2.line(img,(coords[1][0],coords[1][1]),(coords[1][2],coords[1][3]),[0,255,0],10)
    except:
        pass

    
##def draw_lines(img,lines):
##    try:
##        
##        for line in lines:
##            coords = line[0]
##            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],2)
##    except:
##        pass

def process_img(orignal_img):
    
    processed_img = cv2.cvtColor(orignal_img,cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, 200,300)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    vertices = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500]])
    processed_img = roi(processed_img,[vertices])

    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),100,5)
    coords = get_lane(lines)
    draw_lane(processed_img,coords)
    #draw_lines(processed_img,lines)
    return processed_img
 
def main():
    
    t1 = time.time()
    while True:
        t2= time.time()
        print(t2-t1)
        t1 = time.time()
        screen = np.array(ImageGrab.grab(bbox=(0,0,800,600)))
        new_screen = process_img(screen)
        #cv2.imshow('window',new_screen)
        cv2.imshow('window',cv2.cvtColor(screen,cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
