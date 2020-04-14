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
from app.base.k8sclient import os, state_namespaces, state_nodes, state_pods, cluster_name_configured
from app.base.allocated import compute_allocated_resources
from app.base.hexa import hexagons_data


@blueprint.route('/index')
@login_required
def index():
    #if not current_user.is_authenticated:
    #    return redirect(url_for('base_blueprint.login'))

    return render_template('index.html',
                           compute_allocated_resources = compute_allocated_resources(),
                           hexagons_data = hexagons_data(),
                           cluster_name_configured  = cluster_name_configured(),
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
                               state_pods = state_pods(),
                               compute_allocated_resources = compute_allocated_resources(),
                               cluster_name_configured  = cluster_name_configured(),
                               )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/uploadkubeconfig', methods = ['POST'])
def upload_image():
    try:
        if request.method == "POST":
            file = request.files['kubeconfig']
            filename = file.filename
            file.save(os.path.join("/tmp/", filename))
            os.rename("/tmp/" + filename,'.kube/config') 
            return redirect( '/pystol-update-kubeconfig')
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500
