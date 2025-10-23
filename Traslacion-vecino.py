import cv2 as cv
import numpy as np

# Cargo la imagen del gato en escala de grises
imagen = cv.imread('Gato.png', 0)

# Obtengo las dimensiones de la imagen original
alto, ancho = imagen.shape

# Factores de escalado
factor_x, factor_y = 2, 2

# Creo una nueva imagen vacía para colocar los píxeles ampliados
imagen_escalada = np.zeros((int(alto * factor_y), int(ancho * factor_x)), dtype=np.uint8)

# Copio los píxeles originales dejando huecos
for fila in range(alto):
    for col in range(ancho):
        imagen_escalada[fila*factor_y, col*factor_x] = imagen[fila, col]

# Relleno los huecos buscando vecinos
for i in range(imagen_escalada.shape[0]):
    for j in range(imagen_escalada.shape[1]):
        if imagen_escalada[i, j] == 0:
            encontrado = False
            radio = 1
            while not encontrado and radio < max(imagen_escalada.shape):
                for di in range(-radio, radio + 1):
                    for dj in range(-radio, radio + 1):
                        ni, nj = i + di, j + dj
                        if (0 <= ni < imagen_escalada.shape[0] and
                            0 <= nj < imagen_escalada.shape[1] and
                            imagen_escalada[ni, nj] != 0):
                            imagen_escalada[i, j] = imagen_escalada[ni, nj]
                            encontrado = True
                            break
                    if encontrado:
                        break
                radio += 1

# Escalado usando aproximación del vecino más cercano
imagen_escalada_final = np.zeros((int(alto * factor_y), int(ancho * factor_x)), dtype=np.uint8)

for i in range(imagen_escalada_final.shape[0]):
    for j in range(imagen_escalada_final.shape[1]):
        orig_i = min(int(i / factor_y), alto - 1)
        orig_j = min(int(j / factor_x), ancho - 1)
        imagen_escalada_final[i, j] = imagen[orig_i, orig_j]

# Mostrar imágenes
cv.imshow('Original', imagen)
cv.imshow('Huecos', imagen_escalada)
cv.imshow('Rellenada', imagen_escalada)
cv.imshow('Escalado Final', imagen_escalada_final)

cv.waitKey(0)
cv.destroyAllWindows()
