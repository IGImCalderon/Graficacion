import cv2 as cv
import numpy as np

# Captura de video desde la cámara
cap = cv.VideoCapture(0)

# Crear una imagen negra donde se va a dibujar la trayectoria del objeto
trayectoria = None

# Guardar el último centro detectado del objeto
ultimo_centro = None

while True:
    # Leer un nuevo frame de la cámara
    ret, img = cap.read()
    if not ret:
        break

    # Inicializar la imagen de trayectoria si es la primera vez
    if trayectoria is None:
        trayectoria = np.zeros_like(img)

    # Convertir el frame a HSV (más fácil para detección de color)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Rango de color a detectar (ajustable según el objeto)
    uba = (90, 255, 255)   # Valor máximo HSV
    ubb = (40, 40, 40)     # Valor mínimo HSV

    # Crear máscara que detecta solo el color del objeto
    mask = cv.inRange(hsv, ubb, uba)
    res = cv.bitwise_and(img, img, mask=mask)  # Aplicar la máscara al frame original

    # Buscar contornos en la máscara
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        # Tomar el contorno más grande (el objeto principal)
        c = max(contours, key=cv.contourArea)
        M = cv.moments(c)  # Calcular momentos para encontrar el centro
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])  # Coordenada X del centro
            cy = int(M["m01"] / M["m00"])  # Coordenada Y del centro

            # Dibujar un círculo rojo en el centro del objeto
            cv.circle(img, (cx, cy), 5, (0, 0, 255), -1)

            # Dibujar línea verde desde el último centro hasta el actual
            if ultimo_centro is not None:
                cv.line(trayectoria, ultimo_centro, (cx, cy), (0, 255, 0), 2)

            # Actualizar el último centro
            ultimo_centro = (cx, cy)

    # Combinar el video con la trayectoria
    salida = cv.add(img, trayectoria)

    # Mostrar resultados
    cv.imshow('video', salida
