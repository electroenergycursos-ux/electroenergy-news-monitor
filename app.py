import streamlit as st
import google.generativeai as genai

# Configuración de Identidad Corporativa - ElectroEnergy Group LLC
st.set_page_config(page_title="ElectroEnergy Intelligence", layout="wide", page_icon="⚡")

# Estilo visual para el encabezado
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
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password", help="Introduce la clave AIza... para activar el motor de IA.")

if api_key:
    try:
        # Configuración del motor generativo
        genai.configure(api_key=api_key)
        
        # Usamos la ruta completa del modelo para asegurar compatibilidad
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        st.info("Sistema listo para generar reportes técnicos.")
        
        if st.button('Generar Reporte de Inteligencia'):
            with st.spinner('Consultando base de datos y analizando tendencias (Chevron, PDVSA, SEN)...'):
                # Prompt especializado para el sector energético venezolano
                prompt = """
                Actúa como el Ingeniero Jefe de Inteligencia de ElectroEnergy Group LLC. 
                Proporciona un reporte técnico ejecutivo sobre la situación energética en Venezuela hoy.
                Incluye secciones específicas para:
                1. Hidrocarburos: Operaciones de Chevron y PDVSA.
                2. Sistema Eléctrico Nacional (SEN): Estado de la red y generación.
                3. Marco Regulatorio: Licencias OFAC y sanciones.
                Usa un tono profesional, sobrio y técnico.
                """
                
                response = model.generate_content(prompt)
                
                # Despliegue de resultados
                st.markdown("---")
                st.markdown("### 📊 Reporte Consolidado de Inteligencia")
                st.markdown(response.text)
                st.success("Reporte generado exitosamente.")
                
    except Exception as e:
        st.error(f"Error técnico detectado: {e}")
        st.info("Sugerencia: Verifica que la API Key sea correcta y que el modelo 'gemini-1.5-flash' esté habilitado en tu cuenta.")
else:
    st.warning("⚠️ Esperando API Key en la barra lateral para iniciar el monitor.")

# Pie de página profesional
st.markdown("---")
st.caption("ElectroEnergy Group LLC © 2026 | División de Inteligencia y Consultoría Energética")
