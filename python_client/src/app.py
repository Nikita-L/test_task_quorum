from flask import Flask
from web3 import Web3
from solc import compile_source
from web3.middleware import geth_poa_middleware
from flask import jsonify, request


def w3_init():
    provider = Web3.HTTPProvider('http://node_1:8545')
    w3 = Web3(provider)
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    return w3


w3 = w3_init()
app = Flask(__name__)
name_value = None


@app.route('/')
def hello():
    return 'This is Python client server'


@app.route('/create_contract')
def create_contract():
    global name_value

    with open('NameValue.sol', 'rb') as f:
        contract_source_code = f.read().decode()

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:NameValue']

    w3.eth.defaultAccount = w3.eth.accounts[0]

    NameValue = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin']
    )
    tx_hash = NameValue.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    name_value = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi'],
    )

    # tx_hash = name_value.functions.update('test_key', 'test_value').transact()
    # w3.eth.waitForTransactionReceipt(tx_hash)
    # return name_value.functions.get('test_key').call()
    return 'ok'


@app.route('/update')
def update():
    global name_value

    key = request.args.get('key')
    value = request.args.get('value')

    tx_hash = name_value.functions.update(key, value).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    return 'ok'


if __name__ == '__main__':
    app.run()
