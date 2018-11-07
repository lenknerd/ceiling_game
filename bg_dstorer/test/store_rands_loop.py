#!/usr/bin/python3
from datetime import datetime
import mysql.connector
import random


# Insert it
cnx = mysql.connector.connect(user='cguser', password='cguser',
                              host='127.0.0.1',
                              database='ceiling_game')
cursor = cnx.cursor()

quer_distas = ("INSERT INTO distances "
               "(t, distance) "
               "VALUES (%s, %s)")

while True:
    tstamp = 
    print

for rec in events:
    print("Working on event:", rec)
    cursor.execute(quer_events, rec)
    cnx.commit()
    print(" committed.")

for rec in valsts:
    print("Working on dist:", rec)
    cursor.execute(quer_distas, rec)
    cnx.commit()
    print(" committed.")

cnx.close()
