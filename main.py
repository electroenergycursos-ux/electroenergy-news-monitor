import os
import json
import feedparser
import psycopg2
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. CONFIGURACIÓN
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DB_URL = os.getenv("SUPABASE_DB_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. MOTOR DE IA (LÍNEAS CORTAS PARA EVITAR ERRORES)
def analizar_noticia(titular):
    prompt = f"Analiza este titular de energía en Venezuela y responde solo JSON: {titular}"
    try:
        response = model.generate_content(prompt)
        texto = response.text
        # Limpiamos el texto paso a paso para evitar que la línea sea muy larga
        texto = texto.replace('```json', '')
        texto = texto.replace('
```', '')
        clean_json = texto.strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"categoria": "Otros", "impacto": 50, "resumen_ejecutivo": "Error IA"}

# 3. ENDPOINTS
@app.get("/")
def home():
    return {"status": "online", "monitor": "ElectroEnergy Intelligence"}

@app.get("/update-monitor")
def update_monitor():
    feeds = ["https://www.reutersagency.com/feed/?best-topics=energy&format=xml"]
    news_processed = 0
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS energy_intel (
                id SERIAL PRIMARY KEY,
                title TEXT,
                category TEXT,
                impact_score INTEGER,
                summary TEXT,
                source_url TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        for url in feeds:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                if any(x in entry.title.upper() for x in ["VENEZUELA", "PDVSA", "OIL", "GAS"]):
                    analisis = analizar_noticia(entry.title)
                    cur.execute("""
                        INSERT INTO energy_intel (title, category, impact_score, summary, source_url)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (source_url) DO NOTHING
                    """, (entry.title, analisis['categoria'], analisis['impacto'], analisis['resumen_ejecutivo'], entry.link))
                    news_processed += 1
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "Success", "processed": news_processed}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@app.get("/get-intel")
def get_intel():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT title, category, summary FROM energy_intel LIMIT 10")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"data": rows}
    except Exception as e:
        return {"error": str(e)}
