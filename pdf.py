import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

def guardar_pdf(titulo_receta, receta, imagen_url):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
 
 
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(0, 10, titulo_receta)

    #response = requests.get(imagen_url)
    #img = Image.Open(BytesIO(response.content)).convert('RGB')
    #img_path = f"{titulo_receta.replace(' ', '_')}.jpg"
    #img.save(img_path, JPEG)

    #pdf.ln(10)
    #img_width = pdf.image(img_path, x=(pdf.w -img_width)/2, w=img_width, type='JPEG')
    #pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    for line in receta.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_file = "receta.pdf"
    pdf.output(pdf_file)

    return pdf_file

titulo_receta = "titulo receta"
receta = "receta"
imagen_url = "imagen.png"

guardar_pdf(titulo_receta, receta, imagen_url)

#pdf = FPDF()
#pdf.add_page()
#pdf.set_font('Arial', 'B', 16)
#pdf.cell(40, 10, 'Hello World!')
#pdf.output('tuto1.pdf', 'F')