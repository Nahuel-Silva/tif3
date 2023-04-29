import cv2
import os
import numpy as np
from PIL import Image

class Upload_photos():

    def upload(self):
        
        list_images = []

        path_photos = "/home/nahuel/facultad/tif3/fotos paciente"

        for pic in os.listdir(path_photos):
            
            photo = cv2.imread(os.path.join(path_photos, pic))
            pho_bgr = cv2.cvtColor(photo, cv2.COLOR_RGB2BGR)
            pho_blurred = cv2.GaussianBlur(pho_bgr, (5,5), 0)
            list_images.append(pho_blurred)

        return list_images

        