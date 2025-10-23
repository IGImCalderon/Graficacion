import numpy as np
import cv2

# --- FUNCIÓN PARA CALCULAR PUNTO SOBRE LA ELIPSE ---
def punto_elipse(semi_eje_x, semi_eje_y, t):
    # Calcular coordenadas del punto en la elipse
    x = int(semi_eje_x * 2 * np.cos(t) + 200)  # Escalado y centrado horizontal
    y = int(semi_eje_y * np.sin(t) + 200)      # Centrado vertical
    return (x, y)

# Dimensiones de la ventana
ventana_ancho, ventana_alto = 800, 800

# Crear imagen negra
imagen = np.zeros((ventana_alto, ventana_ancho, 3), dtype=np.uint8)

# Parámetros de la elipse
a = 200            # Semieje mayor (ancho)
b = 100            # Semieje menor (alto)
num_puntos = 1000  # Cantidad de puntos para recorrer la elipse suavemente

# Generar valores de t de 0 a 2pi
t_values = np.linspace(0, 2 * np.pi, num_puntos)

# --- BUCLE PRINCIPAL DE ANIMACIÓN ---
for t_actual in t_values:
    # Crear un frame negro en cada iteración
    imagen = np.zeros((ventana_alto, ventana_ancho, 3), dtype=np.uint8)
    
    # Calcular posición del punto actual
    punto = punto_elipse(a, b, t_actual)
    
    # Dibujar punto verde grande
    cv2.circle(imagen, punto, radius=30, color=(0, 255, 0), thickness=-1)
    
    # Dibujar trayectoria completa de la elipse en puntos blancos
    for t_trayectoria in t_values:
        pt = punto_elipse(a, b, t_trayectoria)
        cv2.circle(imagen, pt, radius=1, color=(255, 255, 255), thickness=-1)
    
    # Mostrar frame
    cv2.imshow('Animación Elipse', imagen)
    
    # Pausa breve para animación
    cv2.waitKey(10)

# Cerrar ventana al finalizar
cv2.destroyAllWindows()
