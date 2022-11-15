# coding: utf-8
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
from odoo.exceptions import UserError, ValidationError

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    desc_ley = fields.Char()
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company.id)