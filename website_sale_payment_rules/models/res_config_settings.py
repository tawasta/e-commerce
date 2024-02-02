from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_sale_add_explanation_text = fields.Html(
        string="Website sale: add an explanation",
        related="website_id.add_explanation_text",
        readonly=False,
        translate=True,
    )

    website_sale_add_attachment_text = fields.Html(
        string="Website sale: add an attachment",
        related="website_id.add_attachment_text",
        readonly=False,
        translate=True,
    )

    website_sale_required_product_categ_text = fields.Html(
        string="Website sale: Required product category text",
        related="website_id.product_categ_text",
        readonly=False,
        translate=True,
    )

    website_sale_add_company_info_text = fields.Html(
        string="Website sale: need company data",
        related="website_id.company_info_text",
        readonly=False,
        translate=True,
    )

    website_sale_mandatory_products_text = fields.Html(
        string="Website sale: mandatory products",
        related="website_id.mandatory_products_text",
        readonly=False,
        translate=True,
    )
