odoo.define("website_sale_default_email.copy_email", function () {
    "use strict";
    $(function () {
        var is_company = false;
        // Getting the slider from the xml document
        // of the website_sale_company_slider module
        var slider = document.getElementById("company");

        function slider_onchange() {
            if (slider.checked) {
                is_company = true;
            } else {
                is_company = false;
            }
        }

        if (slider) {
            // We call the function if the slider value changes.
            slider.addEventListener("input", slider_onchange);
            // First time loading the page the slider value does not change
            // So we have to call the function manually.
            slider_onchange();
        }

        // If company, then we want to copy the email to
        // company email field
        var email_input = document.querySelector('#div_email input[name="email"]');
        if (email_input) {
            email_input.addEventListener("input", function () {
                if (is_company) {
                    var company_email = document.querySelector(
                        '#company_email input[name="company_email"]'
                    );
                    company_email.value = email_input.value;
                }
            });
        }
    });
});
