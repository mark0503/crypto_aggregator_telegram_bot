from dataclasses import dataclass
from typing import Union, List

from parsing.models import Order
from parsing.utils.order_utils import OrderInfo
from telegram_bot.core.settings_manager import UserData
from telegram_bot.models import TelegramUser
from telegram_bot.utils.telegram_bot import get_telegram_user_from_db


@dataclass
class UserMessage:
    chat_id: Union[int, str]
    message_text: str
    message_user: TelegramUser
    message_id: int


def process_user_message(message: dict, from_user_dict: dict = None) -> UserMessage:
    chat_id = message['chat']['id']
    message_text = message['text']
    if from_user_dict:
        message_user = get_telegram_user_from_db(from_user_dict)
    else:
        message_user = get_telegram_user_from_db(message['from'])
    return UserMessage(
        chat_id=chat_id,
        message_text=message_text,
        message_user=message_user,
        message_id=message['message_id']
    )


def get_current_settings_user_text(user_data: UserData) -> str:
    current_crypto_currency = user_data.current_crypto_currency if user_data.current_crypto_currency else 'not set'
    current_bank = user_data.current_bank if user_data.current_bank else 'not set'
    current_place = user_data.current_place if user_data.current_place else 'not set'
    current_order_type = user_data.order_type if user_data.order_type else 'not set'
    result_text = (f'Your current settings:'
                   f'\nCrypto currency: {current_crypto_currency}'
                   f'\nCrypto bank: {current_bank}'
                   f'\nCrypto place: {current_place}'
                   f'\nCrypto order type: {current_order_type}')
    return result_text


def get_result_order_text(orders: List[Order]) -> str:
    result_text = ''
    for order in orders:
        if order.order_type == 0:
            order_type = 'BUY'
        else:
            order_type = 'SELL'
        result_text += (f'\n\nBank: {order.bank.name}. Cur.{order.crypto_currency.name}. Type: {order_type}. '
                        f'Price: {order.price}')
    return result_text
