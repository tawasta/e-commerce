import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


def _current_order_id():
    """
    Palauttaa nykyisen ostoskorin (sale.order) id:n, jos se on olemassa.
    Muuten palauttaa None.
    """
    order = request.website.sale_get_order()
    return order.id if order else None


def _is_200_ok(response):
    """
    Palauttaa True jos annetun response-olion status on 200 OK.
    Käytetään erottamaan, onko sivu oikeasti renderöity (200)
    vai oliko kyseessä esim. redirect (303, 302).
    """
    code = getattr(response, "status_code", None)
    if code is None:
        status_text = getattr(response, "status", "")
        try:
            code = int(str(status_text).split(" ", 1)[0])
        except Exception:
            code = None
    return code == 200


class MyWebsiteSale(WebsiteSale):
    def _require_checkout_done(self):
        """
        Apumetodi: tarkistaa onko checkout 'valmis' käyttäjän istunnossa.
        - checkout_done = True
        - checkout_done_so = nykyisen SO:n id
        Jos ehto ei täyty, ohjaa aina takaisin /shop/checkout.
        """
        so_id = _current_order_id()
        ok = (
            request.session.get("checkout_done") is True
            and request.session.get("checkout_done_so") == so_id
        )
        if not ok:
            return request.redirect("/shop/checkout")
        return None

    @http.route()
    def checkout(self, **post):
        """
        Ylikirjoitettu checkout-näkymä.
        - Kutsuu ensin Odoon oletustoiminnon.
        - Jos pyyntö on GET (ei xhr) JA näkymä oikeasti renderöityy (200 OK),
          asetetaan checkout_done-lippu sessioon ja sidotaan se nykyiseen SO:hon.
        """
        response = super().checkout(**post)

        is_get = request.httprequest.method == "GET"
        is_xhr = bool(post.get("xhr"))

        if is_get and not is_xhr and _is_200_ok(response):
            so_id = _current_order_id()
            if so_id:
                request.session["checkout_done"] = True
                request.session["checkout_done_so"] = so_id

        return response

    @http.route()
    def address(self, **post):
        is_post = request.httprequest.method == "POST"

        if is_post:
            post = dict(post)
            post.setdefault("callback", "/shop/checkout")

        response = super().address(**post)

        return response

    @http.route()
    def confirm_order(self, **post):
        """
        Ylikirjoitettu tilausvahvistus.
        - Ennen kuin käyttäjä saa vahvistaa tilauksen,
          tarkistetaan _require_checkout_done().
        """
        guard = self._require_checkout_done()
        if guard:
            return guard
        return super().confirm_order(**post)

    @http.route()
    def shop_payment(self, **post):
        """
        Ylikirjoitettu maksunäkymä.
        - Ennen maksuvaihetta tarkistetaan, että checkout_done on asetettu.
        """
        guard = self._require_checkout_done()
        if guard:
            return guard

        return super().shop_payment(**post)

    @http.route()
    def shop_payment_confirmation(self, **post):
        """
        Ylikirjoitettu maksun vahvistus.
        - Kutsuu Odoon oletustoiminnon.
        - Lopuksi poistaa checkout_done-liput sessiosta,
          jotta ne eivät jää roikkumaan seuraavaan ostoskertaan.
        """
        response = super().shop_payment_confirmation(**post)

        if request.session.get("checkout_done"):
            request.session.pop("checkout_done", None)
            request.session.pop("checkout_done_so", None)

        return response
