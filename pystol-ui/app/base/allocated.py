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

from pint import UnitRegistry
from collections import defaultdict


ureg = UnitRegistry()
# Pod
ureg.define("pods = 1 = [pods]")

# Mem
ureg.define("kmemunits = 1 = [kmemunits]")
ureg.define("Ki = 1024 * kmemunits")
ureg.define("Mi = Ki^2")
ureg.define("Gi = Ki^3")
ureg.define("Ti = Ki^4")
ureg.define("Pi = Ki^5")
ureg.define("Ei = Ki^6")
# CPU
ureg.define("kcpuunits = 1 = [kcpuunits]")
ureg.define("m = 1/1000 * kcpuunits")
ureg.define("k = 1000 * kcpuunits")
ureg.define("M = k^2")
ureg.define("G = k^3")
ureg.define("T = k^4")
ureg.define("P = k^5")
ureg.define("E = k^6")

Q_ = ureg.Quantity

def compute_allocated_resources():
    state_info = {'pods': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'cpu': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'mem': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'storage': {'allocatable': 0, 'allocated': 0, 'percentage': 0}
                  }

    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()

    try:
        nodes_list = core_v1.list_node().items
    except Exception as e:
        print("Problem listing nodes")
        # print("Something bad happened: " + e)

    for node in nodes_list:
        node_name      = node.metadata.name
        node_stats = compute_node_resources(node_name)

        state_info['pods']['allocatable'] = state_info['pods']['allocatable'] + node_stats['pods']['allocatable']
        state_info['pods']['allocated'] = state_info['pods']['allocated'] + node_stats['pods']['allocated']

        state_info['cpu']['allocatable'] = state_info['cpu']['allocatable'] + node_stats['cpu']['allocatable']
        state_info['cpu']['allocated'] = state_info['cpu']['allocated'] + node_stats['cpu']['allocated']

        state_info['mem']['allocatable'] = state_info['mem']['allocatable'] + node_stats['mem']['allocatable']
        state_info['mem']['allocated'] = state_info['mem']['allocated'] + node_stats['mem']['allocated']

        state_info['storage']['allocatable'] = state_info['storage']['allocatable'] + node_stats['storage']['allocatable']
        state_info['storage']['allocated'] = state_info['storage']['allocated'] + node_stats['storage']['allocated']

    state_info['pods']['percentage'] = (int(state_info['pods']['allocated'].magnitude) * 100) // int(state_info['pods']['allocatable'].magnitude)
    state_info['cpu']['percentage'] = (int(state_info['cpu']['allocated'].magnitude) * 100) // int(state_info['cpu']['allocatable'].magnitude)
    state_info['mem']['percentage'] = (int(state_info['mem']['allocated'].magnitude) * 100) // int(state_info['cpu']['allocatable'].magnitude)
    state_info['storage']['percentage'] = (int(state_info['storage']['allocated'].magnitude) * 100) // int(state_info['storage']['allocatable'].magnitude)

    return state_info


def compute_node_resources(node_name):
    state_info = {'pods': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'cpu': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'mem': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'storage': {'allocatable': 0, 'allocated': 0, 'percentage': 0}
                  }

    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()

    field_selector = ("metadata.name=" + node_name)

    try:
        node = core_v1.list_node(field_selector=field_selector).items[0]
    except Exception as e:
        print("Problem listing nodes")
        # print("Something bad happened: " + e)

    stats          = {}
    node_name      = node.metadata.name
    allocatable    = node.status.allocatable
    max_pods       = int(int(allocatable["pods"]) * 1.5)

    field_selector = ("status.phase!=Succeeded,status.phase!=Failed," +
                          "spec.nodeName=" + node_name)

    cpu_allocatable = Q_(allocatable["cpu"])
    cpu_allocatable.ito(ureg.m)
    state_info["cpu"]["allocatable"] = cpu_allocatable

    mem_allocatable = Q_(allocatable["memory"])
    mem_allocatable.ito(ureg.Mi)
    state_info["mem"]["allocatable"] = mem_allocatable

    # https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/
    storage_allocatable = Q_(allocatable["ephemeral-storage"])
    storage_allocatable.ito(ureg.Mi)
    state_info["storage"]["allocatable"] = storage_allocatable

    state_info["pods"]["allocatable"] = max_pods * ureg.pods

    pods = core_v1.list_pod_for_all_namespaces(limit=max_pods,
                                               field_selector=field_selector).items

    state_info["pods"]["allocated"] = len(pods) * ureg.pods

    # compute the allocated resources
    cpureqs,memreqs,storagereqs = [], [], []
    #cpulmts,memlmts,storagelmts = [], [], []

    for pod in pods:
        for container in pod.spec.containers:
            res  = container.resources
            reqs = defaultdict(lambda: 0, res.requests or {})
            lmts = defaultdict(lambda: 0, res.limits or {})

            cpureqs.append(Q_(reqs["cpu"]))
            memreqs.append(Q_(reqs["memory"]))
            storagereqs.append(Q_(reqs["ephemeral-storage"]))

            #cpulmts.append(Q_(lmts["cpu"]))
            #memlmts.append(Q_(lmts["memory"]))
            #storagelmts.append(Q_(lmts["ephemeral-storage"]))

    cpu_allocated = sum(cpureqs)
    cpu_allocated.ito(ureg.m)
    state_info["cpu"]["allocated"] = cpu_allocated

    mem_allocated = sum(memreqs)
    mem_allocated.ito(ureg.Mi)
    state_info["mem"]["allocated"] = mem_allocated

    storage_allocated = sum(storagereqs)
    storage_allocated.ito(ureg.Mi)
    state_info["storage"]["allocated"] = storage_allocated

    state_info['pods']['percentage'] = (int(state_info['pods']['allocated'].magnitude) * 100) // int(state_info['pods']['allocatable'].magnitude)
    state_info['cpu']['percentage'] = (int(state_info['cpu']['allocated'].magnitude) * 100) // int(state_info['cpu']['allocatable'].magnitude)
    state_info['mem']['percentage'] = (int(state_info['mem']['allocated'].magnitude) * 100) // int(state_info['mem']['allocatable'].magnitude)
    state_info['storage']['percentage'] = (int(state_info['storage']['allocated'].magnitude) * 100) // int(state_info['storage']['allocatable'].magnitude)

    return state_info



