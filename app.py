import streamlit as st
import google.generativeai as genai

# Configuración de Identidad Corporativa - ElectroEnergy Group LLC
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide", page_icon="⚡")

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
        # CONFIGURACIÓN CRÍTICA: Forzamos la versión v1 para evitar el error 404
        genai.configure(api_key=api_key, transport='rest') 
        
        # Usamos el identificador del modelo compatible con v1
        model = genai.GenerativeModel('gemini-1.5-flash')

        st.info("Sistema listo para generar reportes técnicos.")
        
        if st.button('Generar Reporte de Inteligencia'):
            with st.spinner('Analizando datos técnicos del sector...'):
                prompt = """
                Actúa como el Ingeniero Jefe de Inteligencia de ElectroEnergy Group LLC. 
                Proporciona un reporte técnico ejecutivo sobre la situación energética en Venezuela hoy.
                Analiza: Chevron, PDVSA, estado del SEN y licencias OFAC.
                """
                # Forzamos la generación a través del modelo validado
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown("### 📊 Reporte Consolidado de Inteligencia")
                st.markdown(response.text)
                st.success("Reporte generado exitosamente.")
                
    except Exception as e:
        st.error(f"Error técnico detectado: {e}")
else:
    st.warning("⚠️ Esperando API Key en la barra lateral.")

st.markdown("---")
st.caption("ElectroEnergy Group LLC © 2026 | División de Inteligencia y Consultoría Energética")
