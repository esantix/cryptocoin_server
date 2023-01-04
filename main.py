from users.user import User
from node_server.transaction import Transaction
from node_server.blockchain import BlockchainHandler

# Create blockchain
cryptoCoin = BlockchainHandler.from_file("index_test.json")

# Create users
esantix = User.from_folder("users/esantix")
miner1 = User.from_folder("users/miner1")
miner2 = User.from_folder("users/miner1")

# Do mining
for i in range(4):
    miner1.request_mineable_block(cryptoCoin)

# Create signed transactions
tx1 = Transaction(to_user=esantix, from_user=miner1, amount=2)
esantix.add_tx_to_chain(tx1, cryptoCoin)

# More mining
miner2.request_mineable_block(cryptoCoin)


# Show chain
cryptoCoin.show()


# Get balance
print("\nBalance:")
balance = cryptoCoin.get_balance()
print(balance)
