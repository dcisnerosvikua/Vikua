# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.bank.statement'

    balance_start = fields.Monetary(string='Starting Balance', states={'confirm': [('readonly', False)]}, default=_default_opening_balance)
    balance_end_real = fields.Monetary('Ending Balance', states={'confirm': [('readonly', False)]})