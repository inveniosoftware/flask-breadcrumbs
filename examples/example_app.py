# -*- coding: utf-8 -*-
#
# This file is part of Flask-Breadcrumbs
# Copyright (C) 2013, 2014, 2015 CERN.
#
# Flask-Breadcrumbs is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Example documenting sample usage of Flask Breadcrumbs.

Depends on `flask_breadcrumbs` extension.
"""

from flask import Flask, render_template_string
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

breadcrumbs_tpl = """
{%- for breadcrumb in breadcrumbs -%}
{{ breadcrumb.text}}, {{ breadcrumb.url}};<br/>
{%- endfor -%}
"""

app = Flask(__name__)

# Initialize Flask-Breadcrumbs
breadcrumbs.Breadcrumbs(app=app)

@app.route('/')
@breadcrumbs.register_breadcrumb(app, '.', 'Home')
def index():
    """
    Endpoint.

    Render the following breadcrumbs:
    Home, /;
    """
    return render_template_string(breadcrumbs_tpl)

@app.route('/topic1.html')
@breadcrumbs.register_breadcrumb(app, '.topic1', 'Home')
def topic1():
    """
    Endpoint.

    Render the following breadcrumbs:
    Home,/;
    Home,/topic1.html;
    """
    return render_template_string(breadcrumbs_tpl)

@app.route('/topic2.html')
@breadcrumbs.register_breadcrumb(app, '.topic2', 'Home')
def topic2():
    """
    Endpoint.

    Render the following breadcrumbs:
    Home,/;
    Home,/topic2.html;
    """
    return render_template_string(breadcrumbs_tpl)

@app.route('/topic1/topic3.html')
@breadcrumbs.register_breadcrumb(app, '.topic1.topic3', 'Home')
@breadcrumbs.register_breadcrumb(app, '.topic2.topic3', 'Home')
def topic3():
    """
    Endpoint.

    Render the following breadcrumbs:
    Home, /;
    Home, /topic1.html;
    Home, /topic1/topic2.html;
    """
    return render_template_string(breadcrumbs_tpl)

if __name__ == '__main__':
    app.run(debug=True)
