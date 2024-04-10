import json
import os
from json import JSONDecodeError

import requests
from requests.adapters import HTTPAdapter, Retry


class BaseHttpClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.proxies = {
            'http': os.getenv('PROXY_URL'),
            'https': os.getenv('PROXY_URL'),
        }
        retry_strategy = Retry(total=5,
                               backoff_factor=0.1,
                               status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount(prefix="https://", adapter=adapter)

    def do_request(self, url: str, data=None, params=None, json_load=False, **kwargs):
        method = kwargs.pop('method', None) or ('POST' if data or 'json' in kwargs else 'GET')

        response = self.session.request(
            method,
            url,
            data=data,
            params=params,
            **kwargs
        ).text

        if json_load:
            try:
                response = json.loads(response)
            except JSONDecodeError:
                raise Exception(f'Error when receiving data as json.'
                                f'{url} \n'
                                f'{response}')
        return response
