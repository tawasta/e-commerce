.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
eCommerce: Partner Default Invoice Address
==========================================

* Extend the functionality of partner_default_invoice_address to
  suggest the default invoice address for eCommerce orders
* Adds a domain limitation to the possible addresses, to avoid
  error 403 in address step of checkout

Configuration
=============
* Configure the Default Invoice Address field for a partner company
* Add portal access to a contact partner of that company

Usage
=====
* Navigate to checkout as that contact. The configured default invoice
  address will be suggested, instead of the contact partner itself.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
