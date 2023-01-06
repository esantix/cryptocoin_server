from flask import Flask, request
from src.blockchain_handler import BlockchainHandler
from src.block import Block
from src.user import User

app = Flask(__name__)

user = User.from_file("tests/users/esantix.json")
cryptoCoin = BlockchainHandler("tests/node_server/", user)



@app.route('/transactions')
def get_transactions():
    block = cryptoCoin.give_block_with_transaction()
    return block.to_dict()

@app.route('/block', methods=['POST'])
def put_block():
    data = request.json

    block_dict = Block.from_dict(data["block"])

    cryptoCoin.new_subscriber(data["alias"], data["key"])
    added = cryptoCoin.recieve_mined_block(block_dict)

    

    return {"status": added}

@app.route('/balance')
def get_balance():
    balance = cryptoCoin.get_balance()
    return balance


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)