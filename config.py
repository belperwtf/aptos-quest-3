EXPLORER_URL = "https://explorer.aptoslabs.com/txn/{transaction}?network=mainnet"
RPC_URL = "https://fullnode.mainnet.aptoslabs.com/v1"
INDEXER_XYZ_API_URL = "https://api.indexer.xyz"
MERCATO_API_URL = "https://www.mercato.xyz/api"

INDEXER_AUTH_PAYLOAD = {
    'X-Api-Key': 'WNQvjQy.1a4d0d1046098f8db1d4a529f7f44dd1',
    'X-Api-User': 'mercato.xyz'
}

MERCATO_COLLECTION_ID = "4f1a0ac4-68d0-4661-a7fd-428da529a9da"

MERCATO_BID_CONTRACT_V2 = "0xe11c12ec495f3989c35e1c6a0af414451223305b579291fc8f3d9d0575a23c26::biddings_v2::collection_bids"
MERCATO_BID_CONTRACT_V1 = "0xe11c12ec495f3989c35e1c6a0af414451223305b579291fc8f3d9d0575a23c26::biddings::collection_bid"

TOPAZ_BID_CONTRACT_V2 = "0x6de37368e31dff4580b211295198159ee6f98b42ffa93c5683bb955ca1be67e0::collection_offer::init_for_tokenv2_entry"
TOPAZ_BID_CONTRACT_V1 = "0x2c7bccf7b31baf770fdbcc768d9e9cb3d87805e255355df5db32ac9a669010a2::collection_marketplace::bid"
TOPAZ_FEE_SCHEDULE = "0x27eb09e72f97befe67d6d57a194af3ba8cad99d85b2976cbe56bb86660d1415a"

BID_NFTS = {
    'AptMap V2': '0xdd68321f2dadca29e37ed7dd05300f3a1bb5df96c5aa72231cb7ba65414cfb10',
    'Buy Bitcoin': '0xec7e43fe3847b302c380caaa6c107a3fc9f2e0bec8c18ddd4e784324481a7cba',
    'Aptos ONE V2': '0x3d94d2eb4aea99cdf051a817c1e9f31d2166c79ed301578c75c31e38d4be747e',
    'Pontem Dark Ages': '0x7fef9d50cd1a2ee2068617b086b98ec434f1728d7cadcc7088c402df4585ce41',
    'MAVRIK': '0xf3778cf4d8b6d61ab3d79c804797ef7417e258449d2735b0f405e604b81f7916',
    'Bruh Bears': '0x43ec2cb158e3569842d537740fd53403e992b9e7349cc5d3dfaa5aff8faaef2',
    'Aptos Undead': '0x5a4505c2e96370b1f3592035109979011bd1a0c5cfe497b922b2584b4a90dfdb'
}

WAPAL_MINT_CONTRACT = "0x6547d9f1d481fdc21cd38c730c07974f2f61adb7063e76f9d9522ab91f090dac::candymachine::mint_script"
WAPAL_MINT_NFTS = [
    '0xa79267255727285e55bc42d34134ffa2133b6983391846810d39f094fb5f1c87'
]

RETRY_ATTEMPTS = 3

with open("files/accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open("files/proxies.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

with open("files/evm.txt", "r") as file:
    EVM = [row.strip() for row in file]

with open("files/twitters.txt", "r") as file:
    TWITTERS = [row.strip() for row in file]
