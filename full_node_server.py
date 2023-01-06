from flask import Flask, request
from blockchain import BlockchainHandler
from block import Block
import json
app = Flask(__name__)

cryptoCoin = BlockchainHandler.from_file("node_server/storage/index.json")



@app.route('/transactions')
def get_transactions():
    block = cryptoCoin.give_block_with_transaction()
    return block.to_dict()

@app.route('/block', methods=['POST'])
def put_block():
    data = request.json

    block_dict = Block.from_dict(data["block"])
    user = data["user"]
    added = cryptoCoin.recieve_mined_block(block_dict,user)

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