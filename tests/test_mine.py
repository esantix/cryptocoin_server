"""_summary_
"""

import json
import requests
import multiprocessing as mp

from src.user import User

# Create blockchain
NODE_ADDR = "http://localhost:5000"


def start_mining(user):
    while True:
        user.mine(chain=NODE_ADDR)
        print(json.loads(requests.get(f'{NODE_ADDR}/balance').content))
        # time.sleep(10/user.speed)


if __name__ == "__main__":
    users = [User.from_file("tests/users/esantix.json"),
             User.from_file("tests/users/miner1.json")]

    ps = []
    for u in users:
        ps.append(mp.Process(target=start_mining, args=(u, )))

    for p in ps:
        p.start()
