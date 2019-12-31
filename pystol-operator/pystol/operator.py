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

import kubernetes

from pystol.const import ALLOWED_EVENT_TYPES, CREATE_TYPES_MAP, \
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
    kubernetes.config.load_incluster_config()
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

def handle_event(v1, specs, event):
    """
    Process the events from the watch method.

    This is a main component of the controller
    """
    # We will here create a new pod (Pystol launcher)
    # Todeploy the action
    # This should call ansible runner in somehow.

    if event['type'] not in ALLOWED_EVENT_TYPES:
        return

    object_ = event['object']
    labels = object_['metadata'].get('labels', {})

    # Look for the matches using selector
    for key, value in specs['selector'].items():
        if labels.get(key) != value:
            return
    # Get active namespaces
    namespaces = map(
        lambda x: x.metadata.name,
        filter(
            lambda x: x.status.phase == 'Active',
            v1.list_namespace().items
        )
    )
    for namespace in namespaces:
        # Clear the metadata, set the namespace
        object_['metadata'] = {
            'labels': object_['metadata']['labels'],
            'namespace': namespace,
            'name': object_['metadata']['name'],
        }
        # Call the method for creating/updating an object
        methodcaller(
            CREATE_TYPES_MAP[specs['ruleType']],
            namespace,
            object_
        )(v1)

    # launch_batch_job()

def launch_batch_job():
    """
    Launch the batch job

    To start events processing via operator.
    """

    kubernetes.config.load_incluster_config()
    v1 = kubernetes.client.AppsV1Api()

    with open(path.join(path.dirname(__file__), "launcher.yaml")) as f:
        dep = yaml.safe_load(f)
        resp = v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)

def handle(specs):
    """
    Initiate the main method.

    To start events processing via operator.
    """
    kubernetes.config.load_incluster_config()
    v1 = kubernetes.client.CoreV1Api()

    # Get the method to watch the objects
    method = getattr(v1, LIST_TYPES_MAP[specs['collection']])
    func = partial(method, specs['namespace'])

    w = kubernetes.watch.Watch()
    for event in w.stream(func):
        handle_event(v1, specs, event)
