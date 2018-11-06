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


@app.route('/')
def index():
    """At start, clear out database for speed, """
    database_utils.wipe_tables()
    return render_template('index.html')


@app.route('/commit_score')
def commit_score():
    """You just finished a turn throwing, commit any score and game moves on"""
    app.logger.debug("Committing score...")
    commit_action(ActionType.COMMIT_TURN_SCORE)


@app.route('/void_turn')
def void_turn():
    """Say you hit the sensor (accelerom not added yet) or other reason to void turn

    void the turn and let play continue to next player"""
    app.logger.debug("Voiding turn...")
    commit_action(ActionType.VOID_TURN_SCORE)


@app.route('/status_update')
def status_update():
    # Use the game class to get data - later more dynamic for diff types of configs
    game = game_types.CeilingGameConfig()
    tabl, sum_lines = game.get_status()
    # Render that data
    return render_template('summary_and_table.html', table=tabl, summary_lines=sum_lines)


if __name__ == '__main__':
    handler = RotatingFileHandler('ceiling_game_debug.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
