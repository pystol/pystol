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
        # print(node)
        node_name      = node.metadata.name
        node_labels = node.metadata.labels
        # print(node_labels)
        if node_labels['node-role.kubernetes.io/master'] == 'true':
            node_role = "Master"
        else:
            node_role = "Non master"

        allocatable    = node.status.allocatable
        hdata = {}
        hdata['name'] = node_name
        hdata['role'] = node_role

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

    print(hexa_data)

    aux = [
{
      "name":"node-00",
      "role":"Master",
      "pods":[
         {
            "name":"coredns-66bf467f8-lzn8z",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.2",
            "phase":"Running"
         },
         {
            "name":"coredns-66bff67f8-vhxp4",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.3",
            "phase":"Running"
         },
         {
            "name":"etcd-minikube",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"kube-apiserver-minikube",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"kube-controller-manager-minikube",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"kube-proxy-5r5txd",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"kube-scheduler-minikube",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"storage-provisioner",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"dashboard-metrics-scraper-84b5fdf55ff-qq6j2",
            "namespace":"kubernetes-dashboard",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.4",
            "phase":"Running"
         },
         {
            "name":"kubernetes-dashboard-bc4456cc64-nm69d",
            "namespace":"kubernetes-dashboard",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.5",
            "phase":"Running"
         },
         {
            "name":"pystol-controller-667df549448-t8brm",
            "namespace":"pystol",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.6",
            "phase":"Running"
         },
         {
            "name":"pystol-ui-8554cbb6558-hg8kh",
            "namespace":"pystol",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.7",
            "phase":"Running"
         }
      ]
   },
   {
      "name":"node-01",
      "role":"Non master",
      "pods":[
         {
            "name":"coredns-66bff467f8-lzn8z",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.2",
            "phase":"Running"
         },
         {
            "name":"coredns-66bff467f8-vhxp4",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.3",
            "phase":"Running"
         },
         {
            "name":"kube-proxy-5rtxd",
            "namespace":"kube-system",
            "host_ip":"192.168.39.125",
            "pod_ip":"192.168.39.125",
            "phase":"Running"
         },
         {
            "name":"dashboard-metrics-scraper-84bfdf55ff-qq6j2",
            "namespace":"kubernetes-dashboard",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.4",
            "phase":"Running"
         },
         {
            "name":"kubernetes-dashboard-bc446cc64-nm69d",
            "namespace":"kubernetes-dashboard",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.5",
            "phase":"Running"
         },
         {
            "name":"pystol-controller-667df49448-t8brm",
            "namespace":"pystol",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.6",
            "phase":"Running"
         },
         {
            "name":"pystol-ui-8554cbb658-hg8kh",
            "namespace":"pystol",
            "host_ip":"192.168.39.125",
            "pod_ip":"172.17.0.7",
            "phase":"Running"
         }
      ]
   }
]
    return hexa_data
    # return aux
