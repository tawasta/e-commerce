.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Website Sale Product Domain Filter
==================================
This module restricts the visibility of products in the Odoo website shop
based on partner-specific domain rules.

Only users matching the defined criteria will be able to see or buy the product.

Features
========

* Define a custom filters for products
* Products are shown only if the current user's partner (`res.partner`) matches the domain
* Filters apply to:
  * Shop search results
  * Autocomplete suggestions
  * Individual product pages
  * Suggested accessories
  * Related / recommended products
  * Add-to-cart logic
* Backend domain editor (domain widget in product form)
* Prevents access to product pages if not allowed
* Prevents restricted products from being added to cart or suggested

Usage
=====

1. Go to **Sales** → **Products**
2. Edit a product and add a **Partner filters**, e.g.:

   ::

       [('country_id.code', '=', 'FI')]

3. In the frontend (website shop), users will only see the product if their partner matches the domain condition

Technical Details
=================

* `user_in_partner_domain` is a computed boolean field based on the current user’s `res.partner`
* Filters are applied at:
  * Product listing
  * Product details
  * Cart suggestions
  * Autocomplete
* `_can_be_added_to_cart()` is overridden to prevent forbidden products being added
* `_cart_accessories()` is extended to exclude restricted products
* Fully compatible with `website_sale` & `website_sale_cart`


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
