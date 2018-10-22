#!/usr/bin/python3
from datetime import datetime
import mysql.connector
from time import sleep
import random
import time


cnx = mysql.connector.connect(user='root', password='red6warm',
                              host='127.0.0.1',
                              database='ceiling_game')

cursor = cnx.cursor()

add_randnumb = ("INSERT INTO distances "
               "(t, distance) "
               "VALUES (%s, %s)")

for i in range(0,30):
    print("Working on index", i)
    # ts = datetime.now().second + (datetime.now().microsecond / 1.0e6)
    ts = datetime.now().timestamp()
    valn = random.random()
    dat_randnumb = (ts, valn)
    cursor.execute(add_randnumb, dat_randnumb)
    cnx.commit()
    print(" committed...")
    sleep(0.06)
        

cnx.close()
