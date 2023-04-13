from cargar_fotos import Upload_photos
from deteccion import *

def main():
    list_photos = Upload_photos().upload()
    Detection().detection_color(list_photos)



if __name__ == '__main__':
    main()