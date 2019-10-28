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

from argparse import ArgumentParser
from os import getenv

import kubernetes

from pystol import __version__
from pystol.load_crd import load_crd
from pystol.operator import handle

pystol_version = __version__


def main():
    """
    Application's entry point.

    Here, application's settings are read from the command line,
    environment variables and CRD. Then, retrieving and processing
    of Kubernetes events are initiated.
    """
    parser = ArgumentParser(
        description='Pystol - copy operator.',
        prog='pystol'
    )
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%(prog)s ' + pystol_version)
    parser.add_argument(
        '--namespace',
        type=str,
        default=getenv('NAMESPACE', 'default'),
        help='Operator Namespace (or ${NAMESPACE}), default: default'
    )
    parser.add_argument(
        '--rule-name',
        type=str,
        default=getenv('RULE_NAME', 'main-rule'),
        help='CRD Name (or ${RULE_NAME}), default: main-rule'
    )

    args = parser.parse_args()

    try:
        kubernetes.config.load_incluster_config()
    except kubernetes.config.config_exception.ConfigException:
        raise RuntimeError(
            'Can not read Kubernetes cluster configuration.'
        )

    try:
        specs = load_crd(args.namespace, args.rule_name)
        handle(specs)

    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...') from err
