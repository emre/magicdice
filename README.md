# magicdice

`magicdice` is a Python library and set of tools to play and analyze STEEM based
magic dice game.

# Installation

Minimum Python requirement is Python3.6 and greater.

```
$ pip install magicdice
```

# Bidding

Bid 0.100 STEEM for under number 50 with the client seed `foo`.

```python
from magicdice.core import Magicdice
m = Magicdice(
    '<account>', '<active_key>')

resp = m.bid('under', '50', '0.100 STEEM', 'foo')
print(resp)
```

However, this doesn't guarentee that the bid is picked up by the game. If you want to ensure
the bid is picked up you can pass `ensure_pickup` flag:

```python
from magicdice.core import Magicdice

m = Magicdice(
    '<account>', '<active_key>')
resp = m.bid('under', '50', '0.100 STEEM', 'foo', ensure_pickup=True)
print(resp)
```

Which will include the roll (bid result) data.

# magic-dice api client

```python
from magicdice.api_client import ApiClient

api_client = ApiClient()
```

## Global Properties

Returns the global properties of the game. (min/max prediction, max payout, house edge, etc.)

```
api_client.globals()
```

## Bets

Return the last N bets:

```
api_client.bets('<username>', {"limit": N})
```

## User info

```
api_client.user('<username>')
```

## Rare wins

```
api_client.rare_wins({"limit": 10})
```

## Top winners

```
api_client.top_winners({"limit": 10})
```

# Verifying Bids

```python
from magicdice.utils import verify


bid_block_id = 30710738
bid_tx_id = "1ddbb2ccd975c7339a22c284fd0a91781ec99094"
roll_block_id = 30710739
roll_tx_id = "7b143697e667fd2a706ab0f88cc1dd9b6f252241"
server_seed = "8cc9pxehpq3kuoi9j5qd"

if verify(
        bid_block_id,
        bid_tx_id,
        roll_block_id,
        roll_tx_id,
        server_seed,
    ):
    print("Roll is solid!")
```

# A simple bot

```python

from magicdice.core import Magicdice

m = Magicdice(
    '<account>', '<private_active_key>')

# Send 10 0.100 STEEM bids with under 50 prediction

for i in range(0, 10):
    resp = m.bid('under', '50', '0.100 STEEM', 'foo', ensure_pickup=True)
    roll = resp[2]
    status = "won" if roll["won"] else "lost"
    print(f"{status} {roll['amount']} {roll['asset']}")
```

# Disclaimer

This library may contain unexpected bugs. Audit the code and use it at your own risk.
