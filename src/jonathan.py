# -*- coding: utf-8 -*-

# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from flask.helpers import send_from_directory

# configuration
DEBUG = True
SECRET_KEY = 'development key'
MEDIA_DIR = 'media/'
MEDIA_URL = '/media/'
PLAYER = "divx"
AUTOPLAY = "1"
TITLE = "El Jonathan"
VALID_EXTENSIONS = [ '.mpg', '.mpeg', '.ogg', '.ogm', '.ogv', '.divx', '.avi', '.webm', '.mkv', '.mov' ]

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.template_filter('dirname')
def dirname_filter(path):
    return os.path.dirname(path)

@app.template_filter('filename')
def filename_filter(path):
    return os.path.basename(path)

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def home(path):
    pwd = os.path.join(MEDIA_DIR,path)
    if os.path.isdir(pwd):
        entries = os.listdir(pwd)

        dirs = [ entry for entry in entries if os.path.isdir(os.path.join(pwd, entry)) ]
        files = [ entry for entry in entries if os.path.isfile(os.path.join(pwd, entry)) ]

        # Filter files by extension
        files = filter(lambda x: os.path.splitext(x)[1] in VALID_EXTENSIONS, files)

        return render_template('listdir.html', path=path, dirs=dirs, files=files, title=TITLE)
    elif os.path.isfile(pwd):
        if not os.path.splitext(path)[1] in VALID_EXTENSIONS:
            abort(404)
        return render_template('playfile.html', path=path, player=PLAYER, autoplay=AUTOPLAY, title=TITLE)
    else:
        abort(404)

@app.route(MEDIA_URL + '/<path:filename>', endpoint='media')
def send_media_file(filename):
    return send_from_directory(MEDIA_DIR, filename)

if __name__ == '__main__':
    app.run()
