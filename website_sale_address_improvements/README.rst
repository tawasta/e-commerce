.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Website Sale - Address Improvements
===================================

This module attempts to improve and clarify the address functionality in the 
webshop by doing the following:

* The "Billing Address" subheading in checkout is renamed to "Your Address" to 
  be in line  with the terminology used in the Address editing page. The 
  original term is also misleading because the shown address may not even 
  represent the actual billing address computed by res_partner.address_get().
* The sidebar in Payment and Confirmation stages now contains all three
  addresses: Your Address, Billing Address and Shipping Address
* The sidebar's Billing Address section shows the edicode and einvoice operator 
  instead of the mail address, if an edicode is set
* Orders placed by a company's contact person are automatically linked to the 
  parent company in the order confirmation phase

Installation
============
\-

Usage
=====
\-

Known issues / Roadmap
======================
* Improvement: make linking orders to parent partner a configurable option
* New feature: allow the user to select an invoice address in a similar way 
  as the shipping address, instead of blindly relying on address_get() 

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
