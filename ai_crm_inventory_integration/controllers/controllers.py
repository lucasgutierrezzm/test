# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class AIRMInventoryController(http.Controller):
    """
    Controlador para endpoints relacionados con la integración de IA, CRM e Inventario.
    
    Este controlador puede extenderse para agregar endpoints REST que permitan
    interacciones adicionales con el módulo desde aplicaciones externas.
    """
    
    @http.route('/ai_crm_inventory/test', type='jsonrpc', auth='user', methods=['POST'])
    def test_integration(self, **kwargs):
        """
        Endpoint de prueba para verificar que el módulo esté funcionando correctamente.
        
        Returns:
            dict: Información del estado del módulo
        """
        try:
            return {
                'success': True,
                'message': 'AI CRM Inventory Integration está funcionando correctamente',
                'version': '19.0.1.0.0'
            }
        except Exception as e:
            _logger.error(f"Error en test_integration: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

