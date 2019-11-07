# version 8 of node
FROM node:8
LABEL maintainer="Carlos Camacho <carloscamachoucv@gmail.com>"
LABEL quay.expires-after=3w

## Initial copy of the repository to the container image
# Bundle app source
COPY . .

## Installing the operator code
# Installing Python3
RUN apt-get update -y 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# We install the operator and dependencies
RUN pip3 install --upgrade /pystol-operator
RUN pip3 install -r /pystol-operator/requirements.txt

## Installing the web UI
# Create a directory for client
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY /pystol-ui .
RUN npm install 
RUN npm run-script build

## Configure ports
# bind to port 3000
EXPOSE 3000

## In the operator.yaml definition we will
## run one container for the web server and
## another container to run the controller CLI

