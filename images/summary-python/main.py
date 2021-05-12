#!/usr/bin/env python
"""
solution with denormalized(original shape) tables
"""

import json
import sqlalchemy


# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@localhost/codetest?charset=utf8mb4", encoding='utf-8')
connection = engine.connect()
metadata = sqlalchemy.schema.MetaData(engine)

# query string to count number of instances per group
summary_query = """
    select pl.`country`, count(*) as n_of_births
    from people as pp
    left join places as pl
    on pp.place_of_birth = pl.city
    group by pl.country
    ;
"""
print(__name__)

if __name__ == "__main__":
    # execute summary query
    output = connection.execute(summary_query)
    print(output)

    # write as output.json {country:count}
    with open('../../data/summary_output.json', 'w') as f:
        rows = [{row[0]: row[1]} for row in output]
        json.dump(rows, f, separators=(',', ':'))

    # with open("./schema.sql", 'r') as s:
    #     q = s.read()
    #     connection.execute(q)
