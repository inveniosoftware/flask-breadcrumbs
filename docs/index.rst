===================
 Flask-Breadcrumbs
===================
.. currentmodule:: flask_breadcrumbs

.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/flask-breadcrumbs">
            <img src="https://travis-ci.org/inveniosoftware/flask-breadcrumbs.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/flask-breadcrumbs">
            <img src="https://coveralls.io/repos/inveniosoftware/flask-breadcrumbs/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>


Flask-Breadcrumbs is a Flask extension that adds support for generating
site breadcrumb navigation.

Contents
--------

.. contents::
   :local:
   :depth: 1
   :backlinks: none


.. _installation:

Installation
============

Flask-Breadcrumbs is on PyPI so all you need is:

.. code-block:: console

    $ pip install Flask-Breadcrumbs

The development version can be downloaded from `its page at GitHub
<http://github.com/inveniosoftware/flask-breadcrumbs>`_.

.. code-block:: console

    $ git clone https://github.com/inveniosoftware/flask-breadcrumbs.git
    $ cd flask-breadcrumbs
    $ python setup.py develop
    $ ./run-tests.sh

Requirements
^^^^^^^^^^^^

Flask-Breadcrumbs has the following dependencies:

* `Flask-Menu <https://pypi.python.org/pypi/Flask-Menu>`_
* `Flask <https://pypi.python.org/pypi/Flask>`_
* `six <https://pypi.python.org/pypi/six>`_

Flask-Breadcrumbs requires Python version 2.6, 2.7 or 3.3+.


.. _usage:

Usage
=====

This guide assumes that you have successfully installed ``Flask-Breadcrumbs``
package already.  If not, please follow the :ref:`installation`
instructions first.

Simple Example
^^^^^^^^^^^^^^

Here is a simple Flask-Breadcrumbs usage example:

.. code-block:: python

    from flask import Flask
    from flask.ext import breadcrumbs

    app = Flask(__name__)

    # Initialize Flask-Breadcrumbs
    breadcrumbs.Breadcrumbs(app=app)

    @app.route('/')
    @breadcrumbs.register_breadcrumb(app, '.', 'Home')
    def index():
        pass

    if __name__ == '__main__':
        app.run(debug=True)


Save this as app.py and run it using your Python interpreter.

.. code-block:: console

    $ python app.py
     * Running on http://127.0.0.1:5000/

.. _templating:

Templating
^^^^^^^^^^

By default, a proxy object to `current_breadcrumbs` is added to your Jinja2
context as `breadcrumbs` to help you with creating navigation bar.
For example:

.. code-block:: jinja

    <div>
    {%- for breadcrumb in breadcrumbs -%}
        <a href="{{ breadcrumb.url }}">{{ breadcrumb.text }}</a>
        {{ '/' if not loop.last }}
    {%- endfor -%}
    </div>

.. _blueprints:

Blueprint Support
^^^^^^^^^^^^^^^^^

The most import part of an modular Flask application is Blueprint. You
can create one for your application somewhere in your code and decorate
your view function, like this:

.. code-block:: python

    from flask import Blueprint
    from flask.ext import breadcrumbs

    account = Blueprint('account', __name__, url_prefix='/account')

    @account.route('/')
    @breadcrumbs.register_breadcrumb(account, '.', 'Your account')
    def index():
        pass


Default breadcrumb root
=======================

Sometimes you want to combine multiple blueprints and organize the
navigation to certain hierarchy using function
:func:`~flask.ext.breadcrumbs.default_breadcrumb_root`.

.. code-block:: python

    from flask import Blueprint
    from flask.ext import breadcrumbs

    social = Blueprint('social', __name__, url_prefix='/social')
    breadcrumbs.default_breadcrumb_root(social, '.account')

    @social.route('/list')
    @breadcrumbs.register_breadcrumb(social, '.list', 'Social networks')
    def list():
        pass

As a result of this, your `current_breadcrumbs` object with contain list
with 3 items during processing request for `/social/list`.

.. code-block:: python

    from example import app
    from flask.ext import breadcrumbs
    import account
    import social
    app.register_blueprint(account.bp_account)
    app.register_blueprint(social.bp_social)
    with app.test_client() as c:
        c.get('/social/list')
        assert map(lambda x: x.url,
                   list(breadcrumbs.current_breadcrumbs)) == [
                      '/', '/account/', '/social/list']


.. _api:

API
===

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

Flask extension
^^^^^^^^^^^^^^^

.. module:: flask.ext.breadcrumbs

.. autoclass:: Breadcrumbs
   :members:

Decorators
^^^^^^^^^^

.. autofunction:: register_breadcrumb

.. autofunction:: default_breadcrumb_root

Proxies
^^^^^^^

.. data:: current_breadcrumbs

   List of breadcrumbs for current request.

.. data:: breadcrumbs_root_path

   Name of breadcrumbs root path.


.. include:: ../CHANGES

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS
