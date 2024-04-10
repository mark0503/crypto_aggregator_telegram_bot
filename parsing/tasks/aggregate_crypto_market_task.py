from parsing.models import TradingPlace, Bank, OrderType, Order, OrderOffer, CryptoCurrency
from crypto_aggregator_telegram_bot.celery import app


class AggregateCryptoMarket(app.Task):

    def import_data(self, place: TradingPlace, bank: Bank, currency: CryptoCurrency):
        from parsing.parsers import get_place_api_by_site_name
        parser = get_place_api_by_site_name(place.name)()
        for tr_type in (OrderType.SELL, OrderType.BUY):
            bank_name = parser.get_bank_name_for_provider(bank_name=bank.name)
            currency_name = parser.get_currency_name_for_provider(currency_name=currency.name)
            for order in parser.get_orders_on_place(currency_name, bank_name, tr_type):
                updated_values = {
                    'amount': order.amount,
                    'price': order.price,
                    'limit_start': order.limit_start,
                    'limit_end': order.limit_end,
                    'order_url': order.order_url
                }
                obj, _ = Order.objects.update_or_create(
                    trading_place=place,
                    bank=bank,
                    crypto_currency=currency,
                    order_type=tr_type.value,
                    title_order=order.title_order,
                    ex_id=order.ex_id,
                    defaults=updated_values,
                )
                OrderOffer.objects.create(
                    price=order.price,
                    order=obj,
                )
