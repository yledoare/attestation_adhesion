from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    organization_title = fields.Char(string='Organization title', required=False)
    organization_season = fields.Char(string='Organization season', required=False)
