#-*- coding: utf-8 -*-
from odoo import models, fields, api, _

class OdooTaxRegime(models.Model):
    _name = 'odoo.tax.regime'
    _description = 'SAT Regimen Fiscal'
    _rec_name = 'code'
    _order = 'code'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string="Code", required=True, tracking=True)
    name = fields.Char(string="Name", required=True, tracking=True)

    _sql_constraints = [
        ('odoo_tax_regime_code_unique', 'unique(code)', 'The SAT tax regime code must be unique.')
    ]
    