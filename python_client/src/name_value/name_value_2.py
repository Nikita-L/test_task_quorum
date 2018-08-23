from datetime import datetime
import csv
import io
import time

from flask import request, make_response, jsonify, Response, Markup

from name_value import w3, BadFunctionCallOutput
from name_value.utils import stream_template


def update(contract):
    key = request.args.get('key')
    value = request.args.get('value')
    author = request.args.get('author')

    tx_hash = contract.functions.update(key, value, author).transact(
        {'gas': 410_000}
    )
    w3.eth.waitForTransactionReceipt(tx_hash)


def dump(contract, file_name):
    keys = contract.dumpKeys()
    rows = []
    for key in keys:
        key_decoded = key.to_bytes(32, byteorder='big').split(
            b'\0', 1
        )[0].decode()
        row = [key_decoded, *contract.get(key_decoded)]
        row[-1] = datetime.fromtimestamp(
            (int(row[-1]) / 1_000_000_000)
        ).strftime("%Y-%m-%d %H:%M:%S")
        rows.append(row)

    si = io.StringIO()
    cw = csv.writer(si)

    cw.writerow(('Key', 'Value', 'Author', 'Date (UTC)'))
    cw.writerows(rows)

    output = make_response(si.getvalue())
    output.headers[
        "Content-Disposition"
    ] = f"attachment; filename={file_name}.csv"
    output.headers["Content-type"] = "text/csv"

    return output


def get_history(contract, key):
    results = []
    for i in range(w3.eth.blockNumber + 1):
        try:
            value = contract.functions.get(key).call(block_identifier=i)
            value[-1] = int(value[-1]) / 1_000_000_000
            results.append(dict(zip(
                ('value', 'author', 'updated_date'), value)
            ))
        except BadFunctionCallOutput:
            pass

    results = [dict(t) for t in {tuple(d.items()) for d in results}]
    results = sorted(results, key=lambda k: k['updated_date'])
    for d in results:
        d['updated_date'] = datetime.fromtimestamp(
            d['updated_date']
        ).strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(results)


def listener(contract):
    key_updated_filter = contract.events.KeyUpdated.createFilter(
        fromBlock='latest'
    )
    key_removed_filter = contract.events.KeyRemoved.createFilter(
        fromBlock='latest'
    )

    def g():
        previous_data = []
        while True:
            key_updated_events = key_updated_filter.get_new_entries()
            key_removed_events = key_removed_filter.get_new_entries()

            data = [*key_updated_events, *key_removed_events]
            data = [dict(e) for e in data]
            data = sorted(data, key=lambda k: k['args']['updated_date'])

            if previous_data != data and data:
                result = ''
                for e in data:
                    e['args'] = dict(e['args'])
                    e['args']['updated_date'] = datetime.fromtimestamp(
                        int(e['args']['updated_date']) / 1_000_000_000
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    result_dict = dict()
                    result_dict['event'] = e['event']
                    result_dict['blockNumber'] = e['blockNumber']
                    result_dict['key'] = e['args']['key']
                    result_dict['value'] = e['args']['value']
                    result_dict['author'] = e['args']['author']
                    result_dict['updated_date'] = e['args']['updated_date']

                    result += f'{result_dict}'

                previous_data = data
                yield result
            else:
                yield
            time.sleep(1)

    return Response(stream_template('listener.html', data=g()))
