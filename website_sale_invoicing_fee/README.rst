.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Invoicing fee on Website sale
=============================
This module allows you to automatically add an invoicing fee (extra product) to a webshop Sale Order based on the selected payment method.

When a customer confirms a webshop order, the system checks whether the selected **Payment Method** has a product assigned. If so, that product (representing the invoicing or payment fee) is added automatically to the Sale Order lines.

Features
========

- Adds a configurable extra product (e.g. invoicing fee) to webshop Sale Orders
- Product selection is done per payment method
- Fee is shown to the customer on the payment screen (frontend badge)
- Works with taxes and fiscal positions

Configuration
=============

1. Go to **Invoicing > Configuration > Payment Methods**
2. Open or create a payment method used in the webshop
3. Assign a product in the field **Extra fee product**

Ensure the product:
- Has a sales price
- Is visible for invoicing (if needed)
- Is available in the correct company/website

Usage
=====

When a customer completes a webshop order and selects a payment method that has a product assigned:

- The product is automatically added to the Sale Order
- The price (with taxes) is shown as a badge next to the payment method during selection


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Miika Nissi <miika.nissi@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
