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
from os import getenv

import kubernetes

from pystol import __version__
from pystol.get_banner import get_banner
from pystol.load_crd import load_crd
from pystol.operator import handle, deploy_action

pystol_version = __version__


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
        '-c',
        '--collection',
        required=True,
        type=str,
        help=("Name of the collection to be installed/executed, "
              "this can be the name of the galaxy collection like: "
              "newswangerd.collection_demo (from galaxy), "
              "or "
              "https://github.com/newswangerd/collection_demo (from a github repo)."
             )
    )
    parser_run.add_argument(
        '-n',
        '--name',
        required=True,
        type=str,
        help=("Name of the role to be executed part of the --collection value, "
              "for example, if the name is: "
              "factoid "
              "It will execute: "
              "newswangerd.collection_demo.factoid "
              "The content of the role depends on the source of the "
              "collection, if it's from Ansible Galaxy or a Git repository."
             )
    )
    parser_run.add_argument(
        '-e',
        '--extra-vars',
        type=str,
        default='{}',
        help=("Passing additional parameters to the Galaxy collection, for example: "
              "-e '{\"pacman\":\"mrs\",\"ghosts\":[\"inky\",\"pinky\",\"clyde\",\"sue\"]}' "
              "This will use the sale JSON syntax as the extra vars from Ansible"
             )
    )

    parser_listen = subparsers.add_parser('listen', help=("CLI options to "
                                                          "watch for CRDs"
                                                         )
    )

    parser_listen.add_argument(
        '-n',
        '--namespace',
        type=str,
        default=getenv('NAMESPACE', 'default'),
        help='Operator Namespace (or ${NAMESPACE}), default: default'
    )

    parser_listen.add_argument(
        '-r',
        '--rule-name',
        type=str,
        default=getenv('RULE_NAME', 'main-rule'),
        help='CRD Name (or ${RULE_NAME}), default: main-rule'
    )

    args = parser.parse_args()

    print("Pystol called with the folowing parameters")
    print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()

    try:
        kubernetes.config.load_incluster_config()
    except kubernetes.config.config_exception.ConfigException:
        raise RuntimeError(
            'Can not read Kubernetes cluster configuration.'
        )

    try:
        if args.command == 'run':
            print("We will run a Pystol action")
            deploy_action(args.collection, args.name, args.extra_vars)
        elif args.command == 'listen':
            print("We will watch for an action")
            specs = load_crd(args.namespace, args.rule_name)
            handle(specs)

    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...' + err)
