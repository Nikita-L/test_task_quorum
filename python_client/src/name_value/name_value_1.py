import csv
import io

from flask import request, make_response

from name_value import w3


def update(contract):
    key = request.args.get('key')
    value = request.args.get('value')

    tx_hash = contract.functions.update(key, value).transact(
        {'gas': 410_000}
    )
    w3.eth.waitForTransactionReceipt(tx_hash)


def dump(contract, file_name):
    keys = contract.dumpKeys()
    result = {}
    for key in keys:
        key_decoded = key.to_bytes(32, byteorder='big').split(
            b'\0', 1
        )[0].decode()
        result[key_decoded] = contract.get(key_decoded)

    si = io.StringIO()
    cw = csv.writer(si)

    cw.writerow(('key', 'value'))
    cw.writerows(result.items())

    output = make_response(si.getvalue())
    output.headers[
        "Content-Disposition"
    ] = f"attachment; filename={file_name}.csv"
    output.headers["Content-type"] = "text/csv"

    return output
