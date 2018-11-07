#!/usr/bin/python3
"""
Database functions and configuration

Copyright 2018, David Lenkner
"""
import mysql.connector

# This doesn't get you anything but game access to ceiling game...
# nothing of much import no need to bother
DB_USER='cguser'
DB_PASSWORD='cguser'

DB_NAME='ceiling_game'
DB_HOST='127.0.0.1'


def get_database_cnx():
    """Get a database connection"""
    return mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                                   host=DB_HOST, database=DB_NAME)


def wipe_tables():
    """At the beginning of a game, wipe tables for space"""
    cnx = get_database_cnx()
    cursor = cnx.cursor()

    q_clear_evts = "DELETE FROM events"
    cursor.execute(q_clear_evts)
    cnx.commit()

    q_clear_dists = "DELETE FROM distances"
    cursor.execute(q_clear_dists)
    cnx.commit()

    cnx.close()   
