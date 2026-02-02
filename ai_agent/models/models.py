from odoo import models, fields
import requests
import logging
import json

_logger = logging.getLogger(__name__)

class AIAgentRecord(models.Model):
    _name = 'ai.agent.record'
    _description = 'AI Agent Record'

    name = fields.Char(string="Título", required=True)
    input_text = fields.Text(string="Texto a resumir")
    ai_summary = fields.Text(string="Resumen generado por IA")

    def action_generate_summary(self):
        # ADMINISTRACIÓN DIRECTA DE LA CLAVE
        # Asegúrate de que no haya espacios dentro de las comillas
        api_key = "AIzaSyCcKjGJXDRYX7eebK-y4UZXPIB0Y00oINs".strip()

        # URL usando v1beta (que suele ser más flexible con Flash)
        # Importante: El modelo es 'gemini-1.5-flash' sin el '-latest'
        model_name = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json",
        }

        for record in self:
            if not record.input_text:
                continue

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"Haz un resumen completo, claro y detallado del siguiente texto, incluyendo contexto, personajes principales y propósito de la obra:\n\n{record.input_text}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 800
                }
            }

            try:
                # Log para ver qué URL se está llamando exactamente (mira el log de Odoo)
                _logger.info(f"Llamando a Gemini con URL: {url.split('key=')[0]}key=HIDDEN")
                
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                # Si esto falla, el raise_for_status nos dará el error detallado
                response.raise_for_status()
                
                data = response.json()
                
                if 'candidates' in data and data['candidates']:
                    summary = data['candidates'][0]['content']['parts'][0]['text']
                    record.ai_summary = summary
                else:
                    record.ai_summary = "Google no devolvió resultados (posible filtro de seguridad)."

            except requests.exceptions.HTTPError as e:
                _logger.error(f"Error HTTP: {response.status_code} - {response.text}")
                record.ai_summary = f"Error {response.status_code}: Revisa si la API Key es válida y el modelo existe."
            except Exception as e:
                _logger.exception("Error inesperado")
                record.ai_summary = f"Error técnico: {str(e)}"
