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

            list_mask.append(filter_image)

        return list_mask