import streamlit as st
import cv2
import numpy as np
import io
from cargar_fotos import *
from deteccion import *
from postural import *
from med_objRef import *
from exportar_pdf import *
from exportar_excel import *


class Main():

    def instructivos(self):
        image_path = "./utils/intru.png"
        image_path2 = "./utils/intru2.png"
        text_app = """Pasos para usar la app: 
        \n1) Subir imagen o imagenes del paciente, de la vista posterior del plano frontal
        \n2) Presionar en el boton "procesar" para que detecte si hay una posible diferencia de hombros y realice el informe
        \n3) Luego si quiere descargar el informe en pdf, coloca el nombre, presiona "aceptar" y luego el boton "descargar en pdf" """
        image = cv2.imread(image_path)
        image2 = cv2.imread(image_path2)
        rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        text_marc2 = """Al momento de tomarle la foto al paciente debe de haber un objeto de referencia de color amarillo
        de 20cm de alto, esto para que el programa tenga una refencia de un objeto de la vida real y pueda
        realizar los calculos precisamente.\n""" 
        text_marc = """Colocación de los marcadores: 
        \n1) P1 Y P2 se colocan en la articulación acromioclavicular derecha e izquierda 
        \n2) P3 Y P4 se colocan en la espina ilíaca posterosuperior derecha e izquierda
        \n\t---------------> LOS MARCADORES DEBEN DE SER DE COLOR VERDE <--------------

        """
        return image, text_app, text_marc, text_marc2, rgb
        

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
    
    def excel(self):

        path = './excel/paciente.xlsx'
        if os.path.isfile(path):
            df = pd.read_excel(path)
            # Crear un objeto BytesIO
            excel_data = io.BytesIO()
            # Guardar el DataFrame en el objeto BytesIO como un archivo Excel
            with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
                
            excel_bytes = excel_data.getvalue()
            return excel_bytes
        else:
            None

    def main(self):

        st.set_page_config(page_title="BIO-HELP", layout="wide")

        col1, col2, col3 = st.columns([2,4,2])

        # Título de la aplicación
        with col2:
            st.title("DETECCIÓN DE ALTERACIONES POSTURALES")

        img, text, text2, text3, img2 = self.instructivos()

        with st.expander("Instructivo para tomarle las fotos al paciente"):
            col1, col2, col3 = st.columns([3, 2, 3])
            with col2:
                st.image(img2, width=300)
            st.write(text3)
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

            medidas_izq = []
            medidas_der = []
            numero_imagenes = []

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
                                medidas_der.append(round(distance_der))
                                medidas_izq.append(round(distance_izq))
                                numero_imagenes.append(f"Imagen{c}")
                                Export().generate_pdf(list_phh, mask_l, distance_der, distance_izq, a, c)
                                self.mostrar(list_phh, mask_l, distance_der, distance_izq, a, c)
                    Export().merge_pdf()
                    ExportExcel().generate_csv(medidas_izq, medidas_der, numero_imagenes)
                    Export().clear()

            #Excel
            data_excel = self.excel()
            #PDF
            data_pdf = self.pdf()
            with st.form(key="myform"):
                name = st.text_input("Ingrese el nombre del paciente: ")
                submit_button = st.form_submit_button(label='Aceptar')
            if submit_button:

                if data_pdf is not None:
                    if data_excel is not None:
                        
                        #Boton de PDF
                        st.download_button(label="Descargar en PDF",
                            data=data_pdf,
                            file_name=f"{name}.pdf")
                        
                        #Boton de excel
                        st.download_button(label="Descargar Excel",
                            data=data_excel,
                            file_name=f"{name}.xlsx", 
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    else:
                        pass
                else:
                    pass
            else:
                pass
            
        

if __name__ == '__main__':
    Main().main()