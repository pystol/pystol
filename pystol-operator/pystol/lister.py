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

import textwrap

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
                     "Creation",
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
                       action['metadata']['creationTimestamp'],
                       action['spec']['action_state'],
                       action['spec']['workflow_state']])
    except ApiException:
        print("No objects found...")
    print(x)


def get_action(name, debug=False):
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
        print("  " + u"\U0001F4AC" + " General information")
        print("    Action: " + resp['spec']['namespace'] + "." +
              resp['spec']['collection'] + "." +
              resp['spec']['role'])

        print("    Extra variables: " + resp['spec']['extra_vars'])

        print("    Source: " + resp['spec']['source'])

        print("  " + u"\U0001F4AC" + " Status information")

        print("    Executed: " + str(resp['spec']['executed']))

        print("    Action state: " + resp['spec']['action_state'])

        print("    Workflow state: " + resp['spec']['workflow_state'])

        prefix = "    Std output: "
        preferredwidth = 70
        wrapper = textwrap.TextWrapper(initial_indent=prefix,
                                       width=preferredwidth,
                                       subsequent_indent=' ' * len(prefix))
        print(wrapper.fill(resp['spec']['action_stdout']))

        prefix = "    Std error: "
        preferredwidth = 70
        wrapper = textwrap.TextWrapper(initial_indent=prefix,
                                       width=preferredwidth,
                                       subsequent_indent=' ' * len(prefix))
        print(wrapper.fill(resp['spec']['action_stderr']))

    except ApiException:
        print("  " + u"\U0001F914" + " Object not found, perhaps you have a typo.")

    if debug:

        api = kubernetes.client.BatchV1Api()
        namespace = "pystol"
        pretty = 'true'
        try:
            resp = api.read_namespaced_job(name=name,
                                           namespace=namespace,
                                           pretty=pretty)
            print("---- Job description begins ----")
            print(resp)
            print("---- Job description ends ----")
        except ApiException:
            print("  " + u"\U0001F914" + " Job not found, perhaps you have a typo.")

        api = kubernetes.client.CoreV1Api()
        namespace = "pystol"
        pretty = 'true'
        try:
            resp = api.list_namespaced_pod(namespace=namespace,
                                           pretty=pretty)
            found = False
            for pod in resp.items:
                if name in pod.metadata.name:
                    found = True
                    resp = api.read_namespaced_pod_log(name=pod.metadata.name,
                                                       namespace=namespace,
                                                       pretty=pretty)
                    print("---- Pod logs begins ----")
                    print("Logs from: " + pod.metadata.name)
                    print(resp)
                    print("---- Pod logs ends ----")
            if not found:
                print("  " + u"\U0001F914" + " Pod not found, perhaps you have a typo.")
        except ApiException:
            print("  " + u"\U0001F914" + " Pod not found, perhaps you have a typo.")
