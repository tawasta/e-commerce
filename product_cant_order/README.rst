.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Product Variant: Prevent Ordering via eCommerce
===============================================

This module adds the ability to mark product variants or templates as "Cannot be Added to Cart".  
It prevents customers from adding such products to their shopping cart on the website.

Features
========
- Adds a boolean field `can_not_order` on product variants (`product.product`)
- Adds a boolean field `can_not_order_template` on product templates (`product.template`)
- Configurable via system parameter `product_cant_order.can_not_order_use_template` to choose whether to check the flag on the variant or on the template level
- Hides the Add to Cart and Buy Now buttons on the website automatically based on the flag
- Provides a JSON route `/check/product/<product_id>` to check product availability for ordering


Configuration
=============
- Enable the "Cannot be Added to Cart" checkbox on the desired product variants or product templates:
  - Go to **Sales > Products > Product Variants** to set variant-level flag
  - Go to **Sales > Products > Product Templates** to set template-level flag
- Set system parameter `product_cant_order.can_not_order_use_template` to `"True"` or `"False"` to decide the check level


Usage
=====
- On the eCommerce product page, selecting a variant or product with the flag set will hide the Add to Cart and Buy Now buttons
- The system uses the config parameter to decide whether to check the variant or the template field

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
