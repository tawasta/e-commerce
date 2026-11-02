.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
eCommerce: Restrict Packagings
==============================

* Enables choosin per product which units and packagings can be bought on eCommerce,
  e.g. selling soda only as a 24-pack but never as single pcs.
* The shop grid price, the product page price and the packaging selector use
  the first allowed packaging, which is also preselected.
* The packaging selector and the cart line packaging are shown also when only
  one packaging is allowed, so the customer sees what is bought.
* Combo items are always added in the base unit, as the combo price does not
  depend on the unit.
* Backend sales are not affected: all units and packagings stay available.

Configuration
=============
* Enable **Settings > Sales > Units & Packagings**.
* On the product, add the packagings in the **Packagings** field
  (**Sales** tab).

Usage
=====
* On the product, set **eCommerce Packagings** to the units and packagings
  that can be bought on eCommerce.
* Leave the field empty to allow all of them (standard Odoo behaviour).

Known issues / Roadmap
======================
* The comparison price (``compare_list_price``) is shown as such and not
  converted to the packaging, as in standard Odoo.

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
