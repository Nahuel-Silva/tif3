import streamlit as st
import cv2
import numpy as np
from cargar_fotos import *
from deteccion import *
from postural import *
from med_objRef import *
from exportar_pdf import *


class Main():

    def instructivos(self):
        image_path = "./utils/intru.jpeg"
        text_app = """Pasos para usar la app: 
        \n1) Subir imagen del paciente, de la vista posterior del plano frontal
        \n2) Apretar en el boton procesar para que detecte si hay una posible diferencia de hombros y realice el informe
        \n3) Luego si quiere descargar el informe en pdf, coloca el nombre, apreta enter y luego el boton descargar en pdf"""
        image = cv2.imread(image_path)
        text_marc = """Colocación de los marcadores: 
        \n1) Los dos primeros marcadores se colocan en la articulación acromioclavicular derecha e izquierda 
        \n2) Y los otros dos marcadores se colocan en la espina ilíaca posterosuperior derecha e izquierda
        \n\t---------------> LOS MARCADORES DEBEN DE SER DE COLOR VERDE <--------------
        \n Al momento de tomarle la foto al paciente debe de haber un objeto de referencia de color amarillo
        de 20cm de alto, esto para que el programa tenga una refencia de un objeto de la vida real y pueda
        realizar los calculos precisamente.
        """
        return image, text_app, text_marc
        

    def mostrar(self, list_ph, mask_l, distance_der, distance_izq, a, c):
        
        with st.expander(f"Imagen {c}"):
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
        path = "./pdf_merge/"
        name = "paciente.pdf"
        archivo_existe = os.path.join(path, name)
        if os.path.isfile(archivo_existe):
            with open(archivo_existe , "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            return PDFbyte
        else:
            pass


    def main(self):

        st.set_page_config(page_title="BIO-HELP", layout="wide")

        col1, col2, col3 = st.columns(3)

        # Título de la aplicación
        with col2:
            st.title("Detección de alteraciones posturales")

        img, text, text2 = self.instructivos()

        with st.expander("Instructivo para tomarle las fotos al paciente"):
            col1, col2, col3 = st.columns([3, 2, 3])
            with col2:
                st.image(img, width=300)
            st.write(text2) 

        with st.expander("Instructivo para usar la web app"):
            st.write(text) 

        # Cargar la imagen
        uploaded_files = st.file_uploader("Cargar imagen del paciente", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        list_ph = []

        # Si se carga la imagen
        if uploaded_files is not None:

            for file in uploaded_files:
                # Leer la imagen utilizando OpenCV
                file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)
                rpg_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                list_ph.append([rpg_img])

            # Crear las columnas
            with st.expander("Imagenes cargas"):
                # Número de columnas
                num_columnas = len(uploaded_files)
                if num_columnas != 0:
                    columnas = st.columns(num_columnas)
                    # Mostrar las imágenes en las columnas
                    for i, columna in enumerate(columnas):
                        columna.image(uploaded_files[i], use_column_width=True, caption=f"Imagen {i+1}")
                else:
                    pass

            c = 0
            if st.button("Procesar"):
                with st.spinner('Cargando...'):
                    for list_phh in list_ph:
                        c += 1
                        # Procesamiento
                        altura_obj = Person().obj_height(list_phh)
                        if altura_obj == None:
                            st.warning("¡¡¡CUIDADO: Foto sin objeto de referencia amarillo!!!")
                            st.stop()
                        else:
                            list_mask = Detection().detection_color(list_phh)
                            if list_mask == None:
                                st.warning("¡¡¡CUIDADO: Foto del paciente sin marcadores!!!")
                                st.stop()
                            else:
                                mask_l, distance_der, distance_izq, a = Postural_change().shoulders_difference(list_mask, altura_obj)
                                Export().generate_pdf(list_phh, mask_l, distance_der, distance_izq, a, c)
                                self.mostrar(list_phh, mask_l, distance_der, distance_izq, a, c)
                    Export().merge_pdf()
                    Export().clear()

            #PDF
            data_pdf = self.pdf()
            name = st.text_input("Ingrese el nombre del paciente: ")
            if name:
                if data_pdf is not None:
                    st.download_button(label="Descargar en PDF",
                        data=data_pdf,
                        file_name=f"{name}.pdf")
                else:
                    pass
            else:
                pass
            
        

if __name__ == '__main__':
    Main().main()