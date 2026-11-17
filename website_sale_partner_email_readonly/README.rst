.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Website Sale: Read-only Own Email
=================================

* Makes the email field read-only in the checkout address form when a portal
  user edits their own contact, and shows a link to the portal security page
  where the username (and with it the email) can be changed.
* The email of delivery and invoice addresses stays editable.
* Applies only when the setting *Update Contact Email on Portal Username Change*
  of ``website_portal_username_change`` is enabled.
* Saving the address with a changed email is also refused on the server, and
  the express checkout routes do not overwrite the email.

Configuration
=============
* Enable Settings > General Settings >
  "Update Contact Email on Portal Username Change".

Usage
=====
* Navigate to Shop > Checkout and edit your own address.

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
