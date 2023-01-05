from flask import Flask, request, jsonify
from blockchain import BlockchainHandler
from block import Block
import json
app = Flask(__name__)

cryptoCoin = BlockchainHandler.from_file("storage/index.json")



@app.route('/transactions')
def get_transactions():
    block = cryptoCoin.give_block_with_transaction()
    return block.to_dict()

@app.route('/block', methods=['POST'])
def put_block():
    data = request
    b = json.loads(data.values.get('block'))

    u = data.values.get('user')
    bl = Block.from_dict(b)
    cryptoCoin.recieve_mined_block(bl,u)

    return {}

@app.route('/balance')
def get_balance():
    balance = cryptoCoin.get_balance()
    return balance


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)