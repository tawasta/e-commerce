odoo.define("website_sale_default_email.copy_email", function () {
    "use strict";
    // Idea: Pitää requestata xml documenttia, jossa on sliderin arvo
    //       -> Tarkastetaan sliderin arvo. Jos kyseessä yritys,
    //          niin kopioidaan emailin arvo invoice email kenttään
    $(function() {
        function testFunc() {
            var field_required = $("input[name='field_required']");
            console.log("TESTI: ", field_required);
        }
    });
});
