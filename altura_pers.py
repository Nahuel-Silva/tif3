import cv2
import numpy as np

class Person():

    def person_height(self, image_list):
        
        for img in image_list:

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Aplicar un filtro de suavizado para reducir el ruido
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # Aplicar el detector de bordes Canny
            edges = cv2.Canny(blur, 100, 200)

            # Buscar los contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Crear una máscara del tamaño de la imagen
            mask = np.zeros_like(gray)

            # Dibujar el contorno de la persona en la máscara
            cv2.drawContours(mask, contours, -1, 255, thickness=2)

            # for i in range(len(contours)):
            #     cv2.putText(mask, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Encontrar los dos contornos que deseas conectar
            cnt1 = contours[0]
            cnt2 = contours[-1]

            # Encontrar los puntos extremos para cada contorno
            x1, y1, w1, h1 = cv2.boundingRect(cnt1)
            x2, y2, w2, h2 = cv2.boundingRect(cnt2)
            pt1 = (int(x1 + w1/2), y1)
            pt2 = (int(x2 + w2/2), y2 + h2)

            cv2.circle(mask, pt1, 5, (0, 0, 255), -1)
            cv2.circle(mask, pt2, 5, (0, 0, 255), -1)

            distancia = cv2.norm(pt1, pt2)

            print(distancia)

            height, width, channels = img.shape

            print(height)

            # Mostrar la imagen con la máscara y el rectángulo dibujado
            cv2.namedWindow('Máscara', cv2.WINDOW_NORMAL)
            cv2.imshow('Máscara', mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()