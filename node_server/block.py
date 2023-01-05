import hashlib
from pprint import pprint
from datetime import datetime
import time
import pickle
import json


class Block:

    @staticmethod
    def from_dict(dict):
        return Block(
            transactions=dict["transactions"],
            previousHash=dict["previousHash"],
            difficulty=dict["difficulty"],
            vhash=dict["hash"]
        )


    def __init__(self, transactions, previousHash='', vhash="", difficulty=1):
        self.difficulty = difficulty
        self.timestamp = str(datetime.now());
        self.transactions = transactions;
        self.previousHash = previousHash;
        self.nonce = 0
        self.index = 0
        self.hash = vhash

    def save(self, folder):
        full_path = f"{folder}/{self.hash}"
        with open(full_path, "wb") as file_:
            pickle.dump(self, file_, -1)
        return full_path

    @staticmethod
    def load(path):
        return pickle.load(open(path, "rb", -1))

    def to_dict(self):
        return json.dumps(self.__dict__)


    def calculateHash(self):
        strh = f'{self.timestamp} {self.transactions} {self.previousHash} {self.nonce}'
        return hashlib.sha256(strh.encode('utf-8')).hexdigest()

    def show(self):
        return pprint(self.__dict__)

    def mineBlock(self):
        while(self.hash[0:self.difficulty] != '0'*self.difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()
            
