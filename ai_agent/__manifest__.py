

{
    'name': "AI Agent",
    'summary': "Módulo de ejemplo para integrar IA (resúmenes con Gemini) en Odoo",
    'description': """
Módulo de prueba que permite generar resúmenes de texto utilizando
un servicio de IA externo (Google Gemini) desde un botón en el formulario.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Tools',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',   # 🔴 ESTO ES OBLIGATORIO
        'views/views.xml',                # vistas del modelo
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
