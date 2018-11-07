#!/usr/bin/python3
"""
Background server-side script to measure distance on gpio, store
or just use bogus rands

Copyright 2018, David Lenkner
"""
import argparse
import random
import time
from webapp.database_utils import get_database_cnx
from datetime import datetime


READ_PAUSE = 0.1  # seconds
RAND_MULTIPLIER = 5.5  # works with a mult_over of 5 default

def main(source: str):
    """Loop and store data indefinitely"""
    cnx = get_database_cnx()
    cursor = cnx.cursor()

    quer_distas = ("INSERT INTO distances "
                   "(t, distance) "
                   "VALUES (%s, %s)")

    while True:
        ts = datetime.now().timestamp()
        if source == 'rands':
            val = random.random() * RAND_MULTIPLIER
        else:
            val = 0.0  # TODO fill in later

        data = (ts, val)
        print(data)
        cursor.execute(quer_distas, data)
        cnx.commit()

        time.sleep(READ_PAUSE)
    
    print("Done.")  # Never clean up if ctl-c is only option, but oh well


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data storage loop for Ceiling Game')
    parser.add_argument('--source', help='Data source',
                        choices=['rands', 'sensor'], required=True)
    args = parser.parse_args()
    main(args.source) 
