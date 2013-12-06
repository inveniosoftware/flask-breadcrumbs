.. _templating:

Templating
==========

By default, a proxy object to `current_breadcrumbs` is added to your Jinja2
context as `breadcrumbs` to help you with creating navigation bar.
For example: ::

    <div>
    {%- for breadcrumb in breadcrumbs -%}
        <a href="{{ breadcrumb.url }}">{{ breadcrumb.text }}</a>
        {{ '/' if not loop.last }}
    {%- endfor -%}
    </div>

.. _blueprints:

Blueprint Support
=================

The most import part of an modular Flask application is Blueprint. You
can create one for your application somewhere in your code and decorate
your view function, like this: ::

    from flask import Blueprint
    from flask.ext import breadcrumbs

    bp_account = Blueprint('account', __name__, url_prefix='/account')

    @bp_account.route('/')
    @breadcrumbs.register_breadcrumb(bp_account, '.', 'Your account')
    def index():
        pass


Default breadcrumb root
-----------------------

Sometimes you want to combine multiple blueprints and organize the
navigation to certain hierarchy using function
:func:`~flask.ext.breadcrumbs.default_breadcrumb_root`. ::

    from flask import Blueprint
    from flask.ext import breadcrumbs

    bp_social = Blueprint('social', __name__, url_prefix='/social')
    breadcrumbs.default_breadcrumb_root(bp_social, '.account')

    @bp_account.route('/list')
    @breadcrumbs.register_breadcrumb(bp_social, '.list', 'Social networks')
    def list():
        pass

As a result of this, your `current_breadcrumbs` object with contain list
with 3 items during processing request for `/social/list`. ::

    >>> from example import app
    >>> from flask.ext import breadcrumbs
    >>> import account
    >>> import social
    >>> app.register_blueprint(account.bp_account)
    >>> app.register_blueprint(social.bp_social)
    >>> with app.test_client() as c:
    ...     c.get('/social/list')
    ...     assert map(lambda x: x.url,
    ...         list(breadcrumbs.current_breadcrumbs)) == \
    ...         ['/', '/account/', '/social/list']

