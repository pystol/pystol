FROM alpine
LABEL maintainer="Carlos Camacho <carloscamachoucv@gmail.com>"
LABEL quay.expires-after=30w

# Arguments
ARG revision

## Initial copy of the repository to the container image
# Bundle app source
COPY . .

# Until https://github.com/grpc/grpc/issues/18150 is fixed
# The grpcio install will be compiled from source.

## Installing dependencies
# Installing Python3
RUN apk add --update build-base bash curl python3 git python3-dev libffi-dev openssl-dev py3-pip iputils
RUN pip3 install --upgrade pip virtualenv setuptools

## Installing pystol launcher requirements
# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

## Installing the operator code
# We install the operator and dependencies
RUN echo "The pystol revision is ${revision}"
RUN pip3 install -r /pystol-operator/requirements.txt
RUN PYSTOL_REVISION=${revision} pip3 install --upgrade /pystol-operator

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
# RUN npm install -g react-scripts && npm install && npm install pystol-wui && npm run-script build
RUN pip3 install -r requirements.txt

## Configure ports
# bind to port 3000
EXPOSE 3000

## In the operator.yaml definition we will
## run one container for the web server and
## another container to run the controller CLI
