import os
import json
import feedparser
import psycopg2
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. CONFIGURACIÓN Y SEGURIDAD
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DB_URL = os.getenv("SUPABASE_DB_URL")

app = FastAPI()

# Permitir acceso desde tu Dashboard de React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el modelo de IA
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. MOTOR DE INTELIGENCIA (IA)
def analizar_noticia(titular):
    prompt = f"""
    Eres un analista experto en energía y riesgo geopolítico en Venezuela.
    Analiza el siguiente titular y responde ESTRICTAMENTE en formato JSON.
    
    Titular: "{titular}"
    
    JSON esperado:
    {{
        "categoria": "Petróleo" | "Gas" | "Eléctrico" | "Sanciones" | "Geopolítica",
        "impacto": un número del 1 al 100,
        "resumen_ejecutivo": "Máximo 15 palabras"
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Limpieza de formato Markdown en la respuesta de la IA
        clean_json = response.text.replace('```json', '').replace('
```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Error analizando con IA: {e}")
        return {
            "categoria": "Otros",
            "impacto": 50,
            "resumen_ejecutivo": "No se pudo analizar la noticia."
        }

# 3. ENDPOINTS DE LA API
@app.get("/")
def home():
    return {"status": "online", "monitor": "Venezuela Energy Intelligence"}

@app.get("/update-monitor")
def update_monitor():
    # Fuentes estratégicas: Reuters y Bloomberg
    feeds = [
        "https://www.reutersagency.com/feed/?best-topics=energy&format=xml",
        "http://feeds.bloomberg.com/energy/news.rss"
    ]
    
    news_processed = 0
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        for url in feeds:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]: # Analizamos las 10 más recientes
                # Filtro de relevancia técnica (Venezuela/PDVSA/Guri)
                if any(x in entry.title.upper() for x in ["VENEZUELA", "PDVSA", "OIL", "CITGO", "GURI", "GAS"]):
                    
                    # Pasar por la IA
                    analisis = analizar_noticia(entry.title)
                    
                    # Guardar en Supabase (Evita duplicados por URL)
                    cur.execute("""
                        INSERT INTO energy_intel (title, category, impact_score, summary, source_url)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (source_url) DO NOTHING
                    """, (
                        entry.title, 
                        analisis['categoria'], 
                        analisis['impacto'], 
                        analisis['resumen_ejecutivo'], 
                        entry.link
                    ))
                    news_processed += 1
        
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "Success", "processed_count": news_processed}
        
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@app.get("/get-intel")
def get_intel():
    # Este endpoint servirá los datos a tu Dashboard de React
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM energy_intel ORDER BY created_at DESC LIMIT 20")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"data": rows}
    except Exception as e:
        return {"error": str(e)}
