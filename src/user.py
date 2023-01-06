import json
import time
import requests
from block import Block
from Crypto.PublicKey import RSA

class User:
    """Representation of user"""
    def __init__(self, alias, pub_key_path, priv_key_path):
        self.pub_key_path = pub_key_path
        self.priv_key_path = priv_key_path
        self.alias = alias

        with open(self.pub_key_path, "r", encoding="utf-8") as t_file:
                self.public_key = t_file.read()


    @property
    def private_key(self):
        "Private key"
        with open(self.priv_key_path, "r", encoding="utf-8") as t_file:
            return RSA.importKey(t_file.read())

    @staticmethod
    def from_file(file_path):
        """ Load from file"""
        with open(file_path, encoding='utf-8') as t_file:
            data = json.load(t_file)
            return User(
                alias=data["alias"],
                pub_key_path=data["public"],
                priv_key_path=data["private"]
            )

    def mine(self, chain):
        response = requests.get(f'{chain}/transactions')
        content = json.loads(response.content)

        block = Block.from_dict(content)

        print(f"{self} mining block {block.number}...")
        start = time.time()
        block.mineBlock(self.public_key)
        end = time.time()
        print(
            f"Block {block.number} mined by {self} in {end - start :.5f}s")

        return self.push_mined_block(block, chain)

    def push_mined_block(self, block, chain):
        """ Send mined block to network"""

        body = {"block": block.to_dict(),
                "key": self.public_key,
                "alias": self.alias}
        response = requests.post(f'{chain}/block', json=body)

        status = json.loads(response.content)["status"]
        print(f"{self.alias} push {block.number} push {status}")
        return

    def __repr__(self):
        return self.alias
    # # TODO: replace with API call
    # def add_tx_to_chain(self, tx, chain):
    #     tx.sign_transaction(self.priv_key_path)
    #     chain.add_transaction(tx)
    #     return
