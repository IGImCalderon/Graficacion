import cv2
import numpy as np

# Abro la cámara para capturar video (0 significa la cámara principal de la compu)
cap = cv2.VideoCapture(0)

# Espero 2 segundos para que la cámara se estabilice antes de empezar
cv2.waitKey(2000)

# Capturo un solo frame para usarlo como "fondo"
ret, background = cap.read()
if not ret:
    # Si no logro capturar, muestro error y cierro todo
    print("Error al capturar el fondo.")
    cap.release()
    exit()

# Creo una lista vacía para guardar los puntos por donde pase el objeto azul
trazo = []

# Mientras la cámara esté abierta
while cap.isOpened():
    # Leo un frame (una imagen del video)
    ret, frame = cap.read()
    if not ret:
        break  # si falla la lectura, salgo del bucle

    # Cambio el espacio de color de BGR (que usa OpenCV) a HSV (más fácil para detectar colores)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Defino el rango del color azul en HSV (puedo ajustar los valores según la luz)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # Creo una máscara: las partes que estén dentro del rango azul se ponen blancas, el resto negras
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Busco los contornos (formas) dentro de la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Elijo el contorno más grande (en caso de que haya varias áreas azules)
        c = max(contours, key=cv2.contourArea)

        # Calculo los momentos (básicamente me dan información de área, centro, etc.)
        M = cv2.moments(c)
        if M["m00"] != 0:  # Evito dividir entre cero
            # Calculo el centroide del objeto azul
            cx = int(M["m10"] / M["m00"])  # coordenada X
            cy = int(M["m01"] / M["m00"])  # coordenada Y

            # Guardo ese punto en mi lista de trazo
            trazo.append((cx, cy))

            # Dibujo un circulito rojo en el centro detectado
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Recorro los puntos guardados y dibujo una línea verde uniendo cada par de puntos
    for i in range(1, len(trazo)):
        cv2.line(frame, trazo[i - 1], trazo[i], (0, 255, 0), 2)

    # Muestro en una ventana el video con el trazo dibujado
    cv2.imshow("Capa de Invisibilidad", frame)

    # También muestro la máscara (blanco = azul detectado, negro = no azul)
    cv2.imshow("Mask", mask)

    # Si presiono la tecla 'q', cierro el programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando salgo del bucle, libero la cámara y cierro las ventanas
cap.release()
cv2.destroyAllWindows()
