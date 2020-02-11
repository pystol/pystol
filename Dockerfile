# We should use CentOS 8 as soon as possible but
# the container fails when building.
FROM registry.centos.org/centos/centos:centos8
LABEL maintainer="Carlos Camacho <carloscamachoucv@gmail.com>"
LABEL quay.expires-after=30w

# Arguments
ARG revision

## Initial copy of the repository to the container image
# Bundle app source
COPY . .

## Installing pystol launcher requirements
# Install kubectl
RUN echo -e "\
[kubernetes] \n\
name=Kubernetes \n\
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64 \n\
enabled=1 \n\
gpgcheck=1 \n\
repo_gpgcheck=1 \n\
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg \
" > /etc/yum.repos.d/kubernetes.repo

RUN /bin/bash -c "yum install -y kubectl"

## Installing the operator code
# Installing Python3
RUN yum install python3 python3-pip git -y

# We install the operator and dependencies
RUN echo "The pystol revision is ${revision}"
RUN pip3 install -r /pystol-operator/requirements.txt
RUN touch README.md
RUN PYSTOL_REVISION=${revision} pip3 install --upgrade /pystol-operator

# Install NodeJS
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN yum install nodejs -y

# Configure Ansible inventory
RUN mkdir /etc/ansible/ /ansible
RUN echo "localhost ansible_connection=local" >> /etc/ansible/hosts

# Install the collection codebase
# Maybe if in the future we want to
# deliver some default roles and modules
# it might be a good idea, to have it already in the image.
# This needs to use also --force if we install it from
# source (check the operator code)
RUN ansible-galaxy collection install pystol.actions

## Moving to the UI install
# Change the current working directory
WORKDIR "/pystol-ui"
## Installing the UI dependencies (Web UI + endpoints) and Build the application
RUN npm install -g react-scripts && npm install && npm install pystol-wui && npm run-script build

## Configure ports
# bind to port 3000
EXPOSE 3000

## In the operator.yaml definition we will
## run one container for the web server and
## another container to run the controller CLI
