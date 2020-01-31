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
from os import getenv

import kubernetes

from pystol.const import CRD_GROUP, \
                         CRD_PLURAL, \
                         CRD_VERSION, \
                         ALLOWED_EVENT_TYPES, \
                         CREATE_TYPES_MAP, \
                         LIST_TYPES_MAP

__all__ = [
    'handle',
]

#
# Part of the operation in charge of adding the custom resources
# to the Kubernetes cluster, this will create an object with
# the CLI parameters.
#

def deploy_action(collection, name, extra_vars):
    """
    Here we will determine where we will insert the CR.

    This is a main component of the input for the controller
    """
    print(collection)
    print(name)
    print(extra_vars)

    resource = {
      "apiVersion": "pystol.org/v1alpha1",
      "kind": "PystolAction",
      "metadata": {"name": "pystol-" + collection + "-" + name},
      "spec": {"collection": collection, "name": name, "extra-vars": extra_vars, "result": "{}"},
    }

    create_object(resource)

def create_object(resource):
    """
    Insert custom objects to run the actions.

    This is a main component of the input for the controller
    """
    try:
        kubernetes.config.load_kube_config(getenv('KUBECONFIG'))
    except IOError:
        try:
            kubernetes.config.load_incluster_config()  # We set up the client from within a k8s pod
        except kubernetes.config.config_exception.ConfigException:
            raise KubernetesException("Could not configure kubernetes python client")

    v1 = kubernetes.client.CustomObjectsApi()

    # create the resource
    v1.create_namespaced_custom_object(
        group="pystol.org",
        version="v1alpha1",
        namespace="default",
        plural="pystolactions",
        body=my_resource,
    )

#
# Part of the operator which will handle the process of new
# PystolAction objects, It will watch for them and create a
# deployment to launch the Ansible role defining the fault
# injection action.
#

def process_objects():
    """
    Initiate the main method.

    To start events processing via operator.
    """
    try:
        kubernetes.config.load_kube_config(getenv('KUBECONFIG'))
    except IOError:
        try:
            kubernetes.config.load_incluster_config()  # We set up the client from within a k8s pod
        except kubernetes.config.config_exception.ConfigException:
            raise KubernetesException("Could not configure kubernetes python client")

    v1 = kubernetes.client.CoreV1Api()

    # Get the method to watch the objects
    # method = getattr(v1, LIST_TYPES_MAP[specs['spec']])
    # func = partial(method, specs['namespace'])

    crds = kubernetes.client.CustomObjectsApi()

    w = kubernetes.watch.Watch()
    # for event in w.stream(func):
    for event in w.stream(crds.list_cluster_custom_object, "pystol.org", "v1alpha1", "pystolactions", resource_version=''):
        print("---------")
        print("---------")
        print(event)
