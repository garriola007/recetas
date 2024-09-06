import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

key = st.text_input('input your Key', type='password')

st.title(key)
