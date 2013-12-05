# -*- coding: utf-8 -*-
##
## This file is part of Flask-Breadcrumbs
## Copyright (C) 2013 CERN.
##
## Flask-Breadcrumbs is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Flask-Breadcrumbs is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Flask-Breadcrumbs; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.

from unittest import TestCase
from flask import Blueprint, Flask, request, url_for, render_template_string

from flask.ext.breadcrumbs import (Breadcrumbs,
                                   current_breadcrumbs,
                                   current_path,
                                   current_function,
                                   default_breadcrumb_root,
                                   register_breadcrumb)

breadcrumbs_tpl = """
{%- for breadcrumb in breadcrumbs -%}
{{ breadcrumb.text}},{{ breadcrumb.url}};
{%- endfor -%}
"""

class FlaskTestCase(TestCase):
    """
    Mix-in class for creating the Flask application
    """

    def setUp(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.logger.disabled = True
        self.app = app

    def tearDown(self):
        self.app = None


class TestBreadcrumbs(FlaskTestCase):

    def setUp(self):
        """Prepares breadcrumbs tree.

        Example::
            test
            |-- level2
            |   |-- level3
            |   |-- level3B

            foo (*blueprint*)
            |-- bar

        """
        super(TestBreadcrumbs, self).setUp()
        self.breadcrumbs = Breadcrumbs(self.app)

        @self.app.route('/test')
        @register_breadcrumb(self.app, '.', 'Test')
        def test():
            return 'test'

        @self.app.route('/level2')
        @register_breadcrumb(self.app, '.level2', 'Level 2')
        def level2():
            return 'level2'

        @self.app.route('/level3')
        @register_breadcrumb(self.app, '.level2.level3', 'Level 3')
        def level3():
            return 'level3'

        @self.app.route('/level3B')
        @register_breadcrumb(self.app, 'breadcrumbs.level2.level3B',
                             'Level 3B')
        def level3B():
            return render_template_string(breadcrumbs_tpl)

        @self.app.route('/missing')
        def missing():
            return 'missing'

        self.foo = Blueprint('foo', 'foo', url_prefix='/foo')

        @self.foo.route('/')
        @register_breadcrumb(self.foo, '.bar', 'Bar')
        def bar():
            return 'bar'

        @self.foo.route('/baz')
        @register_breadcrumb(self.foo, '.baz', 'Baz')
        def baz():
            return render_template_string(breadcrumbs_tpl)

        @self.foo.route('/missing')
        def missing2():
            return 'missing2'

        self.app.register_blueprint(self.foo)

    def tearDown(self):
        del self.app
        del self.foo
        del self.breadcrumbs

    def test_simple_app(self):
        Breadcrumbs(self.app)
        with self.app.test_client() as c:
            c.get('/test')
            self.assertEqual(current_path, 'breadcrumbs')
            self.assertEqual(current_breadcrumbs[-1].url, '/test')

    def test_default_breadcrumb_root(self):
        with self.app.test_client() as c:
            c.get('/foo/')
            self.assertEqual(current_path, 'breadcrumbs.foo.bar')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/')

        with self.app.test_client() as c:
            c.get('/foo/baz')
            self.assertEqual(current_path, 'breadcrumbs.foo.baz')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/baz')

    def test_set_default_breadcrumb_root_different_from_blueprint_name(self):
        default_breadcrumb_root(self.foo, '.fooo')

        with self.app.test_client() as c:
            c.get('/foo/')
            self.assertEqual(current_path, 'breadcrumbs.fooo.bar')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/')

        with self.app.test_client() as c:
            c.get('/foo/baz')
            self.assertEqual(current_path, 'breadcrumbs.fooo.baz')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/baz')

    def test_set_default_breadcrumb_root_as_dot(self):
        default_breadcrumb_root(self.foo, '.')

        with self.app.test_client() as c:
            c.get('/foo/')
            self.assertEqual(current_path, 'breadcrumbs.bar')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/')

        with self.app.test_client() as c:
            c.get('/foo/baz')
            self.assertEqual(current_path, 'breadcrumbs.baz')
            self.assertEqual(current_breadcrumbs[-1].url, '/foo/baz')

    def test_missing_breadcrumbs_detection(self):
        with self.app.test_client() as c:
            c.get('/missing')
            self.assertEqual(current_path, 'breadcrumbs')
            self.assertEqual(current_breadcrumbs[-1].url, '/test')

        with self.app.test_client() as c:
            c.get('/foo/missing')
            self.assertEqual(current_path, 'breadcrumbs.foo')
            self.assertEqual(current_breadcrumbs[-1].url, '#')

    def test_template_context(self):
        default_breadcrumb_root(self.foo, 'breadcrumbs')

        with self.app.test_client() as c:
            response = c.get('/level3B')
            self.assertEqual(response.data.decode('utf8'),
                             'Test,/test;Level 2,/level2;Level 3B,/level3B;')

        with self.app.test_client() as c:
            response = c.get('/foo/baz')
            self.assertEqual(response.data.decode('utf8'),
                             'Test,/test;Baz,/foo/baz;')
