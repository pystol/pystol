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
from app.base.hexa import hexagons_data
from app.base.k8s import list_actions, show_actions
from app.base.k8sclient import (cluster_name_configured,
                                state_namespaces,
                                state_nodes,
                                state_pods)
from app.base.run import insert_pystol_object

from app.available import blueprint

from flask import current_app, redirect, render_template, request, url_for

from flask_login import (current_user,
                         login_required,
                         login_user,
                         logout_user)

from jinja2 import TemplateNotFound
from google.cloud import firestore

try:
    from pystol import __version__
    PYSTOL_VERSION = __version__
except ImportError:
    PYSTOL_VERSION = "Not installed"
#
# Begin authentication
#
try:
    from app.auth.routes import get_session_data
    from app.auth.util import remote_cluster
except ImportError:
    print("Module not available")

try:
    fdb = firestore.Client()
    transaction = fdb.transaction()
except Exception as e:
    print("Cant connect to firestore: %s" % (e))
#
# End authentication
#


@blueprint.route('/')
def available():
    """
    Render all the templates not from base.

    This is a main method
    """
    #
    # Basic authentication module requirement
    # If the auth module is installed and the user is not authenticated, so go to login
    #
    session = {}
    if hasattr(app, 'auth'):
        session = get_session_data(
            transaction=transaction, session_id=request.cookies.get('session_id'))
    else:
        session['kubeconfig'] = None
    # not current_user.is_authenticated:
    if hasattr(app, 'auth') and session['email'] == None:
        return redirect(url_for('auth_blueprint.login'))
    #
    # End basic authentication requirement
    #

    if not 'kubeconfig' in session or session['kubeconfig'] == None or session['kubeconfig'] == '':
        kubeconfig = None
        api_client = None
    else:
        kubeconfig = session['kubeconfig']
        api_client = remote_cluster(kubeconfig=kubeconfig)

    if (not 'username' in session or
        session['username'] == None or
        session['username'] == '' or
        not 'email' in session or
        session['email'] == None or
            session['email'] == ''):

        username = None
        email = None
    else:
        username = session['username']
        email = session['email']

    try:
        return render_template('available.html',
                               username=username, email=email,
                               show_actions=show_actions(
                                   api_client=api_client),
                               compute_allocated_resources=compute_allocated_resources(
                                   api_client=api_client),
                               cluster_name_configured=cluster_name_configured(
                                   api_client=api_client),
                               pystol_version=PYSTOL_VERSION,)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print("Exception found in %s: %s" % (blueprint.name, e))
        if current_app.config['DEBUG']:
            raise e
        return render_template('page-500.html'), 500
