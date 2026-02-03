# -*- coding: utf-8 -*-
{
    'name': 'AI CRM Inventory Integration',
    'version': '19.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'Integración IA para crear oportunidades CRM desde consultas de inventario',
    'description': '''
        AI CRM Inventory Integration
        =============================
        
        Este módulo extiende las capacidades del agente de IA de Odoo para:
        
        * Detectar interés del cliente en productos del inventario
        * Crear automáticamente oportunidades en CRM
        * Vincular conversaciones del chat con oportunidades
        * Facilitar el seguimiento de ventas
        * Calcular valor esperado basado en productos consultados
        
        Características principales:
        ----------------------------
        - Búsqueda inteligente de productos por código
        - Creación o vinculación automática de clientes
        - Registro detallado de productos en la oportunidad
        - Cálculo automático de ingreso esperado
        - Integración perfecta con el chat de IA
        
        Configuración:
        --------------
        1. Instalar el módulo
        2. Crear una Acción del Servidor en Ajustes → Técnico
        3. Asociar la acción a un tema de IA
        4. Configurar el agente de IA con el tema creado
        
    ''',
    'author': 'Tu Nombre / Tu Empresa',
    'website': 'https://www.tuempresa.com',
    'depends': [
        'base',
        'mail',
        'ai',
        'stock',
        'crm',
        'website_livechat',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}

