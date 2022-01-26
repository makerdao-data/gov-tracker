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

from views.main_view import main_page_view, main_page_data
from views.address_views import address_page_view, address_data_view
from views.yay_views import yay_page_view, yay_data_view
from views.poll_views import poll_page_view, poll_data_view
from views.proxy_views import proxy_page_view, proxy_data_view
from views.protocol_parameters_views import parameters_page_view, parameters_data_view
from connectors.sf import sf, sf_disconnect


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


@app.route("/data/protocol_parameters", methods=["GET"])
def get_parameters_page_data():
    dataset = parameters_data_view(sf)
    return jsonify(dataset)



# cleanup tasks
def cleanup_task():
    if not sf.is_closed():
        sf_disconnect(sf)
        print("SF connection closed.")


atexit.register(cleanup_task)


if __name__ == "__main__":
    app.run(debug=False)
