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
import tempfile
import json
import os
import sys
import urllib
import yaml

import kubernetes
from kubernetes import client
from kubernetes.client import Configuration
from kubernetes.config import kube_config
from flask import Flask, redirect, render_template, request, url_for

PYSTOL_BRANCH = "master"

#
# We load the Kubernetes cluster config depending
# where we execute the operator from.
#

def load_kubernetes_config(external_file=None, external_yaml=None):
    """
    Load the initial config details.

    We load the config depending where we execute the code from
    """
    try:
        if external_yaml != None:
            loader = kubernetes.config.kube_config.KubeConfigLoader(config_dict=external_yaml, config_base_path=None)
            call_config = type.__call__(Configuration)
            loader.load_and_set(call_config)
            Configuration.set_default(call_config)
        elif external_file != None:
            kubernetes.config.load_kube_config(external_file)
        elif 'KUBERNETES_PORT' in os.environ:
            # We set up the client from within a k8s pod
            kubernetes.config.load_incluster_config()
        elif 'KUBECONFIG' in os.environ:
            kubernetes.config.load_kube_config(os.getenv('KUBECONFIG'))
        else:
            kubernetes.config.load_kube_config()
    except Exception as e:
        message = ("---\n"
                   "The Python Kubernetes client could not be configured "
                   "at this time.\n"
                   "You need a working Kubernetes deployment to make "
                   "Pystol work.\n"
                   "Check the following:\n"
                   "Use the env var KUBECONFIG with the path to your K8s "
                   "config file like:\n"
                   "    export KUBECONFIG=~/.kube/config\n"
                   "Or run Pystol from within the cluster to make use of "
                   "load_incluster_config.\n"
                   "Error: %s" % (e))
        print(message)


def show_actions():
    """
    Show the available Pystol actions from Galaxy.

    This is a main component of the input for the controller
    """
    url = ("https://galaxy.ansible.com/api/internal/"
           "ui/repo-or-collection-detail/"
           "?namespace=pystol&name=actions")

    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        values = json.loads(data)
        actions = (values['data']['collection']['latest_version']
                   ['contents'])
        # description = (values['data']['collection']['latest_version']
        #                ['metadata']['description'])
        repository = (values['data']['collection']['latest_version']
                      ['metadata']['repository'])
        # documentation = (values['data']['collection']['latest_version']
        #                  ['metadata']['documentation'])
        license = (values['data']['collection']['latest_version']
                   ['metadata']['license'])
        version = (values['data']['collection']['latest_version']
                   ['metadata']['version'])
    except Exception:
        actions = {}
        repository = ""
        license = ""
        version = ""
        print("No objects found...")

    url = ("https://github.com/pystol/pystol-galaxy/tree/" +
           PYSTOL_BRANCH + "/actions/roles/")

    ret = []
    for action in actions:
        if action['content_type'] == "role":
            ret.append({'name': action['name'],
                        'description': action['description'],
                        'documentation': url + action['name'],
                        'license': str(license),
                        'version': str(version),
                        'repository': str(repository)})
    return ret


def list_actions(kubeconfig=None):
    """
    List Pystol actions from the cluster.

    This is a main component of the input for the controller
    """
    load_kubernetes_config(external_yaml=kubeconfig)
    api = kubernetes.client.CustomObjectsApi()

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    pretty = 'true'

    ret = []
    try:
        resp = api.list_namespaced_custom_object(group=group,
                                                 version=version,
                                                 namespace=namespace,
                                                 plural=plural,
                                                 pretty=pretty)
        for action in resp['items']:
            ret.append({'name':
                        action['metadata']['name'],
                        'creationTimestamp':
                        action['metadata']['creationTimestamp'],
                        'action_state':
                        action['spec']['action_state'],
                        'workflow_state':
                        action['spec']['workflow_state'],
                        'stdout':
                        action['spec']['action_stdout'],
                        'stderr':
                        action['spec']['action_stderr']})
    except Exception:
        print("No objects found...")
    return ret


def state_cluster(kubeconfig=None):
    """
    List component of cluster.

    This is a main component of the input for the controller
    """

    load_kubernetes_config(external_yaml=kubeconfig)
    api = kubernetes.client.CustomObjectsApi()

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    pretty = 'true'

    ret = []
    try:
        resp = api.list_namespaced_custom_object(group=group,
                                                 version=version,
                                                 namespace=namespace,
                                                 plural=plural,
                                                 pretty=pretty)
        for action in resp['items']:
            ret.append({'name':
                        action['metadata']['name'],
                        'creationTimestamp':
                        action['metadata']['creationTimestamp'],
                        'action_state':
                        action['spec']['action_state'],
                        'workflow_state':
                        action['spec']['workflow_state']})
    except Exception:
        print("No objects found...")
    return ret
