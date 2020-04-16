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

from app.base.k8s import load_kubernetes_config

import kubernetes


def get_cluster_name():
    return [{"data": {"id": "dacloud","label": "dacloud"},
             "classes": "entity"
           }]


def get_cluster_services():
    load_kubernetes_config()
    api = kubernetes.client.CoreV1Api()
    api_response = api.list_service_for_all_namespaces(pretty='true')
    services_list = []
    for service in api_response.items:
        services_list.append({"data": {"id": service.metadata.name,"label": service.metadata.name,"parent": "services"},"group": "nodes","classes": "input"})
    return services_list


def get_cluster_deployments():
    load_kubernetes_config()
    api = kubernetes.client.AppsV1Api()
    api_response = api.list_deployment_for_all_namespaces(pretty='true')
    deployments_list = []
    for deployment in api_response.items:
        deployments_list.append({"data": {"id": deployment.metadata.name,"label": deployment.metadata.name,"parent": "deployments"},"group": "nodes","classes": "input"})

    return deployments_list


def get_cluster_nodes():
    load_kubernetes_config()
    api = kubernetes.client.CoreV1Api()
    api_response = api.list_node(pretty='true')
    nodes_list = []
    for node in api_response.items:
        nodes_list.append({"data": {"id": node.metadata.name,"label": node.metadata.name,"parent": "nodes"},"classes": "entity"})
    return nodes_list


def get_cluster_pods():
    load_kubernetes_config()
    api = kubernetes.client.CoreV1Api()
    api_response = api.list_pod_for_all_namespaces(pretty='true')
    pods_list = []
    for pod in api_response.items:
        pods_list.append({"data": {"id": pod.metadata.name,"label": pod.metadata.name,"parent": pod.spec.node_name},"group": "nodes","classes": "input"})
    return pods_list

def get_cluster_graph():
    cluster_graph = []
    cluster_graph += get_cluster_name()

    cluster_graph.append({"data": {"id": "services","label": "services","parent": "dacloud"},"classes": "entity"})
    cluster_graph += get_cluster_services()

    cluster_graph.append({"data": {"id": "deployments","label": "deployments","parent": "dacloud"},"classes": "entity"})
    cluster_graph += get_cluster_deployments()

    cluster_graph.append({"data": {"id": "nodes","label": "nodes","parent": "dacloud"},"classes": "entity"})
    cluster_graph += get_cluster_nodes()

    # We add the pods to the nodes
    cluster_graph += get_cluster_pods()
    return cluster_graph
