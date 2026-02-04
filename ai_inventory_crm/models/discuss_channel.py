from odoo import models
import logging

_logger = logging.getLogger(__name__)


class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    def message_post(self, **kwargs):
        message = super().message_post(**kwargs)

        # 🛑 cortar loop: mensajes creados por el bot
        if self.env.context.get("from_ai_bot"):
            return message

        body = kwargs.get("body")
        if not body:
            return message

        _logger.warning("AI MODULE: intercepted discuss message = %s", body)

        self.env["ai.agent.logic"].with_context(
            from_ai_bot=True
        ).process_message(
            channel=self,
            text=body,
        )

        return message
