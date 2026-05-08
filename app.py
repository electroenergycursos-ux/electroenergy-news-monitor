import streamlit as st
import google.generativeai as genai
import os

# Configuración de ElectroEnergy
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide")
st.title("⚡ ElectroEnergy Group LLC")
st.subheader("Venezuela Energy Sector Monitor")

# Configurar la IA (La clave la pondrás en la configuración de la App)
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if st.button('Generar Reporte de Inteligencia'):
        with st.spinner('Analizando datos de PDVSA, Chevron y el SEN...'):
            prompt = """
            Eres el Ingeniero Jefe de Inteligencia de ElectroEnergy Group LLC. 
            Analiza el sector energético de Venezuela hoy. 
            Reporta sobre: Chevron, PDVSA, licencias OFAC y estado del SEN.
            Formato: Usa títulos en negrita y puntos técnicos.
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)
else:
    st.warning("Por favor, ingresa tu API Key en la barra lateral para comenzar.")
