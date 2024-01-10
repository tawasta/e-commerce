.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================================
eCommerce: custom link rel='canonical' support for product pages
================================================================

* By default Odoo sets each page a <link rel="canonical" href="..."/> tag inside <head>
* This module allows bypassing this logic for products, and setting a custom canonical
  link for each product.
* Also updates the <link rel="alternate" hreflang="..."/> tags to point to the canonical
  link's language-specific URLs
* Intended for situations where the installation contains both the Odoo standard shop as 
  well as another set of product-related pages that are more SEO-friendly and
  advertising oriented. The products can then be configured to point to the relevant
  page in their canonical link tag.


Configuration
=============
* Have the product-related page that is outside the shop ready first
* Go to Product template view in backend and select the page in the "Canonical Link Target"


Usage
=====
* Open a product page in shop. Using view source, in its <head> tag you see one rel=canonical
  and multiple (depending on number of installed languages) rel=alternate <link> tags, all
  pointing to the configured website page.
* Note that Odoo applies the canonical link only when a public user views the page, i.e.
  as a logged in user you will not see the tag in <head>.


Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
