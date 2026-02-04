from odoo import models, api
from odoo.tools import html2plaintext
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        message = super().create(vals)

        try:
            # Solo mensajes humanos en canales de Discuss
            if (
                message.model != 'discuss.channel'
                or not message.body
                or message.author_id.user_ids
                and message.author_id.user_ids[0].login == '__odoobot__'
            ):
                return message

            text = html2plaintext(message.body).strip()

            if not text:
                return message

            _logger.warning("AI MODULE: clean message = %s", text)

            channel = self.env['discuss.channel'].browse(message.res_id)

            self.env['ai.inventory.crm.logic'].process_message(
                channel=channel,
                text=text
            )

        except Exception as e:
            _logger.error("AI MODULE ERROR: %s", e)

        return message
