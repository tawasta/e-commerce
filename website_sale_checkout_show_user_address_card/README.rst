.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
eCommerce: Show user address card in checkout
=============================================

* Shows the ordering customer (name, email and phone) in a separate
  "Customer" card above the delivery/billing address cards on the 
  checkout page.
* Makes it clearer who is placing the order and who is billed, e.g. when the
  invoice goes to a company or a separate invoice address.
* The card is shown only to logged-in customers. For guests it would just
  repeat the billing address they have entered.

Configuration
=============
* None needed

Usage
=====
1. Log in, go to **Website Shop** and add items to the cart.
2. Proceed to checkout → the "Customer" card is shown above the delivery and
   billing addresses.

Known issues / Roadmap
======================
* None

Changelog
=========

19.0.1.0.0 This functionality was moved into this separate module from 
17.0 module ``website_sale_billing_address``.

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
