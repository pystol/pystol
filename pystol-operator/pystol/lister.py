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

import json

import kubernetes
from kubernetes.client.rest import ApiException

from prettytable import PrettyTable

from pystol import __version__
from pystol.operator import load_kubernetes_config

pystol_version = __version__


def list_actions():
    """
    List Pystol actions from the cluster.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    api = kubernetes.client.CustomObjectsApi()

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    pretty = 'true'

    x = PrettyTable()
    x.field_names = ["Name",
                     # "Namespace",
                     "Creation",
                     # "Role",
                     # "Collection",
                     # "Source",
                     # "Extra vars",
                     "Action state",
                     "Workflow state"]
    try:
        resp = api.list_namespaced_custom_object(group=group,
                                                 version=version,
                                                 namespace=namespace,
                                                 plural=plural,
                                                 pretty=pretty)

        for action in resp['items']:
            x.add_row([action['metadata']['name'],
                       # action['metadata']['namespace'],
                       action['metadata']['creationTimestamp'],
                       # action['spec']['role'],
                       # action['spec']['collection'],
                       # action['spec']['source'],
                       # action['spec']['extra_vars'],
                       action['spec']['action_state'],
                       action['spec']['workflow_state']])
    except ApiException:
        print("No objects found...")

    print(x)


def get_action(name):
    """
    Get Pystol action details.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    api = kubernetes.client.CustomObjectsApi()

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    try:
        resp = api.get_namespaced_custom_object(group=group,
                                                version=version,
                                                namespace=namespace,
                                                plural=plural,
                                                name=name)
        print(json.dumps(resp['spec'], indent=2))
    except ApiException:
        print("Object not found...")
