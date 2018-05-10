#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from .admin import admin
from .web import web

app = Flask(__name__)
app.debug = True

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(web)
