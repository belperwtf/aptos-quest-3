import json
import ua_generator
import aiohttp
from aiohttp_socks import ProxyConnector

from loguru import logger

from src.utils.async_retry import async_retry

def generate_user_agent(device='desktop', browser='chrome'):
    try:
        ua = ua_generator.generate(device=device, browser=browser)
        user_agent = ua.text
        sec_ch_ua = f'"{ua.ch.brands[2:]}"'
        sec_ch_ua_platform = f'"{ua.platform.title()}"'

        return user_agent, sec_ch_ua, sec_ch_ua_platform
    except Exception as e:
        logger.error(e)
        raise

def get_headers():
    user_agent, sec_ch_ua, sec_ch_ua_platform = generate_user_agent()

    return {
        'accept': '*/*',
        'accept-language': 'en;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'origin': 'https://mobile.twitter.com',
        'referer': 'https://mobile.twitter.com/',
        'sec-ch-ua': sec_ch_ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': sec_ch_ua_platform,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'en',
        'x-csrf-token': '',
        'user-agent': user_agent,
    }

class Twitter:
    def __init__(self, auth_token, proxy):
        self.cookies = {'auth_token': auth_token, 'ct0': ''}
        self.headers = get_headers()
        self.proxy = proxy
        self.proxy = None if self.proxy is None else f"http://{self.proxy}"


    @async_retry
    async def request(self, method, url, acceptable_statuses=None, resp_handler=None, with_text=False, **kwargs):
        headers = self.headers.copy()
        cookies = self.cookies.copy()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        if 'cookies' in kwargs:
            cookies.update(kwargs.pop('cookies'))
        async with aiohttp.ClientSession(connector=self.get_conn(), headers=headers, cookies=cookies) as sess:
            if method.lower() == 'get':
                async with sess.get(url, **kwargs) as resp:
                    self.set_cookies(resp.cookies)
                    return await handle_response(resp, acceptable_statuses, resp_handler, with_text)
            elif method.lower() == 'post':
                async with sess.post(url, **kwargs) as resp:
                    self.set_cookies(resp.cookies)
                    return await handle_response(resp, acceptable_statuses, resp_handler, with_text)
            else:
                raise Exception('Wrong request method')

    async def follow(self, username):
        user_id = await self.get_user_id(username)
        url = 'https://twitter.com/i/api/1.1/friendships/create.json'
        params = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'user_id': user_id,
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        try:
            await self.request('POST', url, params=params, headers=headers, resp_handler=lambda r: r['id'])
            logger.success(f"{username} has been added to followers")
        except Exception as e:
            raise Exception(f'Follow error: {str(e)}')

    async def get_user_id(self, username):
        url = 'https://twitter.com/i/api/graphql/9zwVLJ48lmVUk8u_Gh9DmA/ProfileSpotlightsQuery'
        if username[0] == '@':
            username = username[1:]
        username = username.lower()
        params = {
            'variables': json.dumps({"screen_name": username}, separators=(',', ':'), ensure_ascii=True)
        }
        try:
            return await self.request("GET", url, params=params, resp_handler=lambda r: int(r['data']['user_result_by_screen_name']['result']['rest_id']))
        except Exception as e:
            raise Exception(f'Get user id error: {str(e)}')

    def set_cookies(self, resp_cookies):
        self.cookies.update({name: value.value for name, value in resp_cookies.items()})

    async def start(self):
        ct0 = await self._get_ct0()
        self.cookies.update({'ct0': ct0})
        self.headers.update({'x-csrf-token': ct0})

    async def _get_ct0(self):
        try:
            async with aiohttp.ClientSession(connector=self.get_conn(),
                                             headers=self.headers, cookies=self.cookies) as sess:
                async with sess.get('https://twitter.com/i/api/1.1/dm/user_updates.json', **{}) as resp:
                    new_csrf = resp.cookies.get("ct0")
                    if new_csrf is None:
                        raise Exception('Empty new csrf')
                    new_csrf = new_csrf.value
                    return new_csrf
        except Exception as e:
            raise Exception(f'Failed get ct0: {str(e)}')

    def get_conn(self):
        return ProxyConnector.from_url(self.proxy) if self.proxy else None

async def handle_response(resp_raw, acceptable_statuses=None, resp_handler=None, with_text=False):
    if acceptable_statuses and len(acceptable_statuses) > 0:
        if resp_raw.status not in acceptable_statuses:
            raise Exception(f'Bad status code [{resp_raw.status}]: Response = {await resp_raw.text()}')
    try:
        if resp_handler is not None:
            if with_text:
                return resp_handler(await resp_raw.text())
            else:
                return resp_handler(await resp_raw.json())
        return
    except Exception as e:
        raise Exception(f'{str(e)}: Status = {resp_raw.status}. Response = {await resp_raw.text()}')

