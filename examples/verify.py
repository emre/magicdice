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