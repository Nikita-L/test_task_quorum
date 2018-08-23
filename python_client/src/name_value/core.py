import ast
from datetime import datetime

from flask import request, jsonify
from solc import compile_source

from name_value import (name_value_1, name_value_2, w3, app, redis_store,
                        ConciseContract)


@app.route('/')
def hello():
    return 'This is Python client server'


@app.route('/create_contract')
def create_contract():
    version = request.args.get('version', '1')

    with open(f'NameValue{version}.sol', 'rb') as f:
        contract_source_code = f.read().decode()
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol[f'<stdin>:NameValue{version}']

    NameValue = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin']
    )
    tx_hash = NameValue.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    redis_store.set(f'contractAddress{version}', tx_receipt.contractAddress)
    redis_store.set(
        f'contractInterfaceAbi{version}', contract_interface['abi']
    )

    return 'ok'


@app.route('/get')
def get():
    version = request.args.get('version', '1')

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
        ContractFactoryClass=ConciseContract
    )

    key = request.args.get('key')
    value = name_value.get(key)

    if type(value) == str:
        return value
    value[-1] = datetime.fromtimestamp(
        (int(value[-1]) / 1_000_000_000)
    ).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(dict(zip(('value', 'author', 'updated_date'), value)))


@app.route('/update')
def update():
    version = request.args.get('version', '1')

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi
    )

    if version == '1':
        name_value_1.update(name_value)
    elif version == '2':
        name_value_2.update(name_value)

    return 'ok'


@app.route('/remove')
def remove():
    version = request.args.get('version', '1')

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
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
    version = request.args.get('version', '1')

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
        ContractFactoryClass=ConciseContract
    )
    file = request.args.get('file')

    if version == '1':
        return name_value_1.dump(name_value, file)
    elif version == '2':
        return name_value_2.dump(name_value, file)


@app.route('/get_history')
def get_history():
    version = request.args.get('version', '1')

    if version == '1':
        return 'Not implemented, see version 2'

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
    )

    key = request.args.get('key')

    return name_value_2.get_history(name_value, key)


@app.route('/listener')
def listener():
    version = request.args.get('version', '1')

    if version == '1':
        return 'Not implemented, see version 2'

    contract_address = redis_store.get(f'contractAddress{version}').decode()
    contract_interface_abi = ast.literal_eval(
        redis_store.get(f'contractInterfaceAbi{version}').decode()
    )
    name_value = w3.eth.contract(
        address=contract_address,
        abi=contract_interface_abi,
    )

    return name_value_2.listener(name_value)
