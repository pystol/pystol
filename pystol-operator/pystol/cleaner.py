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

import kubernetes
from kubernetes.client.rest import ApiException

from pystol import __version__
from pystol.operator import load_kubernetes_config

pystol_version = __version__


def purge_pystol(api_client=None):
    """
    Purge Pystol from the cluster.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    v1 = kubernetes.client.CoreV1Api(api_client=api_client)

    name = 'pystol'
    pretty = 'true'
    orphan_dependents = True
    # propagation_policy = 'Foreground'
    propagation_policy = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        v1.delete_namespace(name,
                            pretty=pretty,
                            orphan_dependents=orphan_dependents,
                            propagation_policy=propagation_policy,
                            body=body)
        print("    " + u"\U0001F9F9" + " Namespace removed.")
    except ApiException:
        print("    " + u"\u2757" + " Namespace removing warning.")
        print("       Can't remove it, maybe it's gone...")

    name = 'pystol-service'
    namespace = 'pystol'
    pretty = 'true'
    orphan_dependents = True
    propagation_policy = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        v1.delete_namespaced_service(name,
                                     namespace=namespace,
                                     pretty=pretty,
                                     orphan_dependents=orphan_dependents,
                                     propagation_policy=propagation_policy,
                                     body=body)
        print("    " + u"\U0001F9F9" + " Service removed.")
    except ApiException:
        print("    " + u"\u2757" + " Service removing warning.")
        print("       Can't remove it, maybe it's gone...")

    name = 'pystol-config'
    namespace = 'pystol'
    pretty = 'true'
    orphan_dependents = True
    propagation_policy = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        v1.delete_namespaced_config_map(name,
                                        namespace=namespace,
                                        pretty=pretty,
                                        orphan_dependents=orphan_dependents,
                                        propagation_policy=propagation_policy,
                                        body=body)
        print("    " + u"\U0001F9F9" + " Config map removed.")
    except ApiException:
        print("    " + u"\u2757" + " Config map removing warning.")
        print("       Can't remove it, maybe it's gone...")

    name = 'pystol'
    namespace = 'pystol'
    pretty = 'true'
    orphans = True
    propagation = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        v1.delete_namespaced_service_account(name,
                                             namespace=namespace,
                                             pretty=pretty,
                                             orphan_dependents=orphans,
                                             propagation_policy=propagation,
                                             body=body)
        print("    " + u"\U0001F9F9" + " Service account removed.")
    except ApiException:
        print("    " + u"\u2757" + " Service account removing warning.")
        print("       Can't remove it, maybe it's gone...")

    rbac = kubernetes.client.RbacAuthorizationV1Api(
        api_client=api_client)
    name = 'pystol'
    pretty = 'true'
    orphan_dependents = True
    propagation_policy = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        rbac.delete_cluster_role(name,
                                 pretty=pretty,
                                 orphan_dependents=orphan_dependents,
                                 propagation_policy=propagation_policy,
                                 body=body)
        print("    " + u"\U0001F9F9" + " Cluster role removed.")
    except ApiException:
        print("    " + u"\u2757" + " Cluster role removing warning.")
        print("       Can't remove it, maybe it's gone...")

    rbac = kubernetes.client.RbacAuthorizationV1Api(
        api_client=api_client)
    name = 'pystol'
    pretty = 'true'
    orphan_dependents = True
    propagation_policy = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        rbac.delete_cluster_role_binding(name,
                                         pretty=pretty,
                                         orphan_dependents=orphan_dependents,
                                         propagation_policy=propagation_policy,
                                         body=body)
        print("    " + u"\U0001F9F9" +
              " Cluster role binding removed.")
    except ApiException:
        print("    " + u"\u2757" +
              " Cluster role binding removing warning.")
        print("       Can't remove it, maybe it's gone...")

    ext = kubernetes.client.ApiextensionsV1beta1Api(
        api_client=api_client)
    name = 'pystolactions.pystol.org'
    pretty = 'true'
    orphans = True
    propagation = 'Background'
    body = kubernetes.client.V1DeleteOptions()
    try:
        ext.delete_custom_resource_definition(name,
                                              pretty=pretty,
                                              orphan_dependents=orphans,
                                              propagation_policy=propagation,
                                              body=body)
        print("    " + u"\U0001F9F9" + " CRD removed.")
    except ApiException:
        print("    " + u"\u2757" + " CRD removing warning.")
        print("       Can't remove it, maybe it's gone...")
