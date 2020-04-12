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

from kubernetes.client.rest import ApiException


def hexagons_data():
    hexa_data = []

    # doing this computation within a kubernetes cluster
    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()

    try:
        nodes_list = core_v1.list_node().items
    except Exception as e:
        print("Something bad happened: " + e)

    for node in nodes_list:
        #print(node)
        node_name      = node.metadata.name
        node_labels = node.metadata.labels
        # print(node_labels)
        if "node-role.kubernetes.io/master" in node_labels:
            if node_labels['node-role.kubernetes.io/master'] == 'true':
                node_role = "Master"
            else:
                node_role = "Non master"
        else:
            node_role = "Non master"

        allocatable = node.status.allocatable
        node_info = node.status.node_info


        print("------")
        print("------")
        print("------")
        print(node_info.architecture)
        print("------")
        print("------")
        print("------")
        hdata = {}
        hdata['name'] = node_name
        hdata['role'] = node_role
        hdata['cpu'] = allocatable["cpu"]
        hdata['ephstorage'] = allocatable["ephemeral-storage"]
        hdata['mem'] = allocatable["memory"]
        hdata['maxpods'] = allocatable["pods"]

        hdata['arch'] = node_info.architecture
        hdata['crver'] = node_info.container_runtime_version
        hdata['kernelver'] = node_info.kernel_version
        hdata['kubeproxyver'] = node_info.kube_proxy_version
        hdata['kubeletver'] = node_info.kubelet_version
        hdata['os'] = node_info.operating_system

        max_pods       = int(int(allocatable["pods"]) * 1.5)
        field_selector = ("status.phase!=Succeeded," +
                          "spec.nodeName=" + node_name)
        pods = core_v1.list_pod_for_all_namespaces(limit=max_pods,
                                                   field_selector=field_selector).items
        hdata['pods'] = []
        for pod in pods:
            # print(pod.metadata.name)
            # print(pod)
            hdata['pods'].append({'name': pod.metadata.name,
                                  'namespace':pod.metadata.namespace,
                                  'host_ip':pod.status.host_ip,
                                  'pod_ip':pod.status.pod_ip,
                                  'phase':pod.status.phase})
        hexa_data.append(hdata)

    # print(hexa_data)
    return hexa_data
