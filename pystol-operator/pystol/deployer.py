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


def deploy_pystol():
    """
    Install Pystol from Python.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    v1 = kubernetes.client.CoreV1Api()
    deployment = kubernetes.client.AppsV1Api()
    rbac = kubernetes.client.RbacAuthorizationV1Api()
    apicli = kubernetes.client.ApiClient()

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/namespace.yaml")) as f:
        try:
            resp = v1.create_namespace(
                body=yaml.safe_load(f))
            print("Namespace created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("CoreV1Api->create_namespace: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/upstream_values.yaml")) as f:
        values = yaml.safe_load(f)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/config_map.yaml.j2")) as f:
        template = Template(f.read())
        cm = template.render(values)
        try:
            resp = v1.create_namespaced_config_map(
                body=yaml.safe_load(cm), namespace="pystol")
            print("Config map created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("CoreV1Api->create_namespaced_config: %s\n" % e)

    try:
        resp = kubernetes.utils.create_from_yaml(
            k8s_client=apicli,
            yaml_file=os.path.join(os.path.dirname(__file__),
                                   "templates/crd.yaml"),
            namespace="pystol"
        )
        print("CRD created - status='%s'" % resp.metadata.name)
    except FailToCreateError as e:
        print("CRD problem - ApiClient->create_from_yaml: %s\n" % e)
    except Exception as e:
        print("CRD problem - ApiClient->create_from_yaml: %s\n" % e)
        print("The CRD was created but an exception is raised")
        print("Other error, see:")
        print("https://github.com/kubernetes-client/python/issues/1022")

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/service_account.yaml")) as f:
        try:
            resp = v1.create_namespaced_service_account(
                namespace="pystol",
                body=yaml.safe_load(f))
            print("Service account created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("CoreV1Api->create_namespaced_service_account: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/cluster_role.yaml")) as f:
        try:
            resp = rbac.create_cluster_role(
                body=yaml.safe_load(f))
            print("Role created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("RbacAuthorizationV1Api->create_cluster_role: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/cluster_role_binding.yaml")) as f:
        try:
            resp = rbac.create_cluster_role_binding(
                body=yaml.safe_load(f))
            print("Cluster role binding created - status='%s'"
                  % resp.metadata.name)
        except ApiException as e:
            print("RbacAuthorizationV1Api->create_cluster_role_binding: %s\n"
                  % e)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/controller.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment),
                namespace="pystol")
            print("Deployment created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("AppsV1Api->create_namespaced_deployment: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__),
                           "templates/ui.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment),
                namespace="pystol")
            print("Deployment created - status='%s'"
                  % resp.metadata.name)
        except ApiException as e:
            print("AppsV1Api->create_namespaced_deployment: %s\n" % e)
