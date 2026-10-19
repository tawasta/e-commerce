.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
eCommerce: Always show address-step
===================================

* This module ensures that the checkout **address step** is always shown,
  even if the customer already has saved contact details.
* It is useful if you want to make sure that the user always confirms or updates
  their contact information, and that related contacts are visible.
* By default Odoo skips the checkout page and goes straight to the next step
  (extra info or payment) when the cart has no deliverable products, e.g. only
  services or event tickets. This module disables that skip, so the checkout
  page is shown for every cart.

Configuration
=============
* None needed

Usage
=====
1. Go to **Website Shop**.
2. Add items to cart.
3. Proceed to checkout → Address step is always shown before payment.

Known issues / Roadmap
======================
* Express checkout buttons (e.g. Google Pay) on the cart page would bypass the
  address step by design.
* Opening ``/shop/payment`` directly (e.g. from a bookmark) is not blocked;
  Odoo still requires complete addresses before payment.

Changelog
=========

19.0.1.0.0
----------

* Migrated to 19.0. The implementation now only disables the
  ``try_skip_step`` parameter of ``/shop/checkout`` instead of guarding
  the payment step with a session flag.


Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
