import cv2
import os
class Upload_photos():

    def upload(self):

        path_photos = "/home/nahuel/facultad/tif3/fotos paciente"
        # path_photos_checked = "/home/nahuel/facultad/tif3/fotos paciente - analizadas"

        for pic in os.listdir(path_photos):

            photo = cv2.imread(os.path.join(path_photos, pic))

            return photo
            #test to change the image
            # neg_photo = cv2.bitwise_not(photo)

            # out_photo = os.path.join(path_photos_checked, pic)
            # cv2.imwrite(out_photo, neg_photo)