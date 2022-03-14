odoo.define("website_sale_invisible_recaptcha.product", function (require) {
  "use strict";

  var core = require("web.core");
  var time = require("web.time");

  $(function () {
    $(".check-recaptcha").on("submit", function (event) {
      window.grecaptcha.execute();
    });

    $(".a-submit").on("click", function (event) {
      if (!window.grecaptcha.getResponse()) {
        event.preventDefault();
        event.stopPropagation();
        window.grecaptcha.execute();
      }
    });
  });
  window.onSubmit = function (event) {
    $(".a-submit").trigger("click");
  };
});
