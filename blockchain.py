import json
from block import Block
from transaction import Transaction
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from glob import glob

class BlockchainHandler:
    """Chain of linked Blocks"""

    @staticmethod
    def from_file(path):
        """. """
        with open(path, "r", encoding='utf-8') as index:
            data = json.load(index)

            return BlockchainHandler(
                data=data,
                priv_key=data["metadata"]["priv_key"],
                difficulty=data["metadata"]["difficulty"],
                reward=data["metadata"]["reward"],
                folder=data["metadata"]["folder"],
                name=data["metadata"]["name"])

    def __init__(self, data, priv_key, difficulty=4, reward=10, folder=".", name="chain"):
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = reward
        self.pub_key = ""
        self.name = name
        self.priv_key = priv_key
        self.blocks_path = folder + "/blocks/"



    def add_transaction(self, transaction):
        """Add transaction to pending list"""
        if not self.is_tx_valid(transaction):
            raise ValueError("Transaction not valid")

        if transaction.from_user_address != self.pub_key:

            user_balance = self.get_balance()[transaction.from_user_name]
            if transaction.amount > user_balance:

                raise ValueError(
                    f" '{transaction}' failed. Not enough money ({user_balance})"
                )

        self.pending_transactions.append(transaction)

    def create_genesis(self):
        """Create genesis block"""
        gen_block = Block([], 0)
        gen_block.hash = gen_block.calculateHash()
        gen_block.save(self.blocks_path)


    def give_block_with_transaction(self):
        """Trigger mining""" 
        number = self.length
        block = Block(transactions=self.pending_transactions, difficulty=self.difficulty, number=number)
        block.previous_hash = self.get_block(number - 1).hash
        return block

    def remove_tx_by_uuid(self, uuid):
        for tx in self.pending_transactions:
            if tx.uuid == uuid:
                self.pending_transactions.remove(tx)

    # TODO; make API call
    def recieve_mined_block(self, mined_block, miner_user):

        if mined_block.previous_hash != self.get_block(self.length-1).hash:
            print(f"Invalid block by {miner_user}")
            return False
        else:
            mined_block.save(self.blocks_path)
            for tx in mined_block.transactions:
                self.remove_tx_by_uuid(tx.uuid)

            reward_tx = Transaction(
                uuid=mined_block.hash,
                to_user=miner_user,
                from_user=None,
                amount=self.mining_reward,
                internal=True,
            ).sign_transaction(self.priv_key)

            self.pending_transactions.append(reward_tx)
            print(f"Recieved valid block. Rewarding: {reward_tx}")
            return True



    def get_block(self, idx):
        file_dir = glob(f'{self.blocks_path}/{idx}_**')[0]
        return Block.load(file_dir)

    @property
    def length(self):
        blocks_dirs = glob(f'{self.blocks_path}/**')
        return len(blocks_dirs)

    def is_tx_valid(self, transaction):
        """Check if transaction is valid in chain"""
        if transaction.internal:
            return True

        if transaction.signatue is None:
            raise KeyError("Not signed")

        if not self.verify_tx_sig(
            transaction.calculate_hash(),
            transaction.signatue,
            transaction.from_user_address,
        ):
            return False

        return True

    def verify_tx_sig(self, message, hexsig, pub_key_str):
        """Verify transaction signature"""
        digest = SHA256.new()
        digest.update(message.encode("utf-8"))

        sig = bytes.fromhex(hexsig)  # convert string to bytes object

        with open(pub_key_str, "r", encoding="utf-8") as f:
            pub_key_str = f.read()

        public_key = RSA.importKey(pub_key_str)
        verifier = PKCS1_v1_5.new(public_key)
        verified = verifier.verify(digest, sig)

        if verified:
            return True
        return False

    def get_balance(self):
        """Get balance of all users"""
        balance = {}
        # self.is_valid()
        for i in range(self.length):
            block = self.get_block(i)


            for tx in block.transactions:
                transaction = tx
                to_user_name = transaction.to_user_name
                from_user_name = transaction.from_user_name

                if to_user_name not in balance.keys():
                    balance[to_user_name] = 0
                balance[to_user_name] += transaction.amount

                if from_user_name is None:
                    pass
                else:
                    if from_user_name not in balance.keys():
                        balance[from_user_name] = 0
                    balance[from_user_name] -= transaction.amount


        return balance

    def show(self):
        """Show all chain"""
        for i in range(self.length):
            block = self.get_block(i)
            block.show()

        print("Pending tx:")
        for ptx in self.pending_transactions:
            print(ptx)

    def is_valid(self):
        """Check chain validity"""
        for i in range(1, self.length):
            block = self.get_block(i)
            if block.hash != block.calculateHash():
                print(f"block {block} hash invalid {block.hash}")
                print(block.calculateHash())
                return False

            if block.previous_hash != self.get_block(i - 1).hash:
                print(
                    f"block {block} invalid previous_hash {block.previous_hash}")
                return False

        return True
