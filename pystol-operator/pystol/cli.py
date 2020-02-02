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

from argparse import Action
from argparse import ArgumentParser

import kubernetes
import os
import threading

from pystol import __version__
from pystol.get_banner import get_banner
from pystol.operator import watch_for_pystol_objects, watch_for_pystol_jobs, insert_pystol_object

pystol_version = __version__

t1_stop = threading.Event()
t2_stop = threading.Event()

def main():
    """
    Application's entry point.

    Here, application's settings are read from the command line,
    environment variables and CRD. Then, retrieving and processing
    of Kubernetes events are initiated.
    """
    parser = ArgumentParser(
        description='Pystol - CLI',
        prog='pystol'
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + pystol_version
    )
    parser.add_argument(
        '-b',
        '--banner',
        action='store_true',
        help='Print Pystol.org banner'
    )
    subparsers = parser.add_subparsers(title="Pystol subcommands", dest="command",
                                       help=("These are the options supported: "
                                             "The listen option will watch for "
                                             "CRD events. "
                                             "The run option will execute the "
                                             "Pystol actions against the cluster."
                                            )
    )
    parser_run = subparsers.add_parser('run', help=("CLI options to run the Pystol "
                                                    "actions."
                                                   )
    )
    parser_run.add_argument(
       '-n',
       '--namespace',
        required=True,
        type=str,
        help=("Name of the namespace to be referenced, "
              "this will be the Galaxy handler, like: "
              "pystol (from galaxy), "
              "which will be referenced as "
              "https://galaxy.ansible.com/pystol"
             )
    )
    parser_run.add_argument(
        '-c',
        '--collection',
        required=True,
        type=str,
        help=("Name of the collection to be installed/executed, "
              "this can be the name of the galaxy collection like: "
              "actions (from galaxy), "
              "which will be referenced as "
              "https://galaxy.ansible.com/pystol/actions"
             )
    )
    parser_run.add_argument(
        '-r',
        '--role',
        required=True,
        type=str,
        help=("Name of the role to be executed part of the namespace and collection value, "
              "for example, if the name is: "
              "kill-pods "
              "It will execute: "
              "pystol.actions.kill-pods "
             )
    )
    parser_listen = subparsers.add_parser('listen', help=("CLI options to "
                                                          "watch for CRDs"
                                                         )
    )

    args = parser.parse_args()

    print("Pystol called with the folowing parameters")
    print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()

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
    try:
        if args.command == 'run':
            print("We will run a Pystol action")
            insert_action(args.namespace, args.collection, args.role)
        elif args.command == 'listen':
            print("We will watch for objects to process")
            try:
                t1 = threading.Thread(target=watch_for_pystol_objects, args=(t1_stop,))
                t1.start()
                t2 = threading.Thread(target=watch_for_pystol_jobs, args=(t2_stop,))
                t2.start()
            except:
                print ("Error: unable to start thread")

    except KeyboardInterrupt:
        pass
    except Exception as err:
        raise RuntimeError('There is something wrong...' + err)

    while not t2_stop.is_set() or not not t1_stop.is_set():
        pass
