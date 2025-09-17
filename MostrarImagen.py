Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import cv2
... 
... # Carga la imagen
... imagen = cv2.imread("messi.jpg")  # Reemplaza por tu archivo real
... 
... # Verifica que la imagen se haya cargado
... if imagen is None:
...     print("No se pudo cargar la imagen. Verifica la ruta.")
... else:
...     # Muestra la imagen
...     cv2.imshow("C:\Users\ZoeZi\Desktop\Nueva carpeta (2)\Captura de pantalla 2025-02-20 163203.png", imagen)
...     cv2.waitKey(0)
...     cv2.destroyAllWindows()
