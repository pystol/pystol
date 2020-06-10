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

from jinja2 import Template

import kubernetes
from kubernetes.client.rest import ApiException
from kubernetes.utils.create_from_yaml import FailToCreateError

from pystol import __version__
from pystol.operator import load_kubernetes_config

import yaml

pystol_version = __version__


def deploy_pystol(api_client=None):
    """
    Install Pystol from Python.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    v1 = kubernetes.client.CoreV1Api(api_client=api_client)
    deployment = kubernetes.client.AppsV1Api(api_client=api_client)
    rbac = kubernetes.client.RbacAuthorizationV1Api(
        api_client=api_client)

    if api_client == None:
        apicli = kubernetes.client.ApiClient()
    else:
        apicli = api_client

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.upstreamvalues.yaml")) as f:
        values = yaml.safe_load(f)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.namespace.yaml")) as f:
        try:
            resp = v1.create_namespace(
                body=yaml.safe_load(f))
            print("  " + u"\U0001F4E6" + " Namespace created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" + " Namespace creation warning.")
            print("     Maybe it is already created.")

    '''
    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.configmap.yaml.j2")) as f:
        template = Template(f.read())
        cm = template.render(values)
        try:
            resp = v1.create_namespaced_config_map(
                body=yaml.safe_load(cm), namespace="pystol")
            print("  " + u"\U0001F4E6" + " Config map created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" + " Config map creation warning.")
            print("     Maybe it is already created.")
    '''
    try:
        resp = kubernetes.utils.create_from_yaml(
            k8s_client=apicli,
            yaml_file=os.path.join(os.path.dirname(__file__),
                                   "templates/latest/pystol.crd.yaml"),
            namespace="pystol"
        )
        print("  " + u"\U0001F4E6" + " CRD created.")
        print("     '%s'" % resp.metadata.name)
    except FailToCreateError:
        print("  " + u"\u2757" + " CRD creation warning.")
        print("     Maybe it is already created.")
    except Exception:
        print("  " + u"\U0001F4E6" + " CRD created.")
        print("     We need to wait for a permanent fix, until then...")
        print("     https://github.com/kubernetes-client/python/issues/1022")
        # print("CRD problem - ApiClient->create_from_yaml: %s\n" % e)
        # print("The CRD was created but an exception is raised")
        # print("Other error, see:")
        # print("https://github.com/kubernetes-client/python/issues/1022")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.serviceaccount.yaml")) as f:
        try:
            resp = v1.create_namespaced_service_account(
                namespace="pystol",
                body=yaml.safe_load(f))
            print("  " + u"\U0001F4E6" + " Service account created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" +
                  " Service account creation warning.")
            print("     Maybe it is already created.")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.clusterrole.yaml")) as f:
        try:
            resp = rbac.create_cluster_role(
                body=yaml.safe_load(f))
            print("  " + u"\U0001F4E6" + " Role created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" + " Role creation warning.")
            print("     Maybe it is already created.")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.clusterrolebinding.yaml")) as f:
        try:
            resp = rbac.create_cluster_role_binding(
                body=yaml.safe_load(f))
            print("  " + u"\U0001F4E6" +
                  " Cluster role bindings created.")
            print("     '%s'"
                  % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757"
                       + " Cluster role binding creation warning.")
            print("     Maybe it is already created.")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.controller.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment),
                namespace="pystol")
            print("  " + u"\U0001F4E6"
                       + " Operator deployment created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757"
                       + " Operator deployment creation warning.")
            print("     Maybe it is already created.")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.ui.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment),
                namespace="pystol")
            print("  " + u"\U0001F4E6" + " UI operator created.")
            print("     '%s'"
                  % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" + " UI deployment creation warning.")
            print("     Maybe it is already created.")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/latest/pystol.service.yaml")) as f:
        try:
            resp = v1.create_namespaced_service(
                namespace="pystol",
                body=yaml.safe_load(f))
            print("  " + u"\U0001F4E6" + " Service created.")
            print("     '%s'" % resp.metadata.name)
        except ApiException:
            print("  " + u"\u2757" + " Service creation warning.")
            print("     Maybe it is already created.")
