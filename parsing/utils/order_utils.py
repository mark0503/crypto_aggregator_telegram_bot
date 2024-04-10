from collections import namedtuple
from typing import List, Union

from parsing.models import TradingPlace, CryptoCurrency, OrderType, Bank, Order

OrderInfo = namedtuple(
    'OrderInfo',
    [
        'title',
        'ex_id',
        'amount',
        'price',
        'limit_start',
        'limit_end'
    ]
)


def get_trading_place_from_name(place_name: str) -> TradingPlace:
    return TradingPlace.objects.get(name=place_name)


def get_crypto_currency_from_name(crypto_currency: Union[str, None]) -> Union[CryptoCurrency, None]:
    if crypto_currency is None:
        return None
    return CryptoCurrency.objects.get(name=crypto_currency)


def get_bank_from_name(bank_name: Union[str, None]) -> Union[Bank, None]:
    if bank_name is None:
        return None
    return Bank.objects.get(name=bank_name)


def get_order(
        trading_place: TradingPlace,
        crypto_currency: CryptoCurrency = None,
        order_type: int = None,
        bank: Bank = None,
        limit=10,
        offset=0,
) -> List[Order]:
    orders = Order.objects.filter(
        trading_place=trading_place
    ).select_related('bank', 'crypto_currency', 'cash_currency')
    if crypto_currency:
        orders = orders.filter(
            crypto_currency=crypto_currency
        )
    if order_type:
        if order_type == 'BUY':

            orders = orders.filter(order_type=0)
        else:
            orders = orders.filter(order_type=1)
    if bank:
        orders = orders.filter(bank=bank)
    return orders[offset:offset + limit]
