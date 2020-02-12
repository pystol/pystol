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

from functools import partial
from operator import methodcaller

import json
import kubernetes
import os
import random
import string
import sys
from jinja2 import Template
import yaml

from kubernetes.client.rest import ApiException
from kubernetes.utils.create_from_yaml import FailToCreateError

from pystol.operator import load_kubernetes_config

from pystol import __version__
from pystol.const import CRD_DOMAIN, \
                         CRD_PLURAL, \
                         CRD_VERSION, \
                         ALLOWED_EVENT_TYPES, \
                         CREATE_TYPES_MAP, \
                         LIST_TYPES_MAP

__all__ = [
    'handle',
]

pystol_version = __version__

def deploy_pystol():
    """
    We install Pystol from Python.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()
    v1 = kubernetes.client.CoreV1Api()
    deployment = kubernetes.client.AppsV1Api()
    rbac = kubernetes.client.RbacAuthorizationV1Api()
    apicli = kubernetes.client.ApiClient()

    try:
        resp = kubernetes.utils.create_from_yaml(
            k8s_client=apicli,
            yaml_file=os.path.join(os.path.dirname(__file__), "templates/crd.yaml"),
            namespace="default"
            )
        print("CRD created - status='%s'" % resp.metadata.name)
    except FailToCreateError as e:
        print("CRD problem - Exception when calling ApiClient->create_from_yaml: %s\n" % e)
    except Exception as e:
        print("CRD problem - Exception when calling ApiClient->create_from_yaml: %s\n" % e)
        print("The CRD was created but an exception is raised")
        print("Other error, see https://github.com/kubernetes-client/python/issues/1022")

    with open(os.path.join(os.path.dirname(__file__), "templates/service_account.yaml")) as f:
        try:
            resp = v1.create_namespaced_service_account(
                namespace="default",
                body=yaml.safe_load(f))
            print("Service account created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_service_account: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__), "templates/cluster_role.yaml")) as f:
        try:
            resp = rbac.create_cluster_role(
                body=yaml.safe_load(f))
            print("Cluster role created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling RbacAuthorizationV1Api->create_cluster_role: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__), "templates/cluster_role_binding.yaml")) as f:
        try:
            resp = rbac.create_cluster_role_binding(
                body=yaml.safe_load(f))
            print("Cluster role binding created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling RbacAuthorizationV1Api->create_cluster_role_binding: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__), "templates/upstream_values.yaml")) as f:
       values = yaml.safe_load(f)

    with open(os.path.join(os.path.dirname(__file__), "templates/config_map.yaml.j2")) as f:
        template = Template(f.read())
        cm = template.render(values)
        try:
            resp = v1.create_namespaced_config_map(
                body=yaml.safe_load(cm), namespace="default")
            print("Config map created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_config: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__), "templates/controller.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment), namespace="default")
            print("Deployment created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)

    with open(os.path.join(os.path.dirname(__file__), "templates/ui.yaml.j2")) as f:
        template = Template(f.read())
        rendered_deployment = template.render(values)
        try:
            resp = deployment.create_namespaced_deployment(
                body=yaml.safe_load(rendered_deployment), namespace="default")
            print("Deployment created - status='%s'" % resp.metadata.name)
        except ApiException as e:
            print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)
