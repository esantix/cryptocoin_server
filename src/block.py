import hashlib
from pprint import pprint
from datetime import datetime
import json
from transaction import Transaction
from copy import deepcopy


class Block:

    @staticmethod
    def from_dict(dict):
        return Block(
            transactions=[Transaction.from_dict(t) for t in dict["transactions"]],
            previous_hash=dict["previous_hash"],
            difficulty=dict["difficulty"],
            vhash=dict["hash"],
            number=dict["number"],
            nonce=dict["nonce"],
            hasher=dict["hasher"],
            metadata=dict["metadata"]
        )
    
    def to_dict(self):

        dict_txs = [tx.to_dict() for tx in self.transactions]
        new = deepcopy(self)
        new.transactions = dict_txs
        
        return new.__dict__


    def __init__(self, transactions,  number,metadata={}, hasher=None, nonce=0, previous_hash='', vhash="", difficulty=1):
        self.difficulty = difficulty
        self.timestamp = str(datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.number = number
        self.hash = vhash
        self.hasher = hasher
        self.metadata = metadata

    def save(self, folder):
        full_path = f"{folder}/{self.number}.json"
        with open(full_path, "w") as f:
            json.dump(self.to_dict(), f)
        return

    @staticmethod
    def load(path):
        with open(path, "r") as f:
            data = json.load(f)
        return Block.from_dict(data)


    def calculateHash(self):
        strh = ""
        strh += f'{self.previous_hash}'
        strh += f'{self.difficulty}'
        strh += f'{self.transactions}'
        strh += f'{self.nonce}'
        strh += f'{self.hasher}'
        strh += f'{json.dumps(self.metadata)}'
        return hashlib.sha256(strh.encode('utf-8')).hexdigest()

    def show(self):
        return pprint(self.__dict__)

    def mineBlock(self, key):
        self.hasher = key
        while (self.hash[0:self.difficulty] != '0'*self.difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()
            # print(f'Trying hash: {self.hash[0:10]}',end="\r")
        

    def is_valid(self):
        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return self.hash == self.calculateHash()

if __name__ == "__main__":

    path = f"node_server/storage/blocks/3.json"
    b = Block.load(path)

    b.show()

    print(b.hash)
    print(b.calculateHash())