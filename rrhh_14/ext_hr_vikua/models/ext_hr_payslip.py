# coding: utf-8
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
from odoo.exceptions import UserError, ValidationError


class hr_special_days(models.Model):
    _inherit = 'hr.payslip'

    ############################# ASIGNACIONES #######################################

    ########################33 CAMPO PARA ASIGNACIONES DE COMISIONES ###############################
    comision_check = fields.Boolean(default=False, string="Monto Comisiones adicionales")
    comision_value = fields.Float(default=0)
    ########################33 CAMPO PARA ASIGNACIONES DE COMISIONES ###############################
    bono_uni_check = fields.Boolean(default=False, string="Bono Unico")
    bono_uni_value = fields.Float(default=0)
    ########################33 ASIGNACIONES ESPECIALES ###############################
    asig_espe_check = fields.Boolean(default=False, string="Asig. Especiales")
    asig_espe_value = fields.Float(default=0)
    ########################33 ASIGNACIONES pendientes quincena anterior ###############################
    asig_ante_check = fields.Boolean(default=False, string="Asig. Quincena anterior")
    asig_ante_value = fields.Float(default=0)

    ############################# DEDUCCIONES #######################################

    ########################33 CAMPO PARA ANTICIPO SALARIOS ###############################
    anticipo_salario_check = fields.Boolean(default=False, string="Anticipo Salario")
    anticipo_salario_value = fields.Float(default=0)
    ########################33 CAMPO PARA ADELANTO DE COMISIONES ###############################
    adelanto_comisions_check = fields.Boolean(default=False, string="Adelanto de Comisiones")
    adelanto_comisions_value = fields.Float(default=0)
    ########################33 DESCUENTOS ESPECIALES ###############################
    descuento_esp_check = fields.Boolean(default=False, string="Descuentos Especiales")
    descuento_esp_value = fields.Float(default=0)
    


    def calculo_prestaciones(self):
        if not self.company_id.tipo_metodo:
            raise UserError(_('Configure un tipo de metodo para el cálculo de prestaciones sociales de empleados para esta compañia'))
        if self.company_id.tipo_metodo=='tri':
            if self.struct_id.activo_prestaciones==True:
                for selff in self:
                    sueldo_base_mensual=0.0001
                    nro_ano=dias_disfrutes=alicuota=acumulado=tasa_int=acumulado_int=0
                    mes=0
                    acumulado_add_gps=dias_add_gps=0
                    mes_nomina=selff.mes(selff.date_to)
                    ano_actual=selff.ano(selff.date_to)
                    valida=selff.env['hr.payroll.prestaciones'].search([('employee_id','=',selff.employee_id.id),('ano','=',ano_actual),('nro_mes','=',mes_nomina)])
                    if not valida:
                        if selff.contract_id.wage>0:
                            if selff.struct_id.campo_sueldo=='sc':
                                sueldo_base_mensual=selff.contract_id.sueldo_div
                            if selff.struct_id.campo_sueldo=='sf':
                                sueldo_base_mensual=selff.contract_id.monto_porcentage_sueldo
                            if selff.struct_id.campo_sueldo=='sb':
                                sueldo_base_mensual=selff.contract_id.monto_porcentage_bono
                            if selff.contract_id.sueldo_currency.id!=3:
                                sueldo_base_mensual=sueldo_base_mensual*selff.os_currecy_rate_gene
                            selff.ultimo_suldo_base_mensual=sueldo_base_mensual
                        if selff.tiempo_antiguedad>0:
                            nro_ano=selff.tiempo_antiguedad
                        indicadores=selff.env['hr.payroll.indicadores.economicos'].search([('code','=','DUT')])
                        if indicadores:
                            for det_indi in indicadores:
                                nro_dias_utilidades=det_indi.valor
                        indicadores2=selff.env['hr.payroll.indicadores.economicos'].search([('code','=','TP')])
                        if indicadores2:
                            for det_indi2 in indicadores2:
                                tasa_int=det_indi2.valor
                        verifica=selff.env['hr.payroll.prestaciones'].search([('employee_id','=',selff.employee_id.id),('id','!=',selff.id)],order="id ASC") #('ano','=',ano_actual)
                        if verifica:
                            #raise UserError(_('Ya hay una nomina procesada/pagada en el mes seleccionado para %s')%self.employee_id.name)
                            for det_v in verifica:
                                #acumulado=det_v.alicuota
                                if det_v.mes==11:
                                    mes=0
                                else:
                                    mes=det_v.mes+1
                        if mes==3 or mes==6 or mes==9:
                            dias_disfrutes=15
                        if mes==0:
                            busca_mes=selff.env['hr.payroll.prestaciones'].search([('employee_id','=',selff.employee_id.id),('mes','=','0'),('id','!=',selff.id)],order="mes ASC")
                            if busca_mes:
                                dias_disfrutes=15
                                dias_add_gps=selff.dias_por_antiguedad
                            if not busca_mes:
                                dias_disfrutes=0
                        if mes>0:
                            dias_add_gps=0
                        #if self.tiempo_antiguedad==0:
                            #dias_disfrutes=15
                        #if self.tiempo_antiguedad>0:
                            #dias_disfrutes=self.dias_vacaciones+1
                        sueldo_base_diario=sueldo_base_mensual/30
                        fraccion_diaria_vaca=sueldo_base_diario*selff.dias_vacaciones/360
                        fraccion_diaria_utilidades=sueldo_base_diario*nro_dias_utilidades/360
                        sueldo_integral_mensual=(sueldo_base_diario+fraccion_diaria_vaca+fraccion_diaria_utilidades)*30 # AQUI COLOCAR INASISTENCIA
                        
                        alicuota_add_gps=(sueldo_base_diario+fraccion_diaria_vaca+fraccion_diaria_utilidades)*dias_add_gps
                        acumulado_add_gps=selff.compute_acumulado_add_gps()+alicuota_add_gps

                        alicuota=(sueldo_integral_mensual/30)*dias_disfrutes
                        acumulado=selff.compute_acumulado()+alicuota

                        monto_int=(acumulado*tasa_int)/1200
                        acumulado_int=selff.compute_acumulado_int()+monto_int

                        ret = selff.env['hr.payroll.prestaciones']
                        values = {
                        'employee_id': selff.employee_id.id,
                        'sueldo_int_mensual':sueldo_integral_mensual,
                        'sueldo_base_mensual':sueldo_base_mensual,
                        'nro_ano':nro_ano,
                        'mes':mes,
                        'nro_mes':mes_nomina,
                        'ano':selff.ano(selff.date_to),
                        'dias_disfrutes':dias_disfrutes,
                        'alicuota':alicuota,
                        'acumulado':acumulado,
                        'tasa_int':tasa_int,
                        'monto_int':monto_int,
                        'acumulado_int':acumulado_int,
                        'dias_add_gps':dias_add_gps,
                        'alicuota_add_gps':alicuota_add_gps,
                        'acumulado_add_gps':acumulado_add_gps,
                        }
                        rets=ret.create(values)