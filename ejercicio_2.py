import cv2 as cv
import numpy as np
import math

# --- CARGAR IMAGEN EN ESCALA DE GRISES ---
imagen = cv.imread('pa.png', 0)
alto, ancho = imagen.shape
print(f"Tamaño original: {alto}x{ancho}")

# ========== PASO 1: ESCALADO 2x (VECINO MÁS CERCANO) ==========
factor = 2
nuevo_alto, nuevo_ancho = int(alto * factor), int(ancho * factor)
img_escalada = np.zeros((nuevo_alto, nuevo_ancho), dtype=np.uint8)

print("Escalando imagen 2x con vecino más cercano...")
print(f"Tamaño escalado: {nuevo_alto}x{nuevo_ancho}")
for fila in range(nuevo_alto):
    for col in range(nuevo_ancho):
        # Mapear coordenadas a la imagen original
        orig_fila = min(int(fila / factor), alto-1)
        orig_col = min(int(col / factor), ancho-1)
        img_escalada[fila, col] = imagen[orig_fila, orig_col]

# ========== PASO 2: ROTACIÓN 25° (INTERPOLACIÓN BILINEAL) ==========
angulo = 25
rad = math.radians(angulo)

# Calcular tamaño de imagen rotada
cos_a = abs(math.cos(rad))
sin_a = abs(math.sin(rad))
rot_alto = int(nuevo_alto * cos_a + nuevo_ancho * sin_a)
rot_ancho = int(nuevo_alto * sin_a + nuevo_ancho * cos_a)

img_rotada = np.zeros((rot_alto, rot_ancho), dtype=np.uint8)
print(f"Tamaño rotado: {rot_alto}x{rot_ancho}")

# Centros
centro_ori_x, centro_ori_y = nuevo_ancho // 2, nuevo_alto // 2
centro_rot_x, centro_rot_y = rot_ancho // 2, rot_alto // 2

print("Rotando 25° con interpolación bilineal...")
for fila in range(rot_alto):
    for col in range(rot_ancho):
        # Coordenadas relativas al centro
        rel_x = col - centro_rot_y
        rel_y = fila - centro_rot_x

        # Transformación inversa
        orig_col = rel_x * math.cos(rad) + rel_y * math.sin(rad) + centro_ori_y
        orig_fila = -rel_x * math.sin(rad) + rel_y * math.cos(rad) + centro_ori_x

        # Verificar límites
        if 0 <= orig_col < nuevo_ancho-1 and 0 <= orig_fila < nuevo_alto-1:
            x0 = int(orig_col)
            y0 = int(orig_fila)
            x1 = min(x0 + 1, nuevo_ancho-1)
            y1 = min(y0 + 1, nuevo_alto-1)

            wx = orig_col - x0
            wy = orig_fila - y0

            # Interpolación bilineal
            p00 = img_escalada[y0, x0]
            p01 = img_escalada[y0, x1]
            p10 = img_escalada[y1, x0]
            p11 = img_escalada[y1, x1]

            valor = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11

            img_rotada[fila, col] = np.clip(valor, 0, 255)

# --- MOSTRAR RESULTADOS ---
cv.imshow('1. Imagen Original', imagen)
cv.imshow('2. Imagen Escalada 2x (Vecino Cercano)', img_escalada)
cv.imshow('3. Imagen Rotada 25° (Bilineal)', img_rotada)

print("Presiona cualquier tecla para cerrar las ventanas...")
cv.waitKey(0)
cv.destroyAllWindows()
