import json
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from backend.modules.login_services import LoginService
from backend.utils.logger import LOGGER


class FiinxRequestUtils:
    @classmethod
    def get(cls, url, headers, params):
        # LOGGER.debug(url + json.dumps(params))
        proxies = {
            "http": None,
            "https": None
        }
        session = requests.Session()
        retry = Retry(total=3, connect=3, backoff_factor=10)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers.update(**LoginService.get_header_only_token())
        res = session.get(url, headers=headers, params=params, timeout=300, verify=False, proxies=proxies)
        if int(res.status_code / 100) != 2:
            time.sleep(1)
            headers.update(**LoginService.get_header_only_token())
            res = session.get(url, headers=headers, params=params, timeout=300, verify=False, proxies=proxies)
        return res

    @classmethod
    def post(cls, url, headers, params, payload):
        # LOGGER.debug(url + json.dumps(params) + json.dumps(payload))
        proxies = {
            "http": None,
            "https": None
        }
        session = requests.Session()
        retry = Retry(total=3, connect=3, backoff_factor=10)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers.update(**LoginService.get_header_only_token())
        res = session.post(url, headers=headers, params=params, data=payload, timeout=300, verify=False, proxies=proxies)
        if int(res.status_code / 100) != 2:
            time.sleep(1)
            headers.update(**LoginService.get_header_only_token())
            res = session.post(url, headers=headers, params=params, data=payload, timeout=300, verify=False, proxies=proxies)
        return res
