from dataclasses import dataclass
from typing import Union, List

from parsing.models import CryptoCurrency, Bank, TradingPlace, OrderType


@dataclass
class InlineKeyboard:
    text: str
    callback_data: str


@dataclass
class KeyBoard:
    inline_keyboard: List[List[Union[None, InlineKeyboard]]]


def get_keyboard_for_reset_settings(add_result) -> KeyBoard:
    keyboard = KeyBoard(
        inline_keyboard=[
            [
                InlineKeyboard(
                    text='Reset Setting',
                    callback_data='reset_settings'
                )
            ]
        ]
    )
    if add_result:
        keyboard.inline_keyboard.append(
            [InlineKeyboard(
                text='Get Result Offer',
                callback_data='get_result'
            )]
        )
    return keyboard


def get_keyboard_with_current_settings(add_result=True) -> KeyBoard:
    keyboard = KeyBoard(
        inline_keyboard=[
            [
                InlineKeyboard(
                    text='Current Setting',
                    callback_data='get_current_settings'
                )
            ]
        ]
    )
    if add_result:
        keyboard.inline_keyboard.append(
            [InlineKeyboard(
                text='Get Result Offer',
                callback_data='get_result'
            )]
        )
    return keyboard


def get_keyboard_for_set_place() -> KeyBoard:
    result = []
    places = TradingPlace.objects.filter(is_active=True).values_list('name', flat=True)
    for place in places:
        result.append([InlineKeyboard(
            text=place,
            callback_data=f'set_place_{place}'
        )])
    return KeyBoard(inline_keyboard=result)


def get_keyboard_for_set_order_type() -> KeyBoard:
    result = []
    for tp in [OrderType.BUY, OrderType.SELL]:
        result.append([InlineKeyboard(
            text=tp.name,
            callback_data=f'set_order_type_{tp.name}'
        )])
    return KeyBoard(inline_keyboard=result)


def get_keyboard_for_set_crypro_currency() -> KeyBoard:
    result = []
    crypto_currencies = CryptoCurrency.objects.filter(is_active=True).values_list('name', flat=True)
    for crypto_currency in crypto_currencies:
        result.append([InlineKeyboard(
            text=crypto_currency,
            callback_data=f'set_crypto_currency_{crypto_currency}'
        )])
    return KeyBoard(inline_keyboard=result)


def get_keyboard_for_set_bank() -> KeyBoard:
    result = []
    banks = Bank.objects.filter(is_active=True).values_list('name', flat=True)
    for bank in banks:
        result.append([InlineKeyboard(
            text=bank,
            callback_data=f'set_bank_{bank}'
        )])
    return KeyBoard(inline_keyboard=result)


def get_keyboard_for_get_result() -> KeyBoard:
    result = [[InlineKeyboard(
        text='Get Result Offer',
        callback_data='get_result'
    )]]
    return KeyBoard(inline_keyboard=result)
