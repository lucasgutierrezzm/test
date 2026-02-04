{
    'name': 'AI Inventory CRM Bridge',
    'version': '1.0',
    'category': 'Artificial Intelligence',
    'summary': 'Agente IA que conecta Inventario con CRM',
    'depends': [
        'base',
        'product',
        'crm',
        'mail',
        'ai',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
}

