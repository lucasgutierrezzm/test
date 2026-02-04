from odoo import models
import logging

_logger = logging.getLogger(__name__)


class AIInventoryCRMLogic(models.Model):
    _name = 'ai.inventory.crm.logic'
    _description = 'AI Inventory CRM Bridge Logic'

    def process_message(self, channel, text):
        _logger.warning("AI MODULE: process_message called with text=%s", text)

        product = self._find_product(text)
        if not product:
            _logger.warning("AI MODULE: no product found for text=%s", text)
            return

        _logger.warning("AI MODULE: product found = %s", product.display_name)

        if self._has_commercial_intent(text):
            _logger.warning("AI MODULE: commercial intent detected")

            self.env['crm.lead'].sudo().create({
                'name': f'Interés en {product.display_name}',
                'type': 'lead',
                'description': text,
            })

            channel.message_post(
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
        keywords = ['comprar', 'cotizar', 'precio', 'cliente']
        return any(k in text.lower() for k in keywords)
