import threading
import asyncio
from loguru import logger
from aptos_sdk.account import Account
from aptos_sdk.async_client import ResourceNotFound
from src.services.transaction import TransactionService
from src.services.mercato import Mercato
from src.services.wapal import Wapal
from src.services.twitter import Twitter
from src.services.galxe import Galxe
from src.services.topaz import Topaz

from src.clients.aptos_client import client

from config import ACCOUNTS, PROXIES, TWITTERS, EVM

async def process_account(pk, idx):
    logger.info(f"Account {idx + 1} started execution")
    account = Account.load_key(pk)
    try:
        await client.account_balance(account.address())
    except ResourceNotFound as e:
        print(f"Address {account.address()} Account #{idx + 1} has no aptos")
        return

    proxy = PROXIES[idx] if 0 <= idx < len(PROXIES) else None
    auth_token = TWITTERS[idx]
    evm_pk = EVM[idx]

    account = Account.load_key(pk)

    merkato = Mercato(account)
    topaz = Topaz(account)
    wapal = Wapal(account)
    twitter = Twitter(auth_token, proxy)
    galxe = Galxe(auth_token, evm_pk)

    await wapal.mint()
    await merkato.bid()
    await topaz.bid()

    await galxe.bind_twitter()

    await twitter.start()
    await twitter.follow('BlueMove_OA')
    await twitter.follow('wapal_official')
    await twitter.follow('TopazMarket')
    await twitter.follow('Mercato_xyz')

async def main():
    tasks = []
    for index, account in enumerate(ACCOUNTS):
        task = process_account(account, index)
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())