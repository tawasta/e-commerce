.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
eCommerce: Force login
======================

* Force login/signup before adding products to carts
* Redirects to product page after login/signup

Configuration
=============
\-

Usage
=====
\-

Changelog
=========

17.0.1.2.0
----------

* t-cache attributes taken into use to mitigate issue where the result
  of is_public_user() could be cached and produce wrong results when
  e.g. reloading the page rapidly as a portal user.

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>
* Joona Isoaho <joona.isoaho@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
