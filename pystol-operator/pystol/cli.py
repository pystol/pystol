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
import threading
from argparse import ArgumentParser

from pystol import __version__
from pystol.cleaner import purge_pystol
from pystol.deployer import deploy_pystol
from pystol.get_banner import get_banner
from pystol.operator import insert_pystol_object
from pystol.operator import watch_for_pystol_objects, watch_for_pystol_timeouts

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

    subparsers = parser.add_subparsers(title="Pystol subcommands",
                                       dest="command",
                                       help=("These are the options "
                                             "supported: \n"
                                             "The listen option will "
                                             "watch for CRD events. "
                                             "The run option will "
                                             "execute the Pystol "
                                             "actions against the cluster."))

    parser_purge = subparsers.add_parser('purge',
                                         help=("Purge any Pystol "
                                               "deployed resource."))

    parser_purge.add_argument(
        '-y',
        '--yes',
        action='store_true',
        help=("Run this to avoid having to write 'yes'"))

    parser_run = subparsers.add_parser('run', help=("CLI options to run the "
                                                    "Pystol actions."))

    parser_run.add_argument(
        '-n',
        '--namespace',
        required=True,
        type=str,
        help=("Name of the namespace to be referenced, "
              "this will be the Galaxy handler, like: "
              "pystol (from galaxy), "
              "which will be referenced as "
              "https://galaxy.ansible.com/pystol"))

    parser_run.add_argument(
        '-c',
        '--collection',
        required=True,
        type=str,
        help=("Name of the collection to be installed/executed, "
              "this can be the name of the galaxy collection like: "
              "actions (from galaxy), "
              "which will be referenced as "
              "https://galaxy.ansible.com/pystol/actions"))

    parser_run.add_argument(
        '-r',
        '--role',
        required=True,
        type=str,
        help=("Name of the role to be executed part of the "
              "namespace and collection value, "
              "for example, if the name is: "
              "kill-pods "
              "It will execute: "
              "pystol.actions.kill-pods "))

    parser_run.add_argument(
        '-s',
        '--source',
        default="galaxy.ansible.com",
        type=str,
        help=("The source URL where we will fetch the collection "
              "with the Pystol actions.\n"
              "It can be i.e. git+http://github.com/pystol/pystol-galaxy.git\n"
              "Defaults to: galaxy.ansible.com"))

    parser_run.add_argument(
        '-e',
        '--extra-vars',
        default="{}",
        type=str,
        help=("The extra vars for example:"
              "--extra-vars '{\"a\":\"b\",\"c\":[\",\"d\",\"e\"]}'\n"
              "Defaults to: ''"))

    subparsers.add_parser('listen', help=("CLI options to "
                                          "watch for CRDs"))

    subparsers.add_parser('deploy',
                          help=("Install the Pystol operator "
                                "includes, deployment, "
                                "RBAC rules, and CRD"))

    args = parser.parse_args()

    print("Pystol called with the folowing parameters")
    print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()

    try:
        if (args.command == 'run'):
            api_response = insert_pystol_object(args.namespace,
                                                args.collection,
                                                args.role,
                                                args.source,
                                                args.extra_vars)
            print("The following Pystol action is created:")
            print(json.dumps(api_response, indent=4, sort_keys=True))
            exit()
        elif (args.command == 'listen'):
            print("We will watch for objects to process")
            try:
                t1 = threading.Thread(target=watch_for_pystol_objects,
                                      args=(t1_stop,))
                t1.start()
                t2 = threading.Thread(target=watch_for_pystol_timeouts,
                                      args=(t2_stop,))
                t2.start()
            except Exception as err:
                print("Error: unable to start thread: " + err)
        elif (args.command == 'purge'):
            if not args.yes:
                yes = {'yes', 'y', 'ye', ''}
                msg = ("--------------------------------------------\n"
                       "You are about to purge any Pystol resource\n"
                       "part of the pystol namespace in this cluster.\n"
                       "This includes any deployment, previous runs,\n"
                       "RBAC rules, and any other Pystol resource.\n"
                       "Write 'yes' to proceed.\n"
                       "-------This action can not be undone.-------")
                print(msg)
                choice = input().lower()
                if choice in yes:
                    purge_pystol()
                else:
                    print("Cancelling...")
            else:
                purge_pystol()
            exit()
        elif (args.command == 'deploy'):
            deploy_pystol()
            exit()

    except KeyboardInterrupt:
        pass
    except Exception as err:
        raise RuntimeError('There is something wrong...' + err)

    while not t2_stop.is_set() or not t1_stop.is_set():
        pass
