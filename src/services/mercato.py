from loguru import logger

from src.clients.graphql_client import GraphQLClient
from src.clients.queries import FETCH_EDITION_LAUNCH_BY_ID
from src.clients.mappings import map_edition_launch

from src.clients.http_client import HttpClient
from src.services.transaction import TransactionService

from src.utils.strings import generate_random_string

from config import INDEXER_XYZ_API_URL, INDEXER_AUTH_PAYLOAD, MERCATO_API_URL

class Mercato:
    def __init__(self, account, collection_id):
        self.account = account
        self.collection_id = collection_id
        self.graphql_client = GraphQLClient(INDEXER_XYZ_API_URL)
        self.transaction_service = TransactionService(account)
        

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