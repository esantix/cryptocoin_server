import json
import time

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
        block = chain.give_block_with_transaction()
        
        start = time.time()
        block.mineBlock(difficulty=chain.difficulty)
        end = time.time()
        print(f"Block {block.hash[0:10]}... mined by {self.name} in {end - start :.5f}ms")

        return self.push_mined_block(block, chain)
    
    # TODO: replace with API call
    def push_mined_block(self, block, chain):
        chain.recieve_mined_block(block, self)
        return

    # TODO: replace with API call
    def add_tx_to_chain(self, tx, chain):
        tx.sign_transaction(self.priv_key)
        chain.add_transaction(tx)
        return