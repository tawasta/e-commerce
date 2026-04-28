.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
eCommerce: Suggest eInvoice-based Invoice Address
=================================================

* In checkout, try to suggest an invoicing address with edicode and
  invoice operator, if one exists for the partner
* Intended for B2B shops where you want to steer the user towards
  selecting the einvoicing option

Configuration
=============
* None needed

Usage
=====
* Navigate to checkout. einvoice-based invoice address is suggested
  as a default, if one exists for the partner. Otherwise Odoo core's
  default suggestion logic is used.

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
