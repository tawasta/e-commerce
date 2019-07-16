odoo.define('website_sale_delivery_cleanup.payment_delivery', function (require) {
"use strict";

    $(function () {
        $('.delivery-info').click(function(event) {
            // Don't change the delivery method
            event.preventDefault();

            // Toggle info visibility
            $(this).parent().find('.delivery-description').toggleClass('hidden');
        });
    });
});