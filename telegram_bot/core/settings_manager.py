import json
from dataclasses import dataclass
from typing import Union

from parsing.models import OrderType
from telegram_bot.models import TelegramUser
from crypto_aggregator_telegram_bot.redis import r as redis_client


@dataclass
class UserData:
    current_place: Union[str, None]
    current_crypto_currency: Union[str, None]
    current_bank: Union[str, None]
    order_type: Union[OrderType, None]


class SettingsManager:
    def __init__(self, user: TelegramUser):
        self.user = user

    def set_place_for_user(self, place_name: str):
        old_data = redis_client.get(self.user.telegram_id)
        if not old_data:
            user_data = {
                'current_place': place_name,
                'current_crypto_currency': None,
                'current_bank': None,
                'order_type': None,
            }
        else:
            user_data = json.loads(old_data)
            user_data['current_place'] = place_name
        redis_client.set(self.user.telegram_id, json.dumps(user_data))

    def set_crypto_currency_for_user(self, crypto_currency: str):
        old_data = redis_client.get(self.user.telegram_id)
        if not old_data:
            user_data = {
                'current_place': None,
                'current_crypto_currency': crypto_currency,
                'current_bank': None,
                'order_type': None,
            }
        else:
            user_data = json.loads(old_data)
            user_data['current_crypto_currency'] = crypto_currency
        redis_client.set(self.user.telegram_id, json.dumps(user_data))

    def set_bank_for_user(self, current_bank: str):
        old_data = redis_client.get(self.user.telegram_id)
        if not old_data:
            user_data = {
                'current_place': None,
                'current_crypto_currency': None,
                'current_bank': current_bank,
                'order_type': None,
            }
        else:
            user_data = json.loads(old_data)
            user_data['current_bank'] = current_bank
        redis_client.set(self.user.telegram_id, json.dumps(user_data))

    def set_order_type_for_user(self, order_type: OrderType):
        old_data = redis_client.get(self.user.telegram_id)
        if not old_data:
            user_data = {
                'current_place': None,
                'current_crypto_currency': None,
                'current_bank': None,
                'order_type': order_type.name,
            }
        else:
            user_data = json.loads(old_data)
            user_data['order_type'] = order_type.name
        redis_client.set(self.user.telegram_id, json.dumps(user_data))

    def get_current_setting(self) -> UserData:
        data = redis_client.get(self.user.telegram_id)
        if data:
            user_data = json.loads(data)
            return UserData(
                current_place=user_data.get('current_place'),
                current_crypto_currency=user_data.get('current_crypto_currency'),
                current_bank=user_data.get('current_bank'),
                order_type=user_data.get('order_type'),
            )
        else:
            return UserData(
                current_place=None,
                current_crypto_currency=None,
                current_bank=None,
                order_type=None,
            )

    def reset_current_setting(self):
        data = redis_client.get(self.user.telegram_id)
        if data:
            user_data = {
                'current_place': None,
                'current_crypto_currency': None,
                'current_bank': None,
                'order_type': None,
            }
            redis_client.set(self.user.telegram_id, json.dumps(user_data))
