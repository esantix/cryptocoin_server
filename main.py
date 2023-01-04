from user import User
from transaction import Transaction
from Crypto.PublicKey import RSA
from blockchain import BlockchainHandler
from pprint import pprint

# Create blockchain
cryptoCoin = BlockchainHandler.from_file("index_test.json")

# Create users
esantix = User.from_folder("users/esantix")
miner1 = User.from_folder("users/miner1")
miner2 = User.from_folder("users/miner1")

# Do mining
for i in range(10):
    cryptoCoin.mine_pending_transactions(esantix)

# Create signed transactions
tx1 = Transaction(to_user=miner1, from_user=esantix, amount=4).sign_transaction(esantix)
cryptoCoin.add_transaction(tx1)

# More mining
cryptoCoin.mine_pending_transactions(miner2)

# Show chain
cryptoCoin.show()


# Get balance
balance = cryptoCoin.get_balance()
pprint(balance)
