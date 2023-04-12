# -*- coding: utf-8 -*-
{
    'name': "Recibo de pagos diversos",

    'summary': """Recibo de pagos diversos.""",

    'description': """
      Recibo de pagos diversos.
    """,
    'version': '15.0',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A - Ing. Darrell Sojo',
    'category': 'Tools',
    'website': 'http://soluciones-tecno.com',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr_campos_parametrizacion'],

    # always loaded
    'data': [
        'report/recibo_pago_bono_utiles.xml',
        'report/recibo_pago_bono_juguetes.xml',
        'report/recibo_pago_bono_transporte.xml',
        'report/recibo_pago_bono_inicio_escolar.xml',
        'report/recibo_prestamo.xml',
        #'wizard/wizard.xml',
        #'security/ir.model.access.csv',
    ],
    'application': True,
    'active':False,
    'auto_install': False,
}
