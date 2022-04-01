from datetime import datetime


def pull_filtered_data(request, s, e, session, item):

    offset = int(request.args.get('offset'))

    s = datetime.utcfromtimestamp(int(s) - (offset*3600)).__str__()[:19]
    e = datetime.utcfromtimestamp(int(e) - (offset*3600)).__str__()[:19]

    query = session.query(item)
    query = query.filter(item.timestamp >= s).filter(item.timestamp <= e)

    spell = request.args.get('search_spell')
    if spell:
        query = query.filter(
            item.source.ilike(f'%{str(spell)}%')
        )

    parameter = request.args.get('search_parameter')
    if parameter:
        query = query.filter(
            item.parameter.ilike(f'%{str(parameter)}%')
        )
    
    ilk = request.args.get('search_ilk')
    if ilk:
        query = query.filter(
            item.ilk.ilike(f'%{str(ilk)}%')
        )
    
    return query