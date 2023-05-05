import cv2
import numpy as np


class Detection():

    def detection_color(self, images):

        list_mask = []
        
        for img in images:

            images_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_green = np.array([35,50,50])
            upper_green = np.array([90,255,255])

            mask_green = cv2.inRange(images_hsv, lower_green, upper_green)

            filter_image = cv2.bitwise_and(img, img, mask=mask_green)

            # Aplicar una operación morfológica de apertura para eliminar pequeños objetos en la máscara
            kernel = np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(filter_image, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            list_mask.append(mask)

        return list_mask