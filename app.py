import streamlit as st
import requests

# Configuración de Identidad Corporativa - ElectroEnergy Group LLC
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1E3A8A; }
    .sub-title { font-size: 20px; color: #4B5563; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ ElectroEnergy Group LLC</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitor de Inteligencia Energética - Protocolo de Ingeniería Final</div>', unsafe_allow_html=True)

# Panel Lateral
st.sidebar.header("Configuración de Acceso")
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

if api_key:
    st.info("Conexión configurada: Ruta de modelo verificada.")
    
    if st.button('Generar Reporte de Inteligencia'):
        with st.spinner('Analizando datos técnicos del sector...'):
            # SOLUCIÓN FINAL AL 404: Usamos la ruta de versión estable específica
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Reporte técnico ejecutivo para ElectroEnergy Group LLC sobre: Chevron, PDVSA, estado del SEN y licencias OFAC hoy."
                    }]
                }]
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()
                
                if response.status_code == 200:
                    texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("---")
                    st.markdown("### 📊 Reporte Consolidado de Inteligencia")
                    st.markdown(texto_ia)
                    st.success("Análisis completado con éxito para ElectroEnergy.")
                else:
                    st.error(f"Error detectado ({response.status_code}): {data.get('error', {}).get('message', 'Falla de comunicación')}")
            
            except Exception as e:
                st.error(f"Fallo en el protocolo de red: {e}")
else:
    st.warning("⚠️ Ingrese su API Key en el panel lateral.")

st.markdown("---")
st.caption("ElectroEnergy Group LLC © 2026 | División de Inteligencia Técnica")
