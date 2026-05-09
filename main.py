import os
import json
import feedparser
import psycopg2
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DB_URL = os.getenv("SUPABASE_DB_URL")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model = genai.GenerativeModel('gemini-1.5-flash')

def analizar_noticia(titular):
    # Prompt simplificado para evitar caracteres especiales en el codigo
    p = f"Analiza este titular y responde solo un JSON con las llaves categoria, impacto y resumen_ejecutivo: {titular}"
    try:
        r = model.generate_content(p)
        t = r.text
        # Usamos un metodo de limpieza que no usa comillas invertidas en el codigo fuente
        for borrar in ["`", "json"]:
            t = t.replace(borrar, "")
        return json.loads(t.strip())
    except:
        return {"categoria": "Otros", "impacto": 50, "resumen_ejecutivo": "Error"}

@app.get("/")
def home():
    return {"status": "online", "business": "ElectroEnergy"}

@app.get("/update-monitor")
def update_monitor():
    url = "[https://www.reutersagency.com/feed/?best-topics=energy&format=xml](https://www.reutersagency.com/feed/?best-topics=energy&format=xml)"
    count = 0
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS energy_intel (id SERIAL PRIMARY KEY, title TEXT, category TEXT, impact_score INTEGER, summary TEXT, source_url TEXT UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        
        f = feedparser.parse(url)
        for e in f.entries[:5]:
            if any(k in e.title.upper() for k in ["VENEZUELA", "PDVSA", "OIL", "GAS"]):
                res = analizar_noticia(e.title)
                cur.execute("INSERT INTO energy_intel (title, category, impact_score, summary, source_url) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (source_url) DO NOTHING", (e.title, res['categoria'], res['impacto'], res['resumen_ejecutivo'], e.link))
                count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "Success", "news_added": count}
    except Exception as err:
        return {"status": "Error", "msg": str(err)}
