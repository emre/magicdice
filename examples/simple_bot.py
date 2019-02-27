from magicdice.core import Magicdice

m = Magicdice(
    '<account>', '<private_active_key>')

# Send 10 0.100 STEEM bids with under 50 prediction

for i in range(0, 10):
    resp = m.bid('under', '50', '0.100 STEEM', 'foo', ensure_pickup=True)
    roll = resp[2]
    status = "won" if roll["won"] else "lost"
    print(f"{status} {roll['amount']} {roll['asset']}")