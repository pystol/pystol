# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.k8s import list_actions, show_actions
from app.base.k8sclient import  state_namespaces, state_nodes
from app.base.allocated import compute_allocated_resources

@blueprint.route('/index')
@login_required
def index():
    #if not current_user.is_authenticated:
    #    return redirect(url_for('base_blueprint.login'))

    return render_template('index.html',
                           compute_allocated_resources = compute_allocated_resources()
                          )

@blueprint.route('/<template>')
def route_template(template):
    #if not current_user.is_authenticated:
    #    return redirect(url_for('base_blueprint.login'))
    try:
        return render_template(template + '.html',
                               list_actions = list_actions(),
                               show_actions = show_actions(),
                               state_namespaces = state_namespaces(),
                               state_nodes = state_nodes(),
                               compute_allocated_resources = compute_allocated_resources(),
                               )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

# pystol-actions-before will be displayed anyway as all the
# templates are rendered, see 10 lines before.
# Remove from here, you are skiping the auth
#pystol-actions-before.html
#@blueprint.route('/pystol-actions-before', methods=['GET'])
#def pystol_actions_before():
#    return render_template( 'pystol-actions-before.html',
#    actions=jsonify(show_actions()))
#    #return jsonify(show_actions())
