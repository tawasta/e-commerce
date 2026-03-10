.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
eCommerce: Finnish Company Registry Support
===========================================

* Handling of Finnish company registry (Y-tunnus) on the website checkout form
* Successor to 14.0 website_sale_business_code

Configuration
=============
* None needed

Usage
=====
* Proceed to checkout, select Finland as country, and set the new
  "Company Registry / VAT" field value. The input gets 
  validated as Finnish Y-tunnus format.
* With other countries the standard VAT validation is run
* Click Create Company on the partner backend form afterwards, and the
  created company will have both company registry and VAT fields filled.

Known issues / Roadmap
======================
* The suggested prefill value needs work when used in cases where customers 
  register accounts before ordering, and both Finnish and non-Finnish 
  countries are expected (the former should get a prefill
  with Y-tunnus, the latter with VAT).
* Some compatibility issues with other website_sale_* modules, e.g.
  installing company slider would make the VAT field mandatory.

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
