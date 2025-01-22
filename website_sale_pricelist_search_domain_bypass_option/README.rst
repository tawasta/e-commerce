.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
eCommerce: Pricelist Search Domain Bypass option
================================================

* Context flag for bypassing pricelist domain applied by website_sale
* Intended for situations where you need to read/set a partner's pricelist
  via e.g. portal controllers, but you do not want to be limited to just the 
  pricelists that have their Website field set

Configuration
=============
* None needed

Usage
=====
* Does nothing yet on its own
* Call in other modules using with_context(exclude_website_sale_pricelist_domain=True)
  as needed.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
