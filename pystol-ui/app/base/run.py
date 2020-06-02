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


import random
import string

from pystol.operator import load_kubernetes_config

from flask import redirect, render_template, request, url_for, session

import kubernetes


# CRD Settings
CRD_DOMAIN = 'pystol.org'
CRD_GROUP = 'pystol.org'
CRD_VERSION = 'v1alpha1'
CRD_PLURAL = 'pystolactions'
CRD_NAMESPACE = 'pystol'


def insert_pystol_object(namespace,
                         collection,
                         role,
                         source,
                         extra_vars,
                         api_client=None):
    """
    Determine where we will insert the CR.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi(
        api_client=api_client)

    resource = {
        "apiVersion": CRD_DOMAIN + "/" + CRD_VERSION,
        "kind": "PystolAction",
        "metadata": {"name": "pystol-action-" +
                             namespace +
                             "-" +
                             collection +
                             "-" +
                             role +
                             "-" +
                             id_generator()},
        "spec": {"namespace": namespace,
                 "collection": collection,
                 "role": role,
                 "source": source,
                 "extra_vars": extra_vars,
                 "action_state": "PystolActionCreating",
                 "workflow_state": "PystolOperatorWaitingAction",
                 "action_stderr": "{}",
                 "action_stdout": "{}"},
    }

    try:
        custom_obj.create_namespaced_custom_object(
            group=CRD_DOMAIN,
            version=CRD_VERSION,
            namespace=CRD_NAMESPACE,
            plural=CRD_PLURAL,
            body=resource,
        )

    except Exception as e:
        print("Error :" + e)
        return False
    return True


def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    """
    Generate a random sufix.

    This method will generate a
    random sufix for the created resources.
    """
    return ''.join(random.choice(chars) for _ in range(size))
