.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
Payment Acquirer - Force Autoconfirm Option
===========================================

* Adds a new configuration option to Payment Acquirers that enables the
  autoconfirmation of Sale Orders originating from the website, regardless of
  their payment transaction status
* Intended for situations where there is no Paypal, Paytrail etc. proper 
  payment integration set up, but webshop orders should still get confirmed
  automatically

Installation
============
\-

Usage
=====
* Open the configuration view for the payment acquirer you are using on the 
  website (e.g. Wire Transfer).
* Select the new "Ignore authorization and confirm SO immediately" option for 
  the Configuration -> Order Confirmation setting.

Known issues / Roadmap
======================
* None

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
