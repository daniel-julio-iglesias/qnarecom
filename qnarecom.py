#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Main application module

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# microblog/
#   venv/
#   app/
#    __init__.py
#    routes.py
#  microblog.py

# Linux
# export FLASK_APP=qnarecom.py
# Windows
# set FLASK_APP=qnarecom.py

# flask run
# python qnarecom.py

# http://localhost:5000/
# http://localhost:5000/index

from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

