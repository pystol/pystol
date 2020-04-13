import json
import os
import random
import string
import sys
import urllib
import kubernetes
from kubernetes import client, config, watch
from app.base.k8s import load_kubernetes_config
import subprocess

def state_cluster():
    # Configs can be set in Configuration class directly or using helper
    #config.load_kube_config()
    ret = []
     
    return ret


def state_nodes():
    datanodes = []
    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()
    nodes = core_v1.list_node().items
    for node in nodes:
        #print(node) 
        datanodes.append({'name': node.metadata.name,
                            'status': node.status.phase,       
        })
    return datanodes
    #print(data_nodes)

def state_namespaces():
    datanamespaces = []
    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()
    namespaces = core_v1.list_namespace().items
   # print(datanamespaces)
    for namespace in namespaces:
       # print(namespace) 
        datanamespaces.append({'name':namespace.metadata.name,
                                'status':namespace.status.phase,       
        })
    return datanamespaces

def state_pods():
    data_pods = []
    load_kubernetes_config()
    core_v1 = kubernetes.client.CoreV1Api()
    pods = core_v1.list_pod_for_all_namespaces().items
    
    for pod in pods:
        #print(pod) 
        data_pods.append({'name': pod.metadata.name,
                                  'namespace':pod.metadata.namespace,
                                  'host_ip':pod.status.host_ip,
                                  'pod_ip':pod.status.pod_ip,
                                  'phase':pod.status.phase})
   
    return data_pods
    #print(data_pods)

def web_terminal():
    config.load_kube_config()
    ret = []
    command = 'kubectl get po --all-namespaces' # 'kubectl config view -o jsonpath='{.clusters[].name}'
    output  = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    ret.append(output.decode('utf-8'))
    return ret


def cluster_name_configured():
    config.load_kube_config()
    ret = []
    # TODO: Get cluster name from 
    # kubectl -n kube-system get configmap kubeadm-config -o yaml

    command = 'kubectl config view -o jsonpath="{.clusters[].name}"'
    output  = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    ret.append(output.decode('utf-8'))
    return ret
