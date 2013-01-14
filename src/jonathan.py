# -*- coding: utf-8 -*-

# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from flask.helpers import send_from_directory

import settings

# create our little application :)
app = Flask(__name__)
app.config.from_object(settings)

@app.template_filter('dirname')
def dirname_filter(path):
    return os.path.dirname(path)

@app.template_filter('filename')
def filename_filter(path):
    return os.path.basename(path)

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def display_path(path):
    real_path = os.path.join(app.config['MEDIA_DIR'], path)
    if os.path.isdir(real_path):
        return __display_directory(path)
    elif os.path.isfile(real_path):
        return __display_file(path)
    else:
        abort(404)

@app.route(app.config['MEDIA_URL'] + '/<path:filename>', endpoint='media')
def send_media_file(filename):
    __valid_path_extension_or_404(os.path.join(app.config['MEDIA_DIR'], filename))
    return send_from_directory(app.config['MEDIA_DIR'], filename)

def __display_directory(path):
    real_path = os.path.join(app.config['MEDIA_DIR'], path)

    (files, dirs) = __get_files_and_directories(real_path)

    dirs.sort()
    files.sort()

    files = __filter_files_without_valid_extension(files)

    return render_template('listdir.html', path=path, dirs=dirs, files=files, title=app.config['TITLE'])

def __display_file(path):
    __valid_path_extension_or_404(path)

    return render_template(
            'playfile.html',
            path=path,
            player=app.config['PLAYER'],
            autoplay=app.config['AUTOPLAY'],
            title=app.config['TITLE'],
            baseurl=app.config['BASE_URL']
    )

def __get_files_and_directories(real_path):
    entries = os.listdir(real_path)

    if app.config['IGNORE_POINT_PATH']:
        entries = filter(lambda x: x[0] != ".", entries)

    dirs = [ entry for entry in entries if os.path.isdir(os.path.join(real_path, entry).encode('utf-8')) ]
    files = [ entry for entry in entries if os.path.isfile(os.path.join(real_path, entry).encode('utf-8')) ]

    return (files, dirs)

def __filter_files_without_valid_extension(files):
    return filter(lambda x: os.path.splitext(x)[1] in app.config['VALID_EXTENSIONS'], files)

def __valid_path_extension_or_404(path):
    if not os.path.splitext(path)[1] in app.config['VALID_EXTENSIONS']:
        abort(404)

if __name__ == '__main__':
    app.run()
