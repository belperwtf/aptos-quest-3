import time

from src.clients.aptos_client import client
from loguru import logger

from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from aptos_sdk.transactions import RawTransaction, SignedTransaction, TransactionPayload

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

    async def get_raw_txn(self, payload: dict) -> RawTransaction | None:
        raw_txn =  RawTransaction(
            self.account.account_address,
            await self.client.account_sequence_number(self.account.account_address),
            TransactionPayload(payload),
            1000,
            100,
            int(time.time()) + 60,
            chain_id=1,
        )
        simulated_txn = (await self.client.simulate_transaction(raw_txn, self.account, True))[0]
        if simulated_txn["vm_status"] != 'Executed successfully':
            logger.error(f'Failed status: {simulated_txn["vm_status"]}')
            return
        raw_txn.max_gas_amount = int(simulated_txn["max_gas_amount"])
        raw_txn.gas_unit_price = int(simulated_txn["gas_unit_price"])
        return raw_txn

    async def send_txn(self, raw_txn: RawTransaction) -> None:
        if not raw_txn:
            return
        signature = self.account.sign(raw_txn.keyed())
        auth = Authenticator(Ed25519Authenticator(self.account.public_key(), signature))
        transaction = await self.client.submit_bcs_transaction(SignedTransaction(raw_txn, auth))
        tx_result = await self.client.wait_for_transaction(transaction)
        if tx_result is None:
            logger.success(EXPLORER_URL.format(transaction=transaction))