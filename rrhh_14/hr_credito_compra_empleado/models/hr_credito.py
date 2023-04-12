# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models,api,_
import datetime
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import datetime

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    credito_id=fields.Many2one('hr.credito', string='Lineas de creditos')
    status_credito=fields.Selection(selection=[('hold','En Espera'),('granted','Otorgado'),('solvent','Solvente')],default='hold')
    credito_activo = fields.Boolean(default=False)
    descuento_credito_activo = fields.Boolean(default=False)

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    def action_payslip_done(self):
        #raise UserError(_('Prueba BEBE'))
        res = super(HrPayslip, self).action_payslip_done()

        for det in self:
            empleado = self.env['hr.employee'].search([('id','=',det.employee_id.id)])
            for det_empl in empleado:
                if det_empl.descuento_credito_activo==True:
                    self.actualiza_descuento()
                if det_empl.status_credito=="hold" and det_empl.credito_activo==True:
                    vals={
                    'status_credito':"granted",
                    'credito_activo':False,
                    'descuento_credito_activo':True,
                    }
                    self.env['hr.employee'].browse(det_empl.id).write(vals)
        return res

    def actualiza_descuento(self):
        for selff in self:
            data_credito = self.env['hr.credito'].search([('empleado_id', '=', selff.employee_id.id),('status_credito','=','pending')])
            if data_credito:
                for det in data_credito:
                    monto_cuotas=det.monto_cuotas
                    cuotas=det.cuotas
                    #raise UserError(_('cuotas %s')%cuotas)
                    i=1
                    cont_solvete=0
                    for i in range(cuotas):
                        num=i+1
                        line_credito = self.env['hr.credito.line'].search([('credito_id','=',det.id)],order ="num_cuota asc")
                        if line_credito:
                            booleano=0
                            #cont_solvete=0
                            for det in line_credito:
                                if det.status_pago=="solvent":
                                    cont_solvete=cont_solvete+1
                                if det.status_pago=="pending" and booleano==0:
                                    vals={
                                    'monto_pagado':monto_cuotas,
                                    'status_pago':"solvent",
                                    'fecha_pago':datetime.now(),
                                    'payslip_id':selff.id,
                                    'payslip_run_id':selff.payslip_run_id,
                                    }
                                    self.env['hr.credito.line'].browse(det.id).write(vals)
                                    booleano=1
                                    cont_solvete=cont_solvete+1
                            #raise UserError(_('cont_solvete %s')%cont_solvete)
                            if cont_solvete==cuotas:
                                #raise UserError(_('listo'))
                                data_credito.write({'status_credito':"solvent",})
                                empleado2 = self.env['hr.employee'].search([('id','=',selff.employee_id.id)])
                                #raise UserError(_('empleado2 = %s')%empleado2)
                                for det_empl2 in empleado2:
                                    valss={
                                    'credito_activo':False,
                                    'descuento_credito_activo':False,
                                    'status_credito':"solvent",
                                    }
                                    empleado2.write(valss)



class SaleOrder(models.Model):
    _name = 'hr.credito'

    empleado_id=fields.Many2one("hr.employee",string="Empleado")
    cedula=fields.Char(string="Cedula")
    credito_fecha = fields.Date(string='Fecha del credito')
    monto_credito = fields.Float(string='Monto del credito', help='Monto del credito')
    porcentaje= fields.Float(string='Porcentaje de Interes')
    status_credito=fields.Selection(selection=[('hold','En Espera'),('pending','Pendiente'),('solvent','Solvente')],default='hold',index=True, track_visibility='onchange',readonly=True, copy=False, tracking=True)
    adeudado=fields.Float(string='Monto Adeudado', help='Monto Adeudado')
    cuotas=fields.Integer(string="Nro de Cuotas", default='1')
    monto_cuotas= fields.Float(string="Monto Cuotas")
    credito_line_ids = fields.One2many('hr.credito.line', 'credito_id', string='creditos')
    company_id = fields.Many2one("res.company", string="Compañia", default=lambda self: self.env.company)
    forma_pago=fields.Selection(selection=[
        ('biweekly','Quincenal'),
        ('weekly','Semanal'),
        ('monthly','Mensual'),
        ('quarterly','Trimestral'),
        ('semi-annually','Semestral')
        ])

    @api.onchange('porcentaje','monto_credito')
    def monto_adeudado(self):
        if (self.porcentaje or self.porcentaje>0) and self.porcentaje<=100:
            self.adeudado=(self.monto_credito*self.porcentaje/100)+self.monto_credito
        if self.porcentaje==0 or self.porcentaje==0.00:
            self.adeudado=self.monto_credito
        if self.porcentaje<0:
            raise UserError(_(' El Porcentaje no puede ser Negativo'))
        if self.porcentaje>100:
            raise UserError(_(' El Porcentaje no puede ser ser mayor a 100%'))

    @api.onchange('cuotas','adeudado')
    def valor_cuotas(self):
        if self.cuotas>0 or self.cuotas:
            self.monto_cuotas=self.adeudado/self.cuotas
        if self.cuotas==0:
            raise UserError(_('El Número de cuotas no puede ser Nulo'))
        if self.cuotas<0:
            raise UserError(_('El Número de cuotas no puede ser Negativo'))

    @api.onchange('empleado_id')
    def compute_cedula(self):
        lista_empleado = self.env['hr.employee'].search([('id', '=', self.empleado_id.id)])
        if lista_empleado:
            for det in lista_empleado:
                if det.identification_id:
                    self.cedula=det.identification_id
                else:
                    self.cedula='00000000'
        if not lista_empleado:
            self.cedula='00000000'

    def aprobar(self):
        verifica_credito = self.env['hr.credito'].search([('empleado_id','=',self.empleado_id.id),('status_credito','=','pending')])
        if verifica_credito:
            raise ValidationError(_("Este empleado tiene un credito aun pendiente por pagar."))
        else:
            i=0
            pagos = self.env['hr.credito.line']
            for i in range(self.cuotas):
                num=i+1
                vals={
                'credito_id':self.id,
                'monto_pagado':0.00,
                'status_pago':"pending",
                'num_cuota':num,
                }
                pag = pagos.create(vals)
            self.status_credito='pending'

            empleado = self.env['hr.employee'].search([('id','=',self.empleado_id.id)])
            for det_empl in empleado:
                vals={
                'credito_id':self.id,
                'status_credito':"granted",
                'credito_activo':True,
                'descuento_credito_activo':True,
                #'status_credito':self.status_credito,
                }
                self.env['hr.employee'].browse(det_empl.id).write(vals)


    def cancel(self):
        #verifica=self.env['hr.employee'].search([('id','=',self.empleado_id.id),('status_credito','in',('granted','solvent'))])
        verifica=self.env['hr.employee'].search([('id','=',self.empleado_id.id)])
        #if verifica:
            #raise ValidationError(_("Este empleado tiene un credito ya en ejecucion por nomina. No se puede realizar la accion solicitada"))
        pagos = self.env['hr.credito.line'].search([('credito_id','=',self.id)])
        pagos.unlink()
        self.status_credito='hold'

        empleado = self.env['hr.employee'].search([('id','=',self.empleado_id.id)])
        for det_empl in empleado:
            vals={
            'credito_id':self.id,
            'credito_activo':False,
            'descuento_credito_activo':False,
            #'status_credito':self.status_credito,
            }
            self.env['hr.employee'].browse(det_empl.id).write(vals)


class SaleOrder(models.Model):
    _name = 'hr.credito.line'

    credito_id = fields.Many2one('hr.credito', string='Lineas de creditos')
    fecha_pago = fields.Date(string='Fecha del Pago')
    status_pago = fields.Selection(selection=[('pending','Pendiente'),('solvent','Solvente')],default='pending')
    monto_pagado = fields.Float(string='Monto Pagado')
    num_cuota = fields.Integer(string="#")
    payslip_id = fields.Integer(string="Id pago Individual")
    payslip_run_id = fields.Integer(string="Id pago por lote")


    #one_approve_by = fields.Many2one("res.users",string="Primer Aprobador")
    #statu_one=fields.Selection(selection=[('approve','Aprobado'),('refuse','Rechazado'),('hold','En Espera')],default='hold')
    #one_approve_time = fields.Datetime(string="Fecha de decisión", copy=False, index=True, track_visibility='onchange')
    #two_approve_by = fields.Many2one("res.users",string="Segundo Aprobador")
    #statu_two=fields.Selection(selection=[('approve','Aprobado'),('refuse','Rechazado'),('hold','En Espera')],default='hold')
    #two_approve_time = fields.Datetime(string="Fecha de decisón", copy=False, index=True, track_visibility='onchange')
    #state = fields.Selection(selection_add=[('draft','Quotation'),('sent','Quotation Sent'),('approve','Por Aprobar'),('approve2','Por Segunda Aprobación'),('approves','Aprobado'),('refuse','Rechazado'),('sale','Sales Order'),('done','Locked'),('cancel','Cancelled'),],
                               #string='Status', readonly=False, copy=False, index=True, track_visibility='onchange', default='draft')
