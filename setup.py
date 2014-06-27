# -*- coding: utf-8 -*-
##
## This file is part of Flask-Breadcrumbs
## Copyright (C) 2013, 2014 CERN.
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

from setuptools import setup

setup(
    name='Flask-Breadcrumbs',
    version='0.1.0',
    url='http://github.com/inveniosoftware/flask-breadcrumbs/',
    license='GPLv2',
    author='Invenio collaboration',
    author_email='info@invenio-software.org',
    description='Flask-Breadcrumbs is a Flask extension that adds support '
        'for generating site breadcrumb navigation.',
    long_description=open('README.rst').read(),
    packages=['flask_breadcrumbs'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'six',
        'Flask-Menu>=0.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Development Status :: 5 - Production/Stable'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'coverage'],
)
