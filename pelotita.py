import cv2 as cv  
import numpy as np 

# Creamos una imagen en blanco (fondo blanco de 500x500 pixeles)
img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Posición inicial de la pelotita 1 (la que rebota)
x1, y1 = 50, 50
dx1, dy1 = 4, 4  # Dirección de movimiento en X y Y

# Posición inicial de la pelotita 2 (la que esquiva)
x2, y2 = 400, 400
vel2 = 5  # velocidad de la pelotita que esquiva

# Tamaño del radio de las pelotas
radio = 20

while True:
    # Limpiamos el fondo en cada frame (para que no se vea la estela)
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # ---------------------------
    # LÓGICA DE LA PRIMERA BOLA (rebota)
    # ---------------------------
    x1 += dx1
    y1 += dy1

    # Rebotes en bordes
    if x1 - radio <= 0 or x1 + radio >= 500:
        dx1 *= -1
    if y1 - radio <= 0 or y1 + radio >= 500:
        dy1 *= -1

    # ---------------------------
    # LÓGICA DE LA SEGUNDA BOLA (esquiva)
    # ---------------------------

    # Vector desde pelotita 2 hacia pelotita 1
    vector_x = x2 - x1
    vector_y = y2 - y1
    distancia = np.sqrt(vector_x**2 + vector_y**2)

    # Si la primera bola está cerca (menos de 100 px), la segunda se mueve
    if distancia < 100:
        # Normalizamos el vector para mover con velocidad constante
        if distancia != 0:
            x2 += int((vector_x / distancia) * vel2)
            y2 += int((vector_y / distancia) * vel2)

    # Limitar bordes para que no se salga
    x2 = max(radio, min(500 - radio, x2))
    y2 = max(radio, min(500 - radio, y2))

    # ---------------------------
    # DIBUJAR LAS BOLAS
    # ---------------------------
    cv.circle(img, (x1, y1), radio, (0, 255, 0), -1)
    cv.putText(img, f'({x1}, {y1})', (x1 + radio + 5, y1), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 128, 0), 1, cv.LINE_AA)

    cv.circle(img, (x2, y2), radio, (0, 0, 255), -1)
    cv.putText(img, f'({x2}, {y2})', (x2 + radio + 5, y2), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 0, 128), 1, cv.LINE_AA)

    cv.imshow('Pelotitas con coordenadas', img)

    key = cv.waitKey(30)
    if key == ord('q'):
        break

cv.destroyAllWindows()
