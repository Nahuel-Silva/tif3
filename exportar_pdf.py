from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image

class Export():

    def generate_pdf(image1, image2, dist_der, dist_izq, result, name):

        path = "/home/nahuel/facultad/tif3/pdf"

        # Crear un nuevo archivo PDF
        pdf_file = canvas.Canvas(path+"/"+"paciente_"+name, pagesize=letter)


        for img in image1:
            # Convertir las imágenes de OpenCV a Pillow Image
            image = Image.fromarray(img)
            # Agregar la primera imagen
            pdf_file.drawImage(ImageReader(image), 100, 550, width=3*inch, height=3*inch)


        for img in image2:
            image = Image.fromarray(img)
            # Agregar la segunda imagen
            pdf_file.drawImage(ImageReader(image), 350, 550, width=3*inch, height=3*inch)

        dist_1 = f"De marcador 3 a 1 hay una distancia de {dist_izq}"
        dist_2 = f"De marcador 2 a 0 hay una distancia de {dist_der}"
        # Agregar el string_value
        pdf_file.drawString(100, 500, result)
        pdf_file.drawString(100, 480, dist_1)
        pdf_file.drawString(100, 460, dist_2)

        # Guardar el archivo PDF
        pdf_file.save()
