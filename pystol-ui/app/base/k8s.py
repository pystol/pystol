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
import os
import random
import string
import sys
import urllib

import kubernetes
from kubernetes.client.rest import ApiException

PYSTOL_BRANCH = "master"

#
# We load the Kubernetes cluster config depending
# where we execute the operator from.
#


def load_kubernetes_config():
    """
    Load the initial config details.

    We load the config depending where we execute the code from
    """
    try:
        if 'KUBERNETES_PORT' in os.environ:
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
                   "Error: " % (e))
        print(message)
        print("---")
        print("The current Pystol version is: %s" % (pystol_version))
        print(" ")
        print("Bye...")
        sys.exit(0)


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
        description = (values['data']['collection']['latest_version']
                       ['metadata']['description'])
        repository = (values['data']['collection']['latest_version']
                      ['metadata']['repository'])
        documentation = (values['data']['collection']['latest_version']
                         ['metadata']['documentation'])
        license = (values['data']['collection']['latest_version']
                   ['metadata']['license'])
        version = (values['data']['collection']['latest_version']
                   ['metadata']['version'])
    except Exception as e:
        actions = {}
        description = ""
        repository = ""
        documentation = ""
        license = ""
        version = ""
        print(e)
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
                        'repository': str(repository),
                       })
    return ret


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

    ret = []
    try:
        resp = api.list_namespaced_custom_object(group=group,
                                                 version=version,
                                                 namespace=namespace,
                                                 plural=plural,
                                                 pretty=pretty)
        for action in resp['items']:
            ret.append({'name':action['metadata']['name'],
                        'creationTimestamp':action['metadata']['creationTimestamp'],
                        'action_state':action['spec']['action_state'],
                        'wokflow_state':action['spec']['workflow_state'],
                       })
    except ApiException:
        print("No objects found...")
    return ret
