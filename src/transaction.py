import hashlib
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from utils import verify_siganture

class Transaction:
    """Transaction object done over a blockchain"""

    @staticmethod
    def from_dict(dictionary):
        """ Create from dictionary"""
        return Transaction(
            to_key = dictionary["to_key"],
            from_key = dictionary["from_key"],
            amount = dictionary["amount"],
            signature = dictionary["signature"],
            uuid = dictionary["uuid"]
        )

    def __init__(self, amount, from_key ,to_key, signature=None, uuid=None):
        self.to_key = to_key
        self.from_key = from_key
        self.amount = amount

        self.signature = signature
        self.uuid = uuid

    @property
    def hash(self):
        """Get hash of transaction"""
        strh = f"{self.to_key}{self.from_key}{self.amount}"
        return hashlib.sha256(strh.encode("utf-8")).hexdigest()

    def sign(self, private_key):
        """ Add signature"""
        digest = SHA256.new()
        digest.update(self.hash.encode("utf-8"))
        
        signer = PKCS1_v1_5.new(private_key)
        sig = signer.sign(digest)
        self.signature = str(sig.hex())

        return self.signature

    def to_dict(self):
        """To dict"""
        return self.__dict__

    def is_valid(self):
        return verify_siganture(self.hash, self.signature, self.from_key)

    def __repr__(self):
        return f"${self.amount} from:{self.from_key[0:10]} to:{self.to_key[0:10]}"


class RewardTx(Transaction):
    def is_valid(self):
        return True
