.. _quickstart:

Quickstart
==========

This guide assumes you have successfully installed Flask-Breadcrumbs and
a working Flask application. If not, follow the Flask Quickstart guide.


A Minimal Example
-----------------

A minimal Flask-Breadcrumbs usage looks like this: ::

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


Save this as app.py and run it using your Python interpreter. ::

    $ python app.py
     * Running on http://127.0.0.1:5000/

