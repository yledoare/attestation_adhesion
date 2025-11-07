# -*- coding: utf-8 -*-
{
    'name': "attestation_adhesion",
    'summary': "attestation_adhesion ",
    'description': """
Long description of module's purpose
    """,
    'author': "OS4B",
    'website': "https://www.os4b.bzh",

    'category': 'Attestation',
    'version': '1.01',

    'depends': [
        'mail',
        'base',
        'contacts',
    ],

    'data': [
        # SECURITY
        'security/ir.model.access.csv',
        # VIEWS
        'views/attestation_adhesion.xml',
        'views/res_partner_views.xml',
        # MAIL
        'data/attestation_adhesion_email.xml',
        # REPORT
        'report/attestation_adhesion_report.xml',
        'report/attestation_adhesion_report_template.xml',
    	'report/disable_footer.xml',
        'report/disable_header.xml',
        # MENU
        'views/menu.xml',
    ],

    'assets': {
        'web.report_assets_common': [ 'attestation_adhesion/static/src/css/adhesions.css' ],
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',

}

