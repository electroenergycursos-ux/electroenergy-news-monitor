import streamlit as st
import google.generativeai as genai

# Configuración de Identidad Corporativa - ElectroEnergy Group LLC
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide", page_icon="⚡")

# Estilo visual profesional
st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1E3A8A; }
    .sub-title { font-size: 20px; color: #4B5563; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ ElectroEnergy Group LLC</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Venezuela Energy Sector Monitor - Inteligencia de Campo</div>', unsafe_allow_html=True)

# Panel Lateral para Autenticación
st.sidebar.header("Configuración de Acceso")
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

if api_key:
    try:
        # SOLUCIÓN AL ERROR 404: Forzamos el uso de la API v1 estable y transporte REST
        genai.configure(api_key=api_key, transport='rest')
        
        # Inicializamos el modelo Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')

        st.info("Conexión establecida. Sistema listo para generar reportes.")
        
        if st.button('Generar Reporte de Inteligencia'):
            with st.spinner('Procesando datos técnicos del sector energético...'):
                # Prompt estructurado para consultoría técnica
                prompt = """
                Actúa como el Ingeniero Jefe de Inteligencia de ElectroEnergy Group LLC. 
                Proporciona un reporte ejecutivo sobre el sector energético en Venezuela hoy.
                Analiza puntos críticos en:
                1. Operaciones de Chevron y PDVSA.
                2. Estado actual del SEN (Generación y Transmisión).
                3. Actualizaciones de licencias OFAC.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("### 📊 Reporte Consolidado de Inteligencia")
                st.markdown(response.text)
                st.success("Análisis completado exitosamente.")
                
    except Exception as e:
        st.error(f"Ajuste técnico requerido: {e}")
else:
    st.warning("⚠️ Ingrese su API Key en el panel lateral para activar el monitor.")

st.markdown("---")
st.caption("ElectroEnergy Group LLC © 2026 | División de Inteligencia y Consultoría Energética")
