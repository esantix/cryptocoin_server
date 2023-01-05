from users.user import User
import requests
from pprint import pprint
import json

# Create blockchain
node_addr = "http://localhost:5000"
# Create users
esantix = User.from_folder("users/esantix")
esantix.request_mineable_block(chain=node_addr)

balance = json.loads(requests.get(f'{node_addr}/balance').content)
pprint(balance)
# miner1 = User.from_folder("users/miner1")
# miner2 = User.from_folder("users/miner1")

# # Do mining
# for i in range(4):
#     miner1.request_mineable_block(cryptoCoin)

# # Create transaction
# tx1 = Transaction(to_user=esantix, from_user=miner1, amount=2)
# esantix.add_tx_to_chain(tx1, cryptoCoin)

# # More mining
# miner2.request_mineable_block(cryptoCoin)


# # Show chain
# cryptoCoin.show()


# # Get balance
# print("\nBalance:")
# balance = cryptoCoin.get_balance()
# print(balance)
