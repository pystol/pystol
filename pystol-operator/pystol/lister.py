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
import shutil
import tempfile
import textwrap
import urllib.request

import kubernetes
from kubernetes.client.rest import ApiException

from prettytable import PrettyTable

from pystol import __version__
from pystol.const import PYSTOL_BRANCH
from pystol.operator import load_kubernetes_config

from rich.console import Console
from rich.markdown import Markdown

pystol_version = __version__


def show_action(name):
    """
    Show the docs for specific Pystol action from Galaxy.

    This is a main component of the input for the controller
    """
    url = ("https://raw.githubusercontent.com/pystol/"
           "pystol-galaxy/" + PYSTOL_BRANCH + "/actions/roles/" +
           name + "/README.md")

    console = Console()
    try:
        with urllib.request.urlopen(url) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        with open(tmp_file.name) as html:
            markdown = Markdown(html.read())
        console.print(markdown)
    except Exception:
        print("Action not found")


def show_actions():
    """
    Show the available Pystol actions from Galaxy.

    This is a main component of the input for the controller
    """
    url = ("https://galaxy.ansible.com/api/internal/"
           "ui/repo-or-collection-detail/"
           "?namespace=pystol&name=actions")

    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        values = json.loads(data)
        actions = (values['data']['collection']['latest_version']
                   ['contents'])
        description = (values['data']['collection']['latest_version']
                       ['metadata']['description'])
        repository = (values['data']['collection']['latest_version']
                      ['metadata']['repository'])
        documentation = (values['data']['collection']['latest_version']
                         ['metadata']['documentation'])
        license = (values['data']['collection']['latest_version']
                   ['metadata']['license'])
        version = (values['data']['collection']['latest_version']
                   ['metadata']['version'])
    except Exception:
        actions = {}
        description = ""
        repository = ""
        documentation = ""
        license = ""
        version = ""
        print("No objects found...")

    x = PrettyTable()
    x.title = description
    x.field_names = ["Name",
                     "Description",
                     "Documentation"]

    url = ("https://github.com/pystol/pystol-galaxy/tree/" +
           PYSTOL_BRANCH + "/actions/roles/")

    ret = []
    for action in actions:
        if action['content_type'] == "role":
            ret.append({'name': action['name'],
                        'description': action['description'],
                        'documentation': url + action['name'],
                        'license': str(license),
                        'version': str(version),
                        'repository': str(repository)})

            x.add_row([action['name'],
                       action['description'],
                       url + action['name']])
    print(x)
    print("Actions part of the Pystol core from: " + str(repository))
    print("Documentation: " + str(documentation))
    print("License: " + str(license))
    print("Version: " + str(version))
    print("Published at: https://galaxy.ansible.com/pystol")
    print("For more information go to: https://docs.pystol.org")

    return ret

def list_actions(api_client=None, debug=False):
    """
    List Pystol actions from the cluster.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    api = kubernetes.client.CustomObjectsApi(api_client=api_client)

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    pretty = 'true'

    x = PrettyTable()
    x.field_names = ["Name",
                     "Creation",
                     "Action state",
                     "Workflow state"]
    ret = []
    try:
        resp = api.list_namespaced_custom_object(group=group,
                                                 version=version,
                                                 namespace=namespace,
                                                 plural=plural,
                                                 pretty=pretty)
        for action in resp['items']:

            name = action['metadata']['name']
            job_description = ""
            pod_logs = ""

            if debug:

                namespace = "pystol"
                pretty = 'true'

                apiO = kubernetes.client.BatchV1Api(api_client=api_client)

                try:
                    resp = apiO.read_namespaced_job(name=name,
                                                   namespace=namespace,
                                                   pretty=pretty)
                    job_description = resp
                except ApiException:
                    print("Job not found")

                apiO = kubernetes.client.CoreV1Api(api_client=api_client)

                try:
                    resp = apiO.list_namespaced_pod(namespace=namespace,
                                                   pretty=pretty)
                    found = False
                    for pod in resp.items:
                        if name in pod.metadata.name:
                            found = True
                            resp = apiO.read_namespaced_pod_log(name=pod.metadata.name,
                                                               namespace=namespace,
                                                               pretty=pretty)
                            pod_logs = resp
                    if not found:
                        print("Pod not found.")
                except ApiException:
                    print("Pod not found.")

            ret.append({'name':
                        action['metadata']['name'],
                        'creationTimestamp':
                        action['metadata']['creationTimestamp'],
                        'action_state':
                        action['spec']['action_state'],
                        'workflow_state':
                        action['spec']['workflow_state'],
                        'stdout':
                        action['spec']['action_stdout'],
                        'stderr':
                        action['spec']['action_stderr'],
                        'job_description': job_description,
                        'pod_logs': pod_logs})

            x.add_row([action['metadata']['name'],
                       action['metadata']['creationTimestamp'],
                       action['spec']['action_state'],
                       action['spec']['workflow_state']])
    except Exception as e:
        print("No objects found or error...")
        return []
    print(x)
    return ret


def get_action(name, debug=False, api_client=None):
    """
    Get Pystol action details.

    This is a main component of the input for the controller
    """
    load_kubernetes_config()
    api = kubernetes.client.CustomObjectsApi(api_client=api_client)

    group = "pystol.org"
    version = "v1alpha1"
    namespace = "pystol"
    plural = "pystolactions"
    try:
        resp = api.get_namespaced_custom_object(group=group,
                                                version=version,
                                                namespace=namespace,
                                                plural=plural,
                                                name=name)
        print("  " + u"\U0001F4AC" + " General information")
        print("    Action: " + resp['spec']['namespace'] + "." +
              resp['spec']['collection'] + "." +
              resp['spec']['role'])

        print("    Extra variables: " + resp['spec']['extra_vars'])

        print("    Source: " + resp['spec']['source'])

        print("  " + u"\U0001F4AC" + " Status information")

        print("    Action state: " + resp['spec']['action_state'])

        print("    Workflow state: " + resp['spec']['workflow_state'])

        prefix = "    Std output: "
        preferredwidth = 70
        wrapper = textwrap.TextWrapper(initial_indent=prefix,
                                       width=preferredwidth,
                                       subsequent_indent=' ' * len(prefix))
        print(wrapper.fill(resp['spec']['action_stdout']))

        prefix = "    Std error: "
        preferredwidth = 70
        wrapper = textwrap.TextWrapper(initial_indent=prefix,
                                       width=preferredwidth,
                                       subsequent_indent=' ' * len(prefix))
        print(wrapper.fill(resp['spec']['action_stderr']))

    except ApiException:
        print("  " + u"\U0001F914" +
              " Object not found, perhaps you have a typo.")

    if debug:

        api = kubernetes.client.BatchV1Api(api_client=api_client)
        namespace = "pystol"
        pretty = 'true'
        try:
            resp = api.read_namespaced_job(name=name,
                                           namespace=namespace,
                                           pretty=pretty)
            print("---- Job description begins ----")
            print(resp)
            print("---- Job description ends ----")
        except ApiException:
            print("  " + u"\U0001F914" +
                  " Job not found, perhaps you have a typo.")

        api = kubernetes.client.CoreV1Api(api_client=api_client)
        namespace = "pystol"
        pretty = 'true'
        try:
            resp = api.list_namespaced_pod(namespace=namespace,
                                           pretty=pretty)
            found = False
            for pod in resp.items:
                if name in pod.metadata.name:
                    found = True
                    resp = api.read_namespaced_pod_log(name=pod.metadata.name,
                                                       namespace=namespace,
                                                       pretty=pretty)
                    print("---- Pod logs begins ----")
                    print("Logs from: " + pod.metadata.name)
                    print(resp)
                    print("---- Pod logs ends ----")
            if not found:
                print("  " + u"\U0001F914" +
                      " Pod not found, perhaps you have a typo.")
        except ApiException:
            print("  " + u"\U0001F914" +
                  " Pod not found, perhaps you have a typo.")
