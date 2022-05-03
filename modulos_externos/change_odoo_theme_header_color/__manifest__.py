# -*- coding: utf-8 -*-

{
    'name': 'Change Odoo Theme Navigationbar Color',
    'summary': 'Change Odoo Theme Navigationbar Color',
    'description': "Change Odoo Theme Navigationbar Color",
    'sequence': 1,
    'depends': ['base_setup'],
    'data': [
        'data/data.xml',
        'views/assets.xml',
        'views/res_config_settings_view.xml',
    ],
    'application': True,
    'author': 'Bryan Gomez',
    'maintainer': 'Bryan Gomez',
    'support': 'bryan.gomez1311@gmail.com',
}
