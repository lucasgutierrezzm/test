from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ai_api_key = fields.Char(
        string='AI API Key',
        config_parameter='ai_inventory_crm.api_key'
    )