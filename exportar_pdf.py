from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image
import cv2

class Export():

    def generate_pdf(image1, image2, dist_der, dist_izq, result):

        path = "/home/nahuel/facultad/tif3/pdf"

        # Crear un nuevo archivo PDF
        pdf_file = canvas.Canvas(path+"/"+"paciente.pdf", pagesize=letter)

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
