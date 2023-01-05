"""_summary_
"""

import hashlib
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import json

class Transaction:
    """Transaction object done over a blockchain"""

    @staticmethod
    def from_dict(dict):
        print(dict)
        return Transaction(
            to_user=dict["to_user_name"],
            from_user=dict["from_user_name"],
            amount=dict["amount"],
            internal=dict["internal"],
            signature=dict["signatue"]
        )

    def __init__(self, to_user, from_user=None, amount=0, internal=False, signature=None):
        self.to_user_name = to_user
        self.to_user_address = to_user
        self.from_user_name = from_user.name if not type(from_user)==str else from_user
        self.from_user_address = from_user.address if  not type(from_user)==str else from_user
        self.amount = amount
        self.internal = internal
        self.signatue = signature

    def calculate_hash(self):
        """Get hash of transaction"""
        strh = f"{self.to_user_address} {self.from_user_address} {self.amount}"
        return hashlib.sha256(strh.encode("utf-8")).hexdigest()

    def sign_transaction(self, priv_key):
        """ Add signature"""
        digest = SHA256.new()
        digest.update(self.calculate_hash().encode("utf-8"))
        
        with open(priv_key, "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sig = signer.sign(digest)
        self.signature = str(sig.hex())
        return self

    def to_dict(self):
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return f"Transfer: {self.from_user_name} -> {self.to_user_name} : {self.amount}"
