import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)

while(True):
    ret, img = cap.read()
    if ret:
        cv.imshow('video', img)
        r,g,b=cv.split(img)
        #cv.imshow('r',r)
        #cv.imshow('g',g)
        #cv.imshow('b',b)
        img3 =cv.merge([g,b,r])
        cv.imshow('img3'img3)
        k =cv.waitKey(1) & 0xFF
        if k == 27 :
            break
    else:
        break
   
cap.release()
cv.destroyAllWindows()