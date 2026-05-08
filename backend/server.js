const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

app.get('/api/news', async (req, res) => {
    try {
        const currentDate = new Date().toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
        
        const systemPrompt = `Eres el Ingeniero Jefe de Inteligencia de ElectroEnergy Group LLC. 
        Analiza el sector energético de Venezuela hoy (${currentDate}). 
        Busca datos sobre: Chevron, PDVSA, licencias OFAC, estado del SEN, y generación.
        Responde estrictamente en JSON con este formato:
        {
          "news": [{"title": "string", "source": "string", "date": "string", "url": "string", "summary": "string", "category": "Oil & Gas|Grid|Sanctions", "impact": "Low|Medium|High|Critical"}],
          "ai_summary": "Resumen técnico de 3 líneas."
        }`;

        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
        
        const response = await axios.post(geminiUrl, {
            contents: [{ parts: [{ text: "Genera reporte energético para Venezuela hoy." }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] },
            tools: [{ "google_search": {} }],
            generationConfig: { responseMimeType: "application/json", temperature: 0.1 }
        });

        res.json(JSON.parse(response.data.candidates[0].content.parts[0].text));
    } catch (error) {
        res.status(500).json({ error: "Error al sincronizar inteligencia." });
    }
});

app.listen(PORT, () => console.log(`🚀 Servidor en puerto ${PORT}`));