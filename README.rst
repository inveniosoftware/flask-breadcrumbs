===================
 Flask-Breadcrumbs
===================

.. image:: https://travis-ci.org/inveniosoftware/flask-breadcrumbs.png?branch=master
    :target: https://travis-ci.org/inveniosoftware/flask-breadcrumbs
.. image:: https://coveralls.io/repos/inveniosoftware/flask-breadcrumbs/badge.png?branch=master
    :target: https://coveralls.io/r/inveniosoftware/flask-breadcrumbs
.. image:: https://pypip.in/v/Flask-Breadcrumbs/badge.png
   :target: https://pypi.python.org/pypi/Flask-Breadcrumbs/
.. image:: https://pypip.in/d/Flask-Breadcrumbs/badge.png
   :target: https://pypi.python.org/pypi/Flask-Breadcrumbs/

About
=====
Flask-Breadcrumbs is a Flask extension that adds support for
generating site breadcrumb navigation.

Installation
============
Flask-Breadcrumbs is on PyPI so all you need is: ::

    pip install Flask-Breadcrumbs

Documentation
=============
Documentation is readable at http://flask-breadcrumbs.readthedocs.org or can be build using Sphinx: ::

    git submodule init
    git submodule update
    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the test suite is as simple as: ::

    python setup.py test

or, to also show code coverage: ::

    ./run-tests.sh
