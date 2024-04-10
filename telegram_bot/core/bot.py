from typing import Union
from dataclasses import asdict

from crypto_aggregator_telegram_bot.utils.base_http_client import BaseHttpClient
from telegram_bot.core.keyboard import KeyBoard
from telegram_bot.utils.telegram_bot import get_base_url_for_telegram_bot


class TelegramBot(BaseHttpClient):

    def __init__(self):
        super().__init__()
        self.base_url = get_base_url_for_telegram_bot()

    def send_message(self, chat_id: Union[int, str], text: str, reply_markup: KeyBoard = None):
        url = self.base_url + 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            params['reply_markup'] = asdict(reply_markup)
        response = self.do_request(url=url, json=params, json_load=True)
        return response

    def edit_message(self, text: str, chat_id: Union[int, str] = None, message_id: int = None,
                     reply_markup: KeyBoard = None):
        url = self.base_url + 'editMessageText'
        params = {'chat_id': chat_id, 'text': text, 'message_id': message_id}
        if reply_markup:
            params['reply_markup'] = asdict(reply_markup)
        response = self.do_request(url=url, json=params, json_load=True)
        return response

    def get_updates(self):
        url = self.base_url + 'getUpdates'
        response = self.do_request(url=url, json_load=True)
        return response['result']

    def delete_message(self, chat_id: Union[int, str], message_ids: list[int]):
        url = self.base_url + 'deleteMessages'
        params = {'chat_id': chat_id, 'message_ids': message_ids}
        response = self.do_request(url=url, json_load=True, json=params)
        return response
