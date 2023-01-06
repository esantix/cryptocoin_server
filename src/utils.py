from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

def verify_siganture(message, signature, publick_key):
        """Verify message signature"""
        digest = SHA256.new()
        digest.update(message.encode("utf-8"))

        sig = bytes.fromhex(signature)  # convert string to bytes object

        public_key = RSA.importKey(publick_key)
        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(digest, sig)

        if verified:
            return True
        return False