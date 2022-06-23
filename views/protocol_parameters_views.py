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
from flask import render_template
from connectors.sf import sf_connect
from utils.tables import html_table, link


def parameters_data_view(sf):

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

        parameters_query = f"""
        SELECT block, timestamp, tx_hash, source, parameter, ilk, from_value, to_value
        FROM maker.public.parameters
        ORDER BY block;
        """

        parameters = sf.execute(parameters_query).fetchall()

        # prepare output data
        parameters_data = []
        for block, timestamp, tx_hash, spell, parameter, ilk, from_value, to_value in parameters:
            parameters_data.append(
                dict(
                    BLOCK=block,
                    TIMESTAMP=timestamp,
                    TX_HASH=link(tx_hash, f"https://etherscan.io/tx/{tx_hash}", f"transaction overview", new_window=True),
                    SPELL=link(spell, f"https://etherscan.io/address/{spell}", f"spell address", new_window=True),
                    PARAMETER=parameter,
                    ILK=ilk,
                    FROM_VALUE=from_value,
                    TO_VALUE=to_value
                )
            )

        return dict(
            status="success",
            data=dict(
                parameters=parameters_data
            ),
        )

    except Exception as e:
        print(e)
        return dict(status="failure", data="Backend error: %s" % e)


# flask view for the parameters page
def parameters_page_view(sf):

    # test snowflake connection and reconnect if necessary
    try:
        if sf.is_closed():
            sf = sf_connect()
        if sf.is_closed():
            raise Exception("Reconnection failed")

    except Exception as e:
        print(e)
        return dict(status="failure", data="Database connection error")

    last_update = sf.execute(
        f"""
        SELECT max(load_id)
        FROM {os.getenv("MCDGOV_DB", "mcd")}.internal.votes_scheduler;
    """
    ).fetchone()

    try:

        return render_template("parameters.html", refresh=last_update[0].__str__()[:19])

    except Exception as e:
        print(e)
        return render_template("error.html", error_message=str(e))