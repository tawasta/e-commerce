.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
eCommerce: Hide own address edit in checkout delivery list
==========================================================

* Hides the edit button of the customer's own address card
  in the delivery address list of the checkout page.
* Intended to prevent customers from accidentally changing their 
  own main contact details when they only meant to change where the
  current order is delivered.

Configuration
=============
* None needed

Usage
=====
1. Log in, add a deliverable product to the cart and proceed to checkout.
2. The own address card in the delivery list has no edit button. Use
   "Add Address" to deliver the order elsewhere.

Known issues / Roadmap
======================
* Only the button is hidden. The own address can still be edited from the
  billing address list, the "Customer" card of
  ``website_sale_checkout_show_user_address_card``, the portal's
  "My addresses" page, or by opening the address form URL directly.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
