.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
eCommerce: Shop-related Pages Require Login
===========================================

* Modifies routes so that authentication is required to access shop pages
* Also sets sitemap=False to avoid indexing, for those Shop-related
  routes that had it set to True by default.


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

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
