.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================
Website Sale Address Phone Country Code
========================================

* Adds field for country code to the phone number field in the address form on 
  the checkout page.
* Phone number is stored in E.164 format and normalized with the selected 
  country code. Saves to the phone field in the res.partner model.
* Uses JS async function to remove country code placeholder added by core 
  to the phone field.

Configuration
=============
\-

Usage
=====
* Install the module

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Joonas Lahtinen <joonas.lahtinen@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
