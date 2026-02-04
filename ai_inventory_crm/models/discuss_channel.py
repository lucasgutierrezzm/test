from odoo import models
import logging

_logger = logging.getLogger(__name__)

class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    def message_post(self, **kwargs):
        message = super().message_post(**kwargs)

        body = kwargs.get("body")
        if body:
            _logger.warning("AI MODULE: intercepted discuss message = %s", body)

            self.env["ai.agent.logic"].process_message(
                channel=self,
                text=body,
            )

        return message
