# Generated by Django 5.0.4 on 2024-04-09 14:02

import django.db.models.deletion
import parsing.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of bank', max_length=64)),
                ('short_name', models.CharField(help_text='Short name of bank', max_length=64)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active flag')),
                ('url', models.URLField(help_text='Bank site URL')),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
                'db_table': 'sc_bank',
            },
        ),
        migrations.CreateModel(
            name='CashCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of cash currency', max_length=64)),
                ('short_name', models.CharField(help_text='Short name of cash currency', max_length=32)),
                ('is_active', models.BooleanField(default=True, help_text='Is active flag')),
            ],
            options={
                'verbose_name': 'Cash currency',
                'verbose_name_plural': 'Cash Currencies',
                'db_table': 'sc_cash_currency',
            },
        ),
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of crypto currency', max_length=64)),
                ('short_name', models.CharField(help_text='Short name of crypto currency', max_length=32)),
                ('is_active', models.BooleanField(default=True, help_text='Is active flag')),
            ],
            options={
                'verbose_name': 'Crypto currency',
                'verbose_name_plural': 'Crypto Currencies',
                'db_table': 'sc_crypto_currency',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='Time when order was added')),
                ('date_updated', models.DateTimeField(auto_now_add=True, help_text='Time when order was updated')),
                ('ex_id', models.CharField(blank=True, null=True, verbose_name='Ex id from trading place')),
                ('title_order', models.CharField(blank=True, null=True, verbose_name='Title order on place')),
                ('order_url', models.URLField(help_text='Order URL')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Current amount for order', max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, help_text='Current price for order', max_digits=20)),
                ('order_type', models.SmallIntegerField(choices=[(0, 'BUY'), (1, 'SELL')], help_text='Order Type')),
                ('limit_end', models.DecimalField(decimal_places=2, help_text='Minimum Limit for order', max_digits=20)),
                ('limit_start', models.DecimalField(decimal_places=2, help_text='Maximum Limit for order', max_digits=20)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'sc_order',
            },
        ),
        migrations.CreateModel(
            name='OrderOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, help_text='Current order offer price', max_digits=10)),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='Time when order offer was added')),
                ('is_current', models.BooleanField(default=True, help_text='Is order offer current')),
            ],
            options={
                'db_table': 'sc_crypto_offer',
            },
        ),
        migrations.CreateModel(
            name='TradingPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of trading place', max_length=64)),
                ('short_name', models.CharField(help_text='Short name of trading place', max_length=32)),
                ('is_active', models.BooleanField(default=True, help_text='Is active flag')),
                ('url', models.URLField(help_text='Trading place site URL')),
            ],
            options={
                'verbose_name': 'Trading Place',
                'verbose_name_plural': 'Trading Places',
                'db_table': 'sc_trading_place',
            },
        ),
        migrations.AddConstraint(
            model_name='bank',
            constraint=models.UniqueConstraint(fields=('name', 'url'), name='unique_bank'),
        ),
        migrations.AddConstraint(
            model_name='cashcurrency',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_cash_currency'),
        ),
        migrations.AddConstraint(
            model_name='cryptocurrency',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_crypto_currency'),
        ),
        migrations.AddField(
            model_name='order',
            name='bank',
            field=models.ForeignKey(help_text='Reference to bank', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='parsing.bank'),
        ),
        migrations.AddField(
            model_name='order',
            name='cash_currency',
            field=models.ForeignKey(default=parsing.models.get_default_cash_currency, help_text='Reference to cash currency', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='parsing.cashcurrency'),
        ),
        migrations.AddField(
            model_name='order',
            name='crypto_currency',
            field=models.ForeignKey(help_text='Reference to crypto currency', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='parsing.cryptocurrency'),
        ),
        migrations.AddField(
            model_name='orderoffer',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_offers', to='parsing.order'),
        ),
        migrations.AddConstraint(
            model_name='tradingplace',
            constraint=models.UniqueConstraint(fields=('name', 'url'), name='unique_trading_place'),
        ),
        migrations.AddField(
            model_name='order',
            name='trading_place',
            field=models.ForeignKey(help_text='Reference to trading place', on_delete=django.db.models.deletion.CASCADE, to='parsing.tradingplace'),
        ),
    ]
