import cv2 as cv
import numpy as np
import math

# Cargar la imagen en escala de grises
imagen = cv.imread('pa.png', 0)
alto, ancho = imagen.shape
print(f"Tamaño original: {alto}x{ancho}")

# --- TRASLACIÓN ---
print("Aplicando traslado inverso...")
despl_x, despl_y = -50, -30
imagen_trasladada = np.zeros((alto, ancho), dtype=np.uint8)

for fila in range(alto):
    for col in range(ancho):
        orig_col = col - despl_x
        orig_fila = fila - despl_y

        if 0 <= orig_col < ancho-1 and 0 <= orig_fila < alto-1:
            x0 = int(orig_col)
            y0 = int(orig_fila)
            x1 = min(x0 + 1, ancho-1)
            y1 = min(y0 + 1, alto-1)

            wx = orig_col - x0
            wy = orig_fila - y0

            # Interpolación bilineal
            p00 = imagen[y0, x0]
            p01 = imagen[y0, x1]
            p10 = imagen[y1, x0]
            p11 = imagen[y1, x1]

            valor = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11

            imagen_trasladada[fila, col] = np.clip(valor, 0, 255)

print(f"Tamaño trasladado: {imagen_trasladada.shape}")

# --- ROTACIÓN ---
angulo = 90
rad = math.radians(angulo)

cos_a = abs(math.cos(rad))
sin_a = abs(math.sin(rad))
rot_alto = int(alto * cos_a + ancho * sin_a)
rot_ancho = int(alto * sin_a + ancho * cos_a)
imagen_rotada = np.zeros((rot_alto, rot_ancho), dtype=np.uint8)
print(f"Tamaño rotado: {rot_alto}x{rot_ancho}")

# Centros
centro_ori_x, centro_ori_y = ancho // 2, alto // 2
centro_rot_x, centro_rot_y = rot_ancho // 2, rot_alto // 2

print("Rotando 90° con interpolación bilineal...")
for fila in range(rot_alto):
    for col in range(rot_ancho):
        # Coordenadas relativas al centro
        rel_x = col - centro_rot_y
        rel_y = fila - centro_rot_x

        # Transformación inversa
        orig_col = rel_x * math.cos(rad) + rel_y * math.sin(rad) + centro_ori_y
        orig_fila = -rel_x * math.sin(rad) + rel_y * math.cos(rad) + centro_ori_x

        if 0 <= orig_col < ancho-1 and 0 <= orig_fila < alto-1:
            x0 = int(orig_col)
            y0 = int(orig_fila)
            x1 = min(x0 + 1, ancho-1)
            y1 = min(y0 + 1, alto-1)

            wx = orig_col - x0
            wy = orig_fila - y0

            p00 = imagen_trasladada[y0, x0]
            p01 = imagen_trasladada[y0, x1]
            p10 = imagen_trasladada[y1, x0]
            p11 = imagen_trasladada[y1, x1]

            valor = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11

            imagen_rotada[fila, col] = np.clip(valor, 0, 255)

# --- ESCALADO ---
factor = 2
nuevo_alto, nuevo_ancho = int(rot_alto * factor), int(rot_ancho * factor)
imagen_final = np.zeros((nuevo_alto, nuevo_ancho), dtype=np.uint8)

print("Escalando imagen 2x con vecino más cercano...")
for fila in range(nuevo_alto):
    for col in range(nuevo_ancho):
        orig_fila = min(int(fila / factor), rot_alto-1)
        orig_col = min(int(col / factor), rot_ancho-1)
        imagen_final[fila, col] = imagen_rotada[orig_fila, orig_col]

# --- MOSTRAR RESULTADOS ---
cv.imshow('1. Imagen Original', imagen)
cv.imshow('2. Imagen Trasladada (Bilineal)', imagen_trasladada)
cv.imshow('3. Imagen Rotada 90° (Bilineal)', imagen_rotada)
cv.imshow('4. Imagen Final Escalada 2x (Vecino Cercano)', imagen_final)

print("Presiona cualquier tecla para cerrar las ventanas...")
cv.waitKey(0)
cv.destroyAllWindows()
