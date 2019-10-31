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

import argparse
import difflib
import sys

from github import Github

import requests


def parse_opts(argv):
    """Process the CLI arguments."""
    parser = argparse.ArgumentParser(
        description='This script will check the common '
                    'files across the organization.'
                    'These files should be the same '
                    'everywhere, for example the '
                    'README.md and the LICENSE files.')

    parser.add_argument('--organization',
                        required=True,
                        metavar='<organization name>',
                        help='The organization name '
                             'to compare the files. i.e. pystol',
                        )

    parser.add_argument('--master-repo',
                        required=True,
                        metavar='<master repository>',
                        help='The master repository which '
                             'should have the latest '
                             'versions of the files to '
                             'compare. i.e. pystol'
                        )

    parser.add_argument('--files-to-check',
                        nargs="+", required=True,
                        metavar='<files to check>',
                        help='A list of files to check across '
                             'the repositories of the organization '
                             'i.e. README.md LICENSE')

    opts = parser.parse_args(argv[1:])
    return opts


def main():
    """Process and parse the common files."""
    opts = parse_opts(sys.argv)

    organization = opts.organization
    master_repo = organization + "/" + opts.master_repo
    this_repo = "pystol/pystol"
    files_to_compare = opts.files_to_check

    gh = Github()
    repositories = gh.search_repositories(query='user:' + organization)
    errors = False
    for file in files_to_compare:
        for repo in repositories:
            url = ('https://raw.githubusercontent.com/%s/master/%s' %
                   (repo.full_name, file))

            out = repo.full_name.split("/")[1] + "_" + file
            try:
                r = requests.get(url, stream=True)
                r.raise_for_status()
                open(out, 'wb').write(r.content)
            except Exception as e:
                print("-----")
                print("Error:")
                print("WGET fails to fetch some of the"
                      "common files across the repositories."
                      "Some of the files to download are not"
                      "present in all repos.")
                print(url)
                print(out)
                raise e

        if (this_repo == master_repo):
            base_file = file
        else:
            base_file = master_repo.split("/")[1] + "_" + file

        with open(base_file) as f:
            flines = f.readlines()
            for repo in repositories:
                with open(repo.full_name.split("/")[1] + "_" + file) as g:
                    glines = g.readlines()
                    d = difflib.Differ()
                    diffs = [x for x in
                             d.compare(flines, glines)
                             if x[0] in ('+', '-')]
                    if diffs:
                        print(master_repo.split("/")[1] +
                              "_" +
                              file +
                              " is different than " +
                              repo.full_name.split("/")[1] +
                              "_" +
                              file)
                        errors = True
                    else:
                        print(master_repo.split("/")[1] +
                              "_" +
                              file +
                              " is the same than " +
                              repo.full_name.split("/")[1] +
                              "_" +
                              file)

    if errors:
        print("-----")
        print("Error:")
        print("Some of the files are not synchronized.")
        raise


if __name__ == '__main__':
    main()
