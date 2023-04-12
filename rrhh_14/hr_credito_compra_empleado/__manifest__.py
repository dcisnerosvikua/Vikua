# -*- coding: utf-8 -*-
{
    'name': "Deducccion de creditos de compras empleados por nomina",

    'summary': """Deducccion de creditos de compras empleados por nomina""",

    'description': """
       Deducccion de creditos de compras empleados por nomina.
    """,
    'version': '13.0',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'category': 'Tools',
    'website': 'http://soluciones-tecno.com/',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_payroll'],

    # always loaded
    'data': [
    'views/credito_view.xml',
    #'views/hr_payslip_view.xml',
    'security/ir.model.access.csv',
    ],
    'application': True,
    'active':False,
    'auto_install': False,
}
