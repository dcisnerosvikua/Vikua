# coding: utf-8
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
import time
from odoo.exceptions import UserError, ValidationError

class hr_tiempo_servicio(models.Model):
    _name = 'hr.payroll.dias.vacaciones'
    _description = 'Tiempo Servicio'

    service_years= fields.Integer()
    pay_day = fields.Integer()
    pay_day_garantia = fields.Integer()

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    dias_vacaciones = fields.Integer(string="Dias de disfrutes por tiempo de servicios", compute='_compute_dias_vacaciones')
    tiempo_antiguedad = fields.Integer(string="Tiempo de Antiguedad (años)", compute='_compute_tiempo_antiguedad')
    tiempo_antiguedad_dias = fields.Integer()
    tiempo_fraccion_dias = fields.Integer()
    tiempo_fraccion_meses =fields.Integer()
    dias_totales_disfrutados = fields.Integer(compute='_compute_dias_disfrutar')
    dias_restantes_disfrutar = fields.Integer(compute='_compute_dias_restantes')
    date_actual = fields.Date(string='Date From', compute='_compute_fecha_hoy')
    salario_integral_diario = fields.Float(compute='_compute_salario_integral_diario')
    #date_actual = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))

    def _compute_fecha_hoy(self):
        hoy=datetime.now().strftime('%Y-%m-%d')
        self.date_actual=hoy

    def _compute_salario_integral_diario(self):
        wage_basi_diario=(self.contract_id.wage)/30
        fraccion_diaria_vaca=(wage_basi_diario*(self.dias_vacaciones-self.tiempo_antiguedad+1))/360
        indicadores=self.env['hr.payroll.indicadores.economicos'].search([('code','=','DUT')])
        if indicadores:
            for det_indi in indicadores:
                nro_dias_utilidades=det_indi.valor
        fraccion_diaria_utilidades=wage_basi_diario*nro_dias_utilidades/360
        self.salario_integral_diario=wage_basi_diario+fraccion_diaria_vaca+fraccion_diaria_utilidades



    def _compute_dias_disfrutar(self):
        dias_disfrutar=0
        verifica=self.env['hr.leave'].search([('employee_id','=',self.id),('state','=','validate'),('nro_ano_periodo','=',self.tiempo_antiguedad)])
        if verifica:
            for det in verifica:
                dias_disfrutar=dias_disfrutar+det.number_of_days
        self.dias_totales_disfrutados=dias_disfrutar

    def _compute_dias_restantes(self):
        self.dias_restantes_disfrutar=self.dias_vacaciones-self.dias_totales_disfrutados


    #@api.depends('id')
    def _compute_tiempo_antiguedad(self):
        tiempo=0
        if self.contract_id.date_start:
            fecha_ing=self.contract_id.date_start
        if not self.contract_id.date_start:
            fecha_ing=self.date_actual
        fecha_actual=self.date_actual#time.strftime("%x")#self.date_to
        dias=self.days_dife(fecha_actual,fecha_ing)
        tiempo=dias/360
        fraccion_dias=(dias-int(tiempo)*360)
        self.tiempo_antiguedad=tiempo
        self.tiempo_antiguedad_dias=dias
        self.tiempo_fraccion_dias=fraccion_dias
        self.tiempo_fraccion_meses=fraccion_dias/30

    def _compute_dias_vacaciones(self):
        dias_difrute=0
        for selff in self:
            verifica=selff.env['hr.payroll.dias.vacaciones'].search([('service_years','=',selff.tiempo_antiguedad)])
            if verifica:
                for det in verifica:
                    dias_difrute=det.pay_day
            selff.dias_vacaciones=dias_difrute
            valida=selff.env['hr.leave.type'].search([('code','in',('VAC','vac','Vac'))])
            if valida:
                for det in valida:
                    leave_type_id=det.id
                verifica2=selff.env['hr.leave.allocation'].search([('employee_id','=',selff.id),('holiday_status_id','=',leave_type_id)])
                if verifica2:
                    for det2 in verifica2:
                        self.env['hr.leave.allocation'].browse(det2.id).write({
                            'number_of_days':selff.dias_vacaciones
                            })

    def days_dife(self,d1, d2):
       return abs((d2 - d1).days)

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    nro_ano_periodo=fields.Integer(string="periodo de año a la cual pertenece esta solicitud")

    def action_approve(self):
        res = super(HrLeave, self).action_approve()
        ano=0
        empleado=self.env['hr.employee'].search([('id','=',self.employee_id.id)])
        if empleado:
            for det in empleado:
                ano=det.tiempo_antiguedad
        self.nro_ano_periodo=ano


class ControlVacaciones(models.Model):
    _name = 'hr.control.vacaciones'

    employee_id = fields.Many2one('hr.employee')
    fecha_ingreso = fields.Date(compute='_compute_ingreso')
    date_actual = fields.Date(string='Date From', compute='_compute_fecha_hoy')
    tiempo_antiguedad = fields.Integer(compute='_compute_tiempo_antiguedad')
    periodos_ids = fields.One2many('hr.periodo','control_id', string='Periodos')

    def _compute_fecha_hoy(self):
        hoy=datetime.now().strftime('%Y-%m-%d')
        self.date_actual=hoy

    def _compute_tiempo_antiguedad(self):
        tiempo=0
        for selff in self:
            if selff.employee_id.id:
                fecha_ing=selff.fecha_ingreso
                fecha_actual=selff.date_actual
                if selff.employee_id.contract_id:
                    dias=selff.days_dife(fecha_actual,fecha_ing)
                    tiempo=dias/360
            selff.tiempo_antiguedad=tiempo

    def days_dife(self,d1, d2):
       return abs((d2 - d1).days)

    @api.depends('employee_id')
    def _compute_ingreso(self):
        for rec in self:
            if rec.employee_id.contract_id.date_start:
                rec.fecha_ingreso=rec.employee_id.contract_id.date_start
            else:
                rec.fecha_ingreso="1999-01-01"


    def calcular(self):
        lista=self.env['hr.control.vacaciones'].search([])
        #periodos=self.env['hr.periodo'].search([]).unlink()
        #raise UserError(_('lista= %s')%lista)
        for rec in lista:
            tiempo=rec.tiempo_antiguedad
            dias=60
            inicio=rec.employee_id.contract_id.date_start
            valida_fec_inicio=rec.env['hr.periodo'].search([('control_id','=',rec.id)],order='periodo ASC')
            if valida_fec_inicio:
                for det in valida_fec_inicio:
                    valor=det.hasta
                if valor:
                    inicio=valor
            for seq in range(1,tiempo+1,1):
                valida=rec.env['hr.periodo'].search([('periodo','=',seq),('control_id','=',rec.id)],order='periodo ASC')
                if not valida:
                    hasta=rec.hastadelta(inicio)
                    #raise UserError(_('verifica= %s')%hasta)
                    periodo=self.env['hr.periodo']
                    values={
                    'periodo':seq,
                    'control_id':rec.id,
                    'desde':inicio,
                    'hasta':hasta,
                    }
                    periodo_ids = periodo.create(values)
                    inicio=rec.new_inicio(hasta)


    def hastadelta(self,inicio):
        fecha=str(inicio)
        days = int(fecha[8:10])
        mes = int(fecha[5:7])
        year = int(fecha[0:4])
        if days==1:
            days=30
            if mes>1:
                mes=mes-1
            else:
                mes=12
        else:
            days=days-1
        year=year+1
        if mes<10:
            mess="0"+str(mes)
        else:
            mess=mes
        if days<10:
            dayss="0"+str(days)
        else:
            dayss=str(days)
        resultado=str(year)+"-"+mess+"-"+dayss
        #raise UserError(_('verifica= %s')%resultado)
        return resultado

    def new_inicio(self,hasta):
        fecha=str(hasta)
        days = int(fecha[8:10])
        mes = int(fecha[5:7])
        year = int(fecha[0:4])
        #raise UserError(_('verifica= %s')%year)
        if days>31:
            days=1
            if mes<12:
                mes=mes+1
            else:
                mes=1
        else:
            days=days+1
        if mes<10:
            mess="0"+str(mes)
        else:
            mess=mes
        if days<10:
            dayss="0"+str(days)
        else:
            dayss=str(days)
        resultado=str(year)+"-"+str(mess)+"-"+str(dayss)
        return resultado


class ListaPeriodos(models.Model):
    _name = 'hr.periodo'

    control_id = fields.Many2one('hr.control.vacaciones')
    periodo = fields.Char()
    desde = fields.Date()
    hasta = fields.Date()
    ano_antiguedad = fields.Integer(compute='_compute_ano_antiguedad')
    dias_disfrute = fields.Float(compute='_compute_dias_vacaciones')
    dias_adicionales = fields.Float(compute='_compute_dias_vacaciones')
    dias_disfrute_ley = fields.Float(compute='_compute_dias_vacaciones')
    dias_disfrutados = fields.Float()
    dias_pendientes = fields.Float()

    @api.depends('desde','hasta')
    def _compute_ano_antiguedad(self):
        tiempo=0
        for selff in self:
            dias=selff.days_dife(selff.control_id.employee_id.contract_id.date_start,selff.hasta)
            tiempo=dias/360
            selff.ano_antiguedad=tiempo

    def days_dife(self,d1, d2):
       return abs((d2 - d1).days)

    def _compute_dias_vacaciones(self):
        dias_difrute=0
        for selff in self:
            verifica=selff.env['hr.payroll.dias.vacaciones'].search([('service_years','=',selff.ano_antiguedad)])
            if verifica:
                for det in verifica:
                    dias_difrute=det.pay_day
            selff.dias_disfrute=dias_difrute
            selff.dias_adicionales=dias_difrute-15
            selff.dias_disfrute_ley=15

    def unlink(self):
        for rec in self:
            raise UserError(_("No se pueden eliminar estos registros"))
        super().unlink()



