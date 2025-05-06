.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Website sale billing address
============================

* This Odoo module extends the standard website sale checkout flow by enabling support for a separate billing address and invoice-specific fields. It provides custom logic and dynamic behavior for fields such as company registry number (VAT), invoice transmit method, invoice email, and e-invoice operator details.

The fields are shown or hidden depending on the selected transmit method (e.g. email, post, e-invoice), and validated accordingly. Valid data is written to the sales order's invoice partner only when the form passes all validation checks.

Key features:

- Billing address mode in checkout with dedicated fields
- Company registry/VAT validation during checkout
- Dynamic visibility and required logic for transmit method–specific fields
- Prevents overwriting billing partner if there are form validation errors
- Integration with modules like `website_sale_invoice_transmit_method` and `website_sale_company_email`


Configuration
=============
\-

Usage
=====
- Customer proceeds to checkout
- Billing address and invoice-related fields are displayed
- Selected transmit method (e.g. post or e-invoice) affects which fields are shown
- After submission, valid data is saved to the invoice address

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
