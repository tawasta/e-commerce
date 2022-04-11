odoo.define("website_sale_invisible_recaptcha.product", function (require) {
  "use strict";

  $(".a-submit").on("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    var object = $(this).parents("form").find(".g-recaptcha");
    var widget = grecaptcha.render(object.attr("id"), {
      sitekey: object.parents("form").find(".g-recaptcha").attr("data-sitekey"),
      size: "invisible",
      callback: function (token) {
        object.parents("form").find(".g-recaptcha-response").val(token);
        object.parents("form").submit();
      },
    });
    grecaptcha.execute(widget);
  });
});
