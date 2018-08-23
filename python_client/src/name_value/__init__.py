import sys
from pathlib import Path

from web3 import Web3
from web3.contract import ConciseContract
from web3.exceptions import BadFunctionCallOutput
from web3.middleware import geth_poa_middleware
from flask_redis import FlaskRedis
from flask import Flask


src_path = Path('.', 'src').resolve()
sys.path.append(str(src_path))


def w3_init():
    provider = Web3.HTTPProvider('http://node_1:8545')
    w3 = Web3(provider)
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


w3 = w3_init()
app = Flask(__name__, template_folder='../templates')
app.config['REDIS_URL'] = 'redis://@redis:6379/0'
redis_store = FlaskRedis(app)
