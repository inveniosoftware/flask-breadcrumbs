# -*- coding: utf-8 -*-
#
# This file is part of Flask-Breadcrumbs
# Copyright (C) 2013, 2014, 2016 CERN.
#
# Flask-Breadcrumbs is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-Breadcrumbs adds support for generating site breadcrumb navigation."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'mock>=1.0.0',
    'pytest-invenio>=1.4.0',
]

extras_require = {
    'docs': [
        'Sphinx>=3',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=3.0.0',
]

install_requires = [
    'Flask>=1.0.4',
    'six>=1.12.0',
    'Flask-Menu>=0.2'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('flask_breadcrumbs', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='Flask-Breadcrumbs',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio metadata',
    license='BSD',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/flask-breadcrumbs/',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 5 - Production/Stable'
    ],
)
