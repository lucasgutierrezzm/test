# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)


class MailThreadAICRM(models.Model):
    """
    Extiende mail.thread para agregar funcionalidad de creación automática
    de oportunidades CRM basadas en consultas de productos del inventario.
    """
    _inherit = 'mail.thread'

    @api.model
    def ai_create_crm_opportunity_from_products(self, product_codes, customer_name=None, 
                                                customer_email=None, notes=None):
        """
        Crea una oportunidad en CRM basada en productos consultados por el cliente.
        
        Esta función es llamada por el agente de IA cuando detecta que un cliente
        está consultando sobre productos específicos del inventario.
        
        Args:
            product_codes (list): Lista de códigos de productos (default_code)
            customer_name (str, optional): Nombre del cliente
            customer_email (str, optional): Email del cliente
            notes (str, optional): Notas adicionales sobre la consulta
        
        Returns:
            dict: Diccionario con información del resultado de la operación:
                - success (bool): True si la operación fue exitosa
                - opportunity_id (int): ID de la oportunidad creada
                - opportunity_name (str): Nombre de la oportunidad
                - message (str): Mensaje descriptivo del resultado
        
        Raises:
            No lanza excepciones, retorna un dict con success=False en caso de error
        
        Example:
            >>> result = self.env['mail.thread'].ai_create_crm_opportunity_from_products(
            ...     product_codes=['LAPTOP001', 'MOUSE002'],
            ...     customer_name='Juan Pérez',
            ...     customer_email='juan@example.com',
            ...     notes='Cliente interesado en equipos para oficina'
            ... )
            >>> print(result['message'])
            'Se ha creado la oportunidad "Consulta IA - Laptop HP, Mouse Logitech" con 2 producto(s)'
        """
        try:
            _logger.info(f"Iniciando creación de oportunidad CRM para productos: {product_codes}")
            
            # Validar que se proporcionen códigos de productos
            if not product_codes or not isinstance(product_codes, list):
                return {
                    'success': False,
                    'message': 'Debe proporcionar una lista de códigos de productos'
                }
            
            # Buscar los productos en el inventario por default_code
            products = self.env['product.product'].search([
                ('default_code', 'in', product_codes)
            ])
            
            if not products:
                _logger.warning(f"No se encontraron productos con los códigos: {product_codes}")
                return {
                    'success': False,
                    'message': 'No se encontraron productos con los códigos proporcionados'
                }
            
            # Log de productos encontrados
            _logger.info(f"Productos encontrados: {products.mapped('name')}")
            
            # Buscar o crear el partner (cliente)
            partner = None
            
            # Primero intentar buscar por email si se proporcionó
            if customer_email:
                partner = self.env['res.partner'].search([
                    ('email', '=', customer_email)
                ], limit=1)
                
                if partner:
                    _logger.info(f"Cliente encontrado: {partner.name} (ID: {partner.id})")
            
            # Si no se encontró por email, crear uno nuevo
            if not partner and (customer_name or customer_email):
                partner_vals = {
                    'name': customer_name or customer_email,
                    'customer_rank': 1,  # Marcar como cliente
                }
                
                if customer_email:
                    partner_vals['email'] = customer_email
                
                partner = self.env['res.partner'].create(partner_vals)
                _logger.info(f"Nuevo cliente creado: {partner.name} (ID: {partner.id})")
            
            # Preparar la descripción de la oportunidad
            product_names = ', '.join(products.mapped('name'))
            description_parts = [f"Consulta sobre productos:\n{product_names}"]
            
            if notes:
                description_parts.append(f"\n\nNotas de la conversación:\n{notes}")
            
            description = '\n'.join(description_parts)
            
            # Preparar el nombre de la oportunidad (limitado a 50 caracteres)
            opportunity_name = f'Consulta IA - {product_names}'
            if len(opportunity_name) > 50:
                opportunity_name = f'Consulta IA - {product_names[:47]}...'
            
            # Buscar la primera etapa que no sea ganada para asignar la oportunidad
            stage = self.env['crm.stage'].search([
                ('is_won', '=', False)
            ], limit=1)
            
            if not stage:
                # Si no hay etapas, crear una por defecto
                stage = self.env['crm.stage'].create({
                    'name': 'Nuevo',
                    'sequence': 1,
                })
            
            # Crear la oportunidad en CRM
            opportunity_vals = {
                'name': opportunity_name,
                'description': description,
                'type': 'opportunity',
                'stage_id': stage.id,
            }
            
            # Agregar partner si existe
            if partner:
                opportunity_vals['partner_id'] = partner.id
            
            # Agregar email si se proporcionó (incluso sin partner)
            if customer_email:
                opportunity_vals['email_from'] = customer_email
            
            opportunity = self.env['crm.lead'].create(opportunity_vals)
            
            _logger.info(f"Oportunidad CRM creada: {opportunity.name} (ID: {opportunity.id})")
            
            # Calcular el valor esperado basado en los precios de lista
            expected_revenue = sum(products.mapped('list_price'))
            
            if expected_revenue > 0:
                opportunity.write({'expected_revenue': expected_revenue})
                _logger.info(f"Ingreso esperado calculado: ${expected_revenue:.2f}")
            
            # Agregar los productos como mensaje en la oportunidad con formato HTML
            product_list_html = "".join([
                f"<li><strong>{p.name}</strong> (Ref: {p.default_code or 'N/A'}) - "
                f"${p.list_price:.2f}</li>"
                for p in products
            ])
            
            opportunity.message_post(
                body=f"""
                    <p><strong>Productos consultados:</strong></p>
                    <ul>
                        {product_list_html}
                    </ul>
                    <p><strong>Valor total estimado:</strong> ${expected_revenue:.2f}</p>
                """,
                subject="Productos de interés",
                message_type='comment'
            )
            
            # Retornar resultado exitoso
            return {
                'success': True,
                'opportunity_id': opportunity.id,
                'opportunity_name': opportunity.name,
                'expected_revenue': expected_revenue,
                'products_count': len(products),
                'message': (
                    f'Se ha creado la oportunidad "{opportunity.name}" con '
                    f'{len(products)} producto(s) por un valor estimado de ${expected_revenue:.2f}'
                )
            }
            
        except Exception as e:
            # Capturar cualquier error y retornar información útil
            error_msg = f"Error al crear oportunidad CRM: {str(e)}"
            _logger.error(error_msg, exc_info=True)
            
            return {
                'success': False,
                'message': error_msg
            }

    @api.model
    def ai_get_product_availability(self, product_codes):
        """
        Consulta la disponibilidad de productos en el inventario.
        
        Función auxiliar que puede ser utilizada por el agente de IA para
        verificar el stock de productos antes de crear una oportunidad.
        
        Args:
            product_codes (list): Lista de códigos de productos
        
        Returns:
            dict: Diccionario con información de disponibilidad de cada producto
        
        Example:
            >>> result = self.env['mail.thread'].ai_get_product_availability(['LAPTOP001'])
            >>> print(result)
            {
                'success': True,
                'products': [
                    {
                        'code': 'LAPTOP001',
                        'name': 'Laptop HP Pavilion',
                        'qty_available': 15.0,
                        'price': 899.99,
                        'available': True
                    }
                ]
            }
        """
        try:
            if not product_codes or not isinstance(product_codes, list):
                return {
                    'success': False,
                    'message': 'Debe proporcionar una lista de códigos de productos'
                }
            
            products = self.env['product.product'].search([
                ('default_code', 'in', product_codes)
            ])
            
            if not products:
                return {
                    'success': False,
                    'message': 'No se encontraron productos con los códigos proporcionados'
                }
            
            product_info = []
            for product in products:
                product_info.append({
                    'code': product.default_code,
                    'name': product.name,
                    'qty_available': product.qty_available,
                    'price': product.list_price,
                    'available': product.qty_available > 0,
                })
            
            return {
                'success': True,
                'products': product_info
            }
            
        except Exception as e:
            _logger.error(f"Error al consultar disponibilidad: {str(e)}")
            return {
                'success': False,
                'message': f'Error al consultar disponibilidad: {str(e)}'
            }
