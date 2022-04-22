# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re
from odoo import api, fields, models, _ , exceptions
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = 'hr.contract'

    sueldo_div = fields.Float()
    sueldo_currency = fields.Many2one('res.currency','Moneda',default=2)
    wage_aux = fields.Float(compute='_compute_tasa')
    porcentage_sueldo=fields.Float()
    porcentage_sueldo_aux=fields.Float(compute='_compute_valor')
    monto_porcentage_sueldo=fields.Float(compute='_compute_monto_sueldo')
    porcentage_bono=fields.Float(compute='_compute_diferencia')
    monto_porcentage_bono=fields.Float(compute='_compute_monto_bono')

    @api.depends('sueldo_currency','sueldo_div')
    def _compute_tasa(self):
        for selff in self:
            id_moneda_divisa=selff.sueldo_currency.id
            id_moneda_compa=selff.env.company.currency_id.id
            valor_aux=0.000000000000000000000000000001
            if id_moneda_compa!=id_moneda_divisa:
                tasa= selff.env['res.currency.rate'].search([('currency_id','=',id_moneda_divisa)],order="hora asc") #('hora','>=',selff.date_from)
                for det_tasa in tasa:
                    valor_aux=det_tasa.rate_real
                rate=round(1*valor_aux,2)
                resultado=selff.sueldo_div*rate
            else:
                resultado=selff.sueldo_div
            selff.wage_aux=resultado
            selff.wage=resultado

    @api.depends('porcentage_sueldo')
    def _compute_diferencia(self):
        for rec in self:
            rec.porcentage_bono=100-rec.porcentage_sueldo

    @api.depends('porcentage_sueldo')
    def _compute_monto_sueldo(self):
        for rec in self:
            rec.monto_porcentage_sueldo=rec.sueldo_div*rec.porcentage_sueldo/100

    @api.depends('porcentage_sueldo','monto_porcentage_sueldo')
    def _compute_monto_bono(self):
        for rec in self:
            rec.monto_porcentage_bono=rec.sueldo_div-rec.monto_porcentage_sueldo

    @api.depends('porcentage_sueldo')
    def _compute_valor(self):
        for rec in self:
            if rec.porcentage_sueldo>100:
                raise UserError(_('Este valor no puede ser mayor al 100%'))
            if rec.porcentage_sueldo<0:
                raise UserError(_('Este valor no puede ser negativo'))
            rec.porcentage_sueldo_aux=rec.porcentage_sueldo
