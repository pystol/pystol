# version 10 of node
FROM node:10
LABEL maintainer="Carlos Camacho <carloscamachoucv@gmail.com>"
LABEL quay.expires-after=30w

# Arguments
ARG revision

## Initial copy of the repository to the container image
# Bundle app source
COPY . .

## Install requisites for getting curl with https
RUN apt-get update && apt-get install apt-transport-https -y

## Install kubectl repository
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list

## Update repos
RUN apt-get update

## Installing pystol launcher requirements
# Install kubectl
RUN apt-get install kubectl -y

## Installing the operator code
# Installing Python3
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# We install the operator and dependencies
RUN echo "The pystol revision is ${revision}"

RUN pip3 install -r /pystol-operator/requirements.txt
RUN PYSTOL_REVISION=${revision} pip3 install --upgrade /pystol-operator

# Configure Ansible inventory
RUN mkdir /etc/ansible/ /ansible
RUN echo "[local]" >> /etc/ansible/hosts
RUN echo "127.0.0.1" >> /etc/ansible/hosts

## Copying the UI files
# Create a directory for client
RUN mkdir -p /usr/src/app
COPY /pystol-ui .
RUN ls pystol-wui

## Installing the UI dependencies (Web UI + endpoints)
RUN npm install -g react-scripts
RUN npm install 
RUN npm install pystol-wui

## Build the application
RUN npm run-script build

## Configure ports
# bind to port 3000
EXPOSE 3000

## In the operator.yaml definition we will
## run one container for the web server and
## another container to run the controller CLI
