# from odoo import http


# class AiAgent(http.Controller):
#     @http.route('/ai_agent/ai_agent', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ai_agent/ai_agent/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ai_agent.listing', {
#             'root': '/ai_agent/ai_agent',
#             'objects': http.request.env['ai_agent.ai_agent'].search([]),
#         })

#     @http.route('/ai_agent/ai_agent/objects/<model("ai_agent.ai_agent"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ai_agent.object', {
#             'object': obj
#         })

