import json
import time
import requests
from block import Block
from pprint import pprint


class User:
    def __init__(self, name, pub_key, priv_key) -> None:
        self.name = name
        self.address = pub_key
        self.pub_key = pub_key
        self.priv_key = priv_key

    @staticmethod
    def from_folder(folder_path):
        with open(f'{folder_path}/metadata.json') as f:
            data = json.load(f)

        return User(
            name=data["name"],
            pub_key=data["public_key"],
            priv_key=data["priv_key"]
        )

    def mine(self, chain):
        response = requests.get(f'{chain}/transactions')
        content = json.loads(response.content)
 

        block = Block.from_dict(content)

        print(f"{self.name} mining block {block.number}...")
        start = time.time()
        block.mineBlock()
        end = time.time()
        print(
            f"Block {block.number} mined by {self.name} in {end - start :.5f}s")

        return self.push_mined_block(block, chain)

    def push_mined_block(self, block, chain):
        body = {"block": block.to_dict(),
                  "user": self.name

        }

        response = requests.post(
            f'{chain}/block',
            json=body
            )


        data = response.content
        status = json.loads(data)["status"]



        print(f"{self.name} push {block.number} push {status}")
        return

    # TODO: replace with API call
    def add_tx_to_chain(self, tx, chain):
        tx.sign_transaction(self.priv_key)
        chain.add_transaction(tx)
        return
