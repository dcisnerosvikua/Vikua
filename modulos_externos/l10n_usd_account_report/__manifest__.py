# -*- coding: utf-8 -*-
{
    'name': "Report Fact",
    'description': """Account reports for Venezuela""",
    'version': '1.1',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'website': 'http://soluciones-tecno.com/',
    'category': 'Tools',
    'version': '0.1',
    'depends': ['account'],
    'data': [
        'report/paperformat.xml',
        'report/ir_action_report.xml',
        'views/report_invoice_fact.xml',
    ],
    'application': False,
    'auto_install': False,
}
