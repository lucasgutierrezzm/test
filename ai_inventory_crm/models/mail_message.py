from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        message = super().create(vals)

        try:
            if (
                message.model == 'discuss.channel'
                and message.body
                and message.author_id
            ):
                _logger.warning(
                    "AI MODULE: mail.message intercepted: %s",
                    message.body
                )

                channel = self.env['discuss.channel'].browse(message.res_id)
                self.env['ai.inventory.crm.logic'].process_message(
                    channel=channel,
                    text=message.body
                )
        except Exception as e:
            _logger.error("AI MODULE ERROR: %s", e)

        return message
