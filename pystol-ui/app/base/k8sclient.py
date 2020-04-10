
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


def load_kubernetes_config():
    """
    Load the initial config details.

    We load the config depending where we execute the code from
    """
    try:
        if 'KUBERNETES_PORT' in os.environ:
            # We set up the client from within a k8s pod
            kubernetes.config.load_incluster_config()
        elif 'KUBECONFIG' in os.environ:
            kubernetes.config.load_kube_config(os.getenv('KUBECONFIG'))
        else:
            kubernetes.config.load_kube_config()
    except Exception as e:
        message = ("---\n"
                   "The Python Kubernetes client could not be configured "
                   "at this time.\n"
                   "You need a working Kubernetes deployment to make "
                   "Pystol work.\n"
                   "Check the following:\n"
                   "Use the env var KUBECONFIG with the path to your K8s "
                   "config file like:\n"
                   "    export KUBECONFIG=~/.kube/config\n"
                   "Or run Pystol from within the cluster to make use of "
                   "load_incluster_config.\n"
                   "Error: " % (e))
        print(message)
        print("---")
        print("The current Pystol version is: %s" % (pystol_version))
        print(" ")
        print("Bye...")
        sys.exit(0)



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
    count = 10
    w = watch.Watch()
    ret = []
    for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
        print("Event: %s %s %s" % (
            event['type'],
            event['object'].kind,
            event['object'].metadata.name)
        )
        count -= 1
       # ret.append(event) 
        ret.append({'type': event['type'],
                    'kind': event['object'].kind,
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
               