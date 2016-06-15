# -*- coding: utf-8 -*-
#
# This file is part of Flask-Breadcrumbs
# Copyright (C) 2016 CERN.
#
# Flask-Breadcrumbs is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Example documenting sample usage of Flask Breadcrumbs."""

from flask import Flask, render_template_string

from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

breadcrumbs_tpl = """
{%- for breadcrumb in breadcrumbs %}
  {{ breadcrumb.text}}, {{ breadcrumb.url}};<br/>
{%- endfor %}
"""

app = Flask(__name__)
Breadcrumbs(app=app)


@app.route('/')
@breadcrumbs.register_breadcrumb(app, '.', 'Home')
def index():
    """Home endpoint.

    It renders the following breadcrumbs:
    Home, /;
    """
    return render_template_string(breadcrumbs_tpl)


@app.route('/topic1.html')
@breadcrumbs.register_breadcrumb(app, '.topic1', 'Topic 1')
def topic1():
    """Topic 1 page.

    It renders the following breadcrumbs:
    Home,/;
    Topic 1,/topic1.html;
    """
    return render_template_string(breadcrumbs_tpl)


@app.route('/topic2.html')
@breadcrumbs.register_breadcrumb(app, '.topic2', 'Topic 2')
def topic2():
    """Topic 2 page.

    It renders the following breadcrumbs:
    Home,/;
    Topic 2,/topic1.html;
    """
    return render_template_string(breadcrumbs_tpl)


@app.route('/topic1/sub-topic.html')
@breadcrumbs.register_breadcrumb(app, '.topic1.sub_topic1', 'Sub-Topic 1')
def sub_topic1():
    """Sub-topic of Topic 1.

    It renders the following breadcrumbs:
    Home, /;
    Topic 1, /topic1.html;
    Sub-Topic 1, /topic1/topic2.html;
    """
    return render_template_string(breadcrumbs_tpl)
