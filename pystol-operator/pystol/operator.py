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

import kubernetes
from kubernetes.client.rest import ApiException

from prettytable import PrettyTable

from pystol import __version__
from pystol.const \
    import CRD_DOMAIN, CRD_NAMESPACE, CRD_PLURAL, CRD_VERSION
from pystol.logger import get_logger

pystol_version = __version__

# custom_obj = kubernetes.client.CustomObjectsApi()
# v1 = kubernetes.client.CoreV1Api()

#
# We load the Kubernetes cluster config depending
# where we execute the operator from.
#


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
            kubernetes.config.load_kube_config(
                os.getenv('KUBECONFIG'))
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
                   "Version: %s"
                   "Error: %s" % (pystol_version, e))

#
# Part of the operation in charge of adding the custom resources
# to the Kubernetes cluster, this will create an object with
# the CLI parameters.
#


def insert_pystol_object(namespace,
                         collection,
                         role,
                         source,
                         extra_vars,
                         api_client=None):
    """
    Determine where we will insert the CR.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi(
        api_client=api_client)

    resource = {
        "apiVersion": CRD_DOMAIN + "/" + CRD_VERSION,
        "kind": "PystolAction",
        "metadata": {"name": "pystol-action-" +
                             namespace +
                             "-" +
                             collection +
                             "-" +
                             role +
                             "-" +
                             id_generator()},
        "spec": {"namespace": namespace,
                 "collection": collection,
                 "role": role,
                 "source": source,
                 "extra_vars": extra_vars,
                 "action_state": "PystolActionCreating",
                 "workflow_state": "PystolOperatorWaitingAction",
                 "action_stderr": "{}",
                 "action_stdout": "{}"},
    }

    try:
        # create the resource
        api_response = custom_obj.create_namespaced_custom_object(
            group=CRD_DOMAIN,
            version=CRD_VERSION,
            namespace=CRD_NAMESPACE,
            plural=CRD_PLURAL,
            body=resource,
        )
    except ApiException as e:
        get_logger("insert_pystol_object").debug(e)
        return False

    x = PrettyTable()
    x.field_names = ["Name",
                     "Creation",
                     "Action state",
                     "Workflow state"]

    x.add_row([api_response['metadata']['name'],
               api_response['metadata']['creationTimestamp'],
               api_response['spec']['action_state'],
               api_response['spec']['workflow_state']])

    print(x)
    return True

#
# Part of the operator which will handle the process of new
# PystolAction objects added in the cluster, It will watch
# for a new object and create a software deployment to run
# the selected Pystol action.
#


def watch_for_pystol_timeouts(stop,
                              api_client=None):
    """
    Watch for action with timeouts.

    This method will listen for custom objects
    that times out.
    """
    while True:
        return True


def watch_for_pystol_objects(stop,
                             api_client=None):
    """
    Initiate the main listening method.

    This method will listen for custom objects
    added to the cluster.
    The watcher is defined here.
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi(
        api_client=api_client)

    w = kubernetes.watch.Watch()
    for event in w.stream(custom_obj.list_cluster_custom_object,
                          CRD_DOMAIN,
                          CRD_VERSION,
                          CRD_PLURAL,
                          resource_version=''):
        obj = event["object"]
        operation = event['type']
        spec = obj.get("spec")
        if not spec:
            continue
        metadata = obj.get("metadata")
        name = metadata['name']
        done = spec.get("executed", False)
        if done:
            continue
        print("Processing %s on %s" % (operation, name))
        execute_pystol_action(obj)


def execute_pystol_action(obj,
                          api_client=None):
    """
    Execute the Pystol action.

    This method will execute the Pystol action
    defined in the custom object.
    """
    load_kubernetes_config()
    custom_obj = kubernetes.client.CustomObjectsApi(
        api_client=api_client)

    metadata = obj.get("metadata")
    if not metadata:
        print("No metadata in object, skipping: %s"
              % json.dumps(obj, indent=1))
        return
    name = metadata.get("name")
    namespace = metadata.get("namespace")

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

    # TODO: get object here to update it
    updt = custom_obj.get_namespaced_custom_object(group=CRD_DOMAIN,
                                                   version=CRD_VERSION,
                                                   namespace=namespace,
                                                   plural=CRD_PLURAL,
                                                   name=name)
    updt["spec"]["executed"] = True
    updt["spec"]["workflow_state"] = "PystolOperatorStartProcessingAction"
    # Processing action
    print("Updating processing action: %s" % name)
    custom_obj.patch_namespaced_custom_object(CRD_DOMAIN,
                                              CRD_VERSION,
                                              namespace,
                                              CRD_PLURAL,
                                              name,
                                              updt)

    # Create the job definition
    api_instance = kubernetes.client.BatchV1Api(api_client=api_client)

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
        api_response = api_instance.create_namespaced_job("pystol",
                                                          body,
                                                          pretty=True)
        print(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n"
              % e)

    # Updating the CR with - Creating job
    print("Updating creating job: %s" % name)
    # TODO: get object here to update it
    updt = custom_obj.get_namespaced_custom_object(group=CRD_DOMAIN,
                                                   version=CRD_VERSION,
                                                   namespace=namespace,
                                                   plural=CRD_PLURAL,
                                                   name=name)
    updt["spec"]["workflow_state"] = "PystolOperatorCreatingJob"
    # Processing action
    print("Updating processing action: %s" % name)
    custom_obj.patch_namespaced_custom_object(CRD_DOMAIN,
                                              CRD_VERSION,
                                              namespace,
                                              CRD_PLURAL,
                                              name,
                                              updt)

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
    """
    Create the Pystol job.

    This method will create the k8s job
    that launchs the action.
    """
    load_kubernetes_config()

    # Body is the object Body
    body = kubernetes.client.V1Job(api_version="batch/v1",
                                   kind="Job")
    # Body needs Metadata
    # Attention: Each JOB must have a different name!
    body.metadata = kubernetes.client.V1ObjectMeta(namespace=namespace,
                                                   name=name)
    # And a Status
    body.status = kubernetes.client.V1JobStatus()
    # Now we start with the Template...
    template = kubernetes.client.V1PodTemplate()
    template.template = kubernetes.client.V1PodTemplateSpec()
    # Passing Arguments in Env:
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append(kubernetes.client.V1EnvVar(name=env_name,
                                                   value=env_value))

    # Python interpreter as an extra variable
    # python object to be appended
    y = {"ansible_python_interpreter": "/usr/bin/python3",
         "pystol_action_id": name}
    # parsing JSON string:
    extra_ansible_vars = json.loads(action_extra_vars)
    # appending the data
    extra_ansible_vars.update(y)

    # Recovery ansible variables for the log role
    # In the case a user calls an unrecognized action
    # the container will fail and we will not be able to log this
    # failure.

    # We can use the same extra_ansible_vars as the workflow and
    # action state should not be used by any action from the
    # operator, they are calculated as long as the collection
    # is executed.

    y2 = {"ansible_python_interpreter":
          "/usr/bin/python3",
          "pystol_action_id":
          name,
          "pystol_patch_workflow_state":
          "PystolOperatorEnded",
          "pystol_patch_action_state":
          "PystolActionEndedFail",
          "pystol_patch_action_stdout":
          "This-action-did-not-finish-correctly",
          "pystol_patch_action_stderr":
          "Probably-the-action-was-not-found-Check-the-logs"}
    # rec_extra_ansible_vars = json.loads("{}")
    # rec_extra_ansible_vars.update(y2)
    extra_ansible_vars.update(y2)

    command = ["/bin/bash"]

    if (action_source == '' or action_source is None):
        action_source = "galaxy.ansible.com"

    if (action_source == "galaxy.ansible.com"):
        args = ["-c",
                "echo '---' > req.yml; \
                 echo 'collections:' >> req.yml; \
                 echo '- name: " + action_namespace + "." + action_collection + "' >> req.yml; \
                 echo '  source: https://" + action_source + "' >> req.yml; \
                 ansible-galaxy collection install --force -r req.yml; \
                 ansible -m include_role \
                   -a 'name=" + action_namespace + "." + action_collection + "." + action_role + "' \
                   -e '" + str(extra_ansible_vars) + "' localhost -vv || \
                 ansible -m include_role -a 'name=pystol.actions.patch' -e '" + str(extra_ansible_vars) + "' localhost -vv; \
                 exit 0"]
    else:
        args = ["-c",
                "echo '---'; \
                 git clone " + action_source + " cloned_repo; \
                 cd cloned_repo; \
                 cd " + action_collection + "; \
                 mkdir -p releases; \
                 ansible-galaxy collection build -v \
                                                 --force \
                                                 --output-path releases/; \
                 cd releases; \
                 LATEST=$(ls *.tar.gz | grep -v latest | sort -V | tail -n1); \
                 ansible-galaxy collection install --force $LATEST; \
                 ansible -m include_role \
                   -a 'name=" + action_namespace + "." + action_collection + "." + action_role + "' \
                   -e '" + str(extra_ansible_vars) + "' localhost -vv || \
                 ansible -m include_role -a 'name=pystol.actions.patch' -e '" + str(extra_ansible_vars) + "' localhost -vv; \
                 exit 0"]

    container = kubernetes.client.V1Container(name=name,
                                              image=container_image,
                                              command=command,
                                              args=args,
                                              env=env_list)
    template.template.spec = kubernetes.client.V1PodSpec(
        containers=[container],
        restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = kubernetes.client.V1JobSpec(ttl_seconds_after_finished=600,
                                            template=template.template)
    return body


def id_generator(size=5, chars=string.ascii_lowercase + string.digits):
    """
    Generate a random sufix.

    This method will generate a
    random sufix for the created resources.
    """
    return ''.join(random.choice(chars) for _ in range(size))
