
"""
Uses watch to print the stream of events from list namespaces and list pods.
The script will wait for 10 events related to namespaces to occur within
the `timeout_seconds` threshold and then move on to wait for another 10 events
related to pods to occur within the `timeout_seconds` threshold.
"""
import json
import os
import random
import string
import sys
import urllib
import kubernetes
from kubernetes import client, config, watch
from app.base.k8s import load_kubernetes_config


def state_cluster():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    v1 = client.CoreV1Api()
    count = 10
    w = watch.Watch()
    ret = []
    for event in w.stream(v1.list_namespace, timeout_seconds=10):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
       # ret.append(event) 
        ret.append({'type': event['type'],
                    'name': event['object'].metadata.name,
                       })
        if not count:
            w.stop()
    return ret

"""     for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
        print("Event: %s %s %s" % (
            event['type'],
            event['object'].kind,
            event['object'].metadata.name)
        )
        count -= 1
        if not count:
            w.stop() """

def state_nodes():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    v1 = client.CoreV1Api()
    count = 100
    w = watch.Watch()
    ret = []
    for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
        print("Event: %s %s %s" % (
            event['type'],
            event['object'].kind,
            event['object'].metadata.name),
            event['object'].status.pod_ip, 
            event['object'].metadata.namespace, 
        )
        count -= 1
       # ret.append(event) 
        ret.append({'type': event['type'],
                    'kind': event['object'].kind,
                    'name': event['object'].metadata.name,
                    'ip': event['object'].status.pod_ip, 
                    'namespace': event['object'].metadata.namespace, 
                       })
        if not count:
            w.stop()
    return ret

def state_namespaces():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    v1 = client.CoreV1Api()
    count = 10
    w = watch.Watch()
    ret = []
    for event in w.stream(v1.list_namespace, timeout_seconds=10):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
       # ret.append(event) 
        ret.append({'type': event['type'],
                    'name': event['object'].metadata.name,
                       })
        if not count:
            w.stop()
    return ret

