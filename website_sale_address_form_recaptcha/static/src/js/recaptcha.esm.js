/** @odoo-module **/
import {ReCaptcha} from "@google_recaptcha/js/recaptcha";
import publicWidget from "@web/legacy/js/public/public_widget";

/* This mimics the implementation of signup form check in google_recaptcha module */
const CaptchaFunctionality = {
    events: {
        submit: "_onSubmit",
    },

    init() {
        console.log("init reached");
        this._super(...arguments);
        this._recaptcha = new ReCaptcha();
    },

    async willStart() {
        console.log("willstart reached");
        return this._recaptcha.loadLibs();
    },

    _onSubmit(ev) {
        console.log("onsubmit reached");
        if (
            this._recaptcha._publicKey &&
            !this.$el.find("input[name='recaptcha_token_response']").length
        ) {
            console.log("appending input element");
            ev.preventDefault();

            this._recaptcha.getToken(this.tokenName).then((tokenCaptcha) => {
                this.$el.append(
                    `<input name="recaptcha_token_response" type="hidden" value="${tokenCaptcha.token}"/>`
                );
                this.$el.submit();
            });
        } else {
            console.log("no publickey, or element already exists?");
        }
    },
};

publicWidget.registry.WebsiteSaleAddressFormCaptcha = publicWidget.Widget.extend({
    ...CaptchaFunctionality,
    selector: ".checkout_autoformat",
    tokenName: "website_sale_address_form",
});
