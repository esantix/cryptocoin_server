import json
from block import Block
from transaction import RewardTx
from utils import verify_siganture
from glob import glob

class BlockchainHandler:
    """Chain of linked Blocks"""

    def get_subs(self):
        
        with open(self.subs_path, encoding='utf-8') as t_file:
            data = json.load(t_file)
        return data

    def new_subscriber(self, alias, key):
        data =  self.get_subs()
        
        if key not in data.keys():
            data[key] = {"alias": alias}

        with open(self.subs_path, "w", encoding='utf-8') as f:
            json.dump(data, f)
        return

    def __init__(self, folder, user, reward=10):
        self.pending_transactions = []
        self.path = folder
        self.blocks_path = folder + "storage/blocks/"
        self.subs_path = self.path + "suscribers.json"
        self.user = user

        gen = self.get_block(0)
        reward = gen.metadata["reward"]
        self.mining_reward = reward
        if not self.validate():
            raise ValueError("Unable to load chain. Invalid block/s")


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
        difficulty = self.get_block(number-1).difficulty
        block = Block(transactions=self.pending_transactions, difficulty=difficulty, number=number)
        block.previous_hash = self.get_block(number - 1).hash
        return block

    def remove_tx_by_uuid(self, uuid):
        for tx in self.pending_transactions:
            if tx.uuid == uuid:
                self.pending_transactions.remove(tx)

    # TODO; make API call
    def recieve_mined_block(self, mined_block):

        if mined_block.previous_hash != self.get_block(self.length-1).hash:
            print(f"Too late or invalid")
            return False

        if not mined_block.is_valid():
            print(f"Invalid block")
            return False

       
        mined_block.save(self.blocks_path)
        for tx in mined_block.transactions:
            self.remove_tx_by_uuid(tx.uuid)


        if not self.validate():
            raise ValueError(f"New block broke chain!! Erase {mined_block.number}")
        print(f"Recieved valid block")
        return True



    def get_block(self, idx):
        if idx == -1:
            idx = self.length-1
        file_dir = f'{self.blocks_path}/{idx}.json'
        return Block.load(file_dir)

    @property
    def length(self):
        blocks_dirs = glob(f'{self.blocks_path}/**')
        return len(blocks_dirs)

    def get_balance(self):
        """Get balance of all users"""
        balance = {}

        if not self.validate():
            raise ValueError("Unable to get balance. Invalid block/s")

        for i in range(self.length):
            block = self.get_block(i)
            hs = block.hasher

            for tx in block.transactions:

                to = tx.to_key
                fr = tx.from_key

                if to not in balance.keys():
                    balance[to] = 0
                balance[to] += tx.amount

                if fr not in balance.keys():
                    balance[fr] = 0
                balance[fr] -= tx.amount

            if hs not in balance.keys():
                balance[hs] = 0
            balance[hs] += self.mining_reward

        return balance

    def show(self):
        """Show all chain"""
        for i in range(self.length):
            block = self.get_block(i)
            block.show()

        print("Pending tx:")
        for ptx in self.pending_transactions:
            print(ptx)

    def validate(self):
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
