/** @odoo-module **/
import {ReCaptcha} from "@google_recaptcha/js/recaptcha";
import publicWidget from "@web/legacy/js/public/public_widget";

const CaptchaFunctionality = {
    events: {
        submit: "_onSubmit",
    },

    init() {
        this._super(...arguments);
        this._recaptcha = new ReCaptcha();
    },

    async willStart() {
        return this._recaptcha.loadLibs();
    },

    _onSubmit(ev) {
        if (
            this._recaptcha._publicKey &&
            !this.$el.find("input[name='recaptcha_token_response']").length
        ) {
            ev.preventDefault();

            this._recaptcha.getToken(this.tokenName).then((tokenCaptcha) => {
                this.$el.append(
                    `<input name="recaptcha_token_response" type="hidden" value="${tokenCaptcha.token}"/>`
                );
                this.$el.submit();
            });
        }
    },
};

publicWidget.registry.WebsiteSaleAddressFormCaptcha = publicWidget.Widget.extend({
    ...CaptchaFunctionality,
    selector: ".checkout_autoformat",
    tokenName: "website_sale_address_form",
});
