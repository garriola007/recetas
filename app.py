import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

key = st.text_input('input your Key', type='password')

st.title(key)


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
    response = client.Chat.Completion.create(
            model = 'gpt-4o',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            max_tokents = 1020,
            temperatura = 0.9     
    )

    return response.choices[0].message.content

