# -*- coding: utf-8 -*-
#
# This file is part of Flask-Breadcrumbs
# Copyright (C) 2013, 2014, 2015, 2016 CERN.
#
# Flask-Breadcrumbs is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Provide support for generating site breadcrumb navigation.

Depends on `flask_menu` extension.
"""

from flask import Blueprint, current_app, request
# pylint: disable=F0401,E0611
from flask_menu import Menu, register_menu, current_menu
# pylint: enable=F0401,E0611
from werkzeug.local import LocalProxy

from .version import __version__


def default_breadcrumb_root(app, path):
    """Register default breadcrumb path for all endpoints in this blueprint.

    :param app: The :class:`~flask.Flask` or :class:`flask.Blueprint` object.
    :type app: :class:`flask.Flask` or :class:`flask.Blueprint`
    :param path: Path in the menu hierarchy.
        It should start with '.' to be relative to breadcrumbs root.
    """
    if path.startswith('.'):
        # Path relative to breadcrumb root
        bl_path = LocalProxy(lambda: (
            breadcrumb_root_path + path).strip('.'))
    else:
        bl_path = path

    app.__breadcrumb__ = bl_path


class Breadcrumbs(Menu, object):
    """Breadcrumb organizer for a :class:`~flask.Flask` application."""

    def __init__(self, app=None, init_menu=True):
        """Initialize Breadcrumb extension.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        :param init_menu: If Flask-Menu should be initialized.
        :type init_menu: bool
        """
        self.init_menu = init_menu
        if app is not None:
            self.init_app(app)

    def init_app(self, app, *args, **kwargs):
        """Configure an application. This registers a `context_processor`.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        """
        app.config.setdefault('BREADCRUMBS_ROOT', 'breadcrumbs')
        app.context_processor(Breadcrumbs.breadcrumbs_context_processor)

        self.app = app
        # Follow the Flask guidelines on usage of app.extensions
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        if 'menu' not in app.extensions:
            if self.init_menu:
                super(Breadcrumbs, self).init_app(app)
            else:
                raise RuntimeError('Flask-Breadcrumbs is not initialized.')

    @staticmethod
    def current_path():
        """Determine current location in menu hierarchy.

        Backend function for current_path proxy.
        """
        # str(...) because __breadcrumb__ can hold a LocalProxy
        if hasattr(current_function, '__breadcrumb__'):
            return str(getattr(current_function, '__breadcrumb__', ''))

        return Breadcrumbs.get_path(
            current_blueprint._get_current_object())  # pylint: disable=W0212

    @staticmethod
    def breadcrumbs():
        """Backend function for breadcrumbs proxy.

        :return: A list of breadcrumbs.
        """
        # Construct breadcrumbs using their dynamic lists
        breadcrumb_list = []

        for entry in current_menu.list_path(
                breadcrumb_root_path, current_path) or []:
            breadcrumb_list += entry.dynamic_list

        return breadcrumb_list

    @staticmethod
    def breadcrumbs_context_processor():
        """Add variable ``breadcrumbs`` to template context.

        It contains the list of menu entries to render as breadcrumbs.
        """
        return dict(breadcrumbs=current_breadcrumbs)

    @staticmethod
    def get_path(app):
        """Return path to root of application's or bluerpint's branch."""
        return str(getattr(
            app,
            '__breadcrumb__',
            breadcrumb_root_path + (
                '.' + app.name if isinstance(app, Blueprint) else '')))


def register_breadcrumb(app, path, text, order=0,
                        endpoint_arguments_constructor=None,
                        dynamic_list_constructor=None):
    """Decorate endpoints that should be displayed as a breadcrumb.

    :param app: Application or Blueprint which owns the function.
    :param path: Path to this item in menu hierarchy
        ('breadcrumbs.' is automatically added).
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
            """Lazy path evaluation."""
            bl_path = Breadcrumbs.get_path(app)
            return (bl_path + path).strip('.')

        func_path = LocalProxy(_evaluate_path)

    else:
        func_path = path

    # Get standard menu decorator
    menu_decorator = register_menu(
        app, func_path, text, order,
        endpoint_arguments_constructor=endpoint_arguments_constructor,
        dynamic_list_constructor=dynamic_list_constructor)

    def breadcrumb_decorator(func):
        """Applie standard menu decorator and assign breadcrumb."""
        func.__breadcrumb__ = func_path

        return menu_decorator(func)

    return breadcrumb_decorator


def _lookup_current_function():
    """Return current view function for request endpoint."""
    return current_app.view_functions.get(request.endpoint)


def _lookup_current_blueprint():
    """Return current :class:`~flask.Blueprint` instance.

    Alternatively return :class:`~flask.Flask` application object when no
    blueprint is activated during request.
    """
    return current_app.blueprints.get(
        request.blueprint,
        current_app._get_current_object())  # pylint: disable=W0212


def _lookup_breadcrumb_root_path():
    """Backend function for breadcrumb_root_path proxy."""
    return current_app.config.get('BREADCRUMBS_ROOT')

# Proxies
# pylint: disable-msg=C0103

#: A proxy for the current function.
current_function = LocalProxy(_lookup_current_function)

#: A proxy for the current blueprint or application object.
current_blueprint = LocalProxy(_lookup_current_blueprint)

#: A proxy for breadcrumbs root element path.
breadcrumb_root_path = LocalProxy(_lookup_breadcrumb_root_path)

#: A proxy for detecting current breadcrumb path.
current_path = LocalProxy(Breadcrumbs.current_path)

#: A proxy for current breadcrumbs list.
current_breadcrumbs = LocalProxy(Breadcrumbs.breadcrumbs)
# pylint: enable-msg=C0103
