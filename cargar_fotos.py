import cv2
import os
class Upload_photos():

    def upload(self):
        
        list_images = []

        path_photos = "/home/nahuel/facultad/tif3/fotos paciente"
        # path_photos_checked = "/home/nahuel/facultad/tif3/fotos paciente - analizadas"

        for pic in os.listdir(path_photos):

            photo = cv2.imread(os.path.join(path_photos, pic))

            pho_resized = cv2.resize(photo, (800, 600))
            pho_bgr = cv2.cvtColor(pho_resized, cv2.COLOR_RGB2BGR)
            pho_blurred = cv2.GaussianBlur(pho_bgr, (5,5), 0)

            list_images.append(pho_blurred)

        return list_images
            #test to change the image
            # neg_photo = cv2.bitwise_not(photo)

            # out_photo = os.path.join(path_photos_checked, pic)
            # cv2.imwrite(out_photo, neg_photo)