#-*- coding: utf-8 -*-
from odoo import models, fields, api, _

class OdooTaxReceiptType(models.Model):
    _name = 'odoo.tax.receipt.type'
    _description = 'SAT Tax Receipt Type'
    _rec_name = 'code'
    _order = 'code'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string="Code", required=True, tracking=True)
    name = fields.Char(string="Name", required=True, tracking=True)

    _sql_constraints = [
        ('odoo_tax_receipt_type_code_unique', 'unique(code)', 'The SAT tax receipt type code must be unique.')
    ]