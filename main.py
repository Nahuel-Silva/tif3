from cargar_fotos import *
from deteccion import *
from postural import *
from med_objRef import *
from exportar_pdf import *

def main():
    list_photos = Upload_photos().upload()
    altura_obj = Person().obj_height(list_photos)
    list_mask = Detection().detection_color(list_photos)
    mask_l, distance_der, distance_izq, a = Postural_change().shoulders_difference(list_mask, altura_obj)
    resp = input("Quiere exportar la imagen en pdf?(si o no): ")
    name = input("Nombre del paciente: ")
    if resp == "si":
        Export.generate_pdf(list_photos, mask_l, distance_der, distance_izq, a, name)
    else:
        exit()



if __name__ == '__main__':
    main()