from flask import Flask
from web3 import Web3
from solc import compile_source
from web3.middleware import geth_poa_middleware
from flask import request, make_response
from flask_redis import FlaskRedis
import ast
from web3.contract import ConciseContract
import csv
import io


def w3_init():
    provider = Web3.HTTPProvider('http://node_1:8545')
    w3 = Web3(provider)
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


w3 = w3_init()
app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://@redis:6379/0'
redis_store = FlaskRedis(app)


@app.route('/')
def hello():
    return 'This is Python client server'


@app.route('/create_contract')
def create_contract():
    with open('NameValue.sol', 'rb') as f:
        contract_source_code = f.read().decode()
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:NameValue']

    NameValue = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin']
    )
    tx_hash = NameValue.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    redis_store.set('contractAddress', tx_receipt.contractAddress)
    redis_store.set('contractInterfaceAbi', contract_interface['abi'])

    return 'ok'


@app.route('/update')
def update():
    contract_address = redis_store.get('contractAddress').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get('contractInterfaceAbi').decode()
    )

    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
    )

    key = request.args.get('key')
    value = request.args.get('value')

    tx_hash = name_value.functions.update(key, value).transact(
        {'gas': 410_000}
    )
    w3.eth.waitForTransactionReceipt(tx_hash)
    return 'ok'


@app.route('/get')
def get():
    contract_address = redis_store.get('contractAddress').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get('contractInterfaceAbi').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
        ContractFactoryClass=ConciseContract
    )

    key = request.args.get('key')
    value = name_value.get(key)

    return value


@app.route('/remove')
def remove():
    contract_address = redis_store.get('contractAddress').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get('contractInterfaceAbi').decode()
    )

    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
    )

    key = request.args.get('key')

    tx_hash = name_value.functions.remove(key).transact(
        {'gas': 410_000}
    )
    w3.eth.waitForTransactionReceipt(tx_hash)
    return 'ok'


@app.route('/dump')
def dump():
    contract_address = redis_store.get('contractAddress').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get('contractInterfaceAbi').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
        ContractFactoryClass=ConciseContract
    )
    file = request.args.get('file')

    keys = name_value.dumpKeys()
    result = {}
    for key in keys:
        key_decoded = key.to_bytes(32, byteorder='big').split(
            b'\0', 1
        )[0].decode()
        result[key_decoded] = name_value.get(key_decoded)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(result.items())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={file}.csv"
    output.headers["Content-type"] = "text/csv"

    return output


if __name__ == '__main__':
    app.run()
