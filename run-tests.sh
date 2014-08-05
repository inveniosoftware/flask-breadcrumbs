#!/bin/sh
##
## This file is part of Flask-Breadcrumbs
## Copyright (C) 2013, 2014 CERN.
##
## Flask-Breadcrumbs is free software; you can redistribute it and/or
## modify it under the terms of the Revised BSD License; see LICENSE
## file for more details.

coverage run setup.py test
coverage report -m
