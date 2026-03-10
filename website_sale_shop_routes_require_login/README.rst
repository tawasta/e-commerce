.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
eCommerce: Shop-related Pages Require Login
===========================================

* Modifies routes so that authentication is required to access shop pages
* Also sets sitemap=False to avoid indexing, for those Shop-related
  routes that had it set to True by default.
* Intended for situations where you want even the product catalogue 
  viewing access to be invite-only.


Configuration
=============
* None needed

Usage
=====
* When module is installed and you are not logged in, try to access e.g. /shop. 
* You'll be redirected to login page instead

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

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
