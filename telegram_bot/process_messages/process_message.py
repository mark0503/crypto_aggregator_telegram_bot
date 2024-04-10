from typing import Union

from parsing.models import OrderType
from parsing.utils.order_utils import get_order, get_trading_place_from_name, get_bank_from_name, \
    get_crypto_currency_from_name
from telegram_bot.core.bot import TelegramBot
from telegram_bot.core.keyboard import get_keyboard_with_current_settings, get_keyboard_for_reset_settings, \
    get_keyboard_for_set_place, get_keyboard_for_set_crypro_currency, get_keyboard_for_set_bank, \
    get_keyboard_for_set_order_type
from telegram_bot.core.settings_manager import SettingsManager
from telegram_bot.process_messages.utils import UserMessage, get_current_settings_user_text, get_result_order_text


class ProcessMessage:
    def __init__(self, message_data: UserMessage, callback_query_data: str = None):
        self.message_data: UserMessage = message_data
        self.callback_query_data: Union[str, None] = callback_query_data
        self.bot = TelegramBot()
        self.setting_manager = SettingsManager(user=self.message_data.message_user)

    def process_message(self):
        user_data = self.setting_manager.get_current_setting()
        if not user_data.current_place:
            add_result = False
        else:
            add_result = True
        if self.message_data.message_text == '/set_place' or self.message_data.message_text == '/start':
            self.send_message_for_set_place()
        if self.message_data.message_text == '/set_crypto_currency' or self.message_data.message_text == '/start':
            self.send_message_for_crypro_currency()
        if self.message_data.message_text == '/set_bank' or self.message_data.message_text == '/start':
            self.send_message_for_bank()
        if self.message_data.message_text == '/set_order_type' or self.message_data.message_text == '/start':
            self.send_message_for_order_type()
        if self.message_data.message_text == '/get_current_settings':
            self.send_message_with_current_settings(add_result=add_result)
        if self.message_data.message_text == '/reset_settings':
            self.setting_manager.reset_current_setting()
            self.send_message_with_current_settings(reset_available=False, add_result=False)
            self.send_message_for_set_place()
            self.send_message_for_crypro_currency()
            self.send_message_for_bank()
            self.send_message_for_order_type()
        self.bot.delete_message(
            message_ids=[self.message_data.message_id],
            chat_id=self.message_data.chat_id
        )

    def send_message_for_set_place(self):
        self.bot.send_message(
            chat_id=self.message_data.chat_id,
            text='Select a crypto exchange',
            reply_markup=get_keyboard_for_set_place()
        )

    def send_message_for_crypro_currency(self):
        self.bot.send_message(
            chat_id=self.message_data.chat_id,
            text='Select a crypto exchange',
            reply_markup=get_keyboard_for_set_crypro_currency()
        )

    def send_message_for_bank(self):
        self.bot.send_message(
            chat_id=self.message_data.chat_id,
            text='Select a crypto exchange',
            reply_markup=get_keyboard_for_set_bank()
        )

    def send_message_for_order_type(self):
        self.bot.send_message(
            chat_id=self.message_data.chat_id,
            text='Select a order type',
            reply_markup=get_keyboard_for_set_order_type()
        )

    def send_message_with_current_settings(self, add_result: bool, reset_available: bool = True):
        user_data = self.setting_manager.get_current_setting()
        current_settings_text = get_current_settings_user_text(
            user_data=user_data
        )
        self.bot.send_message(
            chat_id=self.message_data.chat_id,
            text=current_settings_text,
            reply_markup=get_keyboard_for_reset_settings(add_result=add_result) if reset_available else None
        )

    def send_message_with_result_order(self):
        user_data = self.setting_manager.get_current_setting()
        if not user_data.current_place:
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text='Select a crypto exchange',
                reply_markup=get_keyboard_for_set_crypro_currency()
            )
        else:
            orders = get_order(
                trading_place=get_trading_place_from_name(user_data.current_place),
                bank=get_bank_from_name(user_data.current_bank),
                crypto_currency=get_crypto_currency_from_name(user_data.current_crypto_currency),
                order_type=user_data.order_type,
            )
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text=get_result_order_text(orders=orders),
                reply_markup=get_keyboard_with_current_settings(add_result=False)
            )

    def process_callback_query(self):
        user_data = self.setting_manager.get_current_setting()
        if not user_data.current_place:
            add_result = False
        else:
            add_result = True
        if self.callback_query_data.startswith('set_place'):
            place_name = self.callback_query_data.split('_')[2]
            self.setting_manager.set_place_for_user(place_name=place_name)
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text='Current crypto exchange place is set to {}'.format(place_name),
                reply_markup=get_keyboard_with_current_settings(add_result=True)
            )
        elif self.callback_query_data.startswith('set_crypto_currency'):
            crypto_currency = self.callback_query_data.split('_')[3]
            self.setting_manager.set_crypto_currency_for_user(crypto_currency=crypto_currency)
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text='Current crypto_currency is set to {}'.format(crypto_currency),
                reply_markup=get_keyboard_with_current_settings(add_result=add_result)
            )
        elif self.callback_query_data.startswith('set_bank'):
            bank_name = self.callback_query_data.split('_')[2]
            self.setting_manager.set_bank_for_user(current_bank=bank_name)
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text='Current bank is set to {}'.format(bank_name),
                reply_markup=get_keyboard_with_current_settings(add_result=add_result)
            )
        elif self.callback_query_data.startswith('set_order_type'):
            order_type = self.callback_query_data.split('_')[3]
            if order_type == 'BUY':
                self.setting_manager.set_order_type_for_user(order_type=OrderType.BUY)
            else:
                self.setting_manager.set_order_type_for_user(order_type=OrderType.SELL)
            self.bot.send_message(
                chat_id=self.message_data.chat_id,
                text='Current order type is set to {}'.format(order_type),
                reply_markup=get_keyboard_with_current_settings(add_result=add_result)
            )
        elif self.callback_query_data == 'get_current_settings':
            self.send_message_with_current_settings(add_result=add_result)
        elif self.callback_query_data == 'reset_settings':
            self.setting_manager.reset_current_setting()
            self.send_message_with_current_settings(reset_available=False, add_result=False)
            self.send_message_for_set_place()
            self.send_message_for_crypro_currency()
            self.send_message_for_bank()
            self.send_message_for_order_type()
        elif self.callback_query_data == 'get_result':
            self.send_message_with_result_order()


