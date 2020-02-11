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

import json
import kubernetes
import os
import random
import string
import sys

from pystol import __version__
from pystol.const import CRD_DOMAIN, \
                         CRD_PLURAL, \
                         CRD_VERSION, \
                         ALLOWED_EVENT_TYPES, \
                         CREATE_TYPES_MAP, \
                         LIST_TYPES_MAP

__all__ = [
    'handle',
]

pystol_version = __version__

#custom_obj = kubernetes.client.CustomObjectsApi()
#v1 = kubernetes.client.CoreV1Api()

#
# We load the Kubernetes cluster config depending
# where we execute the operator from.
#

def load_kubernetes_config():
    """
    Here we will load the initial config details

    We load the config depending where we execute the code from
    """
    try:
        if 'KUBERNETES_PORT' in os.environ:
            kubernetes.config.load_incluster_config() # We set up the client from within a k8s pod
        elif 'KUBECONFIG' in os.environ:
            kubernetes.config.load_kube_config(os.getenv('KUBECONFIG'))
        else:
            kubernetes.config.load_kube_config()
    except:
        message = ("---\n"
                   "The Python Kubernetes client could not be configured at this time.\n"
                   "You need a working Kubernetes deployment to make Pystol work.\n"
                   "Check the following:\n"
                   "Use the env var KUBECONFIG with the path to your K8s config file like:\n"
                   "    export KUBECONFIG=~/.kube/config\n"
                   "Or run Pystol from within the cluster to make use of load_incluster_config.")
        print(message)
        print("---")
        print("The current Pystol version is: %s"%(pystol_version))
        print("")
        print("Bye...")
        sys.exit(0)

#
# Part of the operation in charge of adding the custom resources
# to the Kubernetes cluster, this will create an object with
# the CLI parameters.
#

def insert_pystol_object(namespace, collection, role, source, extra_vars):
    """
    Here we will determine where we will insert the CR.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()
    v1 = kubernetes.client.CoreV1Api()

    resource = {
      "apiVersion": "pystol.org/v1alpha1",
      "kind": "PystolAction",
      "metadata": {"name": "pystol-action-" + namespace + "-" + collection + "-" + role + "-" + id_generator()},
      "spec": {"namespace": namespace,
               "collection": collection,
               "role": role,
               "source": source,
               "extra_vars": extra_vars,
               "action_state": "CRE",
               "workflow_state": "WFA",
               "action_stderr": "{}",
               "action_stdout": "{}"},
    }

    # create the resource
    api_response = custom_obj.create_namespaced_custom_object(
        group="pystol.org",
        version="v1alpha1",
        # TODO: Move this to a specific namespace
        namespace="default",
        plural="pystolactions",
        body=resource,
    )
    return api_response

#
# Part of the operator which will handle the process of new
# PystolAction objects added in the cluster, It will watch
# for a new object and create a software deployment to run
# the selected Pystol action.
#

def watch_for_pystol_timeouts(stop):
    while True:
      a = 2

def watch_for_pystol_objects(stop):
    """
    Initiate the main listening method.

    This method will listen for custom objects
    added to the cluster.
    The watcher is defined here.
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()
    v1 = kubernetes.client.CoreV1Api()

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
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()
    v1 = kubernetes.client.CoreV1Api()

    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s" % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")
    obj["spec"]["executed"] = True

    # The main Pystol object initial info are the parameters:
    # These values should be the ones defined in the CRD.

    action_spec_params = obj.get("spec")
    action_namespace = action_spec_params["namespace"]
    action_collection = action_spec_params["collection"]
    action_role = action_spec_params["role"]
    action_source = action_spec_params["source"]
    action_extra_vars = action_spec_params["extra_vars"]
    action_action_state = action_spec_params["action_state"]
    action_workflow_state = action_spec_params["workflow_state"]
    action_action_stdout = action_spec_params["action_stdout"]
    action_action_stderr = action_spec_params["action_stderr"]

    print("Updating: %s" % name)
    crds.replace_namespaced_custom_object(CRD_DOMAIN, CRD_VERSION, namespace, CRD_PLURAL, name, obj)

    # Create the job definition
    api_instance = kubernetes.client.BatchV1Api()

    # TODO: This should be configurable
    container_image = "quay.io/pystol/pystol-operator-stable:latest"

    body = kube_create_job_object(name=name,
                                  container_image=container_image,
                                  namespace=namespace,
                                  env_vars={"VAR": "TESTING"},
                                  # CRD variables
                                  action_namespace=action_namespace,
                                  action_collection=action_collection,
                                  action_role=action_role,
                                  action_source=action_source,
                                  action_extra_vars=action_extra_vars,
                                  action_action_state=action_action_state,
                                  action_workflow_state=action_workflow_state,
                                  action_action_stdout=action_action_stdout,
                                  action_action_stderr=action_action_stderr)

    try:
        api_response = api_instance.create_namespaced_job("default", body, pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return

def kube_create_job_object(name,
                           container_image,
                           namespace,
                           env_vars,
                           action_namespace,
                           action_collection,
                           action_role,
                           action_source,
                           action_extra_vars,
                           action_action_state,
                           action_workflow_state,
                           action_action_stdout,
                           action_action_stderr):
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi()
    v1 = kubernetes.client.CoreV1Api()

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

    # Python interpreter as an extra variable
    # python object to be appended
    y = {"ansible_python_interpreter":"/usr/bin/python3","pystol_action_id":name}
    # parsing JSON string:
    extra_ansible_vars = json.loads(action_extra_vars)
    # appending the data
    extra_ansible_vars.update(y)

    command = ["/bin/bash"]
    if (action_source == "galaxy.ansible.com"):
        args = ["-c", "echo '---' > requirements.yml; \
                       echo 'collections:' >> requirements.yml; \
                       echo '- name: " + action_namespace + "." + action_collection + "' >> requirements.yml; \
                       echo '  source: https://" + action_source + "' >> requirements.yml; \
                       ansible-galaxy collection install --force -r requirements.yml; \
                       ansible -m include_role -a 'name=" + action_namespace + "." + action_collection + "." + action_role + "' -e '" + str(extra_ansible_vars) + "' localhost -vv; exit 0"]
    else:
        args = ["-c", "echo '---'; \
                       git clone " + action_source + " cloned_repo; \
                       cd cloned_repo; \
                       cd " + action_collection + "; \
                       mkdir -p releases; \
                       ansible-galaxy collection build -v --force --output-path releases/; \
                       cd releases; \
                       LATEST=$(ls *.tar.gz | grep -v latest | sort -V | tail -n1); \
                       ansible-galaxy collection install --force $LATEST; \
                       ansible -m include_role -a 'name=" + action_namespace + "." + action_collection + "." + action_role + "' -e '" + str(extra_ansible_vars) + "' localhost -vv; exit 0"]

    container = kubernetes.client.V1Container(name=name, image=container_image, command=command, args=args, env=env_list)
    template.template.spec = kubernetes.client.V1PodSpec(containers=[container], restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = kubernetes.client.V1JobSpec(ttl_seconds_after_finished=600, template=template.template)
    return body

def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
