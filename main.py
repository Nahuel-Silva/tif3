from cargar_fotos import *
from deteccion import *
from postural import *
from altura_pers import *

def main():
    list_photos = Upload_photos().upload()
    Person().person_height(list_photos)
    # list_mask = Detection().detection_color(list_photos)
    # Postural_change().shoulders_difference(list_mask)



if __name__ == '__main__':
    main()