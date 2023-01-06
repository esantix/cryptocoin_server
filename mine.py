"""_summary_
"""

import json
from pprint import pprint
import requests
import time
import multiprocessing as mp

from user import User

# Create blockchain
NODE_ADDR = "http://localhost:5000"


def start_mining(user):
    while True:
        user.mine(chain=NODE_ADDR)
        print(json.loads(requests.get(f'{NODE_ADDR}/balance').content))
        time.sleep(3)



if __name__ == "__main__":
    users = [User.from_folder("users/esantix"),
            User.from_folder("users/miner1")]

    ps = []
    for u in users:
        ps.append(mp.Process(target=start_mining, args=(u, )))

    for p in ps:
        p.start()
