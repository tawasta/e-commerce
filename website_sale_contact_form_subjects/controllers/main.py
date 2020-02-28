from odoo import _
from odoo import http
from odoo.http import request
from odoo.http import route


class WebsiteCrm(http.Controller):

    @route('/contactus', type='http', auth='public', website=True)
    def subjects(self, **post):

        values = {}

        subjects = [
            _('Product reservation'),
            _('Resale'),
            _('Returns'),
            _('Technical support'),
            _('Reclamation'),
            _('Feedback'),
            _('Other reason')
        ]

        values.update({
            'subjects': subjects,
        })

        return request.render("website_crm.contactus_form", values)
