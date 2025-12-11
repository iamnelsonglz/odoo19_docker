#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import datetime

import base64
import xml.etree.ElementTree as ET

REGIME_SELECTION_LIST = [
    ('601', '601 - RÉGIMEN GENERAL DE LEY PERSONAS MORALES'),
    ('602', '602 - RÉGIMEN SIMPLIFICADO DE LEY PERSONAS MORALES'),
    ('603', '603 - PERSONAS MORALES CON FINES NO LUCRATIVOS'),
    ('604', '604 - RÉGIMEN DE PEQUEÑOS CONTRIBUYENTES'),
    ('605', '605 - RÉGIMEN DE SUELDOS Y SALARIOS E INGRESOS ASIMILADOS A SALARIOS'),
    ('606', '606 - RÉGIMEN DE ARRENDAMIENTO'),
    ('607', '607 - RÉGIMEN DE ENAJENACIÓN O ADQUISICIÓN DE BIENES'),
    ('608', '608 - RÉGIMEN DE LOS DEMÁS INGRESOS'),
    ('609', '609 - RÉGIMEN DE CONSOLIDACIÓN'),
    ('610', '610 - RÉGIMEN RESIDENTES EN EL EXTRANJERO SIN ESTABLECIMIENTO PERMANENTE EN MÉXICO'),
    ('611', '611 - RÉGIMEN DE INGRESOS POR DIVIDENDOS (SOCIOS Y ACCIONISTAS)'),
    ('612', '612 - RÉGIMEN DE LAS PERSONAS FÍSICAS CON ACTIVIDADES EMPRESARIALES Y PROFESIONALES'),
    ('613', '613 - RÉGIMEN INTERMEDIO DE LAS PERSONAS FÍSICAS CON ACTIVIDADES EMPRESARIALES'),
    ('614', '614 - RÉGIMEN DE LOS INGRESOS POR INTERESES'),
    ('615', '615 - RÉGIMEN DE LOS INGRESOS POR OBTENCIÓN DE PREMIOS'),
    ('616', '616 - SIN OBLIGACIONES FISCALES'),
    ('617', '617 - PEMEX'),
    ('618', '618 - RÉGIMEN SIMPLIFICADO DE LEY PERSONAS FÍSICAS'),
    ('619', '619 - INGRESOS POR LA OBTENCIÓN DE PRÉSTAMOS'),
    ('620', '620 - SOCIEDADES COOPERATIVAS DE PRODUCCIÓN QUE OPTAN POR DIFERIR SUS INGRESOS'),
    ('621', '621 - RÉGIMEN INCORPORACIÓN FISCAL'),
    ('622', '622 - RÉGIMEN DE ACTIVIDADES AGRÍCOLAS, GANADERAS, SILVÍCOLAS Y PESQUERAS PERSONAS MORALES'),
    ('623', '623 - RÉGIMEN DE OPCIONAL PARA GRUPOS DE SOCIEDADES'),
    ('624', '624 - RÉGIMEN DE COORDINADOS'),
    ('625', '625 - RÉGIMEN DE ACTIVIDADES EMPRESARIALES CON INGRESOS A TRAVÉS DE PLATAFORMAS TECNOLÓGICAS'),
    ('626', '626 - RÉGIMEN SIMPLIFICADO DE CONFIANZA'),
]

USE_CFDI_SELECTION_LIST = [
    ('G01',  'G01 - Adquisición de mercancías'),
    ('G02',  'G02 - Devoluciones, descuentos o bonificaciones'),
    ('G03',  'G03 - Gastos en general'),
    ('I01',  'I01 - Construcciones'),
    ('I02',  'I02 - Mobiliario y equipo de oficina por inversiones'),
    ('I03',  'I03 - Equipo de transporte'),
    ('I04',  'I04 - Equipo de cómputo y accesorios'),
    ('I05',  'I05 - Dados, troqueles, moldes, matrices y herramental'),
    ('I06',  'I06 - Comunicaciones telefónicas'),
    ('I07',  'I07 - Comunicaciones satelitales'),
    ('I08',  'I08 - Otra maquinaria y equipo'),
    ('S01',  'S01 - Sin efectos fiscales'),
    ('CP01', 'CP01 - Pagos'),
]

RECEIPT_EFFECT_SELECTION_LIST = [
    ('I', 'Ingreso'), 
    ('G', 'Gasto'), 
    ('T', 'Transferencia'), 
    ('P', 'Pago'), 
    ('N', 'Nómina')
]

DATE_PERIOD_TYPE_SELECTION_LIST = [
    ('unique_date', 'Unique Date'), 
    ('period', 'Period')
]

STATUS_SELECTION_LIST = [
        ('draft', 'Draft'),
        ('emitted', 'Emitted'),
        ('cancelled', 'Cancelled'),
        ('paid', 'Paid')
]

RES_CURRENCY_MODEL = 'res.currency'

class CFDIIssued(models.Model):
    _name = 'odoo.cfdi.issued'
    _description = 'CFDI Issued'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'fiscal_folio'
    _order = 'fiscal_folio asc'

    fiscal_folio = fields.Char(string='Fiscal folio', help='Fiscal folio of CFDI', store=True, required=True, tracking=True)

    rfc_emitter = fields.Char(string='RFC Emitter', help='RFC emitter of CFDI', store=True, required=True, tracking=True)
    name_emitter = fields.Char(string='Name emitter', help='Name emitter of CFDI', store=True, required=True, tracking=True)
    zip_code_emitter = fields.Char(string='Zip code emitter', help='Zip code emitter of CFDI', store=True, required=True, tracking=True)
    fiscal_regime_emitter = fields.Selection(REGIME_SELECTION_LIST, string='Fiscal regime emitter', help='Fiscal regime emitter of CFDI', store=True, required=True, tracking=True)

    rfc_receiver = fields.Char(string='RFC receiver', help='RFC receiver of CFDI', store=True, required=True, tracking=True)
    name_receiver = fields.Char(string='Name receiver', help='Name receiver of CFDI', store=True, required=True, tracking=True)
    zip_code_receiver = fields.Char(string='Zip code receiver', help='Zip code receiver of CFDI', store=True, required=True, tracking=True)
    fiscal_regime_receiver = fields.Selection(REGIME_SELECTION_LIST, string='Fiscal regime receiver', help='Fiscal regime receiver of CFDI', store=True, required=True, tracking=True)

    cfdi_concept = fields.Selection(USE_CFDI_SELECTION_LIST, string='CFDI concept', help='CFDI concept', store=True, required=True, tracking=True)
    receipt_effect = fields.Selection(RECEIPT_EFFECT_SELECTION_LIST, string='Receipt effect', help='Receipt effect of CFDI', store=True, required=True, tracking=True)
    description = fields.Text(string='Description', help='Description of CFDI', store=True, required=True, tracking=True)
    currency_id = fields.Many2one(RES_CURRENCY_MODEL, default=lambda self: self.env.user.company_id.currency_id)
    total = fields.Monetary(string='Total', currency_field='currency_id', help='Total of CFDI', store=True, required=True, tracking=True)
    date_period_type = fields.Selection(DATE_PERIOD_TYPE_SELECTION_LIST, default='unique_date', string='Date period type', help='Date period type of CFDI', store=True, required=True, tracking=True)
    start_date = fields.Date(string='Start date', default=lambda self: fields.Date.context_today(self), help='Start date of CFDI', store=True, required=True, tracking=True)
    end_date = fields.Date(string='End date', help='End date of CFDI', store=True, tracking=True, default=lambda self: fields.Date.context_today(self))
    status = fields.Selection(STATUS_SELECTION_LIST, string='Status', help='Status of CFDI', readonly=True, default='draft', tracking=True)

    xml_file = fields.Binary("XML file", attachment=True, store=True)
    xml_filename = fields.Char("File name")

    _sql_constraints = [
        ('fiscal_folio_unique', 'unique(fiscal_folio)', ('The fiscal folio must be unique.')),
    ]

    @api.constrains('end_date')
    def _end_date_constraint(self):
        for record in self:
            if record.date_period_type == 'period' and record.end_date == False:
                raise ValidationError('You need to specify an end date for period type.')
            elif record.date_period_type == 'period' and record.end_date < record.start_date:
                raise ValidationError('The end date must be greater than or equal to the start date.')
            
    # Override Unlink Method
    def unlink(self):
        for rec in self:
            if rec.status != 'draft':
                raise ValidationError('You can only delete Draft CFDI Issued records.')
            return super(CFDIIssued, self).unlink()

    def _get_element_tree(self, tree, tag):
        for elem in tree.iter():
            if elem.tag.endswith(tag):
                return elem
        return None

    @api.onchange('xml_file')
    def _onchange_xml_file(self):
        if not self.xml_file:
            return False
        try:
            xml_data = base64.b64decode(self.xml_file)
            tree = ET.fromstring(xml_data)
            ns = {
                'cfdi': 'http://www.sat.gob.mx/cfd/4',
            }
            issuer = tree.find('cfdi:Emisor', ns)
            receiver = tree.find('cfdi:Receptor', ns)
            tax_stamp = self._get_element_tree(tree, 'TimbreFiscalDigital')
            receipt = self._get_element_tree(tree, 'Comprobante')
            concept = self._get_element_tree(tree, 'Concepto')
            
            if tax_stamp is not None:
                self.fiscal_folio = tax_stamp.attrib.get('UUID')
            if issuer is not None:
                self.rfc_emitter = issuer.attrib.get('Rfc')
                self.name_emitter = issuer.attrib.get('Nombre')
                self.fiscal_regime_emitter = issuer.attrib.get('RegimenFiscal') 
            if receiver is not None:
                self.rfc_receiver = receiver.attrib.get('Rfc')
                self.name_receiver = receiver.attrib.get('Nombre')
                self.zip_code_receiver = receiver.attrib.get('DomicilioFiscalReceptor')
                self.fiscal_regime_receiver = receiver.attrib.get('RegimenFiscalReceptor')
                self.cfdi_concept = receiver.attrib.get('UsoCFDI')
            if receipt is not None:
                self.zip_code_emitter = receipt.attrib.get('LugarExpedicion')
                self.receipt_effect = receipt.attrib.get('TipoDeComprobante')
                self.total = receipt.attrib.get('Total')
                date_str = receipt.attrib.get('Fecha')
                currency_str = receipt.attrib.get('Moneda')
                if date_str:
                    self.start_date = datetime.fromisoformat(date_str).date()
                    self.end_date = self.start_date
                if currency_str:
                    currency = self.env[RES_CURRENCY_MODEL].search([('name', '=', currency_str)], limit=1)
                    if currency:
                        self.currency_id = currency
            if concept is not None:
                self.description = concept.attrib.get('Descripcion')
        except Exception as e:
            raise ValueError("Error processing XML file: %s" % str(e))
           
    def action_set_emitted(self):
        self.status = 'emitted'

    def action_set_cancelled(self):
        self.status = 'cancelled'

    def action_set_paid(self):
        self.status = 'paid'