import cv2
import numpy as np

# Abre la cámara (el 0 es la cámara principal del equipo)
cap = cv2.VideoCapture(0)

# Espera 2 segundos para que la cámara se active bien
cv2.waitKey(2000)

# Captura una imagen del fondo (no se usa aquí, pero se deja por estructura)
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()

# Aquí se van a guardar los puntos donde pase el color azul
trazo = []

# El color con el que se empieza a dibujar (azul)
color_actual = (255, 0, 0)  # formato BGR

# Tamaño de los cuadros de color que van arriba
cuadro_size = 100
espacio = 20

# Coordenadas de los tres cuadros de color (azul, verde y rojo)
cuadro_azul = (espacio, espacio, espacio + cuadro_size, espacio + cuadro_size)
cuadro_verde = (espacio * 2 + cuadro_size, espacio, espacio * 2 + cuadro_size * 2, espacio + cuadro_size)
cuadro_rojo = (espacio * 3 + cuadro_size * 2, espacio, espacio * 3 + cuadro_size * 3, espacio + cuadro_size)

# Bucle principal (mientras la cámara esté encendida)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convierte los colores del video de BGR a HSV (más fácil para detectar colores)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango de color azul (esto se puede ajustar si la luz cambia)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # Crea una imagen en blanco y negro donde solo el azul se ve blanco
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Busca los contornos (las orillas) del color azul detectado
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Toma el contorno más grande (por si detecta varios azules)
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            # Calcula el centro del objeto azul (coordenadas x, y)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibuja un pequeño círculo donde se detecta el color azul
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Si el objeto azul entra en alguno de los cuadros de color, cambia el color de dibujo
            if cuadro_azul[0] < cx < cuadro_azul[2] and cuadro_azul[1] < cy < cuadro_azul[3]:
                color_actual = (255, 0, 0)  # Azul
            elif cuadro_verde[0] < cx < cuadro_verde[2] and cuadro_verde[1] < cy < cuadro_verde[3]:
                color_actual = (0, 255, 0)  # Verde
            elif cuadro_rojo[0] < cx < cuadro_rojo[2] and cuadro_rojo[1] < cy < cuadro_rojo[3]:
                color_actual = (0, 0, 255)  # Rojo
            else:
                # Si no está dentro de los cuadros, entonces dibuja
                trazo.append((cx, cy, color_actual))

    # Dibuja los tres cuadros de color arriba en la pantalla
    cv2.rectangle(frame, (cuadro_azul[0], cuadro_azul[1]), (cuadro_azul[2], cuadro_azul[3]), (255, 0, 0), -1)
    cv2.rectangle(frame, (cuadro_verde[0], cuadro_verde[1]), (cuadro_verde[2], cuadro_verde[3]), (0, 255, 0), -1)
    cv2.rectangle(frame, (cuadro_rojo[0], cuadro_rojo[1]), (cuadro_rojo[2], cuadro_rojo[3]), (0, 0, 255), -1)

    # Agrega texto debajo de cada cuadro
    cv2.putText(frame, 'Azul', (cuadro_azul[0]+10, cuadro_azul[3]+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(frame, 'Verde', (cuadro_verde[0]+10, cuadro_verde[3]+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(frame, 'Rojo', (cuadro_rojo[0]+10, cuadro_rojo[3]+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # Dibuja todas las líneas guardadas en la lista trazo
    for i in range(1, len(trazo)):
        if trazo[i - 1][:2] and trazo[i][:2]:
            cv2.line(frame, trazo[i - 1][:2], trazo[i][:2], trazo[i][2], 3)

    # Muestra la cámara con el dibujo
    cv2.imshow("Pintor con Cambio de Color", frame)

    # Muestra también la máscara del color azul (para ver cómo lo detecta)
    cv2.imshow("Mascara Azul", mask)

    # Si se presiona la letra 'q', se cierra el programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando se sale del ciclo, se apaga la cámara y se cierran las ventanas
cap.release()
cv2.destroyAllWindows()
