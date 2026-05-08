import os
import feedparser
import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json

# 1. Cargar configuración segura
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DB_URL = os.getenv("SUPABASE_DB_URL")

app = FastAPI()

# Permitir que tu Dashboard de React lea los datos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configurar la IA (Gemini 3 Flash para velocidad)
model = genai.GenerativeModel('gemini-1.5-flash')

def analizar_noticia(titular):
    prompt = f"""
    Analiza este titular de energía sobre Venezuela y responde SOLO en formato JSON:
    Titular: "{titular}"
    
    JSON:
    {{
        "categoria": "Petróleo" | "Gas" | "Eléctrico" | "Sanciones" | "Geopolítica",
        "impacto": un número del 1 al 100,
        "resumen": "una frase corta"
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Limpiar la respuesta para obtener el JSON puro
        clean_json = response.text.replace('```json', '').replace('
```', '').strip()
        return json.loads(clean_json)
    except:
        return {"categoria": "Otros", "impacto": 50, "resumen": "Error en análisis"}

@app.get("/update-monitor")
def update_monitor():
    # 3. Leer fuentes de Reuters y Bloomberg
    feeds = [
        "https://www.reutersagency.com/feed/?best-topics=energy&format=xml",
        "http://feeds.bloomberg.com/energy/news.rss"
    ]
    
    results = []
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    for url in feeds:
        f = feedparser.parse(url)
        for entry in f.entries[:5]:
            # Solo procesar noticias relacionadas con Venezuela o PDVSA
            if any(x in entry.title.upper() for x in ["VENEZUELA", "PDVSA", "OIL", "CITGO", "GURI"]):
                analisis = analizar_noticia(entry.title)
                
                # 4. Guardar en Supabase (Evita duplicados con ON CONFLICT)
                cur.execute("""
                    INSERT INTO energy_intel (title, category, impact_score, summary, source_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (source_url) DO NOTHING
                """, (entry.title, analisis['categoria'], analisis['impacto'], analisis['resumen'], entry.link))
                
                results.append({"title": entry.title, "intel": analisis})
    
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "Monitor Actualizado", "news_processed": len(results)}

@app.get("/")
def home():
    return {"message": "Venezuela Energy Monitor API is Online"}
