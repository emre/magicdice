import time

from steem.account import Account
from steem.transactionbuilder import TransactionBuilder
from steembase import operations

from .utils import get_steem_client
from .constants import MAGICDICE_ACCOUNT
from .api_client import ApiClient


class Magicdice:
    """The main class to broadcast transfers
    """

    def __init__(self, account, active_key):
        self.steem = get_steem_client([active_key,])
        self.api_client = ApiClient()
        self.account = account
        self.active_key = active_key

    def _ensure_pickup(self, bid_block_id, bid_transaction_id):
        """ Ensures a bid picked up by magic-dice.
        """
        bets = self.api_client.bets(self.account, {"limit": 50})
        for bet in bets:
            if bet["refTransactionId"] == bid_transaction_id:
                return bet

        raise ValueError(f"This bid is not picked up by magic dice! "
                         f"{bid_block_id}#{bid_transaction_id}")

    def poll_roll(self):
        pass

    @property
    def steem_account(self):
        """Return a fresh steem.Account instance

        :return (steem.Account)
        """
        return Account(self.account, steemd_instance=self.steem)

    def bid(self, prediction_type, prediction_number,
            amount, client_seed=None, ensure_pickup=False):
        """Create a bid and broadcast to the blockchain.

        :param prediction_type (str): under or over
        :param prediction_number: (min:2, max:95)
        :param amount (str): Bid amount
        :param client_seed (str): Client seed
        :return (tuple): Block ID and tx ID
        """
        ops = [
            operations.Transfer(**{
                "from": self.account,
                "to": MAGICDICE_ACCOUNT,
                "amount": amount,
                "memo": f"{prediction_type} {prediction_number} {client_seed}"
            }),
        ]
        tb = TransactionBuilder(steemd_instance=self.steem)
        tb.appendOps(ops)
        tb.appendSigner(self.account, "active")
        tb.sign()
        response = self.steem.broadcast_transaction_synchronous(tb.json())

        # ensure the transaction is picked up by magic-dice.
        # sleep block generation duration + 1 seconds for safety
        if ensure_pickup:
            time.sleep(4)
            pickup_details = self._ensure_pickup(
                response.get("block_num"), response.get("id"))
            return response.get("id"), response.get("block_num"),\
                   pickup_details

        return response.get("id"), response.get("block_num")