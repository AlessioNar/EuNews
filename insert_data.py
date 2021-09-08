import pandas as pd
sources = pd.read_csv('sources.csv', index_col=False, delimiter = ',')
sources.head()

from db_credentials import connection

conn = connection()
cursor = conn.cursor()

import mysql.connector as msql

cursor.execute("DROP TABLE IF EXISTS sources;")

cursor.execute("""
CREATE TABLE sources (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(255),
  url varchar(514),
  status varchar(255)
);""")


print("Table is created....")

for i,row in sources.iterrows():
    #here %S means string values
    sql = "INSERT INTO sources (name, url, status) VALUES (%s,%s,%s);"
    cursor.execute(sql, tuple(row))
    print("Record inserted")
        # the connection is not auto committed by default, so we must commit to save our changes
    conn.commit()

event_sources = pd.read_csv('event_sources.csv', index_col=False, delimiter = ',')
event_sources.head()

cursor.execute("DROP TABLE IF EXISTS event_sources;")

cursor.execute("""
CREATE TABLE event_sources (
  id int PRIMARY KEY AUTO_INCREMENT,
  name varchar(255),
  url varchar(2048),
  status varchar(255)
);""")


print("Table is created....")

for i,row in event_sources.iterrows():
    #here %S means string values
    sql = "INSERT INTO event_sources (name, url, status) VALUES (%s,%s,%s);"
    cursor.execute(sql, tuple(row))
    print("Record inserted")
        # the connection is not auto committed by default, so we must commit to save our changes
    conn.commit()
