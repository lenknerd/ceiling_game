#!/usr/bin/python3
"""
Webapp user actions on back end
Copyright 2018, David Lenkner
"""

import mysql.connector
from enum import Enum


class ActionType(Enum):
    """Different actions to be taken"""
    COMMIT_TURN_SCORE = 0
    VOID_TURN_SCORE = 1
    START_GAME = 2


def commit_action(a: ActionType):
    """Commit an action to database along with current timestamp
    
    Figure out sql_cursor type btw"""
    cnx = mysql.connector.connect(user='cguser', password='cguser',
                                  host='127.0.0.1',
                                  database='ceiling_game')
    cursor = cnx.cursor()
    ts = datetime.now().timestamp()
    
    quer = ("INSERT INTO events "
               "(t, event_type) "
               "VALUES (%s, %s) ")
    data = (ts, str(a.name))
    cursor.execute(quer, data)
    cnx.commit()
