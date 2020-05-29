#!/usr/bin/env python

"""
Copyright 2019 Pystol (pystol.org).

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""


import os

import app

from app.base.allocated import compute_allocated_resources
from app.base.graph import get_cluster_graph
from app.base.hexa import hexagons_data
from app.base.k8s import list_actions, show_actions
from app.base.k8sclient import (cluster_name_configured,
                                state_namespaces,
                                state_nodes,
                                state_pods)
from app.base.run import insert_pystol_object

from app.home import blueprint

from flask import redirect, render_template, request, url_for

from flask_login import (current_user,
                         login_required,
                         login_user,
                         logout_user)

from jinja2 import TemplateNotFound

try:
    from pystol import __version__
    PYSTOL_VERSION = __version__
except ImportError:
    PYSTOL_VERSION = "Not installed"

# Auth required
try:
    from app.auth.routes import get_session_data
except ImportError:
    print("Module not available")
from google.cloud import firestore
#Auth required
fdb = firestore.Client()
transaction = fdb.transaction()

@blueprint.route('/')
def home_root():
    """
    Render the index of Pystol.

    This is a main method
    """
    #
    # Basic authentication module requirement
    # If the auth module is installed and the user is not authenticated, so go to login
    #
    if hasattr(app, 'auth') and session['email'] == None: #not current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.login'))
    #
    # End basic authentication requirement
    #

    return redirect(url_for('usage_blueprint.usage'))


@blueprint.route('/<template>')
def route_template(template):
    """
    Render all the templates not from base.

    This is a main method
    """
    # The auth module is installed and the user is not authenticated, so go to login
    if hasattr(app, 'auth') and not 'username' in session: #not current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.login'))

    try:
        return render_template(template + '.html',
                               list_actions=list_actions(),
                               show_actions=show_actions(),
                               state_namespaces=state_namespaces(),
                               state_nodes=state_nodes(),
                               state_pods=state_pods(),
                               compute_allocated_resources=
                               compute_allocated_resources(),
                               cluster_name_configured=
                               cluster_name_configured(),
                               cluster_graph=get_cluster_graph(),
                               pystol_version = PYSTOL_VERSION,)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    # except Exception:
    #     return render_template('page-500.html'), 500


@blueprint.route('/api/v1/actionRun', methods = ['POST'])
def action_run():
    """
    Show the executed Pystol actions.

    This is a main method
    """
    #
    # Basic authentication module requirement
    # If the auth module is installed and the user is not authenticated, so go to login
    #
    if hasattr(app, 'auth') and session['email'] == None: #not current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.login'))
    #
    # End basic authentication requirement
    #

    try:
        if request.method == "POST":
            print("Run action by post")
            dict = request.form
            namespace = ""
            collection = ""
            role = ""
            source = ""
            extra_vars = {}

            if 'namespace' in dict:
                namespace = dict['namespace']
            else:
                namespace = ""

            if 'collection' in dict:
                collection = dict['collection']
            else:
                collection = ""

            if 'role' in dict:
                role = dict['role']
            else:
                role = ""

            if 'source' in dict:
                source = dict['source']
            else:
                source = ""

            if 'extra_vars' in dict:
                extra_vars = dict['extra_vars']
            else:
                extra_vars = {}

            insert_pystol_object(namespace=namespace,
                                 collection=collection,
                                 role=role,
                                 source=source,
                                 extra_vars=extra_vars)
            return redirect('/pystol-actions-executed')
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception:
        return render_template('page-500.html'), 500
