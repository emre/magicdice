import hashlib
import hmac
import json
import re

from steem import Steem
from steem.amount import Amount


def get_steem_client(keys=None):
    """Helper function to get the Steem client

    :return (steem.Steem): Main steem instance
    """
    return Steem(nodes=["https://api.steemit.com"], keys=keys)


def get_op_by_tx(block, tx_id):
    """Return the operation data by block num and tx id

    :param block (int): Block number
    :param tx_id (str): Transaction ID
    :return (dict): Operation data
    """
    for transaction in block["transactions"]:
        if transaction["transaction_id"] == tx_id:
            return transaction["operations"][0][1]

    raise ValueError("Invalid transaction ID")


def verify(bid_block, bid_tx, result_block, result_tx, server_seed):
    steem = get_steem_client()

    # get the roll data
    roll_data = get_op_by_tx(steem.get_block(bid_block), bid_tx)
    prediction_type, prediction_number, client_seed = roll_data["memo"].split()
    prediction_number = int(prediction_number)

    # get the result seed
    result_data = get_op_by_tx(
        steem.get_block(result_block), result_tx)

    lost = Amount(result_data["amount"]).amount == 0.001

    # parse json from memo
    json_metadata = json.loads(re.search("{.*}", result_data["memo"]).group(0))
    server_seed_hash = json_metadata.get("serverSeedHash")
    result_roll = json_metadata.get("diceRoll")

    result_seed = hmac.new(
        server_seed.encode('utf8'),
        digestmod=hashlib.sha256
    )
    result_seed.update(f"{client_seed}-{bid_block}".encode("utf8"))
    result_seed = result_seed.hexdigest()

    result_number = int(result_seed[0:10], 16)
    dice_roll = (result_number % 100) + 1

    # verify dice roll
    if dice_roll != result_roll:
        raise ValueError("Dice roll is invalid!")

    # additional check
    # if the prediction is right but the amount is 0.001
    # raise the anomality
    if prediction_type == "under":
        if dice_roll < prediction_number and lost:
            raise ValueError("That should be a win roll!")
    elif prediction_type == "over":
        if dice_roll > prediction_number and lost:
            raise ValueError("That should be a win roll!")

    # verify server seed hash
    seed_hash_check = hashlib.sha256()
    seed_hash_check.update(server_seed.encode("utf8"))
    seed_hash_check = seed_hash_check.hexdigest()

    if seed_hash_check != server_seed_hash:
        raise ValueError("Invalid Seed hash!")

    return True
