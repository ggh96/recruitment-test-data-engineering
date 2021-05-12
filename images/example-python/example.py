#!/usr/bin/env python
"""
solution with denormalized(original shape) tables
"""
import csv
import json
import sqlalchemy
from sqlalchemy import Table, Column, VARCHAR, Integer, Date


# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@localhost/codetest?charset=utf8mb4", encoding='utf-8')
connection = engine.connect()
metadata = sqlalchemy.schema.MetaData(engine)


def create_people(meta):
    """
    to create people table

    :param meta: Metadata for connection
    :return: sqlalchemy table
    """
    temp = Table(
        'people', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('given_name', VARCHAR(50)),
        Column('family_name', VARCHAR(50)),
        Column('date_of_birth', Date),
        Column('place_of_birth', VARCHAR(50))
    )

    return temp


def create_places(meta):
    """
    to create places table

    :param meta: Metadata for connection
    :return: sqlalchemy table
    """
    temp = Table(
        'places', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('city', VARCHAR(50)),
        Column('county', VARCHAR(50)),
        Column('country', VARCHAR(50))
    )

    return temp


def writer(path, table, sample_size=None, conn=connection):
    """
    to insert values to mysql
    suggestion: bulk insert for larger data

    :param path: path to the csv file
    :param table: sqlalchemy table instance
    :param sample_size: int - number of samples to insert, None - entire data
    :param conn: connection instance
    :return: None
    """
    i = 0
    with open(path, encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            try:
                conn.execute(table.insert().values((None,) + tuple(row)))
            except Exception as e:
                print(e)
                print(row)

            if sample_size:
                i += 1
                if i >= sample_size:
                    break

    return None


# query string to count number of instances per group
summary_query = """
    select pl.`country`, count(*) as n_of_births
    from people as pp
    left join places as pl
    on pp.place_of_birth = pl.city
    group by pl.country
    ;
"""

if __name__ == "__main__":
    # drop tables to create new one's later
    connection.execute("drop tables if exists people, places;")

    # create table instances, add to th db
    places = create_places(metadata)
    people = create_people(metadata)
    metadata.create_all()

    # insert values
    writer('../../data/people.csv', people, sample_size=200, conn=connection)
    writer('../../data/places.csv', places, sample_size=None, conn=connection)

    # execute summary query
    output = connection.execute(summary_query)

    # write as output.json {country:count}
    with open('../../data/summary_output.json', 'w') as f:
        rows = [{row[0]: row[1]} for row in output]
        json.dump(rows, f, separators=(',', ':'))

    # with open("./schema.sql", 'r') as s:
    #     q = s.read()
    #     connection.execute(q)
