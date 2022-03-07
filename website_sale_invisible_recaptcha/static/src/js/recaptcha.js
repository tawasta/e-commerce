odoo.define('website_sale_invisible_recaptcha.product', function (require) {
    "use strict";

    var core = require('web.core');
    var time = require('web.time');

    $(function () {

        $('.check-recaptcha').on('submit', function() {
            grecaptcha.execute();
        });

        $('.a-submit').on('click', function() {
            grecaptcha.execute();
        });

    });
    window.onSubmit = function () {
        console.log("success");
    };

});
