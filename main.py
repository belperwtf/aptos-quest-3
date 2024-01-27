import threading
import asyncio
from loguru import logger
from aptos_sdk.account import Account
from src.services.transaction import TransactionService
from src.services.mercato import Mercato
from src.services.wapal import Wapal
from src.services.twitter import Twitter

from config import ACCOUNTS, MERCATO_COLLECTION_ID

async def process_account(pk, idx):
    logger.info(f"Account {idx} started execution")
    proxy = ""
    auth_token = ""

    account = Account.load_key(pk)
    merkato = Mercato(account, MERCATO_COLLECTION_ID)
    wapal = Wapal(account)
    twitter = Twitter(auth_token, proxy)

    wapal.mint()

    await twitter.start()
    await twitter.follow('BlueMove_OA')
    await twitter.follow('wapal_official')
    await twitter.follow('TopazMarket')
    await twitter.follow('Mercato_xyz')

    merkato.mint()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run_async(account, index):
    new_loop = asyncio.new_event_loop()
    asyncio.run(process_account(account, index))


if __name__ == '__main__':
    threads = []
    for index, account in enumerate(ACCOUNTS):
        thread = threading.Thread(target=run_async, args=(account, index + 1))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()