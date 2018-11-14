#!/usr/bin/python3
"""
Interface for Ceiling Game - a ball game with a digital component

Copyright 2018, David Lenkner
"""

import database_utils
import game_types
import logging
from actions import ActionType, commit_action
from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler


app = Flask(__name__)


DEBUG_FILENAME = 'cg_debug.log'


@app.route('/')
def index():
    """At start, clear out database for speed, """
    database_utils.wipe_tables()
    commit_action(ActionType.START_GAME)
    return render_template('index.html')


@app.route('/commit_score')
def commit_score():
    """You just finished a turn throwing, commit any score and game moves on"""
    app.logger.debug("Committing score...")
    commit_action(ActionType.COMMIT_TURN_SCORE)
    # Return element not actually used now but np
    return '<p>All good.</p>'


@app.route('/void_turn')
def void_turn():
    """Say you hit the sensor (accelerom not added yet) or other reason to void turn

    void the turn and let play continue to next player"""
    app.logger.debug("Voiding turn...")
    commit_action(ActionType.VOID_TURN_SCORE)
    # Return element not actually used now but np
    return '<p>Voided turn.</p>'


@app.route('/status_update')
def status_update():
    # Use the game class to get data - later more dynamic for diff types of configs
    game = game_types.BowlingTwoPlayer()
    table, scores_by_player = game.get_status()
    # Render that data
    return render_template('status_table.html', table=table, scores_by_player=scores_by_player)


if __name__ == '__main__':
    handler = RotatingFileHandler(DEBUG_FILENAME, maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
