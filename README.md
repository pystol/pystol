![](https://raw.githubusercontent.com/pystol/pystol-docs/master/assets/images/logo_readme.png)

**The open source, self-hosted and cloud-native fault injection platform**

[![made-with-python](http://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![made-with-love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.pystol.org)

| [pystol](https://github.com/pystol/pystol) | [pystol-galaxy](https://github.com/pystol/pystol-galaxy) | [pystol-ansible](https://github.com/pystol/pystol-ansible) | [pystol-docs](https://github.com/pystol/pystol-docs) | [quay.io](https://quay.io/organization/pystol) | info |
|:---:|:---:|:---:|:---:|:---:|:---:|
| [![Container image build](https://github.com/pystol/pystol/workflows/container-image/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=container-image) | [![Galaxy publish](https://github.com/pystol/pystol-galaxy/workflows/galaxy-publish/badge.svg?event=push)](https://github.com/pystol/pystol-galaxy/actions?workflow=galaxy-publish) | [![Galaxy publish](https://github.com/pystol/pystol-ansible/workflows/ansible-lint/badge.svg?event=push)](https://github.com/pystol/pystol-ansible/actions?workflow=ansible-lint) | [![Docs build](https://github.com/pystol/pystol-docs/workflows/build/badge.svg?event=push)](https://github.com/pystol/pystol-docs/actions?workflow=build) | [![Docker registry STAGING status](https://quay.io/repository/pystol/pystol-operator-staging/status "Docker registry STAGING status")](https://quay.io/repository/pystol/pystol-operator-staging) | [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) |
| [![NodeJS install build](https://github.com/pystol/pystol/workflows/nodejs-install/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=nodejs-install) | | | | [![Docker registry STABLE status](https://quay.io/repository/pystol/pystol-operator-stable/status "Docker registry STABLE status")](https://quay.io/repository/pystol/pystol-operator-stable) | [![GitHub issues](https://img.shields.io/github/issues/pystol/pystol)](https://github.com/pystol/pystol/issues) |
| [![TOX ESlint build](https://github.com/pystol/pystol/workflows/tox-eslint/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=tox-eslint) | | | | | [![IRC channel](https://img.shields.io/badge/freenode-%23pystol-orange.svg)](http://webchat.freenode.net/?channels=%23pystol) |
| [![TOX Flake8 build](https://github.com/pystol/pystol/workflows/tox-flake/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=tox-flake) | | | | | |
| [![TOX NodeJS units build](https://github.com/pystol/pystol/workflows/tox-nodeunits/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=tox-nodeunits) | | | | | |
| [![TOX Pytest build](https://github.com/pystol/pystol/workflows/tox-pytest/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=tox-pytest) | | | | | |
| [![TOX CheckTools build](https://github.com/pystol/pystol/workflows/tox-checktools/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=tox-checktools) | | | | | |
| [![E2E install](https://github.com/pystol/pystol/workflows/e2e-deploy/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=e2e-deploy) | | | | | |
| [![Pypi publish](https://github.com/pystol/pystol/workflows/pypi-publish/badge.svg?event=push)](https://github.com/pystol/pystol/actions?workflow=pypi-publish) | | | | | |


## Documentation

Please refer to the [official documentation](https://docs.pystol.org)
website for any information related to the project.

## CI dashboard

Pystol uses **GitHub actions**
and **badges** to run all the CI
tasks, the result of running these
tasks is represented using badges.

In particular we embrace the use of
CI dashboard as information radiators.

We created the [badgeboad project](https://badgeboard.pystol.org)
to show the value of any set of badges as a dashboard.

For more information you can open the
[CI dashboard](https://badgeboard.pystol.org)
directly or go to the
[project page in GitHub](https://github.com/pystol/badgeboard).

## Container images

All pystol official container images are hosted in Quay.io under
the [Pystol organization](https://quay.io/organization/pystol).

There you will find two repositories:

* The Pystol [staging repository](https://quay.io/repository/pystol/pystol-operator-staging).
Here you will find all the container images from the upstream end-to-end jobs from the GitHub
Actions jobs.

* The Pystol [stable repository](https://quay.io/repository/pystol/pystol-operator-stable).
Here you will find all the container images from the stable branches.

## License

Pystol is open source software
licensed under the [Apache license](LICENSE).
