

1. Importaciones Básicas
python
import cv2           # Para la interfaz gráfica
import numpy as np   # Para manejar matrices y arrays
import threading     # Para los hilos (movimiento simultáneo)
import time          # Para controlar la velocidad
import random        # Para posiciones aleatorias
2. Configuración Inicial
python
TAM = 50             # Tamaño de cada celda (50x50 píxeles)
FILAS, COLS = 8, 12  # 8 filas y 12 columnas de celdas
ANCHO, ALTO = COLS * TAM, FILAS * TAM  # Tamaño total de la ventana
META = [FILAS//2, COLS//2]  # La meta está en el centro (fila 4, columna 6)
particulas = []      # Lista para guardar las posiciones de las partículas
3. Función que Mueve Cada Partícula
python
def mover(id, fila, col):
    while [fila, col] != META:  # Mientras no haya llegado a la meta
        # Primero ajusta la fila
        if fila != META[0]:
            fila += 1 if META[0] > fila else -1
        # Luego ajusta la columna
        elif col != META[1]:
            col += 1 if META[1] > col else -1
        
        particulas[id] = [fila, col]  # Actualiza la posición
        time.sleep(0.5)  # Espera medio segundo entre movimientos
4. Creación de Partículas Aleatorias
python
for i in range(3):  # Crea 3 partículas
    fila = random.randint(0, FILAS-1)  # Fila aleatoria (0-7)
    col = random.randint(0, COLS-1)    # Columna aleatoria (0-11)
    particulas.append([fila, col])     # Guarda la posición
    
    # Crea y inicia el hilo para esta partícula
    threading.Thread(target=mover, args=(i, fila, col), daemon=True).start()
5. Bucle Principal de la Ventana
python
while True:
    # Crea una imagen en blanco (255 = blanco en OpenCV)
    img = np.ones((ALTO, ANCHO, 3), dtype=np.uint8) * 255
    
    # Dibuja la cuadrícula
    for i in range(FILAS+1):
        cv2.line(img, (0, i*TAM), (ANCHO, i*TAM), (200,200,200), 1)
    for j in range(COLS+1):
        cv2.line(img, (j*TAM, 0), (j*TAM, ALTO), (200,200,200), 1)
    
    # Dibuja la meta (cuadrado negro en el centro)
    x1, y1 = META[1]*TAM, META[0]*TAM
    cv2.rectangle(img, (x1, y1), (x1+TAM, y1+TAM), (0,0,0), -1)
    
    # Dibuja las partículas
    colores = [(0,0,255), (0,255,0), (255,0,0)]  # Rojo, Verde, Azul
    for i, (f, c) in enumerate(particulas):
        x, y = c*TAM, f*TAM  # Convierte coordenadas de celda a píxeles
        cv2.rectangle(img, (x, y), (x+TAM, y+TAM), colores[i], -1)
        cv2.putText(img, str(i+1), (x+20, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    
    # Muestra la imagen y verifica si presionaste ESC
    cv2.imshow('Particulas Aleatorias', img)
    if cv2.waitKey(100) == 27:
        break

cv2.destroyAllWindows()  # Cierra la ventana al salir