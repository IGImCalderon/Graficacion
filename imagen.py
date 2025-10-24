import cv2 as cv

img = cv.imread('cascada.png', 0 )
cv.imshow('cascada', img)
cv.waitKey()
cv.destroyAllWindows()