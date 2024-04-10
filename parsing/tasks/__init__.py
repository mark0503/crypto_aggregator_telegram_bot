from parsing.models import TradingPlace, Bank, CryptoCurrency
from parsing.tasks.aggregate_crypto_market_task import AggregateCryptoMarket
from crypto_aggregator_telegram_bot.celery import app


@app.task(base=AggregateCryptoMarket, bind=True, queue='crypto_aggregator')
def periodical_aggregate_place_task(self, place_id: int, bank_id: int, crypto_currency_id: int):
    place = TradingPlace.objects.get(id=place_id)
    bank = Bank.objects.get(id=bank_id)
    currency = CryptoCurrency.objects.get(id=crypto_currency_id)
    self.import_data(place=place, bank=bank, currency=currency)


@app.task(queue='crypto_aggregator')
def check_info_on_supplier():
    places = TradingPlace.objects.filter(is_active=True)
    banks = Bank.objects.filter(is_active=True)
    crypto_currencies = CryptoCurrency.objects.filter(is_active=True)
    for place in places:
        for bank in banks:
            for cur in crypto_currencies:
                periodical_aggregate_place_task.delay(place_id=place.id, bank_id=bank.id, crypto_currency_id=cur.id,)
