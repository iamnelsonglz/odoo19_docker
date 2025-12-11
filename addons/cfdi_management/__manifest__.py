{
    'name': 'CFDI Management',
    'version': '1.0.0',
    'author': 'Nelson René Gordillo González',
    'category': 'Accounting',
    'summary': 'CFDI Management Module',
    'description': """
        Module to manage the issuance and reception of CFDI in Odoo.
    """,
    'depends': [
        'base',
        'mail'
    ],
    'data':[
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Views
        'views/main_menu_view.xml',
        'views/cfdi_issued_view.xml',
        'views/cfdi_paid_view.xml',
        'views/tools/tax_regime_view.xml',

        # Data
        'data/tax_regime_data.xml',
    ],

    'qweb': [
        
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
    'maintainer': 'Nelson René Gordillo González',
    'license': 'LGPL-3',
}