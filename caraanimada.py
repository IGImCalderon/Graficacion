import cv2 as cv 
import numpy as np

# 08/10/25 - Este programa detecta un rostro con la cámara y le dibuja una cara animada encima.
# Tiene movimiento en las pupilas y también una lengua que sube y baja.

# Cargamos el clasificador que detecta rostros (usa el archivo Haar Cascade)
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Activamos la cámara (0 significa la cámara principal)
cap = cv.VideoCapture(0)

# Variables para contar cuadros y controlar los movimientos
frame_count = 0
pupil_direction = 1    # Dirección del movimiento de las pupilas (1 = derecha, -1 = izquierda)
tongue_direction = 1   # Dirección del movimiento de la lengua (1 = baja, -1 = sube)
pupil_offset = 0       # Desplazamiento actual de la pupila
tongue_length = 0      # Longitud actual de la lengua (para animarla)

while True:
    ret, img = cap.read()  # Leemos un cuadro de la cámara
    if not ret:
        break  # Si no se puede leer la cámara, salimos del ciclo
        
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convertimos a escala de grises (mejor para detectar)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)  # Detectamos rostros

    for(x, y, w, h) in rostros:
        # Dibujamos un rectángulo rojo alrededor del rostro
        img = cv.rectangle(img, (x, y), (x+w, y+h), (234, 23, 23), 5)
        
        # Parte inferior del rostro (mandíbula o boca)
        img = cv.rectangle(img, (x, int(y+h/2)), (x+w, y+h), (0, 255, 0), 5)
        
        # ----------------- OJOS -----------------
        # Dibujamos los círculos blancos de los ojos
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 21, (0, 0, 0), 2)  # Contorno ojo izquierdo
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 21, (0, 0, 0), 2)  # Contorno ojo derecho
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 20, (255, 255, 255), -1)  # Blanco del ojo izq
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 20, (255, 255, 255), -1)  # Blanco del ojo der
        
        # Movimiento de las pupilas
        max_pupil_offset = 8  # Qué tanto se pueden mover las pupilas
        pupil_offset += pupil_direction * 0.5  # Se mueven poco a poco
        
        # Si llega al límite, cambia de dirección
        if pupil_offset >= max_pupil_offset:
            pupil_direction = -1
        elif pupil_offset <= -max_pupil_offset:
            pupil_direction = 1
            
        # Dibujamos las pupilas (se mueven de un lado a otro)
        img = cv.circle(img, (x + int(w*0.3) + int(pupil_offset), y + int(h*0.4)), 5, (0, 0, 255), -1)
        img = cv.circle(img, (x + int(w*0.7) + int(pupil_offset), y + int(h*0.4)), 5, (0, 0, 255), -1)
        
        # ----------------- NARIZ -----------------
        # Calculamos puntos para hacer un triángulo que simule una nariz
        nose_width = int(w * 0.15)
        nose_height = int(h * 0.1)
        nose_top = (x + w//2, y + int(h*0.5))
        nose_left = (x + w//2 - nose_width//2, y + int(h*0.5) + nose_height)
        nose_right = (x + w//2 + nose_width//2, y + int(h*0.5) + nose_height)
        
        # Dibujamos el triángulo de la nariz
        triangle_cnt = np.array([nose_top, nose_left, nose_right])
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 100, 200), -1)  # Color de la nariz
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 0, 0), 2)       # Contorno
        
        # ----------------- OREJAS -----------------
        ear_width = int(w * 0.15)
        ear_height = int(h * 0.25)
        
        # Oreja izquierda
        left_ear_center = (x - ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        # Oreja derecha
        right_ear_center = (x + w + ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        # ----------------- BOCA -----------------
        mouth_width = int(w * 0.4)
        mouth_height = int(h * 0.1)
        mouth_center = (x + w//2, y + int(h*0.7))
        
        # Dibujamos una boca semicircular (tipo sonrisa)
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 255), -1)
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 0), 2)
        
        # ----------------- LENGUA (ANIMACIÓN) -----------------
        max_tongue_length = int(h * 0.15)  # Qué tanto puede salir la lengua
        tongue_length += tongue_direction * 2  # Movimiento
        
        # Si llega al máximo o al mínimo, cambia de dirección
        if tongue_length >= max_tongue_length:
            tongue_direction = -1
        elif tongue_length <= 0:
            tongue_direction = 1
            
        # Dibujamos la lengua solo si debe mostrarse
        if tongue_length > 0:
            tongue_radius = int(w * 0.06)
            tongue_center = (x + w//2, y + int(h*0.7) + tongue_length)
            
            # Círculo rojo para simular la lengua
            img = cv.circle(img, tongue_center, tongue_radius, (255, 0, 0), -1)
            img = cv.circle(img, tongue_center, tongue_radius, (0, 0, 0), 2)
        
        # Texto en pantalla para decir cómo salir
        cv.putText(img, "Presiona 'q' para salir", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Contamos los cuadros (solo para control)
    frame_count += 1
    
    # Mostramos la imagen en una ventana
    cv.imshow('img', img)
    
    # Si se presiona la tecla 'q', se sale del programa
    if cv.waitKey(1) == ord('q'):
        break
    
# Cuando se termina, liberamos la cámara y cerramos las ventanas
cap.release()
cv.destroyAllWindows()
