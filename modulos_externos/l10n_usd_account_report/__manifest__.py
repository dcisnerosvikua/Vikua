# -*- coding: utf-8 -*-
{
    'name': "Report Fact",
    'description': """Account reports for Venezuela""",
    'version': '1.1',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'website': 'http://soluciones-tecno.com/',
    #'category': 'Accounting/Localizations/Reporting',
    'category': 'Tools',
    'version': '0.1',
    'depends': ['account'],
    'data': [
        'report/paperformat.xml',
        'report/ir_action_report.xml',
        #'views/account_move_views.xml',
        'views/report_invoice_fact.xml',
        #'views/report_account_invoice_delivery_note.xml',
    ],
    'application': True,
    'auto_install': False,
}
