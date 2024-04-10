import decimal

from lxml.html import fromstring

from parsing.models import OrderType, Order
from parsing.parsers import DefaultScraper


class BestChangeScraper(DefaultScraper):
    PLACE_NAME = 'BestChange'
    URL = 'https://www.bestchange.com/'

    bank_names = {
        'Тинькофф Банк': 'tinkoff',
        'СберБанк': 'sberbank',
        'Альфа Банк': 'alfaclick',
        'Киви': 'qiwi'
    }

    currency_names = {
        'USDT': 'tether-trc20',
        'BTC': 'bitcoin',
        'ETH': 'ethereum'
    }

    order_xpaths = {
        'sellers': '//table[@id="content_table"]/tbody/tr',
        'order_url':  'descendant::a[@rel="nofollow"]/@href',
        'order_title': 'descendant::div[@class="ca"]/text()',
        'limit_start': 'descendant::td[@class="bi"]/descendant::div[@class="fm1"]/text()',
        'limit_end': 'descendant::td[@class="bi"]/descendant::div[@class="fm2"]/text()',
        'order_price': 'descendant::td[@class="bi"]/descendant::div[@class="fs"]/text()'
    }

    def __init__(self):
        super().__init__()
        self.session.headers = {
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.bestchange.ru/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9',
        }

    def get_orders_on_place(self, currency_title: str, bank_name: str, order_type: OrderType):
        if order_type == OrderType.BUY:
            url = f'https://www.bestchange.ru/{bank_name}-to-{currency_title}.html'
        elif order_type == OrderType.SELL:
            url = f'https://www.bestchange.ru/{currency_title}-to-{bank_name}.html'
        else:
            raise ValueError(f'Unsupported trans_type: {order_type}')

        response = self.do_request(url=url)

        selector = fromstring(response)
        sellers = self.get_sellers_from_selector(selector)
        for seller in sellers:
            title_on_order = self.get_order_title_from_selector(seller)
            order_url = self.get_order_url_from_selector(seller)
            limit_start = self.get_order_limit_start_from_selector(seller)
            limit_end = self.get_order_limit_end_from_selector(seller)
            price = self.get_order_price_from_selector(seller)
            order = Order(
                title_order=title_on_order,
                order_url=order_url,
                ex_id=title_on_order.replace(' ', '_'),
                limit_start=decimal.Decimal(limit_start.replace(' ', '').replace('от', '')),
                limit_end=decimal.Decimal(limit_end.replace(' ', '').replace('до', '')),
                price=decimal.Decimal(price.replace(' ', '')),
                amount=1
            )
            yield order
