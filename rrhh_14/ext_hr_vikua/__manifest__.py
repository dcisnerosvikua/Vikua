# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Funcionalidades personalizadas vikua RRHH',
    'version': 'odoo 14',
    'author': 'INM&RDL - Ing Darrell Sojo',
    'category': 'Human Resources',
    'sequence': 104,
    'summary': 'Funcionalidades personalizadas vikua RRHH',
    'description': '''
        Agrega  campos y fuancionalidades adicionales partivulares al modulo rrhh:\n
            
    ''',
    'depends': [
        'base_setup',
        'base',
        'hr',
        'hr_contract',
        'hr_payroll',
        'hr_attendance',
        'hr_holidays',
        'hr_holidays',
        'hr_campos_parametrizacion',  ## este es un modulo de odoo nativo para que haga el asiento de la nomina
    ],
    'data': [
    'views/hr_inherit_payslip_view.xml',
    'views/hr_contract_add_fields_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}