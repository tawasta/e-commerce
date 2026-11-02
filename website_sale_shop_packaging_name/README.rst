.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
eCommerce: Packaging Name in Shop Price
=======================================

* Shows the packaging name next to the price in the shop product
  grid and list, e.g. "€19.90 / 24-pack" or "€1.50 / Units".
* Intended for situations where you are selling only a specific packaging in 
  e-commerce (e.g. with ``website_sale_packaging_restriction``), and you 
  want to make it clear that the price shown in grid is e.g. for a dozen, 
  not a single unit.

Configuration
=============
* None needed

Usage
=====
* The name is shown after installation. To hide it, go to the shop page, 
  click **Edit**, select the product grid and untick **Packaging Name**
  in the shop options. Save.

Known issues / Roadmap
======================
* Dynamic product snippets and product tiles that render their own price do
  not show the name.

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
