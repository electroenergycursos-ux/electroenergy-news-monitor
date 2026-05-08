const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();

// Configuración de seguridad para permitir conexión desde el frontend
app.use(cors());
app.use(express.json());

// Puerto configurado para Render (10000)
const PORT = process.env.PORT || 10000;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

// Ruta raíz para verificar que el servidor de ElectroEnergy está activo
app.get('/', (req, res) => {
    res.send('🚀 Servidor de ElectroEnergy Group LLC Operativo');
});

// Ruta principal de inteligencia energética
app.get('/api/intelligence', async (req, res) => {
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

        // URL actualizada a v1 para evitar el error 404
        const geminiUrl = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
        
        const response = await axios.post(geminiUrl, {
            contents: [{ parts: [{ text: "Genera reporte energético detallado para Venezuela hoy." }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] },
            generationConfig: { responseMimeType: "application/json", temperature: 0.1 }
        });

        // Envío de datos procesados al monitor
        res.json(JSON.parse(response.data.candidates[0].content.parts[0].text));
        
    } catch (error) {
        console.error("Error en el servidor:", error.message);
        res.status(500).json({ error: "Error al sincronizar inteligencia energética." });
    }
});

app.listen(PORT, () => console.log(`🚀 Servidor en puerto ${PORT}`));
