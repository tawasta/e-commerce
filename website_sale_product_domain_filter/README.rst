.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Website Sale Product Domain Filter
==================================
This module restricts visibility of products on the Odoo website shop
based on partner-specific domain rules (`paywall_domain`).

Users will only see products they are allowed to access.

Features
========

* Define a domain (`paywall_domain`) for each product
* Users only see products if their partner (`res.partner`) matches the domain
* Filters apply to:
  * Shop search results
  * Autocomplete suggestions
  * Individual product pages
* Backend domain editor (domain widget in product form)

Usage
=====

1. Go to **Sales** → **Products**
2. Edit a product and add a **Paywall Domain** (e.g., `[('country_id.code', '=', 'FI')]`)
3. In the frontend (website shop), users will only see products matching their `res.partner` via the domain

Technical Details
=================

* `paywall_domain` is a Char field (safe_eval evaluated)
* `user_in_paywall_domain` is a computed boolean field
* Website routes for product views and search are extended to apply filtering
* Autocomplete controller is extended to filter product suggestions


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
