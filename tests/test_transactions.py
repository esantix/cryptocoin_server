from src.transaction import Transaction
from src.user import User


user_esantix = User.from_file("./tests/users/esantix.json")
user_miner = User.from_file("./tests/users/miner1.json")

tx = Transaction(
                from_key = user_miner.public_key,
                to_key = user_esantix.public_key,
                amount = 10)

tx.sign(user_miner.private_key)
tx.amount = 100
tx.sign(user_miner.private_key)

print(f"Is valid? {tx.is_valid()}")
