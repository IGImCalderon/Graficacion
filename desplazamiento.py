import cv2 as cv
import numpy as np
import math

# Cargar la imagen en escala de grises    18/09/2025
img = cv.imread('tr.png', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía para almacenar el resultado
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)
xx, yy = rotated_img.shape
print(xx,yy)
# Calcular el centro de la imagen
cy, cx = int(xx  // 2), int(yy  // 2)

# Definir el ángulo de rotación (en grados) y convertirlo a radianes
# Rotar la imagen
for i in range(x):
    for j in range(y):
        new_x = j+cx
        new_y =i+cy
        if 0 <= new_x < yy and 0 <= new_y < xx:
            rotated_img[new_y, new_x] = img[i, j]

# Mostrar la imagen original y la rotada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada (modo raw)', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()