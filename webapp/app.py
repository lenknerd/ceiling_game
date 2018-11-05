#!/usr/bin/python3
"""
Interface for Ceiling Game - a ball game with a digital component

Copyright 2018, David Lenkner
"""

import actions
import game_types
import logging
from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler


app = Flask(__name__)


@app.route('/')
def index():
    # Start game, clear table of old stuff, return
    return render_template('index.html')


@app.route('/commit_score')
def commit_score():
    # Commit a yay-score action


@app.route('/void_score')
def void_score():
    # Void a score action (i.e. hit sensor)


@app.route('/ajax_status_update')
def ajaxtest_mainpage():
    # Use the game type to render status back to user
    return render_template('ajaxtest_mainpage.html')


if __name__ == '__main__':
    handler = RotatingFileHandler('ceiling_game_debug.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
