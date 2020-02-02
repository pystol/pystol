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

from functools import partial
from operator import methodcaller

import kubernetes
import os
import random
import string

from pystol.const import CRD_DOMAIN, \
                         CRD_PLURAL, \
                         CRD_VERSION, \
                         ALLOWED_EVENT_TYPES, \
                         CREATE_TYPES_MAP, \
                         LIST_TYPES_MAP

__all__ = [
    'handle',
]

try:
    if 'KUBECONFIG' in os.environ:
        kubernetes.config.load_kube_config(os.getenv('KUBECONFIG'))
    else:
        kubernetes.config.load_kube_config()
except IOError:
    try:
        kubernetes.config.load_incluster_config()  # We set up the client from within a k8s pod
    except kubernetes.config.config_exception.ConfigException:
        raise KubernetesException("Could not configure kubernetes python client")

custom_obj = kubernetes.client.CustomObjectsApi()
v1 = kubernetes.client.CoreV1Api()

#
# Part of the operation in charge of adding the custom resources
# to the Kubernetes cluster, this will create an object with
# the CLI parameters.
#

def insert_pystol_object(collection, name, extra_vars):
    """
    Here we will determine where we will insert the CR.

    This is a main component of the input for the controller
    """
    print(collection)
    print(name)
    print(extra_vars)

    resource = {
      "apiVersion": "pystol.org/v1alpha1",
      "kind": "PystolAction",
      "metadata": {"name": "pystol-" + collection + "-" + name},
      "spec": {"collection": collection, "name": name, "extra-vars": extra_vars, "result": "{}"},
    }

    # create the resource
    custom_obj.create_namespaced_custom_object(
        group="pystol.org",
        version="v1alpha1",
        namespace="default",
        plural="pystolactions",
        body=my_resource,
    )

#
# Part of the operator which will handle the process of new
# PystolAction objects added in the cluster, It will watch
# for a new object and create a software deployment to run
# the selected Pystol action.
#

def watch_for_pystol_jobs(stop):
    while True:
      a = 2

def watch_for_pystol_objects(stop):
    """
    Initiate the main listening method.

    This method will listen for custom objects
    added to the cluster.
    The watcher is defined here.
    """
    w = kubernetes.watch.Watch()
    for event in w.stream(custom_obj.list_cluster_custom_object, CRD_DOMAIN, CRD_VERSION, CRD_PLURAL, resource_version=''):
        obj = event["object"]
        operation = event['type']
        spec = obj.get("spec")
        if not spec:
            continue
        metadata = obj.get("metadata")
        resource_version = metadata['resourceVersion']
        name = metadata['name']
        print("Handling %s on %s" % (operation, name))
        done = spec.get("executed", False)
        if done:
            continue
        execute_pystol_action(custom_obj, obj)

def execute_pystol_action(crds, obj):
    """
    Execute the Pystol action.

    This method will execute the Pystol action
    defined in the custom object.
    """

    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["executed"] = True

    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(CRD_DOMAIN, CRD_VERSION, namespace, CRD_PLURAL, name, obj)

    # Create the job definition
    api_instance = kubernetes.client.BatchV1Api()

    container_image = "quay.io/pystol/pystol-operator-stable:latest"

    body = kube_create_job_object(name, container_image, env_vars={"VAR": "TESTING"})
    try: 
        api_response = api_instance.create_namespaced_job("default", body, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return

def kube_create_job_object(name, container_image, namespace="default", container_name="jobcontainer", env_vars={}):

    # Body is the object Body
    body = kubernetes.client.V1Job(api_version="batch/v1", kind="Job")
    # Body needs Metadata
    # Attention: Each JOB must have a different name!
    body.metadata = kubernetes.client.V1ObjectMeta(namespace=namespace, name=name)
    # And a Status
    body.status = kubernetes.client.V1JobStatus()
     # Now we start with the Template...
    template = kubernetes.client.V1PodTemplate()
    template.template = kubernetes.client.V1PodTemplateSpec()
    # Passing Arguments in Env:
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( kubernetes.client.V1EnvVar(name=env_name, value=env_value) )

    command = ["/bin/bash"]
    args = ["-c", "ansible-galaxy collection install newswangerd.collection_demo; \
                   ansible localhost -m newswangerd.collection_demo.real_facts; exit 0"]
    #               ansible-playbook /path/to/collection/collectoin_in_playbook.yml -i /etc/ansible/hosts -vv; exit 0"]
    # args = ["-c", "kubectl get pods"]

    container = kubernetes.client.V1Container(name=container_name, image=container_image, command=command, args=args, env=env_list)
    template.template.spec = kubernetes.client.V1PodSpec(containers=[container], restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = kubernetes.client.V1JobSpec(ttl_seconds_after_finished=600, template=template.template)
    return body

def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
