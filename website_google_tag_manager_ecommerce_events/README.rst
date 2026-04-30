.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Google Tag Manager: Additional eCommerce Events
===============================================

* This module is still in experimental phase.
* Fires some additional events to Google Tag Manager during eCommerce flow:

  * view_item - when product page is opened
  * add_to_cart - when product is added to cart
  * begin_checkout - when reaching /shop/checkout
  * purchase - after confirming purchase in shop

Configuration
=============
* In Odoo, ensure you have GTM Tag configured
* In GTM, configure that you are listening to the above events

Usage
=====
* Events fire on the background during ecommerce flow

Known issues / Roadmap
======================
* Consider adding configuration switches for which events to fire,
  and add support for more GTM events.


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
