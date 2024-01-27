EXPLORER_URL = "https://explorer.aptoslabs.com/txn/{transaction}?network=mainnet"
RPC_URL = "https://fullnode.mainnet.aptoslabs.com/v1"
INDEXER_XYZ_API_URL = "https://api.indexer.xyz"
MERCATO_API_URL = "https://www.mercato.xyz/api"

INDEXER_AUTH_PAYLOAD = {
    'X-Api-Key': 'WNQvjQy.1a4d0d1046098f8db1d4a529f7f44dd1',
    'X-Api-User': 'mercato.xyz'
}

MERCATO_COLLECTION_ID = "4f1a0ac4-68d0-4661-a7fd-428da529a9da"

RETRY_ATTEMPTS = 3

with open("files/accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]
