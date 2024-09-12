.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Website sale create user
========================

* This Odoo module enhances the functionality of sales and product management by integrating user creation based on product category settings directly within the sales order workflow. It includes customization options for products to trigger user creation and attach specific documents when a sale is confirmed.

* When a sales order is confirmed, the system checks each product line to determine if the associated product category has user creation enabled. If at least one product qualifies, and the sales team matches the configured e-commerce team (if the setting is enabled), the module will proceed to create a user.

Features
========

* User Creation Control by Product Category: Set whether users can be created from the sale of products within specific categories.
* Attachment Management: Attach specific documents to the user creation process, managed at the product category level.
* Automatic User Creation: Automatically create portal users when specific conditions are met in the sales order process.

Configuration
=============
\-

Usage
=====
* After configuration, the module operates automatically upon the confirmation of sales orders. Ensure that your sales team is aware of the new features and how they affect sales and user management processes.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
