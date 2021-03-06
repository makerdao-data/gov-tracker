#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Public version #

from flask import Flask, request, jsonify
import atexit
from datetime import datetime
import csv
from io import StringIO
from werkzeug.wrappers import Response
from sqlalchemy import func
from deps import get_db
from utils.query import pull_filtered_data

from views.main_view import main_page_view, main_page_data
from views.address_views import address_page_view, address_data_view
from views.yay_views import yay_page_view, yay_data_view
from views.poll_views import poll_page_view, poll_data_view
from views.proxy_views import proxy_page_view, proxy_data_view
from views.protocol_parameters_views import parameters_page_view, parameters_data_view
from connectors.sf import sf, sf_disconnect

from models import ParameterEvent
from utils.query import pull_filtered_data


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# HTML endpoints -------------------------------------------
@app.route("/")
def main_page():
    return main_page_view(sf)


@app.route("/address/<address>")
def address_page(address):
    return address_page_view(sf, address.lower())


@app.route("/proxy/<proxy>")
def proxy_page(proxy):
    return proxy_page_view(sf, proxy.lower())


@app.route("/yay/<yay_id>")
def yay_page(yay_id):
    return yay_page_view(sf, yay_id)


@app.route("/poll/<poll_id>")
def poll_page(poll_id):
    return poll_page_view(sf, poll_id)


@app.route("/protocol_parameters")
def parameters_page():
    return parameters_page_view(sf)


# DATA endpoints -------------------------------------------
@app.route("/data/main", methods=["GET"])
def get_main_page_data():
    dataset = main_page_data(sf)
    return jsonify(dataset)


@app.route("/data/address/<address>", methods=["GET"])
def get_address_page_data(address):
    dataset = address_data_view(sf, address.lower())
    return jsonify(dataset)


@app.route("/data/proxy/<proxy>", methods=["GET"])
def get_proxy_page_data(proxy):
    dataset = proxy_data_view(sf, proxy.lower())
    return jsonify(dataset)


@app.route("/data/yay/<yay>", methods=["GET"])
def get_yay_page_data(yay):
    dataset = yay_data_view(sf, yay)
    return jsonify(dataset)


@app.route("/data/poll/<poll>", methods=["GET"])
def get_poll_page_data(poll):
    dataset = poll_data_view(sf, poll)
    return jsonify(dataset)


# @app.route("/data/protocol_parameters", methods=["GET"])
# def get_parameters_page_data():
#     dataset = parameters_data_view(sf)
#     return jsonify(dataset)

@app.route("/data/protocol_parameters/<s>/<e>", methods=["GET"])
def get_parameters_page_data(s, e):

    session = next(get_db())
    query = pull_filtered_data(request, s, e, session, ParameterEvent)
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['block', 'timestamp', 'tx_hash', 'source', 'parameter', 'ilk', 'from_value', 'to_value']:
            col_name = 'block'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(ParameterEvent, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    records_total = session.query(ParameterEvent).count()

    # response
    return {
        'data': [record.to_dict() for record in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': records_total,
        'draw': request.args.get('draw', type=int),
    }


@app.route("/data/parameters_history_export/<s>/<e>", methods=["GET"])
def parameters_history_export(s, e):

    session = next(get_db())
    query = pull_filtered_data(request, s, e, session, ParameterEvent)

    def generate():

        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('block', 'timestamp', 'tx_hash', 'source', 'parameter', 'ilk', 'from_value', 'to_value'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in query:
            w.writerow(tuple(item.to_list()))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # stream the response as the data is generated
    response = Response(generate(), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename="export.csv")
    return response


# cleanup tasks
def cleanup_task():
    if not sf.is_closed():
        sf_disconnect(sf)
        print("SF connection closed.")


atexit.register(cleanup_task)


if __name__ == "__main__":
    app.run(debug=False)
