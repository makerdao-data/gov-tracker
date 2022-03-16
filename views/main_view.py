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

import os
import json
from flask import render_template

from connectors.sf import sf_connect
from utils.polls import get_all_polls
from utils.utils import async_queries
from utils.tables import html_table, link


def main_page_data(sf):
    # test snowflake connection and reconnect if necessary
    try:
        if sf.is_closed():
            sf = sf_connect()
        if sf.is_closed():
            raise Exception("Reconnection failed")

    except Exception as e:
        print(e)
        return dict(status="failure", data="Database connection error")

    try:
        result = async_queries(sf, [
            dict(query="SELECT * FROM MCD.TRACKERS.GOV_TRACKER",
                 id="gov_tracker")
        ])['gov_tracker'][0]

        return dict(
            status="success",
            data=dict(
                staked=result[0],
                active=result[1],
                last_vote=result[2],
                voters=json.loads(result[3])['data'],
                voters_num=result[4],
                yays=result[5],
                yays_num=result[6],
                polls=result[7],
                polls_num=result[8],
            ),
        )

    except Exception as e:
        print(e)
        return dict(status="failure", data="Backend error: %s" % e)


# flask view for the main page
def main_page_view(sf):

    # test snowflake connection and reconnect if necessary
    try:
        if sf.is_closed():
            sf = sf_connect()
        if sf.is_closed():
            raise Exception("Reconnection failed")

    except Exception as e:
        print(e)
        return dict(status="failure", data="Database connection error")

    last_update = sf.execute(f"""
        SELECT max(load_id)
        FROM {os.getenv("MCDGOV_DB", "mcd")}.internal.votes_scheduler;
    """).fetchone()

    try:

        return render_template("main.html",
                               refresh=last_update[0].__str__()[:19])

    except Exception as e:
        print(e)
        return render_template("error.html", error_message=str(e))
