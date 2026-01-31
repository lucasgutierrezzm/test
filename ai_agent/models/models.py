from odoo import models, fields
import requests
import logging

_logger = logging.getLogger(__name__)


class AIAgentRecord(models.Model):
    _name = 'ai.agent.record'
    _description = 'AI Agent Record'

    name = fields.Char(string="Título", required=True)
    input_text = fields.Text(string="Texto a resumir")
    ai_summary = fields.Text(string="Resumen generado por IA")

    def action_generate_summary(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('ai_agent.gemini_api_key')

        if not api_key:
            # fallback sin IA real
            for record in self:
                text = record.input_text or ""
                record.ai_summary = text[:150] + "..." if len(text) > 150 else text
            return

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json",
        }

        for record in self:
            prompt = f"""
                    Eres un asistente que resume documentación técnica.
                    
                    INSTRUCCIONES:
                    - No repitas el texto original.
                    - No incluyas comandos de consola.
                    - Extrae solo la idea principal.
                    - Máximo 3 líneas.
                    
                    TEXTO:
                    {record.input_text}
                    """

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()

                summary = data['candidates'][0]['content']['parts'][0]['text']
                record.ai_summary = summary

            except Exception as e:
                _logger.exception("Error llamando a Gemini")
                record.ai_summary = f"Error generando resumen: {str(e)}"
