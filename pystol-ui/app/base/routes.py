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


from app import db, login_manager
from app.base import blueprint
from app.base.forms import CreateAccountForm, LoginForm
from app.base.k8s import list_actions, show_actions
from app.base.k8sclient import (cluster_name_configured,
                                state_namespaces,
                                state_nodes,
                                state_pods,
                                web_terminal)
from app.base.models import User
from app.base.util import verify_pass

from flask import jsonify, redirect, render_template, request, url_for

from flask_login import (current_user,
                         login_user,
                         logout_user)


@blueprint.route('/')
def route_default():
    """
    Define a route.

    This is a main routing method
    """
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/error-<error>')
def route_errors(error):
    """
    Define a route.

    This is a main routing method
    """
    return render_template('errors/{}.html'.format(error))


# API endpoints
@blueprint.route('/api/v1/ListActions', methods=['GET'])
def api_list_actions():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(list_actions())


@blueprint.route('/api/v1/ShowActions', methods=['GET'])
def api_show_actions():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(show_actions())


@blueprint.route('/api/v1/StateNamespaces', methods=['GET'])
def api_state_namespaces():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(state_namespaces())


@blueprint.route('/api/v1/StateNodes', methods=['GET'])
def api_state_nodes():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(state_nodes())


@blueprint.route('/api/v1/StatePods', methods=['GET'])
def api_state_pods():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(state_pods())


@blueprint.route('/api/v1/Terminal', methods=['GET'])
def api_web_terminal():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(web_terminal())


@blueprint.route('/api/v1/ClusterName', methods=['GET'])
def api_cluster_name_configured():
    """
    Define a route.

    This is a main routing method
    """
    return jsonify(cluster_name_configured())


# Login & Registration
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Define a route.

    This is a main routing method
    """
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('login/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('login/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    """
    Define a route.

    This is a main routing method
    """
    LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('login/register.html',
                                   msg='Username already registered',
                                   form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('login/register.html',
                                   msg='Email already registered',
                                   form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('login/register.html',
                               msg='User created <a href="/login">login</a>',
                               form=create_account_form)

    else:
        return render_template('login/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    """
    Define a route.

    This is a main routing method
    """
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    """
    Define a route.

    This is a main routing method
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Define a route.

    This is a main routing method
    """
    return render_template('page-403.html',
                           template_folder="../home/templates/"), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    """
    Define a route.

    This is a main routing method
    """
    return render_template('page-403.html',
                           template_folder="../home/templates/"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    """
    Define a route.

    This is a main routing method
    """
    return render_template('page-404.html',
                           template_folder="../home/templates/"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    """
    Define a route.

    This is a main routing method
    """
    return render_template('page-500.html',
                           template_folder="../home/templates/"), 500
