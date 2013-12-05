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

"""
    flask.ext.breadcrumbs
    ---------------------

    Depends on `flask.ext.menu` extension.
"""

from werkzeug import LocalProxy
from flask import Blueprint, current_app, request
from flask.ext.menu import Menu, current_menu


def _lookup_current_function():
    return current_app.view_functions.get(request.endpoint)


def _lookup_current_blueprint():
    return current_app.blueprints.get(
        request.blueprint,
        current_app._get_current_object())

# context data
current_function = LocalProxy(_lookup_current_function)
current_blueprint = LocalProxy(_lookup_current_blueprint)


def default_breadcrumb_root(app, path):
    """Registers the default breadcrumb path for all endpoints in this blueprint.

    :param app: Flask Application or Blueprint instance.
    :param path: Path in the menu hierarchy.
        It should start with '.' to be relative to breadcrumbs root.
    """

    if path.startswith('.'):
        # Path relative to breadcrumb root
        bl_path = LocalProxy(lambda:
            (breadcrumb_root_path + path).strip('.'))
    else:
        bl_path = path

    app.__breadcrumb__ = bl_path



class Breadcrumbs(Menu):
    """
    Breadcrumb organizer for a Flask application.
    """

    def init_app(self, app, *args, **kwargs):
        super(self.__class__, self).init_app(app, *args, **kwargs)

        app.config.setdefault('BREADCRUMBS_ROOT', 'breadcrumbs')
        app.context_processor(Breadcrumbs.breadcrumbs_context_processor)

    # Proxy functions
    @staticmethod
    def breadcrumb_root_path():
        """
        Backend function for breadcrumb_root_path proxy.
        """
        return current_app.config.get('BREADCRUMBS_ROOT')

    @staticmethod
    def current_path():
        """
        Determines current location in menu hierarchy.
        Backend function for current_path proxy.
        """
        # str(...) because __breadcrumb__ can hold a LocalProxy
        if hasattr(current_function, '__breadcrumb__'):
            return str(getattr(current_function, '__breadcrumb__', ''))

        return Breadcrumbs.get_path(
            current_blueprint._get_current_object())

    @staticmethod
    def breadcrumbs():
        """
        Returns list of breadcrumbs.
        Backend function for breadcrumbs proxy.
        """
        # Construct breadcrumbs using their dynamic lists
        breadcrumb_list = []

        for entry in current_menu.list_path(
                breadcrumb_root_path, current_path) or []:
            breadcrumb_list += entry.dynamic_list

        return breadcrumb_list

    @staticmethod
    def breadcrumbs_context_processor():
        """Adds variable 'breadcrumbs' to template context.

        It contains the list of menu entries to render as breadcrumbs.
        """
        return dict(breadcrumbs=current_breadcrumbs)

    @staticmethod
    def get_path(app):
        """
        :return: Path to root of application's or bluerpint's branch.
        """
        return str(getattr(
            app,
            '__breadcrumb__',
            breadcrumb_root_path + (
                '.' + app.name if isinstance(app, Blueprint) else '')))

    @staticmethod
    def register_breadcrumb(app, path, text,
                            endpoint_arguments_constructor=None,
                            dynamic_list_constructor=None):
        """Decorate endpoints that should be displayed as a breadcrumb.

        :param app: Application or Blueprint which owns the function.
        :param path: Path to this item in menu hierarchy
            ("breadcrumbs." is automatically added).
        :param text: Text displayed as link.
        :param order: Index of item among other items in the same menu.
        :param endpoint_arguments_constructor: Function returning dict of
            arguments passed to url_for when creating the link.
        :param dynamic_list_constructor: Function returning a list of
            breadcrumbs to be displayed by this item. Every object should
            have 'text' and 'url' properties/dict elements.
        """

        # Resolve blueprint-relative paths
        if path.startswith('.'):
            def _evaluate_path():
                bl_path = Breadcrumbs.get_path(app)
                return (bl_path + path).strip('.')

            func_path = LocalProxy(_evaluate_path)

        else:
            func_path = path

        # Get standard menu decorator
        menu_decorator = Menu.register_menu(
            app, func_path, text, 0,
            endpoint_arguments_constructor=endpoint_arguments_constructor,
            dynamic_list_constructor=dynamic_list_constructor)

        def breadcrumb_decorator(f):
            """Applies standard menu decorator and assign breadcrumb."""
            f.__breadcrumb__ = func_path

            return menu_decorator(f)

        return breadcrumb_decorator

# Proxies
breadcrumb_root_path = LocalProxy(Breadcrumbs.breadcrumb_root_path)
current_path = LocalProxy(Breadcrumbs.current_path)
current_breadcrumbs = LocalProxy(Breadcrumbs.breadcrumbs)

# Decorators and API
register_breadcrumb = Breadcrumbs.register_breadcrumb
