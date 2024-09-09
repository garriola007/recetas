import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

key = st.text_input('input your Key', type='password')
client = OpenAI(api_key=key)
#st.title(key)


def generar_receta(ingredientes):
    system_prompt = f'''
        Eres un chef de primera clase premiado con estrellas Michellin.
        '''
    user_prompt = f'''
        Crea una receta detallada unicamente con los siguientes ingredientes: { ', '.join(ingredientes) }
        Por favor, formate la receta de la siguiente manera:
        Título de la receta:
        Ingredientes de la receta con tamaño y porción:
        Lista de instrucciones para la receta:
        '''
    response = client.chat.completions.create(
            model = 'gpt-4o',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            max_tokens = 1020,
            temperature = 0.9     
    )

    return response.choices[0].message.content

def obtener_nombre_receta(texto):
    lineas = texto.splitlines()
    return lineas[1]

def generar_imagen(titulo_receta):
    prompt = f'''
        Genera una imagen fotorealista del plato final titulado: "{ titulo_receta }".
        El plato debe estar bellamente presentado en un plato de cerámica con un enfoque cercano en las texturas y colores.
        de los ingredientes.
        La ambientacion debe ser una mesa de madera con iluminacion natural para resaltar las características apetitosas de la comida. 
        Asegurate de que la imagen capture los colores ricos y vibrantes y los detalles intrincados de la comida, haciendola parecer recién preparada y lista para comer. 
        La imagen debe estar en formato JPG.
    '''
    response = client.images.generate(
        model = 'Dalle-e-3',
        prompt = prompt,
        style = 'vivid',
        size = '1024x1024',
        quality = 'high',
        n=1
    )
    return response.data[0].url

def guardar_pdf(titulo_receta, receta, imagen_url):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(Arial, 12)

    pdf.set_font(Arial, B, 15)
    pdf.cell(0, 10, titulo_receta, 0, C)

    response = requests.get(imagen_url)
    img = Image.Open(BytesIO(response.content)).convert('RGB')
    img_path = f"{titulo_receta.replace(' ', '_')}.jpg"
    img.save(img_path, JPEG)

    pdf.ln(10)
    img_width = pdf.image(img_path, x=(pdf.w -img_width)/2, w=img_width, type='JPEG')
    pdf.ln(10)

    pdf.set_font(Arial, 12)
    for line in receta.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_file = "receta.pdf"
    pdf.output(pdf_file)

    return pdf_file

st.title("Generador")
st.write("Ingrese los ingredientes para genera una receta personalizada")
ingredientes = st.text_input('Ingredientes separadospor coma:', 'ingrediente1, ingrediente2, etc')


if st.button('Generar receta'):
    ingredientes_lista = [ing.strip() for ing in ingredientes.split(",")]
    receta = generar_receta(ingredientes_lista)
    st.session_state.receta = receta
    titulo_receta= obtener_nombre_receta(receta)
    st.session_state.titulo_receta = titulo_receta
    imagen_receta = generar_imagen(titulo_receta)
    st.session_state.imagen_receta = imagen_receta

if st.session_state:
    st.write(f"{st.session_state.titulo_receta}")
    st.write(st.session_state.receta)
    st.image(st.session_state.imagen_receta, caption=st.session_state.titulo_receta)


