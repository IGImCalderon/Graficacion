import cv2
import numpy as np

# --- CAPTURA DE VIDEO DESDE LA CÁMARA ---
camara = cv2.VideoCapture(0)

# Esperar 2 segundos para que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo inicial
ret, fondo = camara.read()
if not ret:
    print("Error al capturar el fondo.")
    camara.release()
    exit()

# --- BUCLE PRINCIPAL ---
while camara.isOpened():
    ret, frame = camara.read()
    if not ret:
        break

    # Convertir frame de BGR a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de color verde (ajustable según la tela)
    verde_min = np.array([80, 40, 40])
    verde_max = np.array([145, 255, 255])

    # Crear máscara que detecta el verde
    mask = cv2.inRange(hsv_frame, verde_min, verde_max)

    # Invertir máscara para áreas que NO son verdes
    mask_no_verde = cv2.bitwise_not(mask)

    # Partes del frame que no son verdes
    frame_no_verde = cv2.bitwise_and(frame, frame, mask=mask_no_verde)

    # Partes del fondo donde estaba el verde
    fondo_verde = cv2.bitwise_and(fondo, fondo, mask=mask)

    # Combinar ambos para efecto de invisibilidad
    salida_final = cv2.addWeighted(frame_no_verde, 1, fondo_verde, 1, 0)

    # Mostrar resultados
    cv2.imshow("Efecto Capa de Invisibilidad", salida_final)
    cv2.imshow("Máscara Verde", mask)

    # Salir con tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar cámara y cerrar ventanas
camara.release()
cv2.destroyAllWindows()
