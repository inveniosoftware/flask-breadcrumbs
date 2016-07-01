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
    from flask_breadcrumbs import Breadcrumbs, register_breadcrumbs

    app = Flask(__name__)

    # Initialize Flask-Breadcrumbs
    Breadcrumbs(app=app)

    @app.route('/')
    @register_breadcrumb(app, '.', 'Home')
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

.. _variables:

Variable rules
^^^^^^^^^^^^^^

For routes with a variable part, a dynamic list constructor can be used to
create a more meaningful breadcrumb. In the example below, the User's primary
key is used to create a breadcrumb displaying their name.

.. code-block:: python

    from flask import request, render_template

    def view_user_dlc(*args, **kwargs):
        user_id = request.view_args['user_id']
        user = User.query.get(user_id)
        return [{'text': user.name, 'url': user.url}]

    @app.route('/users/<int:user_id>')
    @breadcrumbs.register_breadcrumb(app, '.user.id', '',
                                     dynamic_list_constructor=view_user_dlc)
    def view_user(user_id):
        user = User.query.get(user_id)
        return render_template('user.html', user=user)

.. _blueprints:

Blueprint Support
^^^^^^^^^^^^^^^^^

The most import part of a modular Flask application is Blueprint. You
can create one for your application somewhere in your code and decorate
your view function, like this:

.. code-block:: python

    from flask import Blueprint
    from flask_breadcrumbs import register_breadcrumbs

    account = Blueprint('account', __name__, url_prefix='/account')

    @account.route('/')
    @register_breadcrumb(account, '.', 'Your account')
    def index():
        pass

Combining Multiple Blueprints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you want to combine multiple blueprints and organise the
navigation to certain hierarchy.  This can be achieved by using the
function :func:`~flask_breadcrumbs.default_breadcrumb_root`.

.. code-block:: python

    from flask import Blueprint
    from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumbs

    social = Blueprint('social', __name__, url_prefix='/social')
    default_breadcrumb_root(social, '.account')

    @social.route('/list')
    @register_breadcrumb(social, '.list', 'Social networks')
    def list():
        pass

As a result of this, your `current_breadcrumbs` object with contain list
with 3 items during processing request for `/social/list`.

.. code-block:: python

    from example import app
    from flask_breadcrumbs import current_breadcrumbs
    import account
    import social
    app.register_blueprint(account.bp_account)
    app.register_blueprint(social.bp_social)
    with app.test_client() as c:
        c.get('/social/list')
        assert map(lambda x: x.url,
                   list(current_breadcrumbs)) == [
                      '/', '/account/', '/social/list']

Advanced Examples
=================

Use with MethodViews and Blueprints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No routes are used in this example. Take note of the odd syntax for explicitly
calling the decorator.

.. code-block:: python

    from flask import Flask, render_template, Blueprint
    from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
    from flask.views import MethodView

    app = Flask(__name__)
    Breadcrumbs(app=app)
    bp = Blueprint('bp', __name__,)


    class LevelOneView(MethodView):
        def get(self):
            return render_template('template.html')


    class LevelTwoView(MethodView):
        def get(self):
            return render_template('template.html')

    # Define the view by calling the decorator on its own,
    # followed by the view inside parenthesis
    level_one_view = register_breadcrumb(bp, 'breadcrumbs.', 'Level One')(
        LevelOneView.as_view('first')
    )
    bp.add_url_rule('/one', view_func=level_one_view)  # Add the rule to the blueprint

    level_two_view = breadcrumbs.register_breadcrumb(bp, 'breadcrumbs.two', 'Level Two')(
        LevelOneView.as_view('second')
    )
    bp.add_url_rule('/two', view_func=level_two_view)

    app.register_blueprint(bp)


.. code-block:: jinja

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Example</h1>
        <div>
            {%- for breadcrumb in breadcrumbs -%}
                <a href="{{ breadcrumb.url }}">{{ breadcrumb.text }}</a>
                {{ '/' if not loop.last }}
            {%- endfor -%}
        </div>
    </body>
    </html>

.. _api:

API
===

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

Flask extension
^^^^^^^^^^^^^^^

.. module:: flask_breadcrumbs

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


.. include:: ../CHANGES.rst

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS.rst
