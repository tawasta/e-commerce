import re
from odoo import api
from odoo import models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    @api.model
    def create(self, values):
        if 'website_description' in values:
            description, altered = self._format_image_iframe(
                values['website_description'])

        res = super(ProductTemplate, self).create(values)

        if altered:
            self.website_description_force_update(description)

        return res

    @api.multi
    def write(self, values):
        if 'website_description' in values:
            description, altered = self._format_image_iframe(
                values['website_description']
            )

        res = super(ProductTemplate, self).write(values)

        if altered:
            self.website_description_force_update(description)

        return res

    def _format_image_iframe(self, website_description):
        pattern = re.compile(r'[<][a][^>]+[>][<][/][a][>]')
        ir_attachment = self.env['ir.attachment']
        altered = True

        for a in re.findall(pattern, website_description):
            if 'title="iframe' in a:
                # Handle iframe-links differently
                attachment_match = re.search('content[/]([0-9]+)', a)
                if not attachment_match:
                    continue

                attachment_id = int(attachment_match.group(1))
                attachment = ir_attachment.browse([attachment_id])
                # Replace the image URL with iframe
                altered = True
                website_description = website_description.replace(
                    a,
                    attachment.url)

                # Remove the obsolete attachment
                attachment.unlink()

        return website_description, altered

    def website_description_force_update(self, description):
        """
        Force update website description and BYPASS ORM.
        Write and Create methods don't pass sanitize_tags attribute so we can't
        just skip the sanitation (which will remove iframe-tags)

        This may expose the datatabase to an injection attack. AVOID USING THIS!
        """
        self._cr.execute(
            "UPDATE product_template "
            "SET website_description = '{}' "
            "WHERE id = {}".format(description, self.id))
