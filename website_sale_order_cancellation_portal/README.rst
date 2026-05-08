.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Website Sale Order Cancellation Portal
======================================

This module adds a customer portal cancellation notice workflow for sale orders.

The module allows customers to submit a cancellation notice directly from the
sale order portal page when cancellation is still available for the order. The
notice is recorded in Odoo, linked to the related sale order, and confirmed to
the customer by email.

Sales managers are notified when a new cancellation notice is submitted. If the
sale order already has invoices, the notification and sale order chatter message
clearly indicate that possible refunds, credit notes, payment returns, or
accounting actions must be handled manually.

The module can also attempt to cancel the sale order after the cancellation
notice has been submitted. If the automatic sale order cancellation fails, the
failure is logged and a chatter message is added to the sale order for manual
follow-up.

Configuration
=============

To configure the cancellation period:

#. Go to **Sales > Configuration > Settings**.
#. Find **Portal Order Cancellation**.
#. Set **Portal Cancellation Period in Days**.
#. Save the settings.

The configured period defines how many days after the sale order date the
customer can submit a cancellation notice from the portal.

The cancellation button is shown only when all of the following conditions are
met:

* The sale order is not cancelled.
* No cancellation notice has already been submitted for the sale order.
* The cancellation deadline is still valid.
* The sale order contains at least one regular order line with quantity greater
  than zero.

Usage
=====

Customer portal
---------------

#. The customer opens a sale order from **My Account > Orders**.
#. If cancellation is available, the portal shows an **Order cancellation**
   section.
#. The customer clicks **Cancel Order**.
#. A confirmation modal is opened.
#. The modal shows the order number, cancellation deadline, processing
   information, and an optional cancellation reason field.
#. The customer confirms the cancellation notice.
#. Odoo records the cancellation notice and shows a confirmation message in the
   portal.

After submission, the customer receives an email confirmation stating that the
cancellation notice has been received and submitted for processing.

Sales management
----------------

Sales managers can review submitted cancellation notices from:

**Sales > Orders > Cancellation Notices**

Each cancellation notice contains:

* Related sale order
* Customer
* Received date and time
* Optional cancellation reason
* Chatter history and scheduled activities

When a cancellation notice is submitted, the module also:

* Adds a chatter message to the related sale order.
* Sends an email notification to Sales Managers.
* Creates an activity for Sales Managers.
* Highlights if the sale order has invoices that require manual handling.

Notes
-----

Submitting a cancellation notice is not the same as automatically refunding or
reversing accounting entries.

If the sale order has invoices, any required refunds, credit notes, payment
returns, or accounting actions must be handled manually according to the
company's normal accounting process.

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy.