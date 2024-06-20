.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
eCommerce: Suggested Accessories Categorized View
=================================================
* In Order overview, the module sorts all the Suggested Accessories based on configurable categories,
  instead of a single list.
* Provides two new toggles in website editor's Customize section 

  * "Switch to primary button style for Suggested Accessories' Add to Cart buttons (applies to Suggested Accessories Categorized View)"
  * "Hide Order Overview Suggested Accessories' Product Images (applies to Suggested Accessories Categorized View)"

Configuration
=============
* Navigate to Website > Configuration > Suggested Products Categories
* Create a record. Give name and description which is shown in cart for the category.
* Add eCommerce Categories. Products listed under these eCommerce Categories will be shown in cart under Suggested Products Categories.

Usage
=====
* Add to cart a product that has suggested accessories configured. 
* Go to Order Overview. The suggestions appear as categorized under the order lines


Known issues / Roadmap
======================
* Products shown in cart under Suggested Products Categories are fetched from eCommerce Categories.
  Cleaner solution might be to directly set Products in Suggested Products Categories to cut out the confusing middle man eCommerce Category.

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@tawasta.fi>
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
