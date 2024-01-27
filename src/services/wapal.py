from loguru import logger
from src.services.transaction import TransactionService

class Wapal:
    def __init__(self, account):
        self.account = account
        self.transaction_service = TransactionService(account)

    def mint(self):
        logger.info("Processing Wapal minting ...")

        self.transaction_service.send_transaction({
            "function": "0x6547d9f1d481fdc21cd38c730c07974f2f61adb7063e76f9d9522ab91f090dac::candymachine::mint_script",
            "type_arguments": [],
            "arguments": ["0xa79267255727285e55bc42d34134ffa2133b6983391846810d39f094fb5f1c87"],
            "type": "entry_function_payload"
        })