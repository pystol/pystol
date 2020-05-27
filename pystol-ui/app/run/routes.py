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

from app.run import blueprint

from flask import redirect, render_template, request, url_for, session

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


@blueprint.route('/')
def run():
    """
    Render all the templates not from base.

    This is a main method
    """
    # The auth module is installed and the user is not authenticated, so go to login
    if hasattr(app, 'auth') and not 'username' in session: #not current_user.is_authenticated:
        return redirect(url_for('auth_blueprint.login'))

    try:
        return render_template('run.html',
                               compute_allocated_resources=
                               compute_allocated_resources(),
                               cluster_name_configured=
                               cluster_name_configured(),
                               pystol_version = PYSTOL_VERSION,)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    # except Exception:
    #     return render_template('page-500.html'), 500
