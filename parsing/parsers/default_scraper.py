from typing import Union

from parsing.models import OrderType
from crypto_aggregator_telegram_bot.utils.base_http_client import BaseHttpClient


class DefaultScraper(BaseHttpClient):
    bank_names = {}
    currency_names = {}

    order_xpaths = {}

    def get_orders_on_place(self, currency_title: str, bank_name: str, trans_type: OrderType):
        raise NotImplementedError()

    def get_bank_name_for_provider(self, bank_name: str) -> Union[None, str]:
        return self.bank_names.get(bank_name)

    def get_currency_name_for_provider(self, currency_name: str) -> Union[None, str]:
        return self.currency_names.get(currency_name)

    def get_sellers_from_selector(self, page_selector):
        sellers = page_selector.xpath(self.order_xpaths['sellers'])
        return sellers

    def get_order_title_from_selector(self, page_selector):
        order_title = page_selector.xpath(self.order_xpaths['order_title'])
        return order_title[0] if order_title else None

    def get_order_url_from_selector(self, page_selector, first=True):
        order_title = page_selector.xpath(self.order_xpaths['order_url'])
        if first:
            return order_title[0] if order_title else None
        return order_title

    def get_order_amount_from_selector(self, page_selector):
        order_amount = page_selector.xpath(self.order_xpaths['order_amount'])
        return order_amount[0] if order_amount else None

    def get_order_price_from_selector(self, page_selector):
        order_price = page_selector.xpath(self.order_xpaths['order_price'])
        return order_price[0] if order_price else None

    def get_order_limit_start_from_selector(self, page_selector):
        order_limit_start = page_selector.xpath(self.order_xpaths['limit_start'])
        return order_limit_start[0] if order_limit_start else None

    def get_order_limit_end_from_selector(self, page_selector):
        order_limit_end = page_selector.xpath(self.order_xpaths['limit_end'])
        return order_limit_end[0] if order_limit_end else None
