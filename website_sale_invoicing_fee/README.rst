.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Invoicing Fee for Website Sale
=============================
Shows and applies an invoicing/payment fee on the webshop checkout page,
based on the payment method the customer selects.

This module only adds the website checkout badge and the controller hook
that syncs the fee line on the sale order. The fee product itself is
configured per payment method by the ``sale_invoicing_fee`` module, which
this module depends on.

Features
========
- Shows the fee (with tax) as a badge next to each payment method with a
  configured fee product, directly on the ``/shop/payment`` page
- Adds the fee product to the sale order when the customer pays with a
  fee-carrying payment method (fresh selection or a reused saved token)
- Automatically removes the fee line again if the customer switches to a
  different payment method (fee or no fee) before completing payment

Configuration
=============
See ``sale_invoicing_fee``: **Invoicing > Configuration > Payment Methods**,
field **Extra fee product**.

Usage
=====
Nothing to do on the website side: once a payment method has a fee
product configured, the checkout page picks it up automatically.

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
