#!/bin/bash

kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-master-controller.json
kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-master-service.json
kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-slave-controller.json
kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/redis-slave-service.json
kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/guestbook-controller.json
kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook-go/guestbook-service.json

kubectl get svc


echo "Use the following example, if the exit is like:"
echo "guestbook      LoadBalancer   172.30.1.79     a55aec927c735648099.us-east-2.elb.amazonaws.com   3000:30330/TCP   13s"

echo "Then the URL is:"
echo "http://a55aec927c735648099.us-east-2.elb.amazonaws.com:3000/"

echo "Using curl:"
echo "http://a55aec927c735648099.us-east-2.elb.amazonaws.com:3000/rpush/guestbook/carlos"
