import cv2 as cv  # Importamos OpenCV para video y procesamiento de imágenes

# Cargar clasificador de rostros pre-entrenado
clasificador_rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')

# Abrir cámara principal
camara = cv.VideoCapture(0)

# Inicializar variables
x = y = w = h = 0
contador = 0  # Puede usarse para guardar imágenes si se desea

# --- BUCLE PRINCIPAL ---
while True:
    ret, frame = camara.read()
    if not ret:
        break

    # Convertir a gris para mejorar detección
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros
    rostros_detectados = clasificador_rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros_detectados:
        # Centro aproximado del rostro
        centro_x = x + w // 2
        centro_y = y + h // 2

        # Dibujar rectángulo verde alrededor del rostro
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Dibujar círculo azul en el centro del rostro
        cv.circle(frame, (centro_x, centro_y), w // 2, (255, 0, 0), 2)

        # Opcional: guardar la cara detectada
        # cara = frame[y:y+h, x:x+w]
        # contador += 1
        # cv.imwrite(f'/ruta/cara{contador}.jpg', cara)

    # Mostrar resultado
    cv.imshow('Detección de Rostros', frame)

    # Salir si se presiona ESC
    if cv.waitKey(1) & 0xFF == 27:
        break

# Liberar cámara y cerrar ventanas
camara.release()
cv.destroyAllWindows()
