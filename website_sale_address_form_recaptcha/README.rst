.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
eCommerce: Recaptcha for Address Form
=====================================

* Run recaptcha check when user enters their address in 
  web shop flow.
* Intended to prevent bots from creating useless partner records

Configuration
=============
* Add the Recaptcha v3 keys in core's General Setttings view

Usage
=====
* Proceed to the address page in webshop flow. Submitting the form
  triggers the recaptcha check.
* Core prints the submission's recaptcha check score into Odoo log. 
  You can test a rejected form submission by adjusting the 
  Minimum score in General Settings to 0.99 and then submitting the 
  address form  in a fresh incognito window.

Known issues / Roadmap
======================
* None

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
