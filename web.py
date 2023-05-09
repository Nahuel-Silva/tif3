import streamlit as st
import cv2
import numpy as np
from cargar_fotos import *
from deteccion import *
from postural import *
from med_objRef import *
from exportar_pdf import *

class Main():

    def mostrar(self, list_ph, mask_l, distance_der, distance_izq, a):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        for img in list_ph:
            with col2:
                st.image(img, width=300)
        for img in mask_l:
            with col3:
                st.image(img, width=300)
        st.subheader("Informe")
        st.subheader(f"Resultado: {a}")
        st.subheader("Detalle:")
        dist_1 = f"         Del marcador 4 a 1 hay una distancia de {round(distance_der)}cm"
        dist_2 = f"         Del marcador 3 a 2 hay una distancia de {round(distance_izq)}cm"
        st.subheader(f"{dist_1}")
        st.subheader(f"{dist_2}")

    def pdf(self):
        with open("/home/nahuel/facultad/tif3/pdf/paciente.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            return PDFbyte


    def main(self):
        st.set_page_config(page_title="BIO-HELP", layout="wide")

        # Título de la aplicación
        st.title("Deteccion de alteraciones posturales")

        # Cargar la imagen
        uploaded_file = st.file_uploader("Cargar imagen del paciente", type=["jpg", "jpeg", "png"])

        # Si se carga la imagen
        if uploaded_file is not None:

            list_ph = []

            # Leer la imagen utilizando OpenCV
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            rpg_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            list_ph.append(rpg_img)
            # Centrar la imagen
            col1, col2, col3 = st.columns([3, 2, 3])
            with col2:
                st.image(rpg_img, width=300)

            if st.button("Procesar"):
                altura_obj = Person().obj_height(list_ph)
                list_mask = Detection().detection_color(list_ph)
                mask_l, distance_der, distance_izq, a = Postural_change().shoulders_difference(list_mask, altura_obj)
                Export.generate_pdf(list_ph, mask_l, distance_der, distance_izq, a)
                self.mostrar(list_ph, mask_l, distance_der, distance_izq, a)
            data_pdf = self.pdf()
            name = st.text_input("Ingrese su nombre del paciente: ")
            st.download_button(label="Descargar en PDF",
                data=data_pdf,
                file_name=f"{name}.pdf")
        

if __name__ == '__main__':
    Main().main()