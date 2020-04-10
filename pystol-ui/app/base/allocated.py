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
from pint        import UnitRegistry
from collections import defaultdict


PYSTOL_BRANCH = "master"
__all__ = ["compute_allocated_resources"]


def compute_allocated_resources():
    ureg = UnitRegistry()
    ureg.load_definitions(os.path.join(os.getcwd(), 'app/base/kubernetes_units.txt'))
    Q_ = ureg.Quantity
    data = {}

    state_info = {'pods': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'cpu': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'mem': {'allocatable': 0, 'allocated': 0, 'percentage': 0},
                  'storage': {'allocatable': 0, 'allocated': 0, 'percentage': 0}
                  }


    # doing this computation within a kubernetes cluster
    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()

    global_pods_allocatable = 0
    global_pods_allocated = 0

    global_cpu_allocatable = 0
    global_cpu_allocated = 0

    global_mem_allocatable = 0
    global_mem_allocated = 0

    global_storage_allocatable = 10000
    global_storage_allocated = 1750

    try:
        nodes_list = core_v1.list_node().items
    except Exception as e:
        print("Something bad happened: " + e)

    for node in nodes_list:
        stats          = {}
        node_name      = node.metadata.name
        allocatable    = node.status.allocatable
        max_pods       = int(int(allocatable["pods"]) * 1.5)

        global_pods_allocatable = global_pods_allocatable + max_pods

        field_selector = ("status.phase!=Succeeded,status.phase!=Failed," +
                          "spec.nodeName=" + node_name)

        stats["cpu_alloc"] = Q_(allocatable["cpu"])
        stats["mem_alloc"] = Q_(allocatable["memory"])
        stats["storage_alloc"] = Q_(allocatable["ephemeral-storage"])

        global_cpu_allocatable = global_cpu_allocatable + Q_(allocatable["cpu"])
        global_mem_allocatable = global_mem_allocatable + Q_(allocatable["memory"])
        # global_storage_allocatable = global_storage_allocatable + Q_(allocatable["ephemeral-storage"])


        pods = core_v1.list_pod_for_all_namespaces(limit=max_pods,
                                                   field_selector=field_selector).items

        # compute the allocated resources
        cpureqs,cpulmts,memreqs,memlmts,storagereqs = [], [], [], [], []

        global_pods_allocated = global_pods_allocated + len(pods)

        for pod in pods:
            #print("****")
            #print(pod.stats)
            #print("****")
            for container in pod.spec.containers:

                res  = container.resources
                reqs = defaultdict(lambda: 0, res.requests or {})
                lmts = defaultdict(lambda: 0, res.limits or {})
                cpureqs.append(Q_(reqs["cpu"]))
                memreqs.append(Q_(reqs["memory"]))
                storagereqs.append(Q_(reqs["ephemeral-storage"]))

                cpulmts.append(Q_(lmts["cpu"]))
                memlmts.append(Q_(lmts["memory"]))
                #print("----")
                #print(res)
                #print(Q_(reqs["ephemeral-storage"]))
                #print(Q_(lmts["ephemeral-storage"]))
                #print("----")
                # storagelmts.append(Q_(lmts["ephemeral-storage"]))

        stats["cpu_req"]     = sum(cpureqs)
        stats["cpu_lmt"]     = sum(cpulmts)
        stats["cpu_req_per"] = (stats["cpu_req"] / stats["cpu_alloc"] * 100)
        stats["cpu_lmt_per"] = (stats["cpu_lmt"] / stats["cpu_alloc"] * 100)

        stats["mem_req"]     = sum(memreqs)
        stats["mem_lmt"]     = sum(memlmts)
        stats["mem_req_per"] = (stats["mem_req"] / stats["mem_alloc"] * 100)
        stats["mem_lmt_per"] = (stats["mem_lmt"] / stats["mem_alloc"] * 100)

        #stats["storage_req"]     = sum(storagereqs)
        #stats["storage_lmt"]     = sum(storagelmts)
        #stats["storage_req_per"] = (stats["storage_req"] / stats["storage_alloc"] * 100)
        #stats["storage_lmt_per"] = (stats["storage_lmt"] / stats["storage_alloc"] * 100)

        global_cpu_allocated = global_cpu_allocated + sum(cpureqs)
        global_mem_allocated = global_mem_allocated + sum(memreqs)

        data[node_name] = stats

    state_info['pods']['allocatable'] = global_pods_allocatable
    state_info['pods']['allocated'] = global_pods_allocated
    state_info['pods']['percentage'] = (global_pods_allocated * 100) // global_pods_allocatable

    state_info['cpu']['allocatable'] = (global_cpu_allocatable.magnitude * 1000)
    state_info['cpu']['allocated'] = global_cpu_allocated
    state_info['cpu']['percentage'] = ((global_cpu_allocated * 100) // global_cpu_allocatable).magnitude

    state_info['mem']['allocatable'] = global_mem_allocatable.to(ureg.Mi)
    state_info['mem']['allocated'] = global_mem_allocated.to(ureg.Mi)
    state_info['mem']['percentage'] = ((int(global_mem_allocated.to(ureg.Mi).magnitude) * 100) // int(global_mem_allocatable.to(ureg.Mi).magnitude))

    state_info['storage']['allocatable'] = global_storage_allocatable
    state_info['storage']['allocated'] = global_storage_allocated
    state_info['storage']['percentage'] = (global_storage_allocated * 100) // global_storage_allocatable

    return state_info



