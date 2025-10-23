import cv2 as cv   # Importo OpenCV para trabajar con imágenes
import numpy as np  # Importo NumPy para trabajar con matrices (las imágenes son matrices)
import math         # Importo math para poder usar cos, sin y radianes

# Cargar la imagen en escala de grises
img = cv.imread('tr.png', 0)  # 0 indica que se carga en blanco y negro

# Obtener el tamaño de la imagen
x, y = img.shape  # x = alto, y = ancho

# Crear una imagen vacía para almacenar el resultado
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)  # hago la imagen más grande para que no se corte al rotar
xx, yy = rotated_img.shape

# Calcular el centro de la imagen
cx, cy = int(x  // 2), int(y  // 2)  # punto central alrededor del cual se va a rotar

# Definir el ángulo de rotación (en grados) y convertirlo a radianes
angle = 45
theta = math.radians(angle)  # conversion a radianes porque cos y sin usan radianes

# Rotar la imagen
for i in range(x):        # recorro todas las filas de la imagen original
    for j in range(y):    # recorro todas las columnas
        # aplico la fórmula de rotación 2D manual
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)
        # verifico que el nuevo pixel esté dentro de los límites
        if 0 <= new_x < y and 0 <= new_y < x:
            rotated_img[new_y, new_x] = img[i, j]  # copio el valor del pixel a la nueva posición

# Mostrar la imagen original y la rotada
cv.imshow('Imagen Original', img)  # ventana con la imagen original
cv.imshow('Imagen Rotada (modo raw)', rotated_img)  # ventana con la imagen rotada
cv.waitKey(0)  # espero a que se presione una tecla
cv.destroyAllWindows()  # cierro todas las ventanas
