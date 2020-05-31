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

from pystol.operator import load_kubernetes_config

from flask import redirect, render_template, request, url_for, session

import kubernetes


def get_cluster_name(api_client=None):
    """
    Get the cluster name.

    This method returns the cluster name for the Cytoscape graph
    """
    return [{"data": {"id": "dacloud",
                      "label": "dacloud"},
             "classes": "entity"}]


def get_cluster_services(api_client=None):
    """
    Get the cluster services.

    This method returns the cluster services for the Cytoscape graph
    """
    try:
        load_kubernetes_config()

        api = kubernetes.client.CoreV1Api(api_client=api_client)
        api_response = api.list_service_for_all_namespaces(pretty='true')
    except Exception as e:
        print("Cant connect to the cluster: %s" % (e))
        return []

    s_list = []
    for service in api_response.items:
        s_list.append({"data": {"id": "service-" + service.metadata.name,
                                "label": service.metadata.name,
                                "parent": "services"},
                       "group": "nodes", "classes": "svc"})
        if service.spec.selector:
            labels = []
            for k, v in service.spec.selector.items():
                labels.append(k + "=" + v)
            filter = ','.join(map(str, labels))
            for idx, pod in enumerate(get_cluster_pods(label_selector=filter)):
                s_list.append({"data": {"id": "edge-" +
                                              service.metadata.name +
                                              "-" +
                                              str(idx),
                                        "source": "service-" +
                                                  service.metadata.name,
                                        "target": pod['data']['id']},
                               "group": "edges", "classes": "influence"})
    return s_list


def get_cluster_deployments(api_client=None):
    """
    Get the cluster deployments.

    This method returns the cluster deployments for the Cytoscape graph
    """
    try:

        load_kubernetes_config(api_client=api_client)

        api = kubernetes.client.AppsV1Api()
        api_response = api.list_deployment_for_all_namespaces(pretty='true')
    except Exception as e:
        print("Cant connect to the cluster: %s" % (e))
        return []

    dep_list = []
    for deployment in api_response.items:
        dep_list.append({"data": {"id": "deployment-" +
                                        deployment.metadata.name,
                                  "label": deployment.metadata.name,
                                  "parent": "deployments"},
                         "group": "nodes", "classes": "deploy"})
        if deployment.spec.selector:
            labels = []
            for k, v in deployment.spec.selector.match_labels.items():
                labels.append(k + "=" + v)
            filter = ','.join(map(str, labels))
            for idx, pod in enumerate(get_cluster_pods(label_selector=filter)):
                dep_list.append({"data": {"id": "edge-" +
                                                deployment.metadata.name +
                                                "-" +
                                                str(idx),
                                          "source": "deployment-" +
                                                    deployment.metadata.name,
                                          "target": pod['data']['id']},
                                 "group": "edges", "classes": "influence"})
    return dep_list


def get_cluster_nodes(api_client=None):
    """
    Get the cluster nodes.

    This method returns the cluster nodes for the Cytoscape graph
    """
    try:

        load_kubernetes_config()

        api = kubernetes.client.CoreV1Api(api_client=api_client)
        api_response = api.list_node(pretty='true')
    except Exception as e:
        print("Cant connect to the cluster: %s" % (e))
        return []

    nodes_list = []
    for node in api_response.items:
        nodes_list.append({"data": {"id": "node-" +
                                          node.metadata.name,
                                    "label": node.metadata.name,
                                    "parent": "nodes"},
                           "classes": "entity"})
    return nodes_list


def get_cluster_pods(label_selector='', api_client=None):
    """
    Get the cluster pods.

    This method returns the cluster pods for the Cytoscape graph
    """
    try:

        load_kubernetes_config()

        api = kubernetes.client.CoreV1Api(api_client=api_client)
        res = api.list_pod_for_all_namespaces(pretty=
                                              'true',
                                              field_selector=
                                              'status.phase=Running',
                                              label_selector=
                                              label_selector)
    except Exception as e:
        print("Cant connect to the cluster: %s" % (e))
        return []

    pods_list = []
    for pod in res.items:
        pods_list.append({"data": {"id": "pod-" + pod.metadata.name,
                                   "label": pod.metadata.name,
                                   "parent": "node-" + pod.spec.node_name},
                          "group": "nodes", "classes": "pod"})
    return pods_list


def get_cluster_graph(api_client=None):
    """
    Get the cluster graph.

    This method returns the cluster graph data Cytoscape
    """
    cluster_graph = []
    cluster_graph += get_cluster_name()

    cluster_graph.append({"data": {"id": "services",
                                   "label": "services",
                                   "parent": "dacloud"},
                          "classes": "entity"})
    cluster_graph += get_cluster_services()

    cluster_graph.append({"data": {"id": "deployments",
                                   "label": "deployments",
                                   "parent": "dacloud"},
                          "classes": "entity"})
    cluster_graph += get_cluster_deployments()

    cluster_graph.append({"data": {"id": "nodes",
                                   "label": "nodes",
                                   "parent": "dacloud"},
                          "classes": "entity"})
    cluster_graph += get_cluster_nodes()

    # We add the pods to the nodes
    cluster_graph += get_cluster_pods()
    return cluster_graph
