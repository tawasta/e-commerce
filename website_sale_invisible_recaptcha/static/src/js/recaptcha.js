odoo.define("website_sale_invisible_recaptcha.product", function (require) {
  "use strict";

  $(".a-submit").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    grecaptcha.execute();
  });
  function myCallback() {
    $(".g-recaptcha").each(function () {
      var object = $(this);
      grecaptcha.render(object.attr("id"), {
        sitekey: object
          .parents("form")
          .find(".g-recaptcha")
          .attr("data-sitekey"),
        size: "invisible",
        callback: function (token) {
          object.parents("form").find(".g-recaptcha-response").val(token);
          object.parents("form").submit();
        },
      });
    });
  }
  window.onloadCallback = myCallback;
});
