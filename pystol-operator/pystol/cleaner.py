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


def purge_pystol():
    """
    Purge Pystol from the cluster.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    v1 = kubernetes.client.CoreV1Api()

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
        print("Namespace deleted")
        # print("Namespace deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("Namespace: Can't remove it, maybe it's gone...")
        # print("CoreV1Api->delete_namespace: %s\n" % e)

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
        print("Config map deleted")
        # print("Config map deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("Config map: Can't remove it, maybe it's gone...")
        # print("CoreV1Api->delete_namespaced_config_map: %s\n" % e)

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
        print("Service account deleted")
        # print("Service account deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("Service account: Can't remove it, maybe it's gone...")
        # print("CoreV1Api->delete_namespaced_service_account: %s\n" % e)

    rbac = kubernetes.client.RbacAuthorizationV1Api()
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
        print("Cluster role deleted")
        # print("Cluster role deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("Cluster role: Can't remove it, maybe it's gone...")
        # print("RbacAuthorizationV1Api->delete_cluster_role: %s\n" % e)

    rbac = kubernetes.client.RbacAuthorizationV1Api()
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
        print("Cluster role binding deleted")
        # print("Cluster role deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("Cluster role binding: Can't remove it, maybe it's gone...")
        # print("RbacAuthorizationV1Api->delete_cluster_role: %s\n" % e)

    ext = kubernetes.client.ApiextensionsV1beta1Api()
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
        print("CRD deleted")
        # print("CRD deleted - status='%s'" % resp)
    except ApiException:  # as e:
        print("CRD: Can't remove it, maybe it's gone...")
        # print("V1beta1Api->delete_cluster_role_binding: %s\n" % e)
