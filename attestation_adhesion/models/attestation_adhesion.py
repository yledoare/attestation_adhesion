# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import Response, request
from odoo.exceptions import UserError
from io import BytesIO
import base64
import io
import datetime
from datetime import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter

class AttestationAdhesion(models.Model):
    _name = 'attestation.adhesion'
    _inherit = [
            'mail.thread',
            'mail.activity.mixin',
            'image.mixin',
            ]
    _description = 'Adhesions'

    def action_send_mail(self):
      template = self.env.ref('attestation_adhesion.mail_template_attestation_adhesion')
      if template:
        template.send_mail(self.id, force_send=True)
      else:
        raise UserError("Mail Template not found. Please check the template.")
    def send_email_with_pdf_attach(self):
      report_pdf = request.env[ "ir.actions.report" ]._render_qweb_pdf( "attestation_adhesion.attestation_adhesion_report", [self.id])
      pdf_base64 = base64.b64encode(report_pdf[0])
      attachment_values = {
        'name': _("Adhesion") + ".pdf",
        'type': 'binary',
        'datas': pdf_base64,
        'mimetype': 'application/pdf',
      }
      attachment = self.env['ir.attachment'].create(attachment_values)
      ir_values = {
            'name': 'Rent receipt Report',
            'type': 'binary',
            'res_model': 'attestation.adhesion',
            }
      email_template = self.env.ref('attestation_adhesion.mail_template_attestation_adhesion')
      email_template.attachment_ids = [(4, attachment.id)]

      if email_template:
            email_template.send_mail(self.id)
            email_template.attachment_ids = [(5, 0, 0)]

    customer_id = fields.Many2one('res.partner', string='Customer')
    organization_id = fields.Many2one('res.partner', string='Organization')
    amount = fields.Float('Amount')
    payment_date = fields.Date('Payment day')
    currency = fields.Char('Currency', default="Euros")

    name_of_organization = fields.Char( string='Organization Name', related='organization_id.name')
    title_of_organization = fields.Char( string='Title', related='organization_id.organization_title')
    city_of_organization = fields.Char( string='Title', related='organization_id.city')
    current_organization_season = fields.Char( string='Title', related='organization_id.organization_season')
    name_of_customer = fields.Char( string='Customer Name', related='customer_id.name')
    email_of_customer = fields.Char( string='Customer Email', related='customer_id.email')
