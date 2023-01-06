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
            number=dict["number"]
        )
    
    def to_dict(self):

        dict_txs = [tx.to_dict() for tx in self.transactions]
        new = deepcopy(self)
        new.transactions = dict_txs
        
        return new.__dict__


    def __init__(self, transactions, number, previous_hash='', vhash="", difficulty=1):
        self.difficulty = difficulty
        self.timestamp = str(datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.number = number
        self.hash = vhash

    def save(self, folder):
        full_path = f"{folder}/{self.number}_{self.hash}.json"
        with open(full_path, "w") as f:
            json.dump(self.to_dict(), f)
        return

    @staticmethod
    def load(path):
        with open(path, "r") as f:
            data = json.load(f)
        return Block.from_dict(data)


    def calculateHash(self):
        strh = f'{self.timestamp} {self.transactions} {self.previous_hash} {self.nonce}'
        return hashlib.sha256(strh.encode('utf-8')).hexdigest()

    def show(self):
        return pprint(self.__dict__)

    def mineBlock(self):
        while (self.hash[0:self.difficulty] != '0'*self.difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()
            # print(f'Trying hash: {self.hash[0:10]}',end="\r")
