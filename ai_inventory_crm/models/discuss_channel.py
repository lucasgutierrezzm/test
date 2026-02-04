from odoo import models
import logging

_logger = logging.getLogger(__name__)

class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_message(self, message, **kwargs):
        _logger.warning("AI MODULE: _notify_message triggered")
        res = super()._notify_message(message, **kwargs)

        if message.body:
            _logger.warning("AI MODULE: message body = %s", message.body)

            self.env['ai.inventory.crm.logic'].process_message(
                channel=self,
                text=message.body
            )

        return res
