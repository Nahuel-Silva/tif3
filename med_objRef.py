import cv2
import numpy as np

class Person():

    def obj_height(self, image_list):
        
        for img in image_list:

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Convertir la imagen a espacio de color HSV
            hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # Aplicar una operación morfológica de apertura para eliminar pequeños objetos en la máscara
            kernel = np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Aplicar la máscara a la imagen original para aislar los objetos amarillos
            result = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)

            mask_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            # Encontrar los contornos en la máscara
            contours, hierarchy = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 1:
                x, y, w, h = cv2.boundingRect(contours[0])
                return h
            else:
                return None