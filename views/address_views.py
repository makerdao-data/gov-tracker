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
from datetime import datetime, timezone

from connectors.sf import sf_connect
from utils.utils import async_queries
from utils.tables import link
from utils.polls import get_all_polls

from graphs.stake_graph import stake_graph


def address_data_view(sf, address):

    # test snowflake connection and reconnect if necessary
    try:
        if sf.is_closed():
            sf = sf_connect()
        if sf.is_closed():
            raise Exception('Reconnection failed')

    except Exception as e:
        print(e)
        return dict(status='failure', data='Database connection error')

    try:

        # SQL injection prevention
        if not(len(address) == 42 and address[:2] == '0x'):
            return dict(status='failure', data='Unknown address')

        operations_query = f"""
            select timestamp, tx_hash, dstake, operation, yay, option, dapproval, decisive, order_index
            from {os.getenv("MCDGOV_DB", "mcd")}.public.votes 
            where lower(voter) = '{address}' 
            order by timestamp, operation;
        """

        titles_query = f"""
            select code, title
            from {os.getenv("MCDGOV_DB", "mcd")}.internal.yays;
        """

        all_queries = [
            dict(query=operations_query, id='operations'),
            dict(query=titles_query, id='titles'),
        ]

        # snowflake data ingestion

        sf_responses = async_queries(sf, all_queries)
        operations = sf_responses['operations']
        titles = sf_responses['titles']

        titles = {y[0]: y[1] for y in titles}
        titles['0x0000000000000000000000000000000000000000'] = 'Activate DSChief v1.2'

        polls_metadata = get_all_polls()

        voter_operations = []
        x = []
        y = []
        labels = []
        stake = 0
        for operation in operations:

            stake += operation[2] or 0
            poll = operation[4]
            title = titles.get(operation[4], operation[4]) or ''

            if operation[3] in ('FINAL_CHOICE', 'CHOOSE'):
                votes = operation[5].split(',')
                if poll in polls_metadata:
                    options = '<br>'.join([str(polls_metadata[poll][1][vote]) if vote in polls_metadata[poll][1] else 'Not valid' for vote in votes])
                else:
                    options = '<br>'.join([str(vote) for vote in votes])
                poll_link = link(title, '/poll/%s' % poll, title) if poll else ''
            else:
                options = ''
                poll_link = link(title, '/yay/%s' % poll, title) if poll else ''

            if operation[3]:
                if operation[3] != 'FINAL_CHOICE':
                    ops = link(operation[3], 'https://ethtx.info/%s' % operation[1], '%s transaction' % operation[3], new_window=True)
                else:
                    ops = operation[3]
            else:
                ops = ''

            operation_row = [operation[0],
                            ops,
                            "{0:,.2f}".format(operation[2]) if operation[2] else '',
                            "{0:,.2f}".format(stake),
                            poll_link,
                            options,
                            'YES' if operation[7] else '',
                            operation[8]]

            x.append(operation[0])
            y.append(stake)
            labels.append(operation[3])

            voter_operations.append(operation_row)

        x.append(datetime.utcnow().replace(tzinfo=timezone.utc))
        y.append(stake)

        operations_num = "{0:,d}".format(len(voter_operations))

        plot = stake_graph(x, y, labels)

        # prepare output data
        operations_data = []
        for operation in voter_operations:
            operations_data.append(dict(
                TIME=operation[0].strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(operation[7]),
                OPERATION=operation[1],
                TRANSFER=operation[2],
                STAKE=operation[3],
                POLL=operation[4],
                OPTIONS=operation[5],
                DECISIVE=operation[6]
            ))

        return dict(status='success',
                    data=dict(operations=operations_data,
                              operations_num=operations_num,
                              plot=plot))

    except Exception as e:
        print(e)
        return dict(status='failure', data='Backend error: %s' % e)


# flask view for the address page
def address_page_view(sf, address):

    # test snowflake connection and reconnect if necessary
    try:
        if sf.is_closed():
            sf = sf_connect()
        if sf.is_closed():
            raise Exception('Reconnection failed')

    except Exception as e:
        print(e)
        return dict(status='failure', data='Database connection error')

    try:

        # SQL injection prevention
        if not(len(address) == 42 and address[:2] == '0x'):
            return render_template('unknown.html', object_name='address', object_value=address)

        address_data = sf.execute(f"""SELECT v.voter, '', v.stake, v.yay1, v.yay2, v.yay3, v.yay4, v.yay5, v.since, v.last_voting
                                     FROM {os.getenv("MCDGOV_DB", "mcd")}.public.current_voters v  
                                     WHERE lower(v.voter) = \'%s\'; """ % address).fetchall()

        if len(address_data) != 1:
            return render_template('unknown.html', object_name='address', object_value=address)

        address_data = address_data[0]

        proxy = sf.execute(f"""
            select *
            from {os.getenv("MCDGOV_DB", "mcd")}.internal.stg_proxies
            where lower(hot) = lower('{address}')
            order by timestamp desc
            limit 1;
        """).fetchone()

        vote_proxy = ''
        if proxy:
            if proxy[8] != 'break':
                vote_proxy = proxy[7]

        last_update = sf.execute(f"""
            SELECT max(load_id)
            FROM {os.getenv("MCDGOV_DB", "mcd")}.internal.votes_scheduler
        """).fetchone()

        return render_template(
            'address.html',
            address=address_data[0],
            stake="{0:,.2f}".format(address_data[2]) if address_data[2] else '0.00',
            since=address_data[8].strftime("%Y-%m-%d") if address_data[8] else '',
            last_vote=address_data[9].strftime("%Y-%m-%d %H:%M:%S") if address_data[9] else '',
            refresh=last_update[0].__str__()[:19],
            vote_proxy= vote_proxy
        )

    except Exception as e:
        print(e)
        return render_template(
            'error.html',
            error_message=str(e)
        )