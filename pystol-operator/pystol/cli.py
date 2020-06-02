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

import logging
import logging.handlers
import os
import threading
from argparse import ArgumentParser

from pystol import __version__
from pystol.cleaner import purge_pystol
from pystol.const import PYSTOL_LOG_FILE
from pystol.deployer import deploy_pystol
from pystol.get_banner import get_banner
from pystol.lister import get_action, list_actions, show_action, show_actions
from pystol.operator import insert_pystol_object
from pystol.operator import watch_for_pystol_objects, watch_for_pystol_timeouts

pystol_version = __version__

t1_stop = threading.Event()
t2_stop = threading.Event()

handler = logging.handlers.WatchedFileHandler(
    PYSTOL_LOG_FILE)
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


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
                                          "watch for CRs"))

    subparsers.add_parser('list', help=("CLI options to "
                                        "list CRs"))

    parser_get = subparsers.add_parser('get',
                                       help=("Get Pystol resource."))

    parser_get.add_argument(
        "action",
        type=str,
        help=("Specify the action to fetch details"))

    parser_show = subparsers.add_parser('show',
                                        help=("Get available Pystol actions."))

    parser_show.add_argument(
        "action",
        nargs='?',
        default='',
        type=str,
        help=("Specify the action to fetch details"))

    parser_get.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help=("Add the debug flag to show extra information"))

    subparsers.add_parser('deploy',
                          help=("Install the Pystol operator "
                                "includes, deployment, "
                                "RBAC rules, and CRD"))

    args = parser.parse_args()

    # print("Pystol called with the folowing parameters")
    # print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()

    try:
        if (args.command == 'run'):
            print(u"\U0001F52B" + " Starting a Pystol action")
            print("  " + u"\U0001F4BE" + " Inserting the custom resource"
                                         " in the cluster")
            ins = insert_pystol_object(args.namespace,
                                       args.collection,
                                       args.role,
                                       args.source,
                                       args.extra_vars)

            if ins:
                print("  " + u"\U0001F4A8" +
                      " The action was deployed OK")
                print("  " + u"\U0001F916" +
                      " Check its status for details")
                print("  " + u"\U0001F92B" + " Try using the CLI list and get"
                                             " options, 'pystol -h' helps")
            else:
                print("  " + u"\U0001F914" + " We can not add the resource,"
                                             " did you deploy Pystol?")
                print("  " + u"\U0001F440" + " Logs are stored in"
                                             " /tmp/pystol.org")

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
                yes = {'yes', 'y'}
                msg = ("*********This action can not be undone**********\n"
                       "*  You are about to purge any Pystol resource  *\n"
                       "* part of the pystol namespace in the cluster. *\n"
                       "* This includes any deployment, previous runs, *\n"
                       "*  RBAC rules, and any other Pystol resource.  *\n"
                       "*********This action can not be undone**********\n")
                print(msg)
                choice = input(
                    "Write 'yes' and press 'enter' to proceed: \n")
                if choice in yes:
                    print(u"\U0001F480" +
                          " Purging Pystol from the cluster.")
                    print("  " + u"\U0001F4A3" +
                          " Removing resources...")
                    purge_pystol()
                    print(u"\u2728" + " Pystol was removed completely.")
                else:
                    print("Cancelling...")
            else:
                print(u"\U0001F480" + " Purging Pystol from the cluster.")
                print("  " + u"\U0001F4A3" + " Removing resources...")
                purge_pystol()
                print(u"\u2728" + " Pystol was removed completely.")
            exit()
        elif (args.command == 'list'):
            print(u"\U0001F4DA" + " Listing the deployed actions"
                                  " from the cluster.")
            list_actions()
            print(u"\U0001F4A1" + " For further information use:"
                                  " pystol get <action_name> [--debug]")
            exit()
        elif (args.command == 'show'):
            if args.action:
                show_action(args.action)
            else:
                show_actions()
            exit()
        elif (args.command == 'get'):
            print(u"\U0001F4E4" + " Getting the details from"
                                  " an specific action.")
            get_action(args.action, args.debug)
            exit()
        elif (args.command == 'deploy'):
            print(u"\U0001F680" + " Deploying Pystol in the cluster.")
            deploy_pystol()
            print(u"\U0001F3C4" + " Done! Pystol is now deployed.")
            print(u"\U0001F550" + " Wait a few seconds to have the"
                                  " deployments up and running.")
            exit()

    except KeyboardInterrupt:
        pass
    except Exception as err:
        raise RuntimeError('There is something wrong...' + err)

    while not t2_stop.is_set() or not t1_stop.is_set():
        pass
