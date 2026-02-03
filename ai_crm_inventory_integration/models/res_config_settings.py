from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_ai_crm_inventory_integration = fields.Boolean(
        string="AI CRM Integration Module"
    )
