from src.clients.aptos_client import client
from loguru import logger

from config import EXPLORER_URL

class TransactionService:
    def __init__(self, account):
        self.client = client
        self.account = account

    def send_transaction(self, payload):
        try:
            transaction = self.client.submit_transaction(self.account, payload)

            self.client.wait_for_transaction(transaction)

            logger.success(EXPLORER_URL.format(transaction=transaction))
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
