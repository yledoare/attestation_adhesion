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

    user_partner_id = fields.Many2one(
        'res.partner',
        string="User's own partner",
        compute='_compute_user_partner_id',
        store=False
    )

    #user_company_id = fields.Many2one(
    #    'res.company',
    #    string="User's Company",
    #    compute='_compute_user_company_id',
    #    store=False
    #)

    def _compute_user_partner_id(self):
        print("DEBUG YLD1")
        for rec in self:
            print("DEBUG YLD partner id"+str(self.env.partner.id))
            print("DEBUG YLD company id"+str(self.env.company.id))
            print("DEBUG YLD"+self.env.company.name)
            rec.user_partner_id = self.env.company.id
    def _compute_user_company_id(self):
        print("DEBUG YLD0")
        for rec in self:
            print("DEBUG YLD"+str(self.env.company.id))
            print("DEBUG YLD"+self.env.company.name)
            rec.user_company_id = self.env.company.id

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

    #customer_id = fields.Many2one('res.partner', string='Customer',domain="['|', ('company_id', '=', False), ('company_id', 'in', allowed_company_ids)]")
    #customer_id = fields.Many2one('res.partner', string='Customer', domain=lambda self: [ ("is_company", "=", False), ("parent_id", "=", self.env.company.partner_id.id), ])
    customer_id = fields.Many2one('res.partner', string='Customer', 
                  required=True,
                  )
    #organization_id = fields.Many2one('res.partner', string='Organization', domain="['|', ('company_id', '=', False), ('company_id', 'in', allowed_company_ids)]")
    #organization_id = fields.Many2one('res.partner', string='Organization', domain=lambda self: [ ("is_company", "=", False), ("parent_id", "=", self.env.company.partner_id.id), ])
    organization_id = fields.Many2one('res.partner', string='Organization',
  #                default=user_company_id,
                  required=True,
                  )

    amount = fields.Float('Amount', default=30)
    payment_date = fields.Date('Payment day', default=fields.Date.today)
    currency = fields.Char('Currency', default="Euros")

    name_of_organization = fields.Char( string='Organization Name', related='organization_id.name')
    title_of_organization = fields.Char( string='Title', related='organization_id.organization_title')
    city_of_organization = fields.Char( string='Title', related='organization_id.city')
    current_organization_season = fields.Char( string='Title', related='organization_id.organization_season')
    name_of_customer = fields.Char( string='Customer Name', related='customer_id.name')
    email_of_customer = fields.Char( string='Customer Email', related='customer_id.email')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

