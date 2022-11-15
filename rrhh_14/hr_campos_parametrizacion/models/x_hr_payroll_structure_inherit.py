# coding: utf-8
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
from odoo.exceptions import UserError, ValidationError

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    activo_prestaciones = fields.Boolean(string='Calcular Prsetaciones Sociales', default=True)
    shedule_pay_value = fields.Integer(string='Valor Pago Planificado', compute='_compute_dias_pago')
    employee_ids = fields.One2many('hr.payroll.employeed','structure_id')
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company.id)

    @api.onchange('schedule_pay')
    def _compute_dias_pago(self):
        value=15
        if self.schedule_pay=="monthly":
            value=30
        if self.schedule_pay=="quarterly":
            value=90
        if self.schedule_pay=="semi-annually":
            value=180
        if self.schedule_pay=="annually":
            value=360
        if self.schedule_pay=="weekly":
            value=7
        if self.schedule_pay=="bi-weekly":
            value=15
        if self.schedule_pay=="bi-monthly":
            value=60
        self.shedule_pay_value=value

class HrPayrollEmployeed(models.Model):
    _name = 'hr.payroll.employeed'

    structure_id = fields.Many2one('hr.payroll.structure', string='Nómina')
    name=fields.Char()
    empleado_id = fields.Many2one('hr.employee')
    company_id = fields.Many2one('res.company','Company')
    company_aux_id = fields.Many2one('res.company',compute='_compute_company_employee')

    @api.onchange('empleado_id')
    def _compute_company_employe(self):
        valor=self.empleado_id.company_id.id
        self.company_aux_id=valor
        self.company_id=valor