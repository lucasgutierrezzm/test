from odoo import models

class AIInventoryCRMLogic(models.Model):
    _name = 'ai.inventory.crm.logic'
    _description = 'AI Inventory CRM Bridge Logic'

    def process_message(self, channel, text):
        product = self._find_product(text)
        if not product:
            _logger.warning("AI MODULE: no product found for text=%s", text)
            return

        _logger.warning("AI MODULE: product found = %s", product.display_name)

        stock = product.qty_available

        if self._has_commercial_intent(text):
            lead = self.env['crm.lead'].create({
                'name': f'Interés en {product.display_name}',
                'description': (
                    f'Consulta IA:\n{text}\n\n'
                    f'Stock disponible: {stock}'
                ),
            })

            channel.message_post(
                body=f"📌 Lead creado en CRM por interés en {product.display_name}."
            )

    def _find_product(self, text):
        ProductTemplate = self.env['product.template']
            template = ProductTemplate.search(
            [('name', 'ilike', text)],
            limit=1
        )

        if not template:
            return False
    
        return template.product_variant_id

    def _has_commercial_intent(self, text):
        keywords = ['comprar', 'cotizar', 'precio', 'cliente']
        return any(k in text.lower() for k in keywords)
