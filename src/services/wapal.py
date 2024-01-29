from aptos_sdk.transactions import TransactionArgument, Serializer, EntryFunction
from aptos_sdk.account import AccountAddress

from loguru import logger
from random import choice

from src.services.transaction import TransactionService

from config import WAPAL_MINT_CONTRACT, WAPAL_MINT_NFTS

class Wapal:
    def __init__(self, account):
        self.transaction_service = TransactionService(account)

    async def mint(self):
        nft_address = choice(WAPAL_MINT_NFTS)

        logger.info("Processing Wapal minting ...")

        payload = EntryFunction.natural(
            module=WAPAL_MINT_CONTRACT,
            function='mint_script',
            ty_args=[],
            args=[TransactionArgument(AccountAddress.from_str(nft_address), Serializer.struct)]
        )

        raw_txn = await self.transaction_service.get_raw_txn(payload)
        await self.transaction_service.send_txn(raw_txn)
        