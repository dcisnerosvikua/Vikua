{
    'name': "Venezuela - Accounting Reports ",
    'description': """Accounting reports for Venezuela""",
    'version': '1.1',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A',
    'contribuitors': "Bryan Gómez <bryan.gomez1311@gmail.com>",
    'category': 'Accounting/Localizations/Reporting',
    'website': 'http://soluciones-tecno.com/',
    'depends': ['account', 'purchase'],
    'data': [
        'data/account_delivery_note_sequence.xml',
        'report/paperformat.xml',
        'report/ir_action_report.xml',
        'views/account_move_views.xml',
        'views/res_currency_views.xml',
        'views/report_account_invoice.xml',
        'views/report_purchase_order.xml',
    ],
    'application': False,
    'auto_install': False,
}
# -*- coding: utf-8 -*-
