import sys
import httpx
import random
import string
import asyncio
from loguru import logger
from web3 import AsyncWeb3
from datetime import datetime, timedelta
from eth_account.messages import encode_defunct

w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://rpc.ankr.com/eth'))

class Galxe:
    def __init__(self, auth_token, pk):
        self.account = w3.eth.account.from_key(pk)
        self.http = httpx.AsyncClient(verify=False, timeout=50)
        self.http.cookies.update({'auth_token': auth_token})

    async def bind_twitter(self):
        try:
            json_data = {
                "operationName": "BasicUserInfo",
                "variables": {"address": self.account.address},
                "query": "query BasicUserInfo($address: String!) {\n  addressInfo(address: $address) {\n    id\n    username\n    avatar\n    address\n    evmAddressSecondary {\n      address\n      __typename\n    }\n    hasEmail\n    solanaAddress\n    aptosAddress\n    seiAddress\n    injectiveAddress\n    flowAddress\n    starknetAddress\n    bitcoinAddress\n    hasEvmAddress\n    hasSolanaAddress\n    hasAptosAddress\n    hasInjectiveAddress\n    hasFlowAddress\n    hasStarknetAddress\n    hasBitcoinAddress\n    hasTwitter\n    hasGithub\n    hasDiscord\n    hasTelegram\n    displayEmail\n    displayTwitter\n    displayGithub\n    displayDiscord\n    displayTelegram\n    displayNamePref\n    email\n    twitterUserID\n    twitterUserName\n    githubUserID\n    githubUserName\n    discordUserID\n    discordUserName\n    telegramUserID\n    telegramUserName\n    enableEmailSubs\n    subscriptions\n    isWhitelisted\n    isInvited\n    isAdmin\n    accessToken\n    __typename\n  }\n}\n"
            }

            res = await self.http.post('https://graphigo.prd.galaxy.eco/query', json=json_data)
            if res.status_code == 200 and 'addressInfo' in res.text:
                galxe_id = res.json()['data']['addressInfo']['id']
                hasTwitter = res.json()['data']['addressInfo']['hasTwitter']
                if hasTwitter:
                    logger.info(f"{self.account.address} already has a twitter profile")
                    return True
                elif galxe_id == "":
                    logger.info(f"Will create an account for {self.account.address}")
                    if await self.sign_in() and await self.create_new_account():
                        return True
                    else:
                        return False
                else:
                    logger.info(f"{self.account.address} should post a tweet")
                    if await self.sign_in() and await self.create_tweet(galxe_id):
                        return True
                    else:
                        return False
            else:
                logger.error(f"Something went wrong: {self.account.address}")
                return False
        except Exception as e:
            logger.error(f"Something went wrong: {self.account.address}")
            return False

    async def sign_in(self):
        try:
            characters = string.ascii_letters + string.digits
            nonce = ''.join(random.choice(characters) for i in range(17))
            current_time = datetime.utcnow()
            seven_days_later = current_time + timedelta(days=7)
            issued_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            expiration_time = seven_days_later.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            message = f"galxe.com wants you to sign in with your Ethereum account:\n{self.account.address}\n\nSign in with Ethereum to the app.\n\nURI: https://galxe.com\nVersion: 1\nChain ID: 1\nNonce: {nonce}\nIssued At: {issued_time}\nExpiration Time: {expiration_time}"
            signature = self.account.sign_message(encode_defunct(text=message))
            data = {
                "operationName": "SignIn",
                "variables": {
                    "input": {
                        "address": self.account.address,
                        "message": message,
                        "signature": signature.signature.hex(),
                        "addressType": "EVM"
                    }
                },
                "query": "mutation SignIn($input: Auth) {\n  signin(input: $input)\n}\n"
            }
            res = await self.http.post('https://graphigo.prd.galaxy.eco/query', json=data)
            if res.status_code == 200 and 'signin' in res.text:
                logger.success(f"{self.account.address} success login")
                signin = res.json()['data']['signin']
                self.http.headers.update({'Authorization': signin})
                return True
            else:
                logger.error(f"{self.account.address}  Login failed")
                return False
        except Exception as e:
            logger.error(f"{self.account.address} Login failed, {e}")
            return False


    async def create_tweet(self, _gid):
        try:
            res = await self.http.get('https://twitter.com/home')
            json_data = {
                "variables": {
                    "tweet_text": f"Verifying my Twitter account for my #GalxeID gid:{_gid} @Galxe \n\n galxe.com/galxeid ",
                    "dark_request": False,
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "semantic_annotation_ids": []
                },
                "features": {
                    "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True,
                    "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": False,
                    "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "responsive_web_media_download_video_enabled": False,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_enhance_cards_enabled": False
                },
                "queryId": "SoVnbfCycZ7fERGCwpZkYA"
            }
            headers = {
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'en',
                'x-csrf-token': res.cookies.get('ct0'),
                'x-twitter-auth-type': 'OAuth2Session'
            }
            res = await self.http.post('https://twitter.com/i/api/graphql/SoVnbfCycZ7fERGCwpZkYA/CreateTweet', json=json_data, headers=headers)
            if res.status_code == 200 and 'rest_id' in res.text:
                rest_id = res.json()['data']['create_tweet']['tweet_results']['result']['rest_id']
                screen_name = res.json()['data']['create_tweet']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name']
                twitter_url = f"https://twitter.com/{screen_name}/status/{rest_id}"
                logger.success(f"{self.account.address} tweet has been successfully created")
                if await self.verify_twitter_account(twitter_url):
                    return True
                else:
                    logger.success(f"{self.account.address} failed to tweet")
                    return False
            else:
                logger.success(f"{self.account.address} failed to tweet {res.json()['errors'][0]['message']}")
                return False
        except Exception as e:
            logger.error(f"{self.account.address} failed to tweet {e}")
            return False

    async def verify_twitter_account(self, _twitter_url):
        try:
            json_data = {
                "operationName": "VerifyTwitterAccount",
                "variables": {
                    "input": {
                        "address": self.account.address,
                        "tweetURL": _twitter_url
                    }
                },
                "query": "mutation VerifyTwitterAccount($input: VerifyTwitterAccountInput!) {\n  verifyTwitterAccount(input: $input) {\n    address\n    twitterUserID\n    twitterUserName\n    __typename\n  }\n}\n"
            }
            res = await self.http.post('https://graphigo.prd.galaxy.eco/query', json=json_data)
            if res.status_code == 200 and 'twitterUserName' in res.text:
                logger.success(f"[{self.account.address} binding successful")
                return True
            else:
                logger.error(f"{self.account.address} Binding failed {res.json()['errors'][0]['message']}")
                return False
        except Exception as e:
            logger.error(f"{self.account.address} Binding failed {e}")
            return False


    async def create_new_account(self):
        try:
            username = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            json_data = {
                "operationName": "CreateNewAccount",
                "variables": {
                    "input": {
                        "schema": f"EVM:{self.account.address.lower()}",
                        "socialUsername": "",
                        "username": username
                    }
                },
                "query": "mutation CreateNewAccount($input: CreateNewAccount!) {\n  createNewAccount(input: $input)\n}\n"
            }

            res = await self.http.post('https://graphigo.prd.galaxy.eco/query', json=json_data)
            if res.status_code == 200 and 'createNewAccount' in res.text:
                galxe_id = res.json()['data']['createNewAccount']
                if await self.create_tweet(galxe_id):
                    return True
                else:
                    logger.error(f"{self.account.address} account creation failed")
                    return False
            else:
                logger.error(f"{self.account.address} failed to obtain user information")
                return False
        except Exception as e:
            logger.error(f"{self.account.address} failed to obtain user information")
            return False
