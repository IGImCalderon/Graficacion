import cv2 as cv
import numpy as np

# --- CARGAR CLASIFICADOR DE ROSTROS ---
detector_rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Abrir cámara (0 = cámara principal)
camara = cv.VideoCapture(0)

while True:
    # Capturar frame
    ret, frame = camara.read()
    if not ret:
        break

    # Convertir a gris para detectar rostros
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros
    rostros = detector_rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        # --- CARICATURIZAR ROSTRO ---
        
        # Rectángulo rojo para el rostro
        cv.rectangle(frame, (x, y), (x+w, y+h), (234, 23, 23), 5)

        # Rectángulo verde aproximando la boca
        cv.rectangle(frame, (x, y + h//2), (x+w, y+h), (0, 255, 0), 5)

        # Ojos (círculos grandes blancos con borde negro y pupila roja)
        ojos = [(x + int(w*0.3), y + int(h*0.4)), (x + int(w*0.7), y + int(h*0.4))]
        for ox, oy in ojos:
            cv.circle(frame, (ox, oy), 21, (0, 0, 0), 2)   # borde
            cv.circle(frame, (ox, oy), 20, (255, 255, 255), -1)  # blanco
            cv.circle(frame, (ox, oy), 5, (0, 0, 255), -1)       # pupila

        # Nariz como triángulo proporcional
        nose_w = int(w * 0.15)
        nose_h = int(h * 0.1)
        nose_top = (x + w//2, y + h//2)
        nose_left = (x + w//2 - nose_w//2, y + h//2 + nose_h)
        nose_right = (x + w//2 + nose_w//2, y + h//2 + nose_h)
        tri_nariz = np.array([nose_top, nose_left, nose_right])
        cv.drawContours(frame, [tri_nariz], 0, (0, 100, 200), -1)
        cv.drawContours(frame, [tri_nariz], 0, (0, 0, 0), 2)

        # Orejas como elipses
        ear_w, ear_h = int(w*0.15), int(h*0.25)
        left_ear = (x - ear_w//2, y + int(h*0.4))
        right_ear = (x + w + ear_w//2, y + int(h*0.4))
        for centro in [left_ear, right_ear]:
            cv.ellipse(frame, centro, (ear_w//2, ear_h//2), 0, 0, 360, (200, 150, 100), -1)
            cv.ellipse(frame, centro, (ear_w//2, ear_h//2), 0, 0, 360, (0, 0, 0), 2)

        # Boca como arco
        boca_w, boca_h = int(w*0.4), int(h*0.1)
        boca_centro = (x + w//2, y + int(h*0.7))
        cv.ellipse(frame, boca_centro, (boca_w//2, boca_h//2), 0, 0, 180, (0, 0, 255), -1)
        cv.ellipse(frame, boca_centro, (boca_w//2, boca_h//2), 0, 0, 180, (0, 0, 0), 2)

    # Mostrar resultado
    cv.imshow('Caricatura de Rostro', frame)

    # Salir con 'q'
    if cv.waitKey(1) == ord('q'):
        break

# Liberar cámara y cerrar ventanas
camara.release()
cv.destroyAllWindows()
