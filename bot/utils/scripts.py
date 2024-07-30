import os
import glob
import time
import random
import string
import base64
import asyncio
import hashlib

import aiohttp
import aiohttp_proxy
from fake_useragent import UserAgent

from bot.config import settings
from bot.utils.logger import logger
from bot.utils.json_db import JsonDB
from bot.utils.default import DEFAULT_HEADERS, DEFAULT_FINGERPRINT


def get_session_names():
    names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('sessions/*.session')]

    return names


def generate_random_visitor_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    visitor_id = hashlib.md5(random_string.encode()).hexdigest()

    return visitor_id


def escape_html(text: str):
    return text.replace('<', '\\<').replace('>', '\\>')


def decode_cipher(cipher: str):
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')


def get_headers(name: str):
    db = JsonDB("profiles")

    profiles = db.get_data()

    headers = profiles.get(name, {}).get('headers', DEFAULT_HEADERS)

    if settings.USE_RANDOM_USERAGENT:
        android_version = random.randint(24, 33)
        webview_version = random.randint(70, 125)

        headers['Sec-Ch-Ua'] = (
            f'"Android WebView";v="{webview_version}", '
            f'"Chromium";v="{webview_version}", '
            f'"Not?A_Brand";v="{android_version}"'
        )
        headers['User-Agent'] = get_mobile_user_agent()

    return headers


def get_fingerprint(name: str):
    db = JsonDB("profiles")

    profiles = db.get_data()

    fingerprint = profiles.get(name, {}).get('fingerprint', DEFAULT_FINGERPRINT)

    fingerprint['visitorId'] = generate_random_visitor_id()

    return fingerprint


def get_mobile_user_agent():
    ua = UserAgent(platforms=['mobile'], os=['android'])
    user_agent = ua.random
    if 'wv' not in user_agent:
        parts = user_agent.split(')')
        parts[0] += '; wv'
        user_agent = ')'.join(parts)
    return user_agent


async def get_mini_game_cipher(http_client: aiohttp.ClientSession,
                               user_id: int,
                               session_name: str,
                               start_date: str,
                               game_sleep_time: int):
    if settings.USE_RANDOM_MINI_GAME_KEY:
        cipher = f"0{game_sleep_time}{random.randint(10000000000, 99999999999)}"[:10]
        body = f"{cipher}|{user_id}"

        encoded_body = base64.b64encode(body.encode()).decode()

        return encoded_body



def generate_client_id():
    timestamp = str(int(time.time() * 1000))
    random_digits = ''.join(random.choices(string.digits, k=19))

    return f"{timestamp}-{random_digits}"


def generate_event_id():
    first_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    second_part = ''.join(random.choices(string.digits, k=4))
    third_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    fourth_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    fifth_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

    return f"{first_part}-{second_part}-{third_part}-{fourth_part}-{fifth_part}"


async def get_promo_code(app_token: str,
                         promo_id: str,
                         max_attempts: int,
                         event_timeout: int,
                         session_name: str,
                         proxy: str):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.gamepromo.io"
    }

    proxy_conn = aiohttp_proxy.ProxyConnector().from_url(proxy) if proxy else None

    async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
        client_id = generate_client_id()

        json_data = {
            "appToken": app_token,
            "clientId": client_id,
            "clientOrigin": "deviceid"
        }

        response = await http_client.post(url="https://api.gamepromo.io/promo/login-client", json=json_data)

        response_text = await response.text()
        response_json = await response.json()
        access_token = response_json.get("clientToken")

        if not access_token:
            logger.debug(f"{session_name} | Can't login to api.gamepromo.io | Try with proxy | "
                         f"Response text: {escape_html(response_text)[:256]}...")
            return

        http_client.headers["Authorization"] = f"Bearer {access_token}"

        await asyncio.sleep(delay=1)

        attempts = 0

        while attempts < max_attempts:
            try:

                event_id = generate_event_id()
                json_data = {
                    "promoId": promo_id,
                    "eventId": event_id,
                    "eventOrigin": "undefined"
                }

                response = await http_client.post(url="https://api.gamepromo.io/promo/register-event", json=json_data)
                response.raise_for_status()

                response_json = await response.json()
                has_code = response_json.get("hasCode", False)

                if has_code:
                    json_data = {
                        "promoId": promo_id
                    }

                    response = await http_client.post(url="https://api.gamepromo.io/promo/create-code", json=json_data)
                    response.raise_for_status()

                    response_json = await response.json()
                    promo_code = response_json.get("promoCode")

                    if promo_code:
                        logger.info(f"{session_name} | Promo code is found: <lc>{promo_code}</lc>")
                        return promo_code
            except Exception as error:
                logger.debug(f"{session_name} | Error while getting promo code: {error}")

            attempts += 1

            logger.debug(f"{session_name} | Attempt <lr>{attempts}</lr> was unsuccessful | "
                         f"Sleep <lw>{event_timeout}s</lw> before <lr>{attempts + 1}</lr> attempt to get promo code")
            await asyncio.sleep(delay=event_timeout)

    logger.debug(f"{session_name} | Promo code not found out of <lw>{max_attempts}</lw> attempts")
