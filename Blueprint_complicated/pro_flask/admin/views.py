#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import admin


@admin.route('/index')
def index():
    return 'Admin.Index'