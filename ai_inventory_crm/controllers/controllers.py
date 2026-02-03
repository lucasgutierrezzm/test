# from odoo import http


# class AiInventoryCrm(http.Controller):
#     @http.route('/ai_inventory_crm/ai_inventory_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ai_inventory_crm/ai_inventory_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ai_inventory_crm.listing', {
#             'root': '/ai_inventory_crm/ai_inventory_crm',
#             'objects': http.request.env['ai_inventory_crm.ai_inventory_crm'].search([]),
#         })

#     @http.route('/ai_inventory_crm/ai_inventory_crm/objects/<model("ai_inventory_crm.ai_inventory_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ai_inventory_crm.object', {
#             'object': obj
#         })

