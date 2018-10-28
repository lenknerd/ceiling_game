#!/usr/bin/python3
# Just a test

import logging
from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'


@app.route('/insert_test', methods=['POST'])
def insert_test():
    # f = request.form
    app.logger.debug('hey requested')
    v = request.values
    for key in v.keys():
        app.logger.debug(key)
        app.logger.debug(v['n'])
    
    # app.logger.info('hey here info requested')
    # for key in f.keys():
    #    for value in f.getlist(key):
    #        app.logger.debug(key)
    #        app.logger.info(key)
    return "You did a request."


if __name__ == '__main__':
    handler = RotatingFileHandler('ceiling_game_debug.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0')
