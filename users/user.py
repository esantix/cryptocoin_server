import json
import time
import requests
from node_server.block import Block
from pprint import pprint


class User:
    def __init__(self, name, pub_key, priv_key) -> None:
        self.name  = name
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

    # TODO: replace with API call
    def request_mineable_block(self, chain):
        response = requests.get(f'{chain}/transactions')
        content = json.loads(response.content)
        a = content["transactions"]
        parsed_cnt = content
        parsed_cnt["transactions"] = [json.loads(t) for t in a]
        block = Block.from_dict(parsed_cnt)
        start = time.time()
        block.mineBlock()
        end = time.time()

        print(f"Block {block.hash[0:10]}... mined by {self.name} in {end - start :.5f}ms")

        return self.push_mined_block(block, chain)
    
    # TODO: replace with API call
    def push_mined_block(self, block, chain):
        requests.post(f'{chain}/block', data={
            "block":block.to_dict()
             ,"user":self.name
         }
         )
        return

    # TODO: replace with API call
    def add_tx_to_chain(self, tx, chain):
        tx.sign_transaction(self.priv_key)
        chain.add_transaction(tx)
        return