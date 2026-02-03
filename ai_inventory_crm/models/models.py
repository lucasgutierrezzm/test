# from odoo import models, fields, api


# class ai_inventory_crm(models.Model):
#     _name = 'ai_inventory_crm.ai_inventory_crm'
#     _description = 'ai_inventory_crm.ai_inventory_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

