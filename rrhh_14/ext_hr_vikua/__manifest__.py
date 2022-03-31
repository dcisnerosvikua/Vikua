# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Contract Aditional Data',
    'version': 'odoo 14',
    'author': 'INM&RDL - Ing Darrell Sojo',
    'category': 'Human Resources',
    'sequence': 104,
    'summary': 'Adds aditional fields to hr_contract module',
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
    'hr_inherit_payslip_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}