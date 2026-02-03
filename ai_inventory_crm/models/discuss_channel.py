from odoo import models

class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_message(self, message, **kwargs):
        res = super()._notify_message(message, **kwargs)

        if message.body and message.author_id:
            self.env['ai.inventory.crm.logic'].process_message(
                channel=self,
                text=message.body
            )
        return res
