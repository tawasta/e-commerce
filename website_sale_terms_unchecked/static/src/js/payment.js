odoo.define('website_sale_terms_unchecked.payment', function (require) {
"use strict";

    $(document).ready(function () {
        // Trigger confirm button disable
        $('#checkbox_cgv').trigger('change');
    });
});