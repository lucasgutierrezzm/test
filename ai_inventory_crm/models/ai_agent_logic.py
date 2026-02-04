from odoo import models
import logging

_logger = logging.getLogger(__name__)


class AiAgentLogic(models.AbstractModel):
    _name = "ai.agent.logic"

    def process_message(self, channel, text):
        if "comprar" not in (text or "").lower():
            return

        product = self.env["product.template"].search(
            [("name", "ilike", text)], limit=1
        )
        if not product:
            return

        self.env["crm.lead"].sudo().create({
            "name": f"Interés en {product.display_name}",
            "type": "lead",
        })

        channel.with_context(from_ai_bot=True).message_post(
            body=f"📌 Lead creado en CRM por interés en {product.display_name}."
        )


    def _find_product(self, text):
        ProductTemplate = self.env['product.template']
        words = text.lower().split()
    
        for word in words:
            template = ProductTemplate.search(
                [('name', 'ilike', word)],
                limit=1
            )
            if template:
                return template.product_variant_id
    
        return False

    def _has_commercial_intent(self, text):
        if not text:
            return False
    
        text = text.lower().strip()
    
        keywords = [
            'comprar',
            'quiero',
            'necesito',
            'cotizar',
            'precio',
            'interes',
            'interés',
        ]
    
        return any(keyword in text for keyword in keywords)
