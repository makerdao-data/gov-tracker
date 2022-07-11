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
from config import MAP


def parameters_list_data_view(sf):

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
        SELECT distinct parameter
        FROM maker.public.parameters
        ORDER BY parameter;
        """

        parameters = sf.execute(parameters_query).fetchall()

        # prepare output data
        parameters_data = []
        for parameter in parameters:
            
            p = parameter[0].split('.')

            address = None
            contract_name = None
            category = None
            type = None
            info = None
            if p[0] in MAP:
                address = MAP[p[0]]['address']
                contract_name = MAP[p[0]]['contract_name']
                category = MAP[p[0]]['category']
                type = MAP[p[0]]['type']
                info = MAP[p[0]]['info']

            parameters_data.append(
                dict(
                    DICU_PARAMETER_NAME=parameter[0],
                    CONTRACT=p[0],
                    PARAMETER=p[-1],
                    ADDRESS=address,
                    CONTRACT_NAME=contract_name,
                    CATEGORY=category,
                    TYPE=type,
                    INFO= info,
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


# flask view for the parameters list
def parameters_list_view(sf):

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

        return render_template("parameters_list.html", refresh=last_update[0].__str__()[:19])

    except Exception as e:
        print(e)
        return render_template("error.html", error_message=str(e))