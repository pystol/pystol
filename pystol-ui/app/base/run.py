import json
import os
import random
import string
import sys
import urllib

from app.base.k8s import load_kubernetes_config

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
                         extra_vars):
    """
    Determine where we will insert the CR.
    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()


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
        print("Im in: Before")
        print(namespace)
        print(collection)
        print(role)
        print(source)
        print(extra_vars)
        print(resource)

        api_response = custom_obj.create_namespaced_custom_object(
            group=CRD_DOMAIN,
            version=CRD_VERSION,
            namespace=CRD_NAMESPACE,
            plural=CRD_PLURAL,
            body=resource,
        )

        print("After")
        # print(api_response)
    except ApiException as e:
        print("Error :" + e )
        return False
    return True


def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    """
    Generate a random sufix.
    This method will generate a
    random sufix for the created resources.
    """
    return ''.join(random.choice(chars) for _ in range(size))
