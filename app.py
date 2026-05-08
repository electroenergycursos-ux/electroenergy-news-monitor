import streamlit as st
import requests
import json

# Configuración de Identidad Corporativa - ElectroEnergy Group LLC
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1E3A8A; }
    .sub-title { font-size: 20px; color: #4B5563; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ ElectroEnergy Group LLC</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitor de Inteligencia Energética - Protocolo Final v1</div>', unsafe_allow_html=True)

# Panel Lateral
st.sidebar.header("Configuración de Acceso")
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

if api_key:
    st.info("Conexión configurada mediante protocolo REST v1 (Ruta Calificada).")
    
    if st.button('Generar Reporte de Inteligencia'):
        with st.spinner('Analizando datos de Chevron, PDVSA y el SEN...'):
            # SOLUCIÓN AL 404: Usamos la ruta de modelos completa
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            # Ajustamos el payload para asegurar compatibilidad total con v1
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Actúa como Ingeniero Jefe de ElectroEnergy. Reporte técnico hoy sobre Chevron, PDVSA y el SEN en Venezuela."
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1
                }
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("---")
                    st.markdown("### 📊 Reporte Consolidado de Inteligencia")
                    st.markdown(texto_ia)
                    st.success("Análisis completado con éxito.")
                else:
                    # Si falla, mostramos el error exacto de Google
                    mensaje_error = data.get('error', {}).get('message', 'Error desconocido')
                    st.error(f"Error de la API ({response.status_code}): {mensaje_error}")
            
            except Exception as e:
                st.error(f"Fallo en la comunicación: {e}")
else:
    st.warning("⚠️ Ingrese su API Key en el panel lateral.")

st.markdown("---")
st.caption("ElectroEnergy Group LLC © 2026 | División de Consultoría")
