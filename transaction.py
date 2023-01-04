"""_summary_
"""

import hashlib
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

class Transaction:
    """Transaction object done over a blockchain"""

    def __init__(self, to_user, from_user=None, amount=0, internal=False):
        self.to_user_name = to_user.name
        self.to_user_address = to_user.address
        self.from_user_name = from_user.name
        self.from_user_address = from_user.address
        self.amount = amount
        self.internal = internal
        self.signatue = None

    def calculate_hash(self):
        """Get hash of transaction"""
        strh = f"{self.to_user_address} {self.from_user_address} {self.amount}"
        return hashlib.sha256(strh.encode("utf-8")).hexdigest()

    def sign_transaction(self, user):
        """ Add signature"""
        digest = SHA256.new()
        digest.update(self.calculate_hash().encode("utf-8"))
        
        with open(user.priv_key, "r") as myfile:
            private_key = RSA.importKey(myfile.read())

        signer = PKCS1_v1_5.new(private_key)
        sig = signer.sign(digest)
        self.signatue = sig.hex()
        return self

    def __repr__(self) -> str:
        return f"Transaction: {self.from_user_name}, {self.amount}, {self.to_user_name}"
