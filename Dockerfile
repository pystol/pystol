# version 10 of node
FROM node:10
LABEL maintainer="Carlos Camacho <carloscamachoucv@gmail.com>"
LABEL quay.expires-after=3w

# Arguments
ARG revision

## Initial copy of the repository to the container image
# Bundle app source
COPY . .

## Installing the operator code
# Installing Python3
RUN apt-get update -y 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
# We install the operator and dependencies
RUN echo "The pystol revision is ${revision}"

RUN pip3 install -r /pystol-operator/requirements.txt
RUN PYSTOL_REVISION=${revision} pip3 install --upgrade /pystol-operator

## Copying the UI files
# Create a directory for client
RUN mkdir -p /usr/src/app
COPY /pystol-ui .

## Installing the Web UI
WORKDIR /usr/src/app/pystol-wui
RUN npm install 
RUN npm run-script build

# Installing the main app with the endpoints
WORKDIR /usr/src/app
RUN npm install 

## Configure ports
# bind to port 3000
EXPOSE 3000

## In the operator.yaml definition we will
## run one container for the web server and
## another container to run the controller CLI
