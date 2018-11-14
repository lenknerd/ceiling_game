#!/usr/bin/python3
"""
Background server-side script to measure distance on gpio, store
or just use bogus rands.  For now just run until Enter key

Copyright 2018, David Lenkner
"""
import argparse
import random
import RPi.GPIO as GPIO
import sys
import time
from datetime import datetime
from select import select
from webapp.database_utils import get_database_cnx


# Which GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

# Seconds to pause between reads
READ_PAUSE = 0.1

# In random-number no-sensor mode, just generate rands on this scale
RAND_MULTIPLIER = 5.5


def distance_cm():
    """Measure distance to nearest object via HC-SR04"""
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Poll for time of transmitted sound
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Poll for time of reflected sound arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Substract to get time of travel out and back, then multiply
    # by speed of sound (34300 cm/s) for round trip distance, and
    # divide by two for one way (dist to obj).  34300 / 2 = 17150
    # and divide by 2, because there and back.
    return (stop_time - start_time) * 17150


def main(source: str):
    """Loop and store data indefinitely"""
    cnx = get_database_cnx()
    cursor = cnx.cursor()

    quer_distas = ("INSERT INTO distances "
                   "(t, distance) "
                   "VALUES (%s, %s)")

    if source == 'sensor':
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        # GPIO direction (IN / OUT) on those pins
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)


    print("Starting data storage loop. Press enter to exit loop.")
    while True:
        ts = datetime.now().timestamp()
        if source == 'rands':
            val = random.random() * RAND_MULTIPLIER
        else:
            val = distance_cm()

        data = (ts, val)
        print(data)
        cursor.execute(quer_distas, data)
        cnx.commit()

        # Wait a bit before next loop, exit if hit return
        r, w, x = select([sys.stdin], [], [], READ_PAUSE)
        if r:
            break

    print("Closing up...")
    if source == 'sensor':
        GPIO.cleanup()
    cnx.close()
    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data storage loop for Ceiling Game')
    parser.add_argument('--source', help='Data source',
                        choices=['rands', 'sensor'], required=True)
    args = parser.parse_args()
    main(args.source) 
