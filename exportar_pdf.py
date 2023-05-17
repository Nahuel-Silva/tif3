from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image
import os
from PyPDF2 import PdfMerger

class Export():

    def generate_pdf(self, image1, image2, dist_der, dist_izq, result, c):

        path = "/home/nahuel/facultad/tif3/pdf"
        # Crear un nuevo archivo PDF
        pdf_file = canvas.Canvas(path+"/"+f"pdf{c}.pdf", pagesize=letter)

        pdf_file.setTitle("Deteccion de cambios posturales")

        pdf_file.setFont("Helvetica-Bold", 20)
        pdf_file.drawCentredString(letter[0]/2.0, letter[1]-72, "BIO-HELP")

        # Agregar el string_value
        pdf_file.setFont("Helvetica-Bold", 14)
        pdf_file.drawString(75, 650, "Detección de posible diferencia de hombros: ")

        for img in image1:
            # Convertir las imágenes de OpenCV a Pillow Image
            image = Image.fromarray(img)
            # Agregar la primera imagen
            pdf_file.drawImage(ImageReader(image), 75, 400, width=3.3*inch, height=3.3*inch)


        for img in image2:
            image = Image.fromarray(img)
            # Agregar la segunda imagen
            pdf_file.drawImage(ImageReader(image), 325, 400, width=3.3*inch, height=3.3*inch)

        dist_1 = f"         Del marcador 4 a 1 hay una distancia de {round(dist_der)}cm"
        dist_2 = f"         Del marcador 3 a 2 hay una distancia de {round(dist_izq)}cm"

        pdf_file.setFont("Helvetica", 14)
        pdf_file.drawString(75, 370, f"Resultado: {result}")
        pdf_file.setFont("Helvetica", 14)
        pdf_file.drawString(75, 340, "Detalle:")
        pdf_file.drawString(75, 310, dist_1)
        pdf_file.drawString(75, 280, dist_2)

        # Guardar el archivo PDF
        pdf_file.save()
    
    def merge_pdf(self):

        # Directorio que contiene los archivos PDF
        directorio = "/home/nahuel/facultad/tif3/pdf"

        # Obtener la lista de archivos PDF en el directorio
        archivos_pdf = [archivo for archivo in os.listdir(directorio) if archivo.endswith(".pdf")]

        # Crear una instancia del objeto PdfFileMerger
        merger = PdfMerger()

        # Iterar sobre los archivos PDF y agregarlos al objeto merger
        for archivo_pdf in archivos_pdf:
            ruta_pdf = os.path.join(directorio, archivo_pdf)
            merger.append(ruta_pdf)

        # Unir los archivos en uno solo
        merger.write("/home/nahuel/facultad/tif3/pdf_merge/paciente.pdf")

        # Cerrar el objeto PdfFileMerger
        merger.close()

    def clear(self):
        path = "/home/nahuel/facultad/tif3/pdf"
        if os.path.exists(path):
            # Obtener una lista de los elementos dentro del directorio (archivos y subdirectorios)
            elementos = os.listdir(path)
            # Recorrer cada elemento y eliminarlos
            for elemento in elementos:
                ruta_elemento = os.path.join(path, elemento)
                # Eliminar el archivo
                os.remove(ruta_elemento)


