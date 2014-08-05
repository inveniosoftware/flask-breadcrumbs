# -*- coding: utf-8 -*-
##
## This file is part of Flask-Breadcrumbs
## Copyright (C) 2013, 2014 CERN.
##
## Flask-Breadcrumbs is free software; you can redistribute it and/or
## modify it under the terms of the Revised BSD License; see LICENSE
## file for more details.

from setuptools import setup

setup(
    name='Flask-Breadcrumbs',
    version='0.1.1.dev20140801',
    url='http://github.com/inveniosoftware/flask-breadcrumbs/',
    license='BSD',
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
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 5 - Production/Stable'
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'coverage'],
)
