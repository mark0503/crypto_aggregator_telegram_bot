import enum
from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class Bank(models.Model):
    name = models.CharField(help_text='Name of bank', max_length=64)
    short_name = models.CharField(help_text='Short name of bank', max_length=64)
    is_active = models.BooleanField(verbose_name='Is active flag', default=True)
    url = models.URLField(help_text='Bank site URL')

    def __str__(self):
        return f'Bank: {self.name} | {self.short_name} | {self.url}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'url'], name='unique_bank')
        ]
        db_table = 'sc_bank'
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'


class TradingPlace(models.Model):
    name = models.CharField(help_text='Name of trading place', max_length=64)
    short_name = models.CharField(help_text='Short name of trading place', max_length=32)
    is_active = models.BooleanField(help_text='Is active flag', default=True)
    url = models.URLField(help_text='Trading place site URL')

    def __str__(self):
        return f'Trading place: {self.name} | {self.short_name} | {self.url}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'url'], name='unique_trading_place')
        ]
        db_table = 'sc_trading_place'
        verbose_name = 'Trading Place'
        verbose_name_plural = 'Trading Places'


class CryptoCurrency(models.Model):
    name = models.CharField(help_text='Name of crypto currency', max_length=64)
    short_name = models.CharField(help_text='Short name of crypto currency', max_length=32)
    is_active = models.BooleanField(help_text='Is active flag', default=True)

    def __str__(self):
        return f'Crypto currency: {self.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_crypto_currency')
        ]
        db_table = 'sc_crypto_currency'
        verbose_name = 'Crypto currency'
        verbose_name_plural = 'Crypto Currencies'


class CashCurrency(models.Model):
    name = models.CharField(help_text='Name of cash currency', max_length=64)
    short_name = models.CharField(help_text='Short name of cash currency', max_length=32)
    is_active = models.BooleanField(help_text='Is active flag', default=True)

    def __str__(self):
        return f'Cash currency: {self.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_cash_currency')
        ]
        db_table = 'sc_cash_currency'
        verbose_name = 'Cash currency'
        verbose_name_plural = 'Cash Currencies'


class OrderType(enum.Enum):
    BUY = 0
    SELL = 1


def get_default_cash_currency():
    return CashCurrency.objects.get_or_create(name='Rubles', short_name='RUR')[0].id


class Order(models.Model):
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        help_text='Reference to bank',
        related_name='orders'
    )
    crypto_currency = models.ForeignKey(
        CryptoCurrency,
        on_delete=models.CASCADE,
        help_text='Reference to crypto currency',
        related_name='orders'
    )
    cash_currency = models.ForeignKey(
        CashCurrency,
        default=get_default_cash_currency,
        on_delete=models.CASCADE,
        help_text='Reference to cash currency',
        related_name='orders'
    )
    trading_place = models.ForeignKey(
        TradingPlace,
        on_delete=models.CASCADE,
        help_text='Reference to trading place',
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text='Time when order was added'
    )
    date_updated = models.DateTimeField(
        auto_now_add=True,
        help_text='Time when order was updated'
    )
    ex_id = models.CharField(
        verbose_name='Ex id from trading place',
        blank=True,
        null=True
    )
    title_order = models.CharField(
        verbose_name='Title order on place',
        blank=True,
        null=True
    )
    order_url = models.URLField(help_text='Order URL')
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text='Current amount for order'
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text='Current price for order'
    )
    order_type = models.SmallIntegerField(
        choices=[(choice.value, choice.name) for choice in OrderType],
        help_text='Order Type'
    )
    limit_end = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text='Minimum Limit for order'
    )
    limit_start = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        help_text='Maximum Limit for order'
    )

    def __str__(self):
        return (f'Order on {self.order_type}. Bank: {self.bank.name}. CryptoCurrency: {self.crypto_currency.name}. '
                f'Price: {self.price}. Amount: {self.amount}')

    class Meta:
        db_table = 'sc_order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderOffer(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Current order offer price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_offers')
    created_time = models.DateTimeField(
        auto_now_add=True, help_text='Time when order offer was added'
    )
    is_current = models.BooleanField(default=True, help_text='Is order offer current')

    def save(self, *args, **kwargs):
        if self.is_current:
            self.order.order_offers.filter(
                created_time__lt=now() - timedelta(hours=1),
                is_current=True,
            ).exclude(id=self.id).update(is_current=False)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'sc_crypto_offer'
