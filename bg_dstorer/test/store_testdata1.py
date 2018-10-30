#!/usr/bin/python3
from datetime import datetime
import mysql.connector
import random


# Define some test data
events = [(0, 'new_game_bowling1'),
	 (12.0, 'ok_next_turn'),
         (19.5, 'ok_next_turn'),
         (25.0, 'blewit_next_turn'),
         (54.2, 'ok_next_turn')]

valsts = [(0.5, 2.1),
          (3.0, 6.0),
          (9.0, 5.2),
          (13.0, 4.0),
          (16.0, 2.4),
          (20.0, 7.0),
          (21.5, 9.5),
          (23.0, 0.0),
          (27.0, 4.0),
          (54.7, 3.5)]

# Insert it
cnx = mysql.connector.connect(user='root', password='red6warm',
                              host='127.0.0.1',
                              database='ceiling_game')
cursor = cnx.cursor()

quer_events = ("INSERT INTO events "
               "(t, event_type) "
               "VALUES (%s, %s)")

quer_distas = ("INSERT INTO distances "
               "(t, distance) "
               "VALUES (%s, %s)")

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
