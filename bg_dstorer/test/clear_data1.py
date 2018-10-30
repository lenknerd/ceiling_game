#!/usr/bin/python3
from datetime import datetime
import mysql.connector
import random


# Declare connector
cnx = mysql.connector.connect(user='root', password='red6warm',
                              host='127.0.0.1',
                              database='ceiling_game')
cursor = cnx.cursor()

q_clear_evts = "DELETE FROM events"

q_clear_dists = "DELETE FROM distances"

cursor.execute(q_clear_evts)
cnx.commit()

cursor.execute(q_clear_dists)
cnx.commit()

print("Cleared two tables.")

cnx.close()
