## B0R9F3D9

from loguru import logger
from random import choice, randint

from aptos_sdk.account import AccountAddress
from aptos_sdk.transactions import TransactionArgument, Serializer, EntryFunction, AccountAddress

from src.clients.graphql_client import GraphQLClient
from src.clients.queries import FETCH_EDITION_LAUNCH_BY_ID
from src.clients.mappings import map_edition_launch

from src.clients.http_client import HttpClient
from src.services.transaction import TransactionService

from src.utils.strings import generate_random_string

from config import INDEXER_XYZ_API_URL, INDEXER_AUTH_PAYLOAD, MERCATO_API_URL, MERCATO_BID_CONTRACT_V2, MERCATO_BID_CONTRACT_V1, BID_NFTS, MERCATO_COLLECTION_ID

class Mercato:
    def __init__(self, account, collection_id=MERCATO_COLLECTION_ID):
        self.account = account
        self.collection_id = collection_id
        self.graphql_client = GraphQLClient(INDEXER_XYZ_API_URL)
        self.transaction_service = TransactionService(account)

    async def bid(self):
        nft_name = choice(list(BID_NFTS.keys()))
        nft_address = BID_NFTS[nft_name]
        nft_address = AccountAddress.from_str(nft_address)
        bid_amount = randint(88, 345)
        bid_quantity = 1

        args = [
            TransactionArgument(nft_address, Serializer.struct),
            TransactionArgument(bid_amount, Serializer.u64),
            TransactionArgument(bid_quantity, Serializer.u64),
        ]

        if 'V2' in nft_name:
            contract = MERCATO_BID_CONTRACT_V2
            func = 'collection_bids'
        else:
            args.insert(1, TransactionArgument(nft_name, Serializer.str))
            contract = MERCATO_BID_CONTRACT_V1
            func = 'collection_bid'

        payload = EntryFunction.natural(
            module=contract,
            function=func,
            ty_args=[],
            args=args
        )

        raw_txn = await self.transaction_service.get_raw_txn(payload)
        await self.transaction_service.send_txn(raw_txn)

    def fetch_edition_launch_by_id(self):
        response = self.graphql_client.execute_query(
            FETCH_EDITION_LAUNCH_BY_ID,
            { "id": self.collection_id },
            INDEXER_AUTH_PAYLOAD
        )

        return map_edition_launch(response)

    def emulate_click_action(self, collection_slug):
        address = self.account.address()
        anonymous_id = generate_random_string()
        event_url = f"/aptos/collection/{collection_slug}?tab=mint&mintTokenId={self.collection_id}&bottomTab=trades"

        http_client = HttpClient(MERCATO_API_URL)

        data = {
            "anonymousId": f"{anonymous_id}",
            "event": "BUTTON_CLICK",
            "properties": {
                "action" : "Clicked on action button",
                "chain": "null",
                "component": "CollectionEditionMint",
                "path": "/[chain]/collection/[slug]",
                "tab": "mint",
                "url": event_url,
                "wallet": f"{address}",
                "website": "mercato"
            },
            "userId": f"{address}",
        }
        http_client.post("/segment", json=data)

    def pre_mint(self, token_id):
        http_client = HttpClient(INDEXER_XYZ_API_URL)
        data = {
            "id": "3",
            "jsonrpc": "2.0",
            "method": "Mint",
            "params": [f"{self.account.address()}", token_id]
        }

        res = http_client.post("/aptos/launchpad", json=data)
        response = res.json()

        return response['result']['contractCallData']

    def mint(self):
        logger.info("Processing Mercato minting ...")

        edition_launch = self.fetch_edition_launch_by_id()
        self.emulate_click_action(edition_launch['collection_slug'])
        contract_data = self.pre_mint(edition_launch['token_id'])

        self.transaction_service.send_transaction({
            "type": "entry_function_payload",
            "function": contract_data['functionName'],
            "type_arguments": [],
            "arguments": list(map(str, contract_data['arguments']))
        })